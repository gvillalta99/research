---
title: "Research Repository Structure Overview"
description: "Visual guide to the research project management system"
---

# 🏗️ Research Repository Structure

Este repositório implementa um sistema completo de gerenciamento de projetos de pesquisa com pipeline automatizado de agentes IA.

## 📁 Estrutura Completa

```
research/
│
├── 📄 README.md                          # 🎯 Leia primeiro: Visão geral do sistema
├── 📄 RESEARCH_PLAN.md                   # 📊 Plano estratégico e progresso
├── 📄 RESEARCH_IDEAS.md                  # 💡 Ideas e oportunidades de pesquisa
├── 📄 GIT_SUBMODULES_GUIDE.md           # 🔧 Como usar submodules para projetos
├── 📄 STRUCTURE_OVERVIEW.md             # 👈 Este arquivo
│
├── 📁 projects/                          # 🎓 Projetos de pesquisa (submodules git)
│   ├── 📄 AGENTS.md                     # ⚙️ Instruções para agentes aqui
│   ├── 📁 seu-projeto-1/                # 1º projeto
│   ├── 📁 seu-projeto-2/                # 2º projeto
│   └── 📁 seu-projeto-n/                # Enésimo projeto
│
├── 📁 bibliografia/                     # 📚 Corpus de referências organizadas
│   ├── 📄 AGENTS.md                     # ⚙️ Como agentes catalogam
│   ├── 📄 INDEX.md                      # 📋 Inventário (gerado por agentes)
│   ├── 📄 STATISTICS.md                 # 📊 Análises do corpus (gerado)
│   ├── 📄 CATEGORY_TAGS.md              # 🏷️ Taxonomy de temas
│   ├── 📁 livros/                       # 📖 Monografias e livros
│   ├── 📁 artigos/                      # 📰 Journal & conference papers
│   ├── 📁 teses/                        # 🎓 Dissertações e teses
│   ├── 📁 preprints/                    # 📄 ArXiv, bioRxiv, etc
│   └── 📁 relatorios/                   # 📋 Technical reports, whitepapers
│
├── 📁 inbox/                            # 📥 Referências não processadas
│   ├── 📄 AGENTS.md                     # ⚙️ Como agentes processam
│   ├── 📄 PROCESSING_LOG.md             # 📋 Log de processamento
│   ├── 📁 quarantine/                   # ⚠️ Referências problemáticas
│   └── [arquivos a processar]           # PDFs, links, etc
│
├── 📁 research-output/                  # 🎯 Resultados de pesquisas
│   ├── 📄 AGENTS.md                     # ⚙️ Como agentes gerenciam
│   ├── 📄 INDEX.md                      # 📋 Inventário de outputs
│   ├── 📄 QUALITY_STANDARDS.md          # ✅ Padrões de qualidade
│   ├── 📁 project-1/                    # Outputs do projeto 1
│   │   ├── 📁 literature-review/
│   │   ├── 📁 data-analysis/
│   │   ├── 📁 findings/
│   │   ├── 📁 draft-paper/
│   │   └── 📁 final/
│   └── 📁 archive/                      # Versões antigas
│
├── 📁 tools/                            # 🛠️ Scripts e utilitários
│   ├── 📄 AGENTS.md                     # ⚙️ Desenvolvimento de tools
│   ├── 📄 README.md                     # 📖 Guia de ferramentas
│   ├── 📄 requirements.txt               # 📦 Python dependencies
│   ├── 📁 scripts/                      # 🐍 Python scripts
│   │   ├── process_bibtex.py
│   │   ├── extract_metadata.py
│   │   ├── sync_bibliography.py
│   │   ├── cleanup_duplicates.py
│   │   └── generate_reports.py
│   ├── 📁 notebooks/                    # 📓 Jupyter notebooks
│   │   ├── corpus_analysis.ipynb
│   │   └── quality_audit.ipynb
│   ├── 📁 templates/                    # 📋 Templates reutilizáveis
│   │   ├── RESEARCH_BRIEF_TEMPLATE.md
│   │   ├── metadata.yaml
│   │   └── analysis_report.md
│   └── 📁 logs/                         # 📝 Processing logs
│
└── 📄 .gitignore                        # 🔒 Arquivos a ignorar

```

## 🔄 Fluxo de Dados na Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                  RESEARCH PIPELINE OVERVIEW                      │
└─────────────────────────────────────────────────────────────────┘

