# AGENTS.md

## Escopo
`inbox/` recebe referências ainda não processadas.

## O que pode entrar aqui
- PDFs, EPUBs e outros arquivos brutos.
- URLs salvas em `.txt`, `.md` ou `.url`.
- Exportações RIS, BibTeX ou JSON ainda não normalizadas.
- Pastas temporárias com notas de coleta.

## Regras
- Nenhum item deve permanecer aqui depois de processado.
- Antes de mover qualquer item para `../bibliografia/`, validar metadados mínimos: título, autor principal e ano.
- Duplicatas ou itens problemáticos devem ir para `quarantine/`.
- Se houver processamento em lote, registrar um `PROCESSING_LOG.md`.

## Fluxo recomendado
1. Validar o item.
2. Classificar a categoria de destino.
3. Deduplicar contra `../bibliografia/`.
4. Gerar metadata `.md` e entrada `.bib`.
5. Mover para a categoria apropriada ou para `quarantine/`.

## Skills preferenciais
- `agents-orchestrator`
- `ai-engineer`
- `trend-researcher`
