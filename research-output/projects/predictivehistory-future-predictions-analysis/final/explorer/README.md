# PredictiveHistory Future Forecast Explorer

Site estático para explorar as previsões extraídas do canal PredictiveHistory.

## Arquivos
- `index.html`
- `styles.css`
- `app.js`
- `../../assets/predictions-explorer-data.js`
- `../../assets/predictions-explorer-data.json`

## Como abrir
Opção mais simples:

```bash
cd /home/gustavo/src/gvillalta99/research/research-output/projects/predictivehistory-future-predictions-analysis/final/explorer
python3 -m http.server 8000
```

Depois abra:
- `http://localhost:8000`

Também deve funcionar abrindo `index.html` diretamente, porque o dataset principal é carregado via script local (`./predictions-explorer-data.js`).
cipal é carregado via script local (`predictions-explorer-data.js`).
