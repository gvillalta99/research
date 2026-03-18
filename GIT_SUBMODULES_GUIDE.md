---
title: "Git Submodules Guide for Research Projects"
description: "Como usar Git submodules para gerenciar projetos de pesquisa independentes"
version: "1.0"
---

# Git Submodules Guide for Research Projects

Cada projeto de pesquisa em `projects/` é um repositório Git independente, gerenciado como um **Git submodule**. Isto permite que cada projeto tenha seu próprio histórico de versão e seja potencialmente compartilhado com colaboradores.

## 🎯 Por Quê Submodules?

- ✅ Cada projeto tem versionamento independente
- ✅ Colaboradores podem trabalhar no projeto separadamente
- ✅ Repositório principal fica limpo (só referencia)
- ✅ Fácil adicionar/remover projetos
- ✅ Escalável para 10+ projetos simultâneos

## 📋 Como Adicionar um Novo Projeto

### Opção 1: Novo Projeto Novo (Mais Comum)

```bash
# 1. Crie um novo repositório vazio para o projeto
# (Pode ser no GitHub, GitLab, ou servidor privado)
# Exemplo URL: git@github.com:seu-usuario/projeto-ml-scalability.git

# 2. Adicione como submodule
cd /home/gustavo/src/gvillalta99/research
git submodule add git@github.com:seu-usuario/projeto-ml-scalability.git projects/projeto-ml-scalability

# 3. Configure submodule
cd projects/projeto-ml-scalability
git config core.sparsecheckout false

# 4. Crie estrutura inicial
mkdir -p data notebooks results
touch README.md RESEARCH_BRIEF.md references.bib

# 5. Commit inicial
git add .
git commit -m "Initial commit: project structure"
git push

# 6. Volte à raiz e commit submodule
cd /home/gustavo/src/gvillalta99/research
git add projects/projeto-ml-scalability .gitmodules
git commit -m "Add submodule: projeto-ml-scalability"
git push
```

### Opção 2: Projeto Existente

```bash
# Se você tem um repositório existente que quer adicionar:

cd /home/gustavo/src/gvillalta99/research
git submodule add git@github.com:seu-usuario/projeto-existente.git projects/projeto-existente

# Commit
git add .gitmodules
git commit -m "Add existing project as submodule"
git push
```

## 🔄 Operações Comuns com Submodules

### Clonar Repository com Submodules

```bash
# Opção 1: Clone e inicialize submodules recursivamente
git clone --recurse-submodules git@github.com:seu-usuario/research.git

# Opção 2: Se já clonou sem --recurse-submodules
cd research
git submodule update --init --recursive
```

### Atualizar Submodule para Versão Mais Nova

```bash
# Ir ao diretório do projeto
cd projects/seu-projeto

# Ver commits mais recentes
git log --oneline -5

# Fazer checkout de um commit específico
git checkout nome-da-branch-ou-hash

# Ou atualizar para mais recente da branch
git pull origin master

# Voltar à raiz e commit a atualização
cd /home/gustavo/src/gvillalta99/research
git add projects/seu-projeto
git commit -m "Update projeto-ml-scalability to latest version"
git push
```

### Trabalhar em um Projeto (Fluxo Normal)

```bash
cd projects/seu-projeto

# Crie uma branch para sua feature
git checkout -b feature/melhor-analise

# Faça seu trabalho e commits
echo "nova análise" >> analysis.md
git add analysis.md
git commit -m "Add comprehensive scalability analysis"

# Envie para remote
git push origin feature/melhor-analise

# Crie pull request (se no GitHub, etc)

# Após merge, volte à raiz
cd /home/gustavo/src/gvillalta99/research

# Atualize referência do submodule
git add projects/seu-projeto
git commit -m "Update seu-projeto to merged version"
git push
```

### Listar Status de Todos os Projetos

```bash
# Ver qual é a versão de cada submodule
git submodule foreach 'echo "=== $path ===" && git rev-parse --short HEAD'

# Ver status (mudanças não commitadas)
git submodule foreach 'git status'

# Ver últimos commits
git submodule foreach 'echo "=== $path ===" && git log --oneline -3'
```

### Sincronizar Todos os Submodules

```bash
# Se colaboradores atualizaram projetos, você precisa sincronizar
git pull
git submodule update --remote

# Ou se quer também fazer checkout de branches mais recentes
git submodule foreach 'git checkout main && git pull'
```

## ⚠️ Cuidados Importantes

### ❌ Não Faça Isto

```bash
# ❌ Não edite um arquivo diretamente no submodule sem estar na branch
# (voce deixará o submodule em estado detached)

# ❌ Não force push sem comunicar aos colaboradores
# (pode quebrar o código deles)

# ❌ Não delete um submodule sem documentação
# (histórico será perdido se repo também deletar)
```

