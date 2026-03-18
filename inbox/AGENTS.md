# AGENTS.md - Inbox Module

## 🎯 Propósito
Triagem e processamento de referências bibliográficas não catalogadas. Inbox funciona como "staging area" onde novas referências são processadas e movidas para categorias apropriadas em `../bibliografia/`.

## 📋 Responsabilidades dos Agentes

### Agents Esperados
- **ai-engineer**: Extração de metadata, validação de qualidade
- **trend-researcher**: Classificação temática, avaliação de relevância
- **project-shepherd**: Coordenação do fluxo de processamento

### Entrada (Input)
- PDFs soltos
- Links (URLs)
- Texto com citações
- Metadados parciais
- Duplicatas de outras fontes

### Processamento
1. **Recebimento**: Armazenar referência em inbox/
2. **Validação**: Verificar se é referência legítima
3. **Extração**: Extrair metadata (title, authors, year, DOI)
4. **Classificação**: Determinar categoria (livro, artigo, tese, etc)
5. **Deduplicação**: Verificar se já existe em ../bibliografia/
6. **Enriquecimento**: Buscar metadata completa (DOI, abstract, etc)
7. **Moveção**: Transferir para categoria apropriada
8. **Cleanup**: Remover de inbox/ após processamento

### Saída (Output)
- Referências processadas movidas para `../bibliografia/{categoria}/`
- Relatório de processamento (PROCESSING_LOG.md)
- Referências rejeitadas em `quarantine/` (se houver)

## 📁 Estrutura

```
inbox/
├── AGENTS.md                  # Este arquivo
├── PROCESSING_LOG.md          # Log de processamento (mantido por agentes)
├── quarantine/                # Referências problemáticas
├── [referencia-1]             # Pode ser arquivo ou pasta
├── [referencia-2]
└── [referencia-3]
```

## 🔄 Workflow com Agentes

### Ciclo Diário/Semanal de Processamento

```
1. Agente-scheduler checa inbox/ por novos itens
2. Para cada item:
   a. ai-engineer: Valida e extrai metadata
   b. trend-researcher: Classifica e avalia relevância
   c. Decisão: Processar? Descartar? Quarantena?
   d. Se processar: Move para ../bibliografia/{categoria}/
3. Atualiza PROCESSING_LOG.md com timestamp e resultado
4. Gera relatório de processamento
```

### Fase 1: Validação & Extração (ai-engineer)

```
ai-engineer analisa item e:
- Valida se é referência legítima
- Extrai título, autores, ano, tipo
- Busca DOI via CrossRef/Google Scholar
- Obtém abstract (se disponível)
- Valida qualidade de metadata
- Retorna: metadata validada ou REJECT
```

### Fase 2: Classificação & Relevância (trend-researcher)

```
trend-researcher avalia:
- Tipo de referência (journal/conference/book/thesis/preprint/report)
- Determina categoria (livros/artigos/teses/preprints/relatorios)
- Sugere tags temáticas
- Calcula relevância score (1-10) para corpus
- Identifica se complementa pesquisas ativas
- Retorna: categoria recomendada + tags + score
```

### Fase 3: Deduplicação (ai-engineer)

```
ai-engineer verifica:
- DOI já existe em ../bibliografia/?
- Título similar já catalogado?
- Autores + ano combinado já existe?
- Se duplicata encontrada: SKIP com notificação
- Se novo: Prosseguir para Fase 4
```

### Fase 4: Enriquecimento & Setup (ai-engineer)

```
ai-engineer cria na categoria destino:
- arquivo.md com YAML metadata completo
- arquivo.bibtex com entrada BibTeX
- arquivo_notes.md se houver notas iniciais
- Move arquivo original (PDF/etc) para categoria
- Remove de inbox/
```

### Fase 5: Atualização de Índices (analytics-reporter)

```
analytics-reporter:
- Atualiza ../bibliografia/INDEX.md
- Atualiza ../bibliografia/STATISTICS.md
- Notifica projetos relacionados (se houver)
```

## ⚡ Instruções para Agentes

### 🎬 Para Processar Inbox Completamente

**Spawn command:**
```
Por favor, use a skill agents-orchestrator para processar inbox completo:

Pipeline:
1. Spawn ai-engineer para validar cada item em ./inbox/
   - Extrair metadata: título, autores, ano, tipo
   - Buscar DOI e abstract
   - Validar qualidade
   - Retornar: {status: "valid"/"invalid", metadata, reason}

2. Para cada item VÁLIDO, spawn trend-researcher para classificar
   - Tipo: journal/conference/book/thesis/preprint/report
   - Categoria destino: livros/artigos/teses/preprints/relatorios
   - Tags temáticas (até 5)
   - Relevância score (1-10)

3. Para cada item CLASSIFICADO, spawn ai-engineer para deduplicar
   - Verificar DOI em ../bibliografia/
   - Verificar título similar
   - Se duplicata: Mark como SKIP
   - Se novo: Prosseguir para enriquecimento

4. Para cada item NEW, spawn ai-engineer para:
   - Criar {id}.md com YAML metadata
   - Criar {id}.bibtex com entrada
   - Mover PDF/arquivo para categoria
   - Remover de inbox/

5. Spawn analytics-reporter para atualizar índices
   - Atualizar ../bibliografia/INDEX.md
   - Atualizar ../bibliografia/STATISTICS.md

6. Atualizar PROCESSING_LOG.md com results completos
```

