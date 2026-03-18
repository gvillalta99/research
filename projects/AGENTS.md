# AGENTS.md

## Escopo
`projects/` contém apenas submódulos Git de projetos de pesquisa e o contexto comum desta pasta.

## Regras
- Cada projeto novo deve ser criado com `git submodule add <url> projects/<project-slug>`.
- Use `kebab-case` no nome do submódulo.
- Não guardar referências brutas aqui; isso pertence a `../inbox/`.
- Outputs consolidados pertencem a `../research-output/projects/<project-slug>/`.

## Estrutura mínima esperada em cada submódulo
- `RESEARCH_BRIEF.md`
- `RESEARCH_PLAN.md`
- `STATUS.md`
- `references.bib`
- `notes/`
- `data/` quando houver dados próprios

## Fluxo recomendado
1. Ler `RESEARCH_BRIEF.md`.
2. Consultar `../bibliografia/` para montar corpus do projeto.
3. Registrar plano, status e referências locais no submódulo.
4. Publicar drafts, revisões e finais em `../research-output/projects/<project-slug>/`.

## Skills preferenciais
- `senior-project-manager`
- `agents-orchestrator`
- `feedback-synthesizer`
- `reality-checker`