### ✅ Faça Isto

```bash
# ✅ Sempre faça checkout de uma branch explícita ao entrar em submodule
cd projects/seu-projeto
git checkout -b minha-feature

# ✅ Communicate ao team quando atualizar versão de um projeto
# Use commit message descritiva

# ✅ Se deletar submodule, documente o motivo
```

## 🚨 Troubleshooting

### Submodule em "Detached HEAD" State

```bash
# Sintoma: git status mostra algo diferente

# Solução:
cd projects/seu-projeto
git checkout main  # ou a branch que quer
```

### Submodule não está sincronizado

```bash
# Sintoma: mudanças no submodule não aparecem

# Solução:
cd projects/seu-projeto
git pull

# Volte à raiz
cd /home/gustavo/src/gvillalta99/research
git add projects/seu-projeto
git commit -m "Sync submodule"
```

### Clonar com Submodules Falha

```bash
# Tente:
git clone git@github.com:seu-usuario/research.git
cd research
git submodule update --init --recursive --depth 1
```

## 📝 Estrutura Recomendada de Cada Projeto

```
projects/seu-projeto/
├── README.md                 # Descrição do projeto
├── RESEARCH_BRIEF.md        # Brief inicial (cópia do template)
├── RESEARCH_PLAN.md         # Plano detalhado (preenchido)
├── STATUS.md                # Status atual
├── REFERENCED_PAPERS.md     # BibTeX de papers relevantes
├── data/                    # Datasets do projeto
├── notebooks/               # Jupyter notebooks
│   ├── 01_exploratory.ipynb
│   ├── 02_analysis.ipynb
│   └── 03_synthesis.ipynb
├── results/                 # Outputs finais
│   ├── figures/
│   ├── tables/
│   └── paper_draft.md
├── references.bib          # BibTeX completo local
└── .gitignore              # Ignore patterns específicos
```

## 🔐 Gerenciamento de Acesso

### Projetos Privados vs Públicos

**Privado** (padrão recomendado):
```bash
# Use SSH URLs para submodules privados
git submodule add git@github.com:seu-usuario/private-project.git
```

**Público** (se compartilhando):
```bash
# Use HTTPS URLs para fácil acesso
git submodule add https://github.com/seu-usuario/public-project.git
```

### Adicionando Colaboradores

Se um projeto tiver múltiplos colaboradores:

```bash
# No repositório do submodule, adicione como colaborador no GitHub
# Eles poderão fazer git push diretamente

# No repositório principal (research), você pode:
# - Deixar como ssh (mais restritivo)
# - Deixar como https (mais aberto)
```

## 📊 Exemplo de Workflow Completo

```bash
# 1. Você começa novo projeto
cd /home/gustavo/src/gvillalta99/research

# 2. Adiciona submodule
git submodule add https://github.com/user/ml-scalability.git projects/ml-scalability

# 3. Configura projeto inicial
cd projects/ml-scalability
cp ../../tools/templates/RESEARCH_BRIEF_TEMPLATE.md RESEARCH_BRIEF.md
# ... preenche RESEARCH_BRIEF.md

git add RESEARCH_BRIEF.md README.md
git commit -m "Initialize project with research brief"
git push

# 4. Volta à raiz e registra
cd /home/gustavo/src/gvillalta99/research
git add projects/ml-scalability .gitmodules
git commit -m "Add ml-scalability project"
git push

# 5. Pesquisadores trabalham normalmente
cd projects/ml-scalability
git checkout -b feature/literature-review
# ... trabalha ...
git push origin feature/literature-review
# ... cria PR ...
# ... merge ...

# 6. Você sincroniza na raiz
cd /home/gustavo/src/gvillalta99/research
git pull
git submodule update --remote
git add projects/ml-scalability
git commit -m "Update ml-scalability to merged version"
git push

# 7. Colaboradores conseguem as mudanças
git pull
git submodule update --recursive
```

## 🎯 Best Practices

1. **Faça commits atômicos**: Um conceito/feature por commit
2. **Write descritivas**: "Add RQ2 analysis" vs "Fix bug"
3. **Use branches**: main/master para produção, dev/work para experimentação
4. **Review antes de merge**: PR review mesmo em projetos pequenos
5. **Sincronize regularmente**: Pull da main no mínimo semanal
6. **Documente decisões**: Em README ou DESIGN.md
7. **Backup importante**: Considere push em múltiplos remotes

## 📚 Recursos

- [Git Submodules Official Doc](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [GitHub Submodules Guide](https://docs.github.com/en/github/working-with-git/working-with-submodules)
- [GitLab Submodules](https://docs.gitlab.com/ee/topics/submodules.html)

---

**Last Updated**: 2026-03-18
**Questions?**: See git submodule documentation or contact team
