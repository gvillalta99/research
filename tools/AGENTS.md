# AGENTS.md - Tools Module

## 🎯 Propósito
Manutenção de scripts, utilitários e ferramentas para suportar a pipeline de pesquisa. Inclui processamento de dados, conversão de formatos, limpeza de corpus e automações.

## 📋 Responsabilidades dos Agentes

### Agents Esperados
- **ai-engineer**: Desenvolvimento de ferramentas de processamento
- **devops-automator**: Automação e scheduling
- **backend-architect**: Arquitetura de sistemas de processamento

### Entrada (Input)
- Requisitos de automação dos projetos
- Necessidades de processamento de dados
- Workflows repetitivos
- Tarefas de manutenção

### Responsabilidades
1. **Manutenção de Ferramentas**: Scripts e utilitários
2. **Processamento**: Conversão, limpeza, transformação
3. **Automação**: Scheduled tasks e pipelines
4. **Documentação**: READMEs e exemplos de uso
5. **Versionamento**: Controle de versão de tools

### Saída (Output)
- Scripts testados e documentados
- Logs de execução
- Dados processados
- Métricas de performance

## 📁 Estrutura

```
tools/
├── AGENTS.md                      # Este arquivo
├── README.md                      # Guide de ferramentas disponíveis
├── requirements.txt               # Dependencies Python
├── scripts/
│   ├── process_bibtex.py         # Processa e valida BibTeX
│   ├── sync_bibliography.py      # Sincroniza corpus
│   ├── extract_metadata.py       # Extrai de PDFs/URLs
│   ├── generate_reports.py       # Gera relatórios
│   └── cleanup_duplicates.py     # Remove duplicatas
├── notebooks/
│   ├── corpus_analysis.ipynb     # Análise exploratória
│   └── quality_audit.ipynb       # Auditoria de qualidade
├── templates/
│   ├── research_brief.md         # Template para novo projeto
│   ├── metadata.yaml             # Template de metadata
│   └── analysis_report.md        # Template de relatório
└── logs/
    ├── processing.log            # Log de processamento
    └── errors.log                # Log de erros
```

## 🔧 Ferramentas Principais

### 1. process_bibtex.py
Processa e valida arquivos BibTeX
```bash
python tools/scripts/process_bibtex.py \
  --input ../bibliografia/artigos/ \
  --validate \
  --output processed_bibtex.bib
```

### 2. extract_metadata.py
Extrai metadata de PDFs ou URLs
```bash
python tools/scripts/extract_metadata.py \
  --file reference.pdf \
  --format yaml \
  --output reference.yaml
```

### 3. sync_bibliography.py
Sincroniza corpus com sources externas
```bash
python tools/scripts/sync_bibliography.py \
  --action update \
  --source crossref \
  --target ../bibliografia/
```

### 4. cleanup_duplicates.py
Remove duplicatas por DOI/título
```bash
python tools/scripts/cleanup_duplicates.py \
  --search ../bibliografia/ \
  --by-doi \
  --report duplicates_found.csv
```

### 5. generate_reports.py
Gera relatórios de corpus
```bash
python tools/scripts/generate_reports.py \
  --corpus ../bibliografia/ \
  --type statistics \
  --output corpus_stats.md
```

## ⚡ Instruções para Agentes

### 🛠️ Para Desenvolver Nova Ferramenta

**Spawn command:**
```
Por favor, desenvolva uma nova ferramenta de processamento:

1. Especificação:
   - Nome da ferramenta
   - Input esperado
   - Output desejado
   - Casos de uso

2. Implementação em tools/scripts/:
   - Código Python bem documentado
   - Com docstrings
   - Tratamento de erros robusto
   - Logging adequado

3. Testes:
   - Unit tests em tools/tests/
   - Teste com dados reais
   - Valide output

4. Documentação:
   - Atualize tools/README.md
   - Inclua exemplos de uso
   - Descreva flags/opções

5. Integração:
   - Atualize requirements.txt
   - Registre em AGENTS.md
```

### 🔄 Para Automatizar um Processo Repetitivo

**Spawn command:**
```
Por favor, use a skill devops-automator para automatizar:

1. Identifique o processo em:
   - Qual input?
   - Qual processamento?
   - Qual output?
   - Frequência?

2. Crie script em tools/scripts/:
   - Parametrizável
   - Com logging
   - Tratamento de erros

3. Configure scheduling (se necessário):
   - Cron job ou equivalent
   - Documentado em tools/cron_jobs/

4. Teste completo:
   - Uma execução manual
   - Valide resultado
   - Documente qualquer manual intervention necessária

5. Registre uso em AGENTS.md
```

