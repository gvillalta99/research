# AGENTS.md - Research Output Module

## 🎯 Propósito
Gestão de outputs de pesquisa: relatórios, sínteses, análises, papers em draft e resultados finais. Este é o "resultado" tangível de toda a pipeline de pesquisa.

## 📋 Responsabilidades dos Agentes

### Agents Esperados
- **analytics-reporter**: Análise de dados e geração de relatórios
- **feedback-synthesizer**: Síntese de múltiplas análises
- **reality-checker**: Validação de qualidade e rigor metodológico
- **ai-engineer**: Processamento de dados e visualizações

### Entrada (Input)
- Drafts de pesquisadores
- Resultados de análises
- Sínteses de literatura
- Dados brutos de estudos
- Comentários de revisores

### Processamento
1. **Recebimento**: Registrar novo output
2. **Validação**: Verificar estrutura e qualidade
3. **Análise**: Executar controle de qualidade
4. **Síntese**: Consolidar múltiplas versões/análises
5. **Refinement**: Iterar baseado em feedback
6. **Publicação**: Marcar como ready-to-publish
7. **Arquivamento**: Versionar e documentar

### Saída (Output)
- Relatórios finais
- Papers em markdown/LaTeX
- Datasets processados
- Visualizações
- Summaries para sharing

## 📁 Estrutura

```
research-output/
├── AGENTS.md                    # Este arquivo
├── INDEX.md                     # Inventário de outputs
├── QUALITY_STANDARDS.md         # Padrões de qualidade esperados
├── (by-project)/
│   ├── project-name/
│   │   ├── literature-review/   # Sínteses de literatura
│   │   ├── data-analysis/       # Análises de dados
│   │   ├── findings/            # Descobertas principais
│   │   ├── draft-paper/         # Versão em escrita
│   │   └── final/               # Versão publicável
│   └── another-project/
├── (by-type)/
│   ├── reports/                 # Relatórios técnicos
│   ├── papers/                  # Papers em draft/final
│   ├── datasets/                # Dados processados
│   └── visualizations/          # Gráficos e diagramas
└── archive/                     # Versões antigas
```

## 📊 Tipos de Outputs

### Literature Review
- Sínteses temáticas do corpus
- Mapping de pesquisas relacionadas
- Identificação de gaps
- **Formato**: Markdown com referências BibTeX

### Data Analysis
- Resultados de experimentos
- Análises estatísticas
- Tabelas comparativas
- **Formato**: Jupyter notebooks + reports em MD

### Findings
- Descobertas principais
- Conclusões preliminares
- Recomendações
- **Formato**: Structured markdown ou MD

### Draft Paper
- Manuscrito em preparação
- Versões iterativas
- Com comments e TODOs
- **Formato**: LaTeX ou Markdown with metadata

### Final Publication
- Versão publicável
- Peer-reviewed
- Pronto para submission
- **Formato**: LaTeX PDF + Source

## 🔄 Workflow com Agentes

### Fase 1: Recebimento de Output

```
Output chega (draft, análise, resultado):
├─ Pesquisador cria pasta em research-output/{project}/
├─ Documenta inicial_status.md
└─ Agentes são notificados via INDEX.md
```

### Fase 2: Validação Inicial (ai-engineer)

```
ai-engineer verifica:
1. Estrutura básica está presente?
   - Título/objetivo claro?
   - Metodologia documentada?
   - Referências listadas?

2. Completude de metadata:
   - Data de criação
   - Autor(es)
   - Versão/status
   - Links para dataset/código

3. Retorna checklist de ajustes necessários
```

### Fase 3: Análise Substantiva (reality-checker)

```
reality-checker questiona:
1. Qualidade metodológica:
   - Métodos apropriados para questão?
   - Foram validadas hipóteses?
   - Limitations documentadas?

2. Rigor das conclusões:
   - Evidências suportam conclusões?
   - Generalizações adequadas?
   - Alternative explanations consideradas?

3. Relevância do output:
   - Responde questão de pesquisa?
   - Contribui ao knowledge?
   - Impacto potencial?

4. Retorna: PASS / NEEDS_REVISION / REJECT com feedback
```

