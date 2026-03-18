# AGENTS.md

## Escopo
Este repositório coordena projetos de pesquisa, corpus bibliográfico, triagem de referências e outputs consolidados.

## Estrutura canônica
- `projects/`: cada projeto deve existir como submódulo Git.
- `bibliografia/`: corpus já processado e classificado.
- `inbox/`: referências ainda não processadas.
- `research-output/`: entregáveis e sínteses gerados a partir dos projetos.
- `tools/`: scripts, templates e logs de suporte.

## Skills preferenciais
Estas são as skills padrão deste repositório e devem ser priorizadas quando aplicáveis:
- `agents-orchestrator`: coordenação de pipelines que cruzam múltiplas pastas.
- `senior-project-manager`: abertura, escopo e acompanhamento de projetos.
- `ai-engineer`: extração de metadados, indexação, RAG e automações de dados.
- `trend-researcher`: classificação temática e detecção de tendências.
- `analytics-reporter`: estatísticas do corpus e relatórios quantitativos.
- `feedback-synthesizer`: sínteses comparativas e revisões de literatura.
- `reality-checker`: validação metodológica e crítica de conclusões.

## Regras operacionais
- Material bruto entra primeiro em `inbox/`.
- Material processado sai de `inbox/` e vai para uma categoria em `bibliografia/`.
- Cada referência processada deve compartilhar um mesmo identificador base entre arquivo original, metadata `.md` e `.bib`.
- Projetos em `projects/` são a fonte de escopo; outputs finais ficam em `research-output/`.
- Não remover ou sobrescrever referências existentes sem evidência clara de duplicidade ou instrução explícita.
- Sempre ler o `AGENTS.md` mais local antes de agir.