### 📊 Para Gerar Relatório de Corpus

**Spawn command:**
```
Por favor, gere relatório de corpus usando ferramentas:

1. Execute em tools/scripts/:
   python generate_reports.py \
     --corpus ../bibliografia/ \
     --type statistics \
     --output corpus_report.md

2. Analise resultado:
   - Total papers por categoria
   - Distribuição temporal
   - Temas principais
   - Gaps identificados

3. Atualize ../bibliografia/STATISTICS.md com:
   - Números consolidados
   - Trends temporais
   - Análises temáticas

4. Se análise mais profunda, dispare:
   - Jupyter notebook em tools/notebooks/
   - Visualizações e gráficos
   - Insights adicionais
```

### ✅ Para Validar Qualidade de Corpus

**Spawn command:**
```
Por favor, execute auditoria de qualidade:

1. Execute em tools/notebooks/:
   - Abra quality_audit.ipynb
   - Analise metadados completos?
   - Verifica duplicatas?
   - Identifica PDFs corrompidos?

2. Relatório de achados:
   - Quantos items precisam fix
   - Quais campos faltando
   - Duplicatas encontradas
   - PDFs problemáticos

3. Priorize ações:
   - Crítico (corrompido, inúti)
   - Alto (metadados incompletos)
   - Médio (duplicatas)
   - Baixo (metadata inconsistências)

4. Produza audit_report_{date}.md em tools/
```

### 🔗 Para Manter Links & Validar Acesso

**Spawn command:**
```
Por favor, valide todos os links em corpus:

1. Crie script tools/scripts/validate_links.py que:
   - Varre ../bibliografia/*/*.md
   - Extrai todas as URLs
   - Testa acesso (HEAD request)
   - Registra status (200, 404, 403, timeout)

2. Produza relatório:
   - Links válidos vs. broken
   - Substitutos para links quebrados
   - Recomendações para fix

3. Atualize referências com:
   - URLs ainda válidas
   - URLs alternativas se encontradas

4. Reporte problemas em tools/logs/broken_links.log
```

## 🏆 Convenções

- **Nomes de script**: Use `verb_noun.py` (ex: `process_bibtex.py`)
- **Logging**: Log INFO e WARNING, mais DEBUG se verbose
- **Configuração**: Use argumentos CLI ou config files
- **Testes**: Cada script com testes unitários
- **Documentação**: Docstring + exemplos de uso

## 📝 README.md (para manter atualizado)

```markdown
# Research Tools

## Available Tools

### Bibliography Processing
- `process_bibtex.py`: Validate and format BibTeX files
- `extract_metadata.py`: Extract metadata from PDFs/URLs
- `sync_bibliography.py`: Sync with external sources (CrossRef, etc)
- `cleanup_duplicates.py`: Find and remove duplicate entries

### Reporting
- `generate_reports.py`: Generate corpus statistics and analysis
- `validate_links.py`: Check URL accessibility
- `audit_quality.py`: Comprehensive quality audit

### Utilities
- `convert_formats.py`: Convert between BibTeX, RIS, JSON
- `merge_bibliography.py`: Combine multiple corpora

## Installation
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Usage Examples

### Validate Bibliography
\`\`\`bash
python scripts/process_bibtex.py --input ../bibliografia/artigos/ --validate
\`\`\`

### Extract from PDF
\`\`\`bash
python scripts/extract_metadata.py --file paper.pdf --output paper.yaml
\`\`\`

### Generate Statistics
\`\`\`bash
python scripts/generate_reports.py --corpus ../bibliografia/ --type statistics
\`\`\`
```

## 📌 Exemplo de Workflow com Tools

```
Problema: Corpus tem muitas referências mal formatadas

Solução:
1. Execute validation:
   python scripts/process_bibtex.py --corpus ../bibliografia/ --validate
   
2. Analise erros encontrados
3. Execute cleanup:
   python scripts/process_bibtex.py --corpus ../bibliografia/ --fix-format
   
4. Valide resultado:
   python scripts/generate_reports.py --type quality-check
   
5. Se OK, commit changes
6. Se não, iterar com fixes específicos
```

## 🔐 Boas Práticas

- **Sempre fazer backup** antes de processar corpus
- **Testar com subset** antes de rodar em dataset completo
- **Logar everything** para poder reproduzir
- **Documentar mudanças** em commit messages
- **Versionartools** quando mudanças significativas

---

**Utilitários que suportam a pipeline de pesquisa**