### Fase 4: Síntese & Integração (feedback-synthesizer)

```
Se múltiplas análises/versões:
1. Consolida insights principais
2. Resolve contradições
3. Identifica pontos de consenso
4. Gera síntese integrada
```

### Fase 5: Refinement Iterativo (ai-engineer + realit-checker)

```
Baseado em feedback:
1. ai-engineer atualiza conteúdo
2. reality-checker re-valida
3. Loop continua até PASS
4. Quando pronto: marcar como FINAL
```

## ⚡ Instruções para Agentes

### 🎬 Para Registrar Novo Output

**Spawn command:**
```
Por favor, registre um novo output de pesquisa:

1. Leia o arquivo(s) em ./research-output/{project}/{tipo}/
2. Extraia metadata:
   - Título, autores, data
   - Tipo (literatura-review, data-analysis, findings, draft-paper, final)
   - Status (draft, under-review, accepted, published)
   - Link para projeto pai
   - Keywords/tags

3. Crie ou atualize INDEX.md com:
   - Entrada nova do output
   - Links para arquivo
   - Status atual
   - Última atualização

4. Valide estrutura básica (use checklist QUALITY_STANDARDS.md)
```

### 📋 Para Gerar Relatório de Qualidade

**Spawn command:**
```
Por favor, use a skill reality-checker para validar um output:

Avalie em relação a QUALITY_STANDARDS.md:

1. **Estrutura & Completude** (checklist)
   - Título, abstract/resumo, objetivo
   - Metodologia clara
   - Seções esperadas presentes
   - Referências BibTeX

2. **Qualidade Metodológica** (crítica substantiva)
   - Métodos apropriados? Por quê/por quê não?
   - Foram validadas? Evidence?
   - Limitations documentadas?
   - Replicabilidade?

3. **Rigor de Conclusões** (validação lógica)
   - Evidências suportam?
   - Claims têm qualificadores apropriados?
   - Generalizações justificadas?
   - Reconhece alternative explanations?

4. **Impacto & Relevância** (contexto)
   - Responde questão de pesquisa original?
   - Novo conhecimento vs. repetição?
   - Potencial impacto?

5. **Produção Report**:
   - Formato: research-output/{project}/{tipo}/REVIEW_{date}.md
   - Inclua: PASS / NEEDS_REVISION / REJECT
   - Feedback específico em cada seção
   - Recomendações para melhoria
```

### 🔄 Para Sintetizar Múltiplas Análises

**Spawn command:**
```
Por favor, use a skill feedback-synthesizer para consolidar múltiplas análises:

1. Identifique todas as análises relacionadas em:
   ./research-output/{project}/*/
   
2. Para cada tipo de análise (data-analysis, findings, etc):
   - Leia todos os outputs daquele tipo
   - Identifique insights principais de cada
   - Extraia dados/números chave
   
3. Consolide em síntese integrada:
   - Pontos de consenso entre análises
   - Contradições (e como resolvê-las)
   - Insights novos quando combinadas
   - Gaps não cobertos
   
4. Crie SYNTHESIS_{date}.md com:
   - Resumo executivo
   - Achados principais integrados
   - Recomendações
   - Links para analyses originais
```

### 📊 Para Processar Dataset

**Spawn command:**
```
Por favor, processe um dataset para research output:

1. Localize dados em: ./research-output/{project}/data/
2. Analise:
   - Estrutura (CSV, JSON, DB, etc)
   - Completude (missing values?)
   - Validação de tipo
   - Outliers/anomalias

3. Processe:
   - Limpeza (se necessário)
   - Normalização
   - Visualizações exploratórias
   - Sumários estatísticos

4. Produza:
   - Arquivo cleaned_{tipo}.{ext}
   - notebook com EDA (Exploratory Data Analysis)
   - DATASET_README.md com descrição
   - Links para relatório de análise

5. Registre em INDEX.md
```

### ✏️ Para Preparar Paper para Publicação