1. ENTRADA
   ├── New references → inbox/
   ├── Research briefs → projects/*/RESEARCH_BRIEF.md
   └── Existing corpus → bibliografia/

2. PROCESSAMENTO
   ├── inbox/ → (ai-engineer + trend-researcher)
   │           → Bibliografia categorizada
   │           → Metadata validado
   │           → Duplicatas removidas
   │
   ├── projects/ → (project-shepherd)
   │             → Planejamento de pesquisa
   │             → Metodologia definida
   │             → Referências vinculadas
   │
   └── bibliografia/ → (ai-engineer + analytics-reporter)
                     → Corpus indexado
                     → RAG system ativo
                     → Estatísticas geradas

3. ANÁLISE
   ├── Literatura reviews → (feedback-synthesizer)
   ├── Dados analysis → (analytics-reporter)
   ├── Sínteses → (ai-engineer)
   └── Findings → (all specialties)

4. VALIDAÇÃO
   └── reality-checker → Qualidade verificada
                      → Metodologia rigorosa
                      → Outputs prontos

5. SAÍDA
   └── research-output/ → Relatórios finais
                       → Papers em markdown/LaTeX
                       → Datasets processados
                       → Visualizações

```

## 🤖 Agents & Responsabilidades

### Coordenação Central
- **agents-orchestrator**: Orquestra toda a pipeline
- **project-shepherd**: Coordena cronograma e escopo

### Processamento de Referências
- **ai-engineer**: Extração de metadata, indexação, RAG
- **trend-researcher**: Classificação temática, análise de tendências
- **data-consolidation-agent**: Catalogação e consolidação

### Análise & Síntese
- **analytics-reporter**: Estatísticas, relatórios, qualidade
- **feedback-synthesizer**: Síntese de múltiplas análises
- **ux-researcher**: Estrutura de estudos empíricos

### Validação & Qualidade
- **reality-checker**: Validação de rigor metodológico
- **code-reviewer**: Review de metodologia (se aplicável)

## 📊 Exemplos de Uso

### Exemplo 1: Adicionar Nova Referência

```bash
# 1. Coloque o arquivo em inbox/
cp ~/Downloads/new_paper.pdf research/inbox/

# 2. Agentes processam automaticamente
# - ai-engineer: Extrai metadata
# - trend-researcher: Classifica tema
# - Se válido: Move para bibliografia/{categoria}/
# - Se duplicata: Notifica

# 3. Resultado
# research/bibliografia/artigos/lastname2024title.*
#                              ├── .md (metadata)
#                              ├── .bibtex (BibTeX)
#                              └── .pdf (original)
```

### Exemplo 2: Criar Novo Projeto

```bash
# 1. Setup submodule
git submodule add <repo-url> projects/meu-projeto

# 2. Criar research brief
cp tools/templates/RESEARCH_BRIEF_TEMPLATE.md \
   projects/meu-projeto/RESEARCH_BRIEF.md
# ... preencha com detalhes ...

# 3. Agentes processam
# - project-shepherd: Cria plano
# - ai-engineer: Vincula referências
# - analytics-reporter: Gera initial report

# 4. Resultado
# projects/meu-projeto/
#                ├── RESEARCH_BRIEF.md (preenchido)
#                ├── RESEARCH_PLAN.md (gerado)
#                ├── REFERENCED_PAPERS.md (agente)
#                └── STATUS.md (atualizado)
```

### Exemplo 3: Executar Análise

```bash
# 1. Pesquisador coloca draft em
# research-output/projeto-x/draft-paper/

# 2. Agentes processam
# - ai-engineer: Valida estrutura
# - reality-checker: Verifica rigor
# - feedback-synthesizer: Integra com outras análises

# 3. Iteração baseada em feedback
# - Pesquisador atualiza
# - Agentes re-validam
# - Até PASS

# 4. Resultado
# research-output/projeto-x/final/
#                           ├── paper_v1.0.md
#                           ├── paper_v1.0.pdf
#                           └── SUBMISSION.md
```

## 📚 Leitura Recomendada

### Primeiro Acesso
1. ✅ **README.md** - Visão geral
2. ✅ **RESEARCH_PLAN.md** - Estratégia
3. ✅ **Seu AGENTS.md específico** - Para o módulo que usa

### Antes de Criar Projeto
1. **GIT_SUBMODULES_GUIDE.md** - Como funciona versionamento
2. **tools/templates/RESEARCH_BRIEF_TEMPLATE.md** - Template para brief
3. **projects/AGENTS.md** - Fluxo de projetos

### Antes de Adicionar Referência
1. **inbox/AGENTS.md** - Processo de triagem
2. **bibliografia/AGENTS.md** - Estrutura de corpus
3. **tools/README.md** - Ferramentas disponíveis

### Para Publicar Resultados
1. **research-output/AGENTS.md** - Gestão de outputs
2. **research-output/QUALITY_STANDARDS.md** - Padrões
3. **GIT_SUBMODULES_GUIDE.md** - Versionamento

## ⚙️ Configuração Inicial

### 1. Clone com Submodules
```bash
git clone --recurse-submodules <repo-url>
```

### 2. Configure Git (se novo)
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### 3. Instale Dependências
```bash
cd tools
pip install -r requirements.txt
```

### 4. Crie Primeiro Projeto (opcional)
```bash
# Veja GIT_SUBMODULES_GUIDE.md para detalhes
git submodule add <seu-repo> projects/seu-projeto
```

## 🎯 Métricas de Saúde do Repositório

| Métrica | Ideal | Crítico |
|---------|-------|---------|
| Referências catalogadas | 1000+ | <100 |
| Projetos ativos | 10+ | <2 |
| Outputs finalizados | 5+ | 0 |
| Update frequency | Semanal | <Mensal |
| Quality score (avg) | 8+/10 | <6/10 |
| Processing rate | 50+ refs/week | <10 |

## 🆘 Suporte & Troubleshooting

### Problemas Comuns

**Q: Arquivo grande não faz commit**
A: Veja .gitignore; se for PDF, considere armazenar separadamente

**Q: Submodule em detached HEAD**
A: Execute `cd projects/seu-projeto && git checkout main`

**Q: Agentes não processam referência**
A: Veja inbox/AGENTS.md; pode ser arquivo corrompido ou formato não suportado

**Q: Corpus muito lento para buscar**
A: Execute ferramentas de reindexação em tools/scripts/

### Recursos

- **inbox/AGENTS.md** - Como triagem funciona
- **tools/README.md** - Ferramentas disponíveis
- **tools/notebooks/** - Análises exploratórias
- **GIT_SUBMODULES_GUIDE.md** - Git troubleshooting

## 📈 Próximos Passos

1. ✅ Estrutura criada
2. ⏳ Processar primeiras referências (inbox/)
3. ⏳ Criar primeiro projeto
4. ⏳ Executar primeira análise
5. ⏳ Publicar primeira síntese

---

**Repository Setup Date**: 2026-03-18
**Status**: 🟡 Infrastructure Ready, awaiting projects
**Maintained By**: Research Team + AI Agents
