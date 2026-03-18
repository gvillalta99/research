# AGENTS.md - Bibliografia Module

## 🎯 Propósito
Gerenciar corpus organizado de referências bibliográficas: livros, artigos, teses, preprints e relatórios. Este é o "knowledge base" central que alimenta todos os projetos de pesquisa.

## 📚 Estrutura de Categorias

```
bibliografia/
├── livros/              # Monografias, books, textbooks
├── artigos/             # Journal articles, conference papers (peer-reviewed)
├── teses/               # MSc dissertations, PhD theses
├── preprints/           # ArXiv, bioRxiv, preprints de acesso aberto
└── relatorios/          # Technical reports, whitepapers, industry research
```

## 📋 Responsabilidades dos Agentes

### Agents Esperados
- **ai-engineer**: Indexação, criação de vetores, RAG system setup
- **analytics-reporter**: Estatísticas, análise de corpus, trends
- **trend-researcher**: Identificação de tópicos emergentes
- **data-consolidation-agent**: Catalogação e consolidação de metadata

### Entrada (Input)
- Referências em inbox/ (processadas por outro AGENTS.md)
- Requests de projetos em ../projects/
- Atualizações periódicas de publishers

### Processamento
1. **Catalogação**: Registrar metadata (title, authors, DOI, year, etc)
2. **Classificação**: Tag temática automática baseada em conteúdo
3. **Indexação**: Criar índices para busca rápida
4. **Deduplicação**: Evitar duplicatas entre categorias
5. **Linking**: Cross-referências entre papers relacionados
6. **Atualização**: Manter corpus sincronizado com sources

### Saída (Output)
- `INDEX.md` - Inventário completo com metadata
- `CATEGORY_TAGS.md` - Taxonomy de tópicos
- `STATISTICS.md` - Análises do corpus
- Ficheiros BibTeX organizados por tema
- Vector embeddings para RAG (em .embeddings/)

## 📁 Estrutura de Arquivo em Cada Categoria

```
categoria/
├── reference_id.pdf          # Arquivo principal
├── reference_id.md           # Metadata + resumo
├── reference_id.bibtex       # Entrada BibTeX
└── (opcionalmente) reference_id_notes.md   # Anotações
```

## 📝 Formato de Metadata (reference_id.md)

```yaml
---
id: "lastname2024title"
title: "Full Title of Paper"
authors: ["First Author", "Second Author"]
year: 2024
type: "journal"  # journal, conference, book, thesis, preprint, report
doi: "10.xxxxx/xxxxx"
url: "https://..."
tags: ["machine-learning", "distributed-systems", "scalability"]
keywords: ["keyword1", "keyword2"]
abstract: "Summary of the paper..."
relevance_score: 8  # 1-10, relatedness to active research areas
---

## Key Contributions
- Main finding 1
- Main finding 2

## Methods
- Method description

## Connection to Other Papers
- Links to related references

## Relevance to Projects
- Relevant for: project-name (reason)
```

## 🔄 Workflow com Agentes

### Fase 1: Recepção de Referências
```
Referências chegam em ../inbox/
AGENTS.md em inbox/ processa e move para categoria apropriada
```

### Fase 2: Catalogação (ai-engineer)
```
ai-engineer:
1. Extrai metadata (título, autores, DOI, abstract)
2. Gera reference_id único
3. Cria arquivo .md com metadata
4. Produz entrada BibTeX
```

### Fase 3: Classificação Temática (trend-researcher)
```
trend-researcher:
1. Analisa conteúdo para temas principais
2. Sugere tags de categorização
3. Identifica termos-chave
4. Classifica força da relevância (1-10)
```

### Fase 4: Indexação e Linking (ai-engineer)
```
ai-engineer:
1. Cria embeddings vetoriais do abstract
2. Identifica papers relacionados por similaridade
3. Atualiza INDEX.md
4. Configura busca RAG para projetos
```

### Fase 5: Relatório de Corpus (analytics-reporter)
```
analytics-reporter:
1. Gera STATISTICS.md com:
   - Total papers por categoria
   - Distribuição temporal
   - Tópicos emergentes
   - Gaps na literatura
   - Autores mais citados
```

## ⚡ Instruções para Agentes

### 🎬 Para Processar Referência Nova

