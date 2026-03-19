#!/usr/bin/env python3
"""Generate MOC markdown files for bibliography sources via OpenRouter.

Pipeline:
1. Discover bibliography source files (.pdf/.epub) without a matching MOC_-*.md.
2. Extract text in chunks.
3. Build a cumulative extraction dossier, sending the previous dossier into each next LLM step.
4. Consolidate the final dossier into a MOC using bibliografia/MOC-PROMPT.md.

Usage examples:
  python3 tools/scripts/generate_mocs.py --dry-run
  OPENROUTER_API_KEY=... python3 tools/scripts/generate_mocs.py --limit 2
  OPENROUTER_API_KEY=... python3 tools/scripts/generate_mocs.py --only "bibliografia/livros/Golpe en Brasil.pdf"
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
BIB_ROOT = REPO_ROOT / "bibliografia"
PROMPT_PATH = BIB_ROOT / "MOC-PROMPT.md"
LOG_ROOT = REPO_ROOT / "tools" / "logs" / "moc_pipeline"
DEFAULT_MODELS = [
    "xiaomi/mimo-v2-pro",  # janela de contexto ~1,05M
    "moonshotai/kimi-k2.5",  # janela de contexto ~262k
    "deepseek/deepseek-v3.2",  # janela de contexto ~164k
]
MODEL_CONTEXT_WINDOWS = {
    "xiaomi/mimo-v2-pro": 1_050_000,
    "moonshotai/kimi-k2.5": 262_000,
    "deepseek/deepseek-v3.2": 164_000,
}
SOURCE_EXTENSIONS = {".pdf", ".epub"}
ROMAN_MAP = {
    "i": "1",
    "ii": "2",
    "iii": "3",
    "iv": "4",
    "v": "5",
    "vi": "6",
    "vii": "7",
    "viii": "8",
    "ix": "9",
    "x": "10",
}


@dataclass
class WorkItem:
    source_path: Path
    target_moc_path: Path
    title_hint: str
    source_type: str


@dataclass
class Chunk:
    index: int
    label: str
    text: str


class NeedSmallerChunkError(RuntimeError):
    def __init__(self, model: str, recommended_chars: int, detail: str):
        super().__init__(detail)
        self.model = model
        self.recommended_chars = recommended_chars
        self.detail = detail


class OpenRouterClient:
    def __init__(self, api_key: str, models: Sequence[str], timeout: int = 300):
        self.api_key = api_key
        self.models = [m.strip() for m in models if m.strip()]
        if not self.models:
            raise ValueError("É necessário fornecer ao menos um modelo OpenRouter.")
        self.timeout = timeout
        self.session = requests.Session()
        self.preferred_model_index = 0

    def preferred_model(self) -> str:
        return self.models[self.preferred_model_index]

    def preferred_chunk_chars(self) -> int:
        return model_safe_chunk_chars(self.preferred_model())

    @staticmethod
    def _extract_error_info(response: requests.Response) -> Tuple[Optional[int], str, bool]:
        text = response.text[:2000]
        retryable = response.status_code in {408, 409, 425, 429, 500, 502, 503, 504}
        try:
            data = response.json()
        except Exception:  # noqa: BLE001
            return response.status_code, text, retryable

        error = data.get("error", {}) if isinstance(data, dict) else {}
        message = error.get("message") or text
        metadata = error.get("metadata", {}) if isinstance(error, dict) else {}
        raw = metadata.get("raw", "") if isinstance(metadata, dict) else ""
        provider_name = metadata.get("provider_name", "") if isinstance(metadata, dict) else ""
        combined = " | ".join(part for part in [message, raw, provider_name] if part)
        if "rate-limit" in combined.lower() or "temporarily rate-limited" in combined.lower():
            retryable = True
        return response.status_code, combined or text, retryable

    def chat(
        self,
        messages: Sequence[Dict[str, str]],
        temperature: float = 0.2,
        max_retries_per_model: int = 4,
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://local.research.repo",
            "X-Title": "bibliografia-moc-pipeline",
        }
        errors: List[str] = []
        total_chars = sum(len(m.get("content", "")) for m in messages)
        start_index = self.preferred_model_index

        for offset in range(len(self.models)):
            actual_index = (start_index + offset) % len(self.models)
            model = self.models[actual_index]
            model_input_budget = model_safe_total_input_chars(model)
            if total_chars > model_input_budget:
                detail = (
                    f"context_too_large model={model} total_chars={total_chars} budget={model_input_budget} "
                    f"recommended_chunk_chars={model_safe_chunk_chars(model)}"
                )
                errors.append(detail)
                print(f"   -> pulando modelo {model}: contexto grande demais ({total_chars} > {model_input_budget})")
                if actual_index > start_index:
                    raise NeedSmallerChunkError(model, model_safe_chunk_chars(model), detail)
                continue

            payload = {
                "model": model,
                "messages": list(messages),
                "temperature": temperature,
            }
            print(f"   -> OpenRouter usando modelo {actual_index + 1}/{len(self.models)}: {model}")
            for attempt in range(1, max_retries_per_model + 1):
                try:
                    response = self.session.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=self.timeout,
                    )
                    if response.status_code >= 400:
                        status_code, detail, retryable = self._extract_error_info(response)
                        if retryable and attempt < max_retries_per_model:
                            wait_seconds = min(5 * (2 ** (attempt - 1)), 60)
                            print(
                                f"   -> modelo {model} retornou HTTP {status_code}; aguardando {wait_seconds}s antes de tentar novamente"
                            )
                            time.sleep(wait_seconds)
                            continue
                        raise RuntimeError(
                            f"modelo={model} HTTP {status_code}: {detail[:1200]}"
                        )
                    data = response.json()
                    self.preferred_model_index = actual_index
                    return data["choices"][0]["message"]["content"]
                except Exception as exc:  # noqa: BLE001
                    if isinstance(exc, RuntimeError):
                        errors.append(str(exc))
                        print(f"   -> falha no modelo {model}: {exc}")
                        break
                    if attempt < max_retries_per_model:
                        wait_seconds = min(5 * (2 ** (attempt - 1)), 60)
                        print(
                            f"   -> erro transitório no modelo {model}: {exc}; aguardando {wait_seconds}s"
                        )
                        time.sleep(wait_seconds)
                        continue
                    errors.append(f"modelo={model}: {exc}")
                    print(f"   -> falha definitiva no modelo {model}: {exc}")
                    break

            if offset < len(self.models) - 1:
                print(f"   -> alternando para próximo modelo após falha com {model}")

        raise RuntimeError(
            "Falha ao chamar OpenRouter após backoff e troca de modelo: " + " || ".join(errors)
        )


def strip_accents(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def normalized_title_tokens(text: str) -> List[str]:
    text = strip_accents(text)
    text = text.lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    return [ROMAN_MAP.get(tok, tok) for tok in tokens]


def normalize_title(text: str) -> str:
    return "_".join(normalized_title_tokens(text))


def estimate_safe_chunk_chars(models: Sequence[str]) -> int:
    windows = [MODEL_CONTEXT_WINDOWS[m] for m in models if m in MODEL_CONTEXT_WINDOWS]
    if not windows:
        return 30000
    smallest_window = min(windows)
    estimated = int(smallest_window * 3 * 0.25)
    return max(30000, estimated)


def model_safe_chunk_chars(model: str) -> int:
    window = MODEL_CONTEXT_WINDOWS.get(model)
    if not window:
        return 30000
    return max(30000, int(window * 3 * 0.25))


def model_safe_total_input_chars(model: str) -> int:
    window = MODEL_CONTEXT_WINDOWS.get(model)
    if not window:
        return 120000
    return max(120000, int(window * 3 * 0.70))


def split_text_for_budget(text: str, budget: int) -> List[str]:
    text = text.strip()
    if len(text) <= budget:
        return [text]

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paragraphs:
        return [text[i : i + budget] for i in range(0, len(text), budget)]

    parts: List[str] = []
    buffer: List[str] = []
    buffer_len = 0
    for para in paragraphs:
        if len(para) > budget:
            if buffer:
                parts.append("\n\n".join(buffer))
                buffer = []
                buffer_len = 0
            parts.extend([para[i : i + budget] for i in range(0, len(para), budget)])
            continue
        if buffer and buffer_len + len(para) + 2 > budget:
            parts.append("\n\n".join(buffer))
            buffer = [para]
            buffer_len = len(para)
        else:
            buffer.append(para)
            buffer_len += len(para) + 2
    if buffer:
        parts.append("\n\n".join(buffer))
    return parts


def slugify(text: str, max_len: int = 72) -> str:
    slug = normalize_title(text)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug[:max_len].rstrip("_") or "moc"


def titles_match(a: str, b: str) -> bool:
    ta = normalized_title_tokens(a)
    tb = normalized_title_tokens(b)
    na = "_".join(ta)
    nb = "_".join(tb)
    if na == nb or na in nb or nb in na:
        return True
    common_prefix = 0
    for xa, xb in zip(ta, tb):
        if xa != xb:
            break
        common_prefix += 1
    if common_prefix >= 5:
        return True
    set_a, set_b = set(ta), set(tb)
    if set_a and set_b:
        overlap = len(set_a & set_b) / min(len(set_a), len(set_b))
        if overlap >= 0.8 and any(tok.isdigit() for tok in set_a & set_b):
            return True
    return False


def preferred_source(paths: Sequence[Path]) -> Path:
    ranked = sorted(
        paths, key=lambda p: (0 if p.suffix.lower() == ".pdf" else 1, len(p.name))
    )
    return ranked[0]


def source_candidates(root: Path) -> Dict[Path, List[Path]]:
    groups: Dict[Path, List[Path]] = {}
    by_dir = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SOURCE_EXTENSIONS:
            continue
        if path.name.startswith("MOC_-"):
            continue
        by_dir.setdefault(path.parent, []).append(path)

    for directory, paths in by_dir.items():
        used = set()
        group_id = 0
        for path in sorted(paths):
            if path in used:
                continue
            current = [path]
            used.add(path)
            for other in sorted(paths):
                if other in used:
                    continue
                if titles_match(path.stem, other.stem):
                    current.append(other)
                    used.add(other)
            groups[directory / f"group_{group_id}"] = current
            group_id += 1
    return groups


def existing_mocs_for_dir(directory: Path) -> List[Path]:
    return sorted(p for p in directory.glob("MOC_-*.md") if p.is_file())


def has_matching_moc(source: Path, mocs: Sequence[Path]) -> bool:
    for moc in mocs:
        moc_title = moc.stem.replace("MOC_-", "", 1)
        if titles_match(source.stem, moc_title):
            return True
    return False


def discover_work_items(
    root: Path, only: Optional[Sequence[str]] = None
) -> List[WorkItem]:
    only_paths = {
        str((REPO_ROOT / item).resolve())
        if not os.path.isabs(item)
        else str(Path(item).resolve())
        for item in only or []
    }
    items: List[WorkItem] = []
    for _, variants in source_candidates(root).items():
        source = preferred_source(variants)
        if only_paths and str(source.resolve()) not in only_paths:
            continue
        mocs = existing_mocs_for_dir(source.parent)
        if has_matching_moc(source, mocs):
            continue
        slug = slugify(source.stem)
        target = source.parent / f"MOC_-_{slug}.md"
        items.append(
            WorkItem(
                source_path=source,
                target_moc_path=target,
                title_hint=source.stem,
                source_type=source.suffix.lower().lstrip("."),
            )
        )
    return sorted(items, key=lambda i: str(i.source_path))


def run_command(command: Sequence[str]) -> str:
    proc = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=REPO_ROOT,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Comando falhou ({' '.join(command)}):\n{proc.stdout}")
    return proc.stdout


def pdf_metadata(path: Path) -> Dict[str, str]:
    output = run_command(["pdfinfo", str(path)])
    data: Dict[str, str] = {}
    for line in output.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def extract_pdf_text_range(path: Path, start_page: int, end_page: int) -> str:
    output = run_command(
        [
            "pdftotext",
            "-layout",
            "-f",
            str(start_page),
            "-l",
            str(end_page),
            str(path),
            "-",
        ]
    )
    return output.strip()


def pdf_chunks(
    path: Path, chunk_pages: int, max_chars: int
) -> Tuple[List[Chunk], Dict[str, str]]:
    meta = pdf_metadata(path)
    total_pages = int(meta.get("Pages", "0") or "0")
    chunks: List[Chunk] = []
    idx = 1

    page_windows: List[Tuple[int, int, str]] = []
    for start in range(1, total_pages + 1, chunk_pages):
        end = min(start + chunk_pages - 1, total_pages)
        text = extract_pdf_text_range(path, start, end)
        if text:
            page_windows.append((start, end, text))

    buffer_texts: List[str] = []
    buffer_len = 0
    buffer_start: Optional[int] = None
    buffer_end: Optional[int] = None

    def flush_buffer() -> None:
        nonlocal idx, buffer_texts, buffer_len, buffer_start, buffer_end
        if not buffer_texts or buffer_start is None or buffer_end is None:
            return
        combined = "\n\n".join(buffer_texts).strip()
        if len(combined) <= max_chars:
            chunks.append(
                Chunk(index=idx, label=f"pages {buffer_start}-{buffer_end}", text=combined)
            )
            idx += 1
        else:
            parts = split_text_for_budget(combined, max_chars)
            for part_no, part in enumerate(parts, start=1):
                label = f"pages {buffer_start}-{buffer_end}"
                if len(parts) > 1:
                    label += f" part {part_no}"
                chunks.append(Chunk(index=idx, label=label, text=part))
                idx += 1
        buffer_texts = []
        buffer_len = 0
        buffer_start = None
        buffer_end = None

    for start, end, text in page_windows:
        text_len = len(text)
        if text_len > max_chars:
            flush_buffer()
            parts = split_text_for_budget(text, max_chars)
            for part_no, part in enumerate(parts, start=1):
                label = f"pages {start}-{end}"
                if len(parts) > 1:
                    label += f" part {part_no}"
                chunks.append(Chunk(index=idx, label=label, text=part))
                idx += 1
            continue

        if buffer_texts and buffer_len + text_len + 2 > max_chars:
            flush_buffer()

        if not buffer_texts:
            buffer_start = start
        buffer_texts.append(text)
        buffer_len += text_len + 2
        buffer_end = end

    flush_buffer()

    return chunks, {
        "title": meta.get("Title") or path.stem,
        "author": meta.get("Author") or "Autor não identificado",
        "pages": str(total_pages or ""),
        "source": "PDF",
    }


def html_to_text(data: str) -> str:
    data = re.sub(r"<script\b.*?</script>", " ", data, flags=re.I | re.S)
    data = re.sub(r"<style\b.*?</style>", " ", data, flags=re.I | re.S)
    data = re.sub(
        r"<(h1|h2|h3|h4|h5|h6|p|div|section|article|li|blockquote|pre|tr|table|br)[^>]*>",
        "\n",
        data,
        flags=re.I,
    )
    data = re.sub(r"<[^>]+>", " ", data)
    data = html.unescape(data)
    data = re.sub(r"\r", "\n", data)
    data = re.sub(r"\n{3,}", "\n\n", data)
    data = re.sub(r"[ \t]{2,}", " ", data)
    return data.strip()


def epub_chunks(path: Path, max_chars: int) -> Tuple[List[Chunk], Dict[str, str]]:
    container_ns = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
    opf_ns = {
        "opf": "http://www.idpf.org/2007/opf",
        "dc": "http://purl.org/dc/elements/1.1/",
    }
    chunks: List[Chunk] = []
    with tempfile.TemporaryDirectory(prefix="moc_epub_") as td:
        tempdir = Path(td)
        with zipfile.ZipFile(path) as zf:
            zf.extractall(tempdir)
        container = ET.fromstring((tempdir / "META-INF" / "container.xml").read_bytes())
        opf_rel = container.find(".//c:rootfile", container_ns).attrib["full-path"]
        opf_path = tempdir / opf_rel
        opf = ET.fromstring(opf_path.read_bytes())
        base = opf_path.parent
        manifest = {
            item.attrib["id"]: item.attrib.get("href", "")
            for item in opf.findall(".//opf:manifest/opf:item", opf_ns)
        }
        spine = [
            item.attrib["idref"]
            for item in opf.findall(".//opf:spine/opf:itemref", opf_ns)
        ]
        title = (
            opf.findtext(".//dc:title", default=path.stem, namespaces=opf_ns)
            or path.stem
        )
        author = (
            opf.findtext(
                ".//dc:creator", default="Autor não identificado", namespaces=opf_ns
            )
            or "Autor não identificado"
        )
        idx = 1
        buffer: List[str] = []
        buffer_len = 0
        range_start = 1
        current_section = 1
        for idref in spine:
            href = manifest.get(idref)
            if not href:
                current_section += 1
                continue
            section_path = base / href
            if not section_path.exists():
                current_section += 1
                continue
            try:
                raw = section_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                raw = section_path.read_text(encoding="latin-1", errors="ignore")
            text = html_to_text(raw)
            if not text:
                current_section += 1
                continue
            if buffer and buffer_len + len(text) + 2 > max_chars:
                chunks.append(
                    Chunk(
                        index=idx,
                        label=f"spine sections {range_start}-{current_section - 1}",
                        text="\n\n".join(buffer),
                    )
                )
                idx += 1
                buffer = [text]
                buffer_len = len(text)
                range_start = current_section
            else:
                buffer.append(text)
                buffer_len += len(text) + 2
            current_section += 1
        if buffer:
            chunks.append(
                Chunk(
                    index=idx,
                    label=f"spine sections {range_start}-{current_section - 1}",
                    text="\n\n".join(buffer),
                )
            )
    return chunks, {
        "title": title,
        "author": author,
        "pages": "",
        "source": "EPUB",
    }


def load_prompt_template() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def fill_prompt_template(
    template: str, title: str, author: str, pages: str, source: str
) -> str:
    filled = template
    filled = filled.replace("[TÍTULO]", title)
    filled = filled.replace("[AUTOR]", author)
    filled = filled.replace("[NÚMERO DE PÁGINAS, se souber]", pages or "não informado")
    filled = filled.replace("[PDF / EPUB / texto extraído / OCR / transcrição]", source)
    return filled


def ensure_dirs() -> None:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    (LOG_ROOT / "state").mkdir(parents=True, exist_ok=True)


def state_dir_for(source_path: Path) -> Path:
    slug = slugify(str(source_path.relative_to(REPO_ROOT)))
    return LOG_ROOT / "state" / slug


def dated_log_path(source_path: Path) -> Path:
    date_prefix = dt.datetime.now().strftime("%Y%m%d")
    slug = slugify(str(source_path.relative_to(REPO_ROOT)))
    return LOG_ROOT / f"{date_prefix}_{slug}.log"


def append_log(log_path: Path, message: str) -> None:
    timestamp = dt.datetime.now().isoformat(timespec="seconds")
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(f"[{timestamp}] {message}\n")


def save_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_json(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def extract_chunks(
    work: WorkItem, chunk_pages: int, max_chars: int
) -> Tuple[List[Chunk], Dict[str, str]]:
    if work.source_path.suffix.lower() == ".pdf":
        return pdf_chunks(
            work.source_path, chunk_pages=chunk_pages, max_chars=max_chars
        )
    if work.source_path.suffix.lower() == ".epub":
        return epub_chunks(work.source_path, max_chars=max_chars)
    raise RuntimeError(f"Formato não suportado: {work.source_path.suffix}")


def build_dossier_prompt(
    meta: Dict[str, str], chunk: Chunk, prior_dossier: str
) -> List[Dict[str, str]]:
    system = (
        "Você é um analista de conhecimento construindo um dossiê cumulativo de extração para um livro. "
        "Sua tarefa é atualizar o dossiê com base no novo trecho, preservando o que já foi descoberto e "
        "deixando explícitas incertezas. Não invente. Não copie trechos longos; sintetize. "
        "Responda em Markdown com estas seções exatas: \n"
        "# Dossiê cumulativo\n"
        "## Metadados\n"
        "## Estrutura identificada até agora\n"
        "## Tese central em elaboração\n"
        "## Conceitos-chave acumulados\n"
        "## Domínios de aplicação observados\n"
        "## Evidências textuais curtas\n"
        "## Lacunas / ambiguidades a verificar\n"
        "## Próximos pontos de atenção\n"
    )
    user = (
        f"Metadados conhecidos:\n"
        f"- Título: {meta.get('title') or 'não identificado'}\n"
        f"- Autor: {meta.get('author') or 'não identificado'}\n"
        f"- Total de páginas: {meta.get('pages') or 'não informado'}\n"
        f"- Fonte: {meta.get('source') or 'não informada'}\n\n"
        f"Dossiê acumulado anterior:\n\n{prior_dossier or '(primeiro trecho; ainda não há dossiê anterior)'}\n\n"
        f"Novo trecho: {chunk.label}\n\n"
        f"Texto extraído do trecho:\n\n{chunk.text}\n"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def build_final_prompt(
    template: str, meta: Dict[str, str], dossier: str
) -> List[Dict[str, str]]:
    prompt = fill_prompt_template(
        template,
        title=meta.get("title") or "Título não identificado",
        author=meta.get("author") or "Autor não identificado",
        pages=meta.get("pages") or "não informado",
        source=meta.get("source") or "texto extraído",
    )
    system = (
        "Você é um analista de conhecimento especializado em produzir mapas de conteúdo completos. "
        "Você deve seguir rigorosamente o formato pedido, em português do Brasil, e deixar claro quando algo for inferência."
    )
    user = (
        f"Use o prompt-base abaixo como especificação obrigatória:\n\n{prompt}\n\n"
        "A seguir está o dossiê cumulativo consolidado a partir de múltiplos trechos do arquivo. "
        "Baseie-se nele como fonte principal. Se os intervalos de páginas não forem exatos, sinalize aproximações com honestidade.\n\n"
        f"{dossier}\n"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def process_work(
    client: OpenRouterClient,
    work: WorkItem,
    prompt_template: str,
    chunk_pages: int,
    max_chars: int,
    max_chunks: Optional[int],
    force: bool,
    item_index: int,
    item_total: int,
) -> None:
    ensure_dirs()
    state_dir = state_dir_for(work.source_path)
    log_path = dated_log_path(work.source_path)
    state_dir.mkdir(parents=True, exist_ok=True)
    progress_path = state_dir / "progress.json"
    dossier_path = state_dir / "dossier.md"
    final_draft_path = state_dir / "final_moc.md"

    print(
        f"\n[{item_index}/{item_total}] Iniciando: {work.source_path.relative_to(REPO_ROOT)}"
    )
    append_log(log_path, f"Iniciando processamento de {work.source_path}")
    chunks, meta = extract_chunks(work, chunk_pages=chunk_pages, max_chars=max_chars)
    if max_chunks is not None:
        chunks = chunks[:max_chunks]
    if not chunks:
        raise RuntimeError(f"Nenhum texto extraído de {work.source_path}")
    print(
        f"[{item_index}/{item_total}] Extração concluída: {len(chunks)} chunks detectados | fonte={meta.get('source')} | título={meta.get('title')}"
    )

    progress = {} if force else load_json(progress_path)
    completed = int(progress.get("completed_chunks", 0) or 0)
    dossier = (
        ""
        if force
        else (dossier_path.read_text(encoding="utf-8") if dossier_path.exists() else "")
    )

    meta["title"] = meta.get("title") or work.title_hint
    if not meta.get("author"):
        meta["author"] = "Autor não identificado"

    save_json(
        progress_path,
        {
            "source": str(work.source_path.relative_to(REPO_ROOT)),
            "target_moc": str(work.target_moc_path.relative_to(REPO_ROOT)),
            "completed_chunks": completed,
            "chunk_count": len(chunks),
            "metadata": meta,
        },
    )

    if completed:
        print(
            f"[{item_index}/{item_total}] Retomando de estado salvo: {completed}/{len(chunks)} chunks já concluídos"
        )

    for chunk in chunks[completed:]:
        initial_budget = client.preferred_chunk_chars()
        pending_parts = split_text_for_budget(chunk.text, initial_budget)
        total_parts = len(pending_parts)
        part_index = 0
        while pending_parts:
            current_text = pending_parts.pop(0)
            part_index += 1
            part_label = chunk.label if total_parts == 1 else f"{chunk.label} subpart {part_index}/{total_parts}"
            print(
                f"[{item_index}/{item_total}] Chunk {chunk.index}/{len(chunks)} -> {part_label} | chars={len(current_text)} | modelo-preferido={client.preferred_model()}"
            )
            append_log(
                log_path, f"Processando chunk {chunk.index}/{len(chunks)} ({part_label})"
            )
            working_chunk = Chunk(index=chunk.index, label=part_label, text=current_text)
            messages = build_dossier_prompt(meta, working_chunk, dossier)
            started = time.time()
            try:
                dossier = client.chat(messages, temperature=0.1)
            except NeedSmallerChunkError as exc:
                print(
                    f"[{item_index}/{item_total}] Contexto grande demais para fallback {exc.model}; repartindo para ~{exc.recommended_chars:,} chars"
                )
                subparts = split_text_for_budget(current_text, exc.recommended_chars)
                total_parts = total_parts - 1 + len(subparts)
                pending_parts = subparts + pending_parts
                part_index -= 1
                continue
            elapsed = time.time() - started
            save_text(dossier_path, dossier)
            print(
                f"[{item_index}/{item_total}] Chunk {chunk.index}/{len(chunks)} parte concluída em {elapsed:.1f}s | dossiê={len(dossier)} chars"
            )

        completed = chunk.index
        save_json(
            progress_path,
            {
                "source": str(work.source_path.relative_to(REPO_ROOT)),
                "target_moc": str(work.target_moc_path.relative_to(REPO_ROOT)),
                "completed_chunks": completed,
                "chunk_count": len(chunks),
                "metadata": meta,
            },
        )
        print(
            f"[{item_index}/{item_total}] Chunk {chunk.index}/{len(chunks)} totalmente concluído"
        )

    print(f"[{item_index}/{item_total}] Consolidando MOC final...")
    append_log(log_path, "Gerando MOC final a partir do dossiê cumulativo")
    final_messages = build_final_prompt(prompt_template, meta, dossier)
    started = time.time()
    final_moc = client.chat(final_messages, temperature=0.2)
    elapsed = time.time() - started
    save_text(final_draft_path, final_moc)
    save_text(work.target_moc_path, final_moc)
    print(
        f"[{item_index}/{item_total}] MOC final salvo em {work.target_moc_path.relative_to(REPO_ROOT)} | tamanho={len(final_moc)} chars | tempo={elapsed:.1f}s"
    )
    append_log(log_path, f"MOC salvo em {work.target_moc_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera MOCs para fontes em bibliografia/ usando OpenRouter."
    )
    parser.add_argument(
        "--root",
        default="bibliografia",
        help="Raiz da bibliografia relativa ao repositório.",
    )
    parser.add_argument(
        "--model",
        dest="models",
        action="append",
        help="Modelo OpenRouter a usar. Pode ser repetido; a ordem define o fallback.",
    )
    parser.add_argument(
        "--chunk-pages", type=int, default=20, help="Páginas por chunk para PDFs."
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=None,
        help="Tamanho máximo de texto por chunk enviado ao modelo. Se omitido, o script calcula automaticamente com base na menor janela de contexto dos modelos configurados.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limita quantos trabalhos serão processados.",
    )
    parser.add_argument(
        "--max-chunks",
        type=int,
        default=None,
        help="Limita quantos chunks por trabalho serão processados (útil para teste).",
    )
    parser.add_argument(
        "--only", nargs="*", help="Processa apenas estes arquivos fonte específicos."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Somente lista os trabalhos sem MOC."
    )
    parser.add_argument(
        "--force", action="store_true", help="Reprocessa mesmo se houver estado salvo."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = (REPO_ROOT / args.root).resolve()
    if not root.exists():
        print(f"Raiz não encontrada: {root}", file=sys.stderr)
        return 1
    prompt_template = load_prompt_template()
    items = discover_work_items(root, only=args.only)
    if args.limit is not None:
        items = items[: args.limit]

    if not items:
        print("Nenhum trabalho sem MOC encontrado.")
        return 0

    print("Trabalhos elegíveis:")
    for item in items:
        print(
            f"- {item.source_path.relative_to(REPO_ROOT)} -> {item.target_moc_path.relative_to(REPO_ROOT)}"
        )

    if args.dry_run:
        return 0

    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        print("OPENROUTER_API_KEY não definido.", file=sys.stderr)
        return 1

    models = args.models or list(DEFAULT_MODELS)
    print("Modelos OpenRouter em ordem de fallback:")
    for idx, model in enumerate(models, start=1):
        window = MODEL_CONTEXT_WINDOWS.get(model)
        suffix = f" | janela ~{window:,}" if window else ""
        print(f"  {idx}. {model}{suffix}")

    effective_max_chars = args.max_chars or model_safe_chunk_chars(models[0])
    fallback_floor = estimate_safe_chunk_chars(models)
    print(f"Chunk text budget inicial (modelo preferido): {effective_max_chars:,} caracteres por envio")
    print(f"Piso seguro estimado considerando todos os fallbacks: {fallback_floor:,} caracteres")

    client = OpenRouterClient(api_key=api_key, models=models)
    failures: List[Tuple[WorkItem, Exception]] = []
    total_items = len(items)
    for idx, item in enumerate(items, start=1):
        try:
            process_work(
                client=client,
                work=item,
                prompt_template=prompt_template,
                chunk_pages=args.chunk_pages,
                max_chars=effective_max_chars,
                max_chunks=args.max_chunks,
                force=args.force,
                item_index=idx,
                item_total=total_items,
            )
        except Exception as exc:  # noqa: BLE001
            failures.append((item, exc))
            print(f"FALHA em {item.source_path}: {exc}", file=sys.stderr)

    if failures:
        print("\nFalhas encontradas:", file=sys.stderr)
        for item, exc in failures:
            print(
                f"- {item.source_path.relative_to(REPO_ROOT)}: {exc}", file=sys.stderr
            )
        print(
            f"\nResumo: {total_items - len(failures)}/{total_items} concluídos com sucesso, {len(failures)} falharam."
        )
        return 1

    print(
        f"\nPipeline concluído com sucesso. {total_items}/{total_items} trabalhos processados."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