### ✅ Para Validar Uma Referência Específica

**Spawn command:**
```
Por favor, valide a referência em ./inbox/{item}/:

1. Extraia metadata completa:
   - Título exato
   - Autores (first author et al se necessário)
   - Ano de publicação
   - Fonte (journal, conference, publisher)
   - DOI (se disponível)
   - URL/link de acesso

2. Valide qualidade:
   - Peer-reviewed? (sim para journal/conference)
   - Autores legítimos? (verifiação rápida)
   - Conteúdo relevante para research? 

3. Retorne relatório com:
   - Status: VALID / INVALID / NEEDS_HUMAN_REVIEW
   - Metadata extraída (se válido)
   - Motivo de rejeição (se inválido)
```

### 🏷️ Para Classificar Referência

**Spawn command:**
```
Por favor, classifique a referência com metadata:

1. Determine o tipo:
   - journal: Artigos em periódicos revisados por pares
   - conference: Papers em anais de conferências
   - book: Livros, monografias
   - thesis: MSc dissertations, PhD theses
   - preprint: ArXiv, bioRxiv, papers não publicados
   - report: Technical reports, whitepapers

2. Selecione categoria:
   - livros/ para: books, monografias
   - artigos/ para: journal, conference
   - teses/ para: thesis
   - preprints/ para: preprint
   - relatorios/ para: report, whitepaper

3. Sugira tags (até 7):
   - Temas principais de pesquisa
   - Use snake_case
   - Exemplo: machine-learning, distributed-systems, scalability

4. Avalie relevância (1-10):
   - 10: Essencial, cita frequentemente
   - 7-9: Muito relevante, complementa bem
   - 5-6: Relevante, mas especializado
   - 3-4: Periférico, pode ser útil
   - 1-2: Baixa relevância, mas catalogado

5. Retorne: {categoria, tags, relevance_score}
```

### 🚨 Para Quarentena de Referências Problemáticas

**Spawn command:**
```
Se uma referência não puder ser processada:

1. Mova para quarantine/ com nome descritivo
2. Crie quarantine/{item}_ISSUE.md com:
   - Motivo da rejeição
   - Qual informação está faltando
   - Próximos passos possíveis
   - Data e responsável

Exemplos de problemáticas:
- Arquivo corrompido (PDF ilegível)
- Metadata incompleta impossível completar
- Não é referência acadêmica legítima
- Conteúdo não relevante para escopo de research
- Arquivo duplicado (já existe em biblioteca)
```

### 📋 Para Gerar Relatório de Processamento

**Spawn command:**
```
Crie um relatório de processamento:

1. Resuma o processamento realizado:
   - Data/período do processamento
   - Total de itens processados
   - Itens válidos/inválidos
   - Movidos para categorias

2. Gere PROCESSING_LOG.md com:
   - Timestamp de execução
   - Lista de itens com resultado (VALID/SKIP/QUARANTINE)
   - Categoria destino de cada item
   - Qualquer issue encontrada
   - Próximas ações recomendadas

3. Notifique em ../README.md:
   - Última atualização de corpus
   - Novo total de referências
```

## 🏆 Convenções

- **Nomes de arquivo**: Use nome descritivo ou `lastname_year`
- **Formatos aceitos**: PDF, URLs, JSON com metadata, BibTeX
- **Metadados mínimos**: Título, autor principal, ano
- **Duplicatas**: Verificar por DOI antes de tudo
- **Rejeições**: Documentar motivo em quarantine/

## 📌 Exemplo de Fluxo

```
inbox/
├── bishop2006pattern.pdf                    # PDF chegou
├── paper_from_colleague.pdf                 # Outra fonte
└── https://arxiv.org/abs/2306.00000         # Link

Processamento:
1. ai-engineer extrai:
   - bishop2006pattern.pdf -> title, authors, DOI
   - Encontra: "Pattern Recognition and Machine Learning"
   - Bishop, Christopher M.; 2006

2. trend-researcher classifica:
   - Tipo: book
   - Categoria: livros/
   - Tags: machine-learning, pattern-recognition, neural-networks
   - Score: 10 (essencial para ML research)

3. Resultado:
   - Movido para: ../bibliografia/livros/bishop2006pattern.*
   - SKIP: Outra fonte (duplicata por DOI)
   - Adicionado: paper_from_colleague.pdf com metadata

4. Atualizado:
   - PROCESSING_LOG.md
   - ../bibliografia/INDEX.md
   - ../bibliografia/STATISTICS.md
   
Inbox fica vazio até próximas referências
```

## ⚠️ Problemas Comuns

| Problema | Solução |
|----------|---------|
| PDF corrompido | Mover para quarantine/, solicitar nova cópia |
| Metadados incompletos | Buscar em Google Scholar/CrossRef por título |
| Está em 2 formatos | Manter PDF, descartar duplicata |
| Muito antigo (pré-1970) | Avaliar relevância, pode mover para archive/ |
| Não é paper acadêmico | Mover para quarantine/ com justificativa |

---

**Entrada da pipeline bibliográfica - Mantém corpus organizado e limpo**