**Spawn command:**
```
Por favor, prepare um paper para publicação:

1. Leia versão current: ./research-output/{project}/draft-paper/
2. Valide contra QUALITY_STANDARDS.md para papers:
   - Introdução contextualizando
   - Metodologia replicável
   - Resultados com dados/números
   - Discussão com limitações
   - Conclusões e trabalho futuro
   - Referências completas em BibTeX

3. Execute checks:
   - Grammar e ortografia
   - Referências cruzadas funcionar
   - Figuras/tabelas referenciadas
   - Formato consistente

4. Prepare versão final:
   - Copie para research-output/{project}/final/
   - Nome: paper_{version}_{date}.{tex|md}
   - Gere PDF
   - Crie SUBMISSION.md com:
     - Journals/conferences sugeridos
     - Checklist de submission
     - Historia de revisões

5. Registre em INDEX.md como READY_FOR_SUBMISSION
```

### 📈 Para Visualizar Progresso

**Spawn command:**
```
Por favor, gere visão geral de outputs por projeto:

1. Analise todos os outputs em ./research-output/*/
2. Crie PROGRESS.md com:
   - Tabela por projeto:
     | Projeto | Literature | Analysis | Findings | Paper | Status |
   - Contadores: Drafts, Under Review, Final
   - Timeline de criação (gráfico)
   - Next milestones by project

3. Identifique:
   - Projetos on-track vs behind
   - Outputs bloqueados
   - Próximos deadlines
```

## 🏆 Convenções

- **Nomeação**: Use `type_projectname_date` ou `type_v{version}`
- **Versionamento**: Use git + semantic versioning (v1.0, v1.1-alpha)
- **Metadata**: YAML front-matter em TODOS os .md
- **Referências**: BibTeX completo, validado
- **Status**: Sempre incluir no front-matter (draft/review/final)

## 📝 QUALITY_STANDARDS.md

(Este arquivo será criado automaticamente)

```yaml
---
title: "Research Output Quality Standards"
categories:
  - literature-review
  - data-analysis
  - findings
  - draft-paper
  - final-paper
---

## All Outputs
- [ ] Título claro e descritivo
- [ ] Autores e data
- [ ] Objetivo/questão respondida
- [ ] Resumo (abstract/summary)
- [ ] Referências bibliográficas

## Literature Reviews
- [ ] Corpus identificado claramente
- [ ] Método de busca documentado
- [ ] Síntese temática (não apenas lista)
- [ ] Gaps identificados
- [ ] Trends reconhecidos

## Data Analysis
- [ ] Dataset descrito (origem, tamanho, schema)
- [ ] Metodologia estatística justificada
- [ ] Resultados com números/gráficos
- [ ] Validação (confidence intervals, p-values)
- [ ] Limitations reconhecidas

## Findings
- [ ] Claims suportadas por evidência
- [ ] Contexto em relação a literature
- [ ] Implicações para prática/teoria
- [ ] Trabalho futuro sugerido

## Draft Papers
- [ ] Estrutura completa (Intro, Methods, Results, Discussion)
- [ ] Introdução contextualizando problema
- [ ] Metodologia replicável
- [ ] Resultados quantificados
- [ ] Discussão com limitações

## Final Papers
- [ ] Tudo acima
- [ ] Grammar e ortografia perfeita
- [ ] Formatação consistente (se submissão específica)
- [ ] Pronto para revisor ler
```

## 📌 Exemplo de Fluxo Completo

```
Pesquisador cria:
└── research-output/ml-scalability/data-analysis/analysis_v1.md
    - Análise de benchmark de 3 arquiteturas
    - 15 páginas, draft status
    
Agentes processam:
1. ai-engineer: Valida estrutura (OK)
2. reality-checker: Avalia rigor (NEEDS_REVISION)
   - Feedback: "Statistical significance não testada"
3. Pesquisador atualiza (v2)
4. reality-checker: Re-valida (PASS)
5. feedback-synthesizer: Compara com outras análises
   - Consolida com findings relacionados
6. Paper pronto em research-output/ml-scalability/final/

Index atualizado:
└── INDEX.md: ml-scalability/data-analysis v2 ACCEPTED
```

---

**Output da pipeline - Tangível results da pesquisa**
