# AGENTS.md - Projects Module

## 🎯 Propósito
Cada pasta `projects/` contém um submodulo git independente com um projeto de pesquisa específico. Este módulo é o ponto de entrada para coordenação entre pesquisas e gerenciamento de escopo.

## 📋 Responsabilidades dos Agentes Aqui

### Agents Esperados
- **project-shepherd**: Coordenação geral, timeline, milestones
- **agents-orchestrator**: Orquestração de pipeline de pesquisa
- **senior-project-manager**: Controle de escopo e requisitos

### Entrada (Input)
- `RESEARCH_BRIEF.md` em cada subprojeto
- Timeline de pesquisa com marcos
- Referências bibliográficas recomendadas de `../bibliografia/`
- Requisitos específicos do domínio

### Processamento
1. Ler `RESEARCH_BRIEF.md` de cada projeto
2. Extrair palavras-chave e scopos de pesquisa
3. Linkar com referências relevantes em `../bibliografia/`
4. Criar plano de execução com tarefas para agentes especializados
5. Coordenar handoffs entre diferentes agentes de pesquisa

### Saída (Output)
- `RESEARCH_PLAN.md` - Plano detalhado de execução
- `STATUS.md` - Status atual do projeto
- Referências aos outputs em `../research-output/`
- Commits regulares com progresso

## 📁 Estrutura de um Projeto (Submodulo)

```
projects/seu-projeto/
├── RESEARCH_BRIEF.md       # Escopo, objetivos, perguntas de pesquisa
├── RESEARCH_PLAN.md        # Plano de execução (gerado por agents)
├── STATUS.md               # Progresso atual
├── data/                   # Datasets específicos do projeto
├── notebooks/              # Análises exploratórias
├── results/                # Outputs finais
└── references.bib          # BibTeX com referências selecionadas
```

## 🔄 Workflow com Agentes

### Fase 1: Briefing & Planning (project-shepherd)
```
project-shepherd lê RESEARCH_BRIEF.md e:
- Define tarefas específicas de pesquisa
- Cria timeline com marcos
- Identifica dependências entre tarefas
- Produz RESEARCH_PLAN.md
```

### Fase 2: Análise Bibliográfica (ai-engineer + analytics-reporter)
```
ai-engineer:
- Consulta corpus em ../bibliografia/
- Cria índices de referências relevantes
- Setup RAG system para análise contextualizada

analytics-reporter:
- Gera estatísticas do corpus
- Identifica gaps na literatura
- Produz sínteses temáticas
```

### Fase 3: Execução de Pesquisa
Depends on project type. Pode envolver:
- **Data Science**: ai-engineer com pipelines de dados
- **Literature Review**: feedback-synthesizer com sínteses
- **Systematic Review**: agents-orchestrator coordenando análises paralelas
- **Original Studies**: experimental-tracker com validações

### Fase 4: Validação (reality-checker)
```
reality-checker avalia:
- Rigor metodológico
- Validez das conclusões
- Qualidade das evidências
- Comparabilidade com literatura
```

## ⚡ Instruções para Agentes

### 🎬 Para Começar um Novo Projeto

**Spawn command:**
```
Por favor, use a skill project-shepherd para:
1. Ler o arquivo RESEARCH_BRIEF.md em projects/{projeto-name}/
2. Consultar arquivos em ../bibliografia/ para temas relevantes
3. Criar um arquivo RESEARCH_PLAN.md detalhado com:
   - Objetivos de pesquisa claros
   - Metodologia proposta
   - Tarefas específicas e sequenciamento
   - Timeline com marcos
   - Recursos bibliográficos já identificados
   - Métricas de sucesso

Inclua no plano as referências específicas em ../referencias/
que são relevantes para este projeto.
```

### 🔍 Para Vincular Referências

**Spawn command:**
```
Por favor, use a skill ai-engineer para:
1. Analisar RESEARCH_BRIEF.md do projeto
2. Consultar todos os arquivos em ../bibliografia/
3. Criar uma seção "REFERENCED_PAPERS.md" com:
   - Lista BibTeX das referências relevantes
   - Abstract de cada referência
   - Tag com tema/categoria
   - Força da relação com o escopo (forte/média/fraca)
   
Salve como projects/{projeto-name}/REFERENCED_PAPERS.md
```

### 📊 Para Atualizar Status

**Spawn command:**
```
Por favor, crie um arquivo STATUS.md em projects/{projeto-name}/ com:
- Data da última atualização
- Tarefas completadas (checklist)
- Tarefas em progresso
- Bloqueadores identificados
- Próximos passos
- Desvios da timeline (se houver)
```

## 🏆 Convenções

- **Nomes**: Use `kebab-case` para nomes de projetos: `meu-projeto-2024`
- **RESEARCH_BRIEF**: Arquivo OBRIGATÓRIO em cada subprojeto
- **Atualizações**: STATUS.md deve ser atualizado a cada 2 semanas
- **Commits**: Um commit por progresso meaningful, com descrição clara

## 📌 Exemplos de RESEARCH_BRIEF.md

```yaml
---
title: "Análise de Escalabilidade em Sistemas Distribuídos"
author: "Your Name"
date: "2026-03-18"
status: "planning"
---

## Questões de Pesquisa
1. Quais padrões arquiteturais maximizam escalabilidade?
2. Como o particionamento de dados afeta latência?
3. Trade-offs entre consistência e disponibilidade?

## Escopo
- Foco: Sistemas de tempo real (< 100ms latency)
- Período: 2023-2026
- Linguagens: Distributed systems literature
- Datasets: Simulações e benchmarks públicos

## Metodologia
- Literatura Review: Análise de papers em topologia de cluster
- Análise Comparativa: Benchmarking de 3 arquiteturas
- Simulação: Modelos de carga para validação

## Outputs Esperados
- Taxonomy de padrões de escalabilidade
- Comparative analysis table
- Recommendations framework

## Referências Iniciais
Veja REFERENCED_PAPERS.md (será gerado por AI agent)
```

---

**Mantém coordenação central entre projetos e corpus bibliográfico global**
