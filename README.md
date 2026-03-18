# Research Project Management

Estrutura centralizada para gerenciar projetos de pesquisa com integração de agentes IA para análise de referências bibliográficas e execução de estudos sistemáticos.

## 📁 Estrutura do Repositório

```
research/
├── projects/                    # Submodulos git para cada projeto de pesquisa
├── bibliografia/               # Corpus de referências bibliográficas organizadas
│   ├── livros/                # Livros e monografias
│   ├── artigos/               # Artigos de periódicos e conferências
│   ├── teses/                 # Dissertações e teses
│   ├── preprints/             # Preprints e working papers
│   └── relatorios/            # Relatórios técnicos
├── inbox/                     # Referências não processadas para triagem
├── research-output/           # Resultados de pesquisas executadas
├── tools/                     # Scripts e utilitários para processamento
└── RESEARCH_PLAN.md          # Planejamento estratégico de pesquisa
```

## 🤖 Workflow de Pesquisa com Agentes

### 1. Coleta e Processamento de Referências
- **Inbox**: Novas referências adicionadas sem classificação
- **Agents**: `ai-engineer` + `trend-researcher` processam e indexam
- **Output**: Referências catalogadas em `bibliografia/`

### 2. Design de Estudos
- **Input**: Projetos em `projects/` com research briefs
- **Agents**: `ai-engineer` + `project-shepherd` + `ux-researcher`
- **Output**: Planos de pesquisa e metodologias

### 3. Análise e Síntese
- **Input**: Corpus bibliográfico + research briefs
- **Agents**: `ai-engineer` (RAG/NLP) + `analytics-reporter` + `feedback-synthesizer`
- **Output**: Sínteses, insights e relatórios em `research-output/`

### 4. Validação e Iteração
- **Input**: Drafts de resultados
- **Agents**: `reality-checker` + `code-reviewer` (para metodologia)
- **Output**: Research-ready papers

## 🎯 Cada Módulo tem:

- **AGENTS.md**: Instruções específicas para agentes naquele contexto
- **INDEX.md**: Inventário e metadata de conteúdo (quando aplicável)
- **README.md**: Documentação e convenções locais (quando complexo)

## 🚀 Início Rápido

### Adicionar Nova Referência
```bash
# 1. Coloque o arquivo em inbox/
cp paper.pdf research/inbox/

# 2. Execute processamento
# Agentes lerão AGENTS.md em inbox/ e processarão automaticamente
```

### Criar Novo Projeto
```bash
# 1. Adicione submodulo git em projects/
git submodule add <url> projects/meu-projeto

# 2. Crie research brief em projects/meu-projeto/RESEARCH_BRIEF.md
# 3. Agentes lerão contexto e referências relevantes para execução
```

### Executar Pesquisa
```bash
# Agentes-orchestrator lê AGENTS.md em todos os módulos
# Coordena pipeline de análise bibliográfica
# Gera outputs em research-output/
```

## 📚 Guias por Módulo

- [Projects](./projects/AGENTS.md) - Gestão de subprojetos
- [Bibliografia](./bibliografia/AGENTS.md) - Corpus bibliográfico
- [Inbox](./inbox/AGENTS.md) - Triagem de referências
- [Research Output](./research-output/AGENTS.md) - Gestão de resultados

## 🔗 Skills Integradas

Este projeto usa os seguintes agentes especializados:

- **ai-engineer**: Processamento de dados, indexação, RAG systems
- **project-shepherd**: Coordenação de projetos e timelines
- **analytics-reporter**: Análise de dados bibliográficos
- **trend-researcher**: Identificação de tendências em pesquisa
- **feedback-synthesizer**: Síntese de múltiplas fontes
- **agents-orchestrator**: Orquestração do pipeline completo
- **reality-checker**: Validação de metodologias e qualidade
- **ux-researcher**: Estrutura de estudos empíricos

## 📝 Convenções

- Nomes de arquivos: `snake_case` para dados, `PascalCase` para projetos
- Metadata: YAML front matter em .md para indexação
- Referências: Usar BibTeX quando possível para compatibilidade
- Versionamento: Git para controle, com commits granulares

---

**Última atualização**: 2026-03-18
**Mantido por**: Research Team + AI Agents
