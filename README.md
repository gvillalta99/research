# Research Project Management

Estrutura de trabalho para pesquisa assistida por agentes, com separação clara entre projetos, corpus bibliográfico, triagem e outputs.

## Estrutura

```text
research/
├── AGENTS.md
├── projects/                         # cada projeto é um submódulo Git
├── bibliografia/
│   ├── AGENTS.md
│   ├── livros/
│   ├── artigos/
│   ├── teses/
│   ├── preprints/
│   └── relatorios/
├── inbox/
│   ├── AGENTS.md
│   └── quarantine/
├── research-output/
│   ├── AGENTS.md
│   ├── projects/
│   └── shared/
└── tools/
    ├── AGENTS.md
    ├── scripts/
    ├── templates/
    └── logs/
```

## Regras centrais

- Todo projeto novo entra em `projects/` como submódulo.
- Toda referência nova entra primeiro em `inbox/`.
- Toda referência processada vai para `bibliografia/<categoria>/`.
- Todo entregável consolidado vai para `research-output/`.
- Cada pasta operacional possui seu próprio `AGENTS.md`.

## Fluxo recomendado

1. Coloque material novo em `inbox/`.
2. Processe, classifique e deduplique contra `bibliografia/`.
3. Trabalhe o escopo e a execução dentro do submódulo em `projects/<project-slug>/`.
4. Publique sínteses, drafts e versões finais em `research-output/projects/<project-slug>/`.
5. Use `research-output/shared/` para artefatos transversais.

## Skills previstas

As instruções locais já foram preparadas para priorizar estas skills:
- `agents-orchestrator`
- `senior-project-manager`
- `ai-engineer`
- `trend-researcher`
- `analytics-reporter`
- `feedback-synthesizer`
- `reality-checker`

## Convenções

- Slugs de projeto em `kebab-case`.
- Identificadores bibliográficos em `author_year_slug`.
- Referências processadas devem ter, quando aplicável, arquivo original + `.md` + `.bib`.
- Outputs devem manter vínculo explícito com o projeto ou corpus de origem.
