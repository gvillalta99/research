# Relatório — Previsões de Futuro no canal PredictiveHistory

## Resumo executivo

- Vídeos processados: **134**
- Vídeos com ao menos uma previsão: **118**
- Vídeos sem previsões identificadas: **16**
- Total de previsões consolidadas: **450**

## Distribuição por status

- **still_open**: 397
- **not_verifiable**: 22
- **concluded_true**: 16
- **concluded_false**: 13
- **ambiguous**: 2

## Distribuição por tema

- **Geopolítica**: 28
- **Geopolítica/Guerra**: 27
- **Geopolitics**: 14
- **Economia**: 10
- **Política**: 7
- **Geopolítica/Religião**: 6
- **Demografia**: 5
- **Geopolítica/Economia**: 5
- **Geopolítica/Militar**: 5
- **Politics**: 4
- **Demographics**: 4
- **Militar**: 4
- **Sociologia/Geopolítica**: 3
- **Economia/Sociedade**: 3
- **Geopolitics/War**: 3

## Distribuição por confiança

- **medium**: 206
- **high**: 173
- **low**: 71

## Vídeos com mais previsões extraídas

- **Game Theory #14: The Law of Proximity** (`nOQqGy4boBY`): 13 previsões
- **Game Theory #12:  The Law of Eschatological Convergence** (`spg58Glfz68`): 12 previsões
- **Secret History #END: Pax Judaica** (`WFWizN3QoPg`): 10 previsões
- **Geo-Strategy Update #7:  When Eschatologies Converge** (`YQ-xg1nIbMs`): 10 previsões
- **Geo-Strategy Update #6:  Is Putin the Ubermensch?** (`ZgvAHZqaawA`): 10 previsões
- **Game Theory #9:  The US-Iran War** (`jIS2eB-rGv0`): 10 previsões
- **Secret History #3:  Death by Gerontocracy** (`0g3yo1DjiLM`): 9 previsões
- **Geo-Strategy #10: Putin's Strategic Imagination** (`B_al2wgk49Y`): 9 previsões
- **Civilization #31:  The Oceanic Currents of History** (`HIoYQBbBllk`): 9 previsões
- **Civilization #END:  The Decline and Fall of the American Empire** (`_gH4PvIni5E`): 9 previsões

## Leitura analítica

1. O corpus contém tanto previsões concretas quanto projeções estruturais de longa duração. Em vários vídeos, o Professor Jiang formula prognósticos amplos sobre hegemonia, colapso, guerra, tecnologia e transformação civilizacional.
2. A categoria `still_open` tende a dominar quando a previsão é de horizonte longo ou quando o enunciado é sistêmico e não associado a uma data de corte rígida.
3. As categorias `concluded_true` e `concluded_false` aparecem quando o modelo identificou previsões verificáveis com algum fechamento factual no horizonte atual.
4. Parte das previsões é vaga ou interpretativa, o que empurra itens para `ambiguous` ou `not_verifiable`. Esses casos precisam de revisão humana posterior para maior rigor metodológico.
5. Os temas mais frequentes ajudam a mapear o foco narrativo do canal: geopolítica, sistemas globais, China, Estados Unidos, guerra, economia política e civilização.

## Exemplos por status

### concluded_true
- Vídeo: **Geo-Strategy #8:  The Iran Trap** (`7y_hbz6loEo`)
- Previsão: Donald Trump will become president of the United States again in November.
- Horizonte: 2024-11-05
- Evidência: it's very likely that Trump will become president of the United States again um um in November

### concluded_false
- Vídeo: **Geo-Strategy #8:  The Iran Trap** (`7y_hbz6loEo`)
- Previsão: Trump will pick Nikki Haley as his Vice Presidential candidate.
- Horizonte: 2024-07-01
- Evidência: and he will pick Nikki Haley as his VP

### still_open
- Vídeo: **Civilization #44:  The Spanish Conquest of the New World** (`-DnfGcvZrfA`)
- Previsão: Rússia e Estados Unidos não utilizarão armas nucleares em seus conflitos atuais porque isso constitui o tabu definitivo da humanidade.
- Horizonte: Futuro próximo/Contemporâneo
- Evidência: It's not going to happen because it's the ultimate taboo. If anyone uses nuclear weapons, the world ends. It's like killing God. No one would do would do it.

### ambiguous
- Vídeo: **Great Books #3:  Poets and Prophets** (`XRP407WsA0w`)
- Previsão: Os poetas atuam como profetas através dos quais o futuro fala ao presente; suas obras são espelhos das 'sombras gigantescas' que o futuro projeta sobre o mundo atual.
- Horizonte: Longo prazo/Civilizacional
- Evidência: The mirrors of the gigantic shadows which future cast upon the present. There are prophets because of future speaking to us today.

### not_verifiable
- Vídeo: **Civilization #44:  The Spanish Conquest of the New World** (`-DnfGcvZrfA`)
- Previsão: Sociedades com hierarquias extremamente rígidas, onde a maioria é forçada a adorar uma minoria, permanecerão vulneráveis a invasões e conquistas externas.
- Horizonte: Indeterminado/Princípio Geral
- Evidência: Whenever society has an extremely strict hierarchy where the the majority are forced to worship minority. It makes a study extremely vulnerable to invasion and conquest.

## Arquivos de dados gerados

- Dataset JSON consolidado: `projects/predictivehistory-future-predictions-analysis/data/processed/consolidated/all_predictions.json`
- Dataset CSV consolidado: `projects/predictivehistory-future-predictions-analysis/data/processed/consolidated/all_predictions.csv`
- Resumo agregado: `projects/predictivehistory-future-predictions-analysis/data/processed/consolidated/summary.json`

## Observações metodológicas

- A extração foi feita a partir das legendas/transcrições disponíveis no YouTube.
- A classificação de status foi produzida pelo Gemini CLI e deve ser tratada como triagem analítica inicial.
- Recomenda-se auditoria manual dos itens de maior impacto ou dos casos classificados como ambíguos.