**Spawn command:**
```
Por favor, use a skill ai-engineer para processar uma referência em ./inbox/:

1. Leia o arquivo (PDF, link, ou texto)
2. Extraia metadata completa:
   - Título, autores, ano, tipo (journal/conference/book)
   - DOI, URL, abstract
3. Determine a categoria correta (livros/artigos/teses/preprints/relatorios)
4. Crie os arquivos em categoria/{reference_id}.*:
   - reference_id.md com YAML metadata completo
   - reference_id.bibtex com entrada BibTeX
5. Remova de inbox/ após processamento
6. Atualize INDEX.md com a nova referência
```

### 🏷️ Para Atualizar Classificação Temática

**Spawn command:**
```
Por favor, use a skill trend-researcher para revisar e atualizar tags temáticas:

1. Analise todos os arquivos .md em ./[categoria]/
2. Para cada referência:
   - Leia title, abstract, keywords
   - Sugira top 5 tags principais
   - Classifique relevância atual (1-10 score)
3. Atualize o YAML front-matter em cada .md
4. Gere CATEGORY_TAGS.md com:
   - Lista de todos os tags usados
   - Contagem de referências por tag
   - Temas emergentes identificados
```

### 📊 Para Gerar Estatísticas de Corpus

**Spawn command:**
```
Por favor, use a skill analytics-reporter para criar STATISTICS.md:

1. Analise todos os arquivos em todas as categorias
2. Gere relatório com:
   - Total de referências por categoria
   - Distribuição temporal (por década)
   - Temas mais frequentes
   - Autores mais publicados
   - Gaps identificados
   - Trends crescentes
3. Crie visualizações em formato markdown
4. Identifique oportunidades de pesquisa (novos tópicos não cobertos)
```

### 🔗 Para Criar Índice Centralizado

**Spawn command:**
```
Por favor, use a skill data-consolidation-agent para criar INDEX.md:

1. Varre todas as pastas (livros, artigos, teses, preprints, relatorios)
2. Consolide um índice único com:
   - Tabela de todos os papers com: ID | Título | Autores | Ano | Tipo | Tags
   - Subtabelas por categoria
   - Links para acesso rápido
3. Ordene por tema, depois cronologicamente
4. Mantenha sumário com contadores
5. Atualize quando novas referências forem adicionadas
```

### 🤖 Para Setup RAG System

**Spawn command:**
```
Por favor, use a skill ai-engineer para criar índice vetorial para busca RAG:

1. Processe todos os abstracts em ./*/reference_id.md
2. Crie embeddings usando modelo de language apropriado
3. Salve embeddings em .embeddings/index.faiss (ou similar)
4. Crie arquivo de mapping: embedding_id -> reference_id
5. Teste buscas semânticas:
   - Query exemplo: "machine learning scalability"
   - Retorne top 5 papers mais relevantes
6. Documente no arquivo .embeddings/README.md como usar
```

## 🏆 Convenções

- **IDs**: Use `lastname_year_abbrev` (ex: `bishop2006pattern`)
- **Metadata**: YAML front-matter em TODOS os .md
- **BibTeX**: Válido e pronto para importar em LaTeX/Zotero
- **Tags**: Use snake_case, máximo 5-7 tags por referência
- **Atualização**: INDEX.md e STATISTICS.md atualizar mensalmente

## 📌 Exemplo de Metadata Completa

```yaml
---
id: "goodfellow2016deep"
title: "Deep Learning"
authors: ["Ian Goodfellow", "Yoshua Bengio", "Aaron Courville"]
year: 2016
type: "book"
doi: "10.1016/B978-0-12-801312-2.X5000-1"
url: "https://www.deeplearningbook.org/"
tags: ["deep-learning", "neural-networks", "machine-learning", "optimization"]
keywords: ["convolutional neural networks", "recurrent neural networks", "optimization algorithms"]
abstract: "The Deep Learning textbook is a resource intended to help students and practitioners..."
relevance_score: 10
---

## Principais Contribuições
- Cobertura comprehensive de arquiteturas modernas
- Tratamento rigoroso de teoria matemática
- Capítulos em aplicações práticas

## Relevância para Projetos
- Relevante para: all-ai-projects (fundamento teórico)
- Complementa: papers específicos em RL, NLP, CV
```

## 📚 Gerenciamento Contínuo

### Checklist Mensal
- [ ] Processar novas referências em inbox/
- [ ] Atualizar tags temáticas
- [ ] Gerar STATISTICS.md
- [ ] Validar links (DOI, URLs)
- [ ] Backup de embeddings

### Integração com Projetos
- Cada projeto lê CATEGORY_TAGS.md para descoberta
- Projetos usam busca RAG via embeddings
- Feedback dos projetos volta para reranking de relevância

---

**Central knowledge repository que alimenta toda a pesquisa**
