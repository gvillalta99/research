const state = {
  data: null,
  filtered: [],
  search: '',
  status: 'all',
  originalStatus: 'all',
  theme: 'all',
  validated: 'all',
  bibliography: 'all',
  sort: 'effective_status',
};

const el = (id) => document.getElementById(id);
const fmt = new Intl.NumberFormat('pt-BR');

function unique(values) {
  return ['all', ...Array.from(new Set(values.filter(Boolean))).sort((a, b) => a.localeCompare(b, 'pt-BR'))];
}

function fillSelect(node, values, labelAll = 'Todos') {
  node.innerHTML = '';
  values.forEach((value) => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = value === 'all' ? labelAll : value;
    node.appendChild(option);
  });
}

function normalize(s) {
  return (s || '').toString().toLowerCase();
}

function badge(label, kind) {
  return `<span class="badge ${kind}">${label}</span>`;
}

function renderHero(summary) {
  const cards = [
    ['Previsões', fmt.format(summary.prediction_count)],
    ['Vídeos', fmt.format(summary.video_count)],
    ['Validadas', fmt.format(summary.validated_count)],
    ['Divergências', fmt.format(summary.status_mismatches)],
  ];
  el('heroStats').innerHTML = cards.map(([label, value]) => `<div class="hero-card"><span>${label}</span><strong>${value}</strong></div>`).join('');
}

function renderMetrics(items) {
  const validated = items.filter((item) => item.has_validation).length;
  const withBiblio = items.filter((item) => item.has_bibliographic_grounding).length;
  const mismatch = items.filter((item) => item.has_validation && item.effective_status !== item.status).length;
  const high = items.filter((item) => item.confidence === 'high').length;
  const open = items.filter((item) => item.effective_status === 'still_open').length;
  const metrics = [
    ['Itens exibidos', items.length],
    ['Com bibliografia', withBiblio],
    ['Validados nesta seleção', validated],
    ['Mismatchs visíveis', mismatch],
    ['Still open', open],
    ['Confiança alta', high],
    ['Vídeos cobertos', new Set(items.map((item) => item.video_id)).size],
  ];
  el('metricCards').innerHTML = metrics.map(([label, value]) => `<div class="metric-card"><span>${label}</span><strong>${fmt.format(value)}</strong></div>`).join('');
}

function renderBars(containerId, counter, limit = 8) {
  const total = Object.values(counter).reduce((acc, n) => acc + n, 0) || 1;
  const entries = Object.entries(counter).sort((a, b) => b[1] - a[1]).slice(0, limit);
  el(containerId).innerHTML = entries.map(([label, count]) => {
    const pct = (count / total) * 100;
    return `<div class="bar-item"><div class="bar-meta"><strong>${label}</strong><span>${fmt.format(count)}</span></div><div class="bar-track"><div class="bar-fill" style="width:${pct.toFixed(1)}%"></div></div></div>`;
  }).join('');
}

function renderVideoList(containerId, items, mapper) {
  el(containerId).innerHTML = items.map(mapper).join('');
}

function renderTable(items) {
  el('resultCount').textContent = `${fmt.format(items.length)} itens`;
  el('resultsTable').innerHTML = items.map((item) => `
    <tr data-row-id="${item.row_id}">
      <td class="summary-cell">
        <strong>${item.prediction_text}</strong>
        <div class="badges">
          ${badge(item.normalized_theme || 'Outros', 'badge-theme')}
          ${badge(`orig: ${item.status}`, 'badge-original')}
          ${badge(`efetivo: ${item.effective_status}`, 'badge-effective')}
          ${item.has_validation ? badge('validado', 'badge-validated') : ''}
          ${item.has_validation && item.effective_status !== item.status ? badge('mismatch', 'badge-mismatch') : ''}
        </div>
      </td>
      <td><a class="linkish" href="${item.video_url}" target="_blank" rel="noreferrer">${item.title}</a></td>
      <td>${item.normalized_theme || 'Outros'}</td>
      <td>${item.status}</td>
      <td>${item.effective_status}</td>
      <td>${item.has_bibliographic_grounding ? `${(item.bibliographic_refs || []).length} refs` : '—'}</td>
    </tr>
  `).join('');

  document.querySelectorAll('#resultsTable tr').forEach((row) => {
    row.addEventListener('click', () => openDetail(row.dataset.rowId));
  });
}

function openDetail(rowId) {
  const item = state.data.predictions.find((entry) => entry.row_id === rowId);
  if (!item) return;
  el('detailContent').innerHTML = `
    <div class="detail-grid">
      <div>
        <p class="section-kicker">${item.row_id}</p>
        <h3>${item.title}</h3>
      </div>
      <div class="detail-block">
        <p><strong>Previsão</strong></p>
        <p>${item.prediction_text}</p>
        <div class="badges">
          ${badge(item.normalized_theme || 'Outros', 'badge-theme')}
          ${badge(`original: ${item.status}`, 'badge-original')}
          ${badge(`efetivo: ${item.effective_status}`, 'badge-effective')}
        </div>
      </div>
      <div class="detail-block">
        <p><strong>Evidência textual</strong></p>
        <p>${item.evidence_quote || 'Não informada.'}</p>
        <p><strong>Raciocínio inicial</strong></p>
        <p>${item.reasoning || 'Não informado.'}</p>
      </div>
      <div class="detail-block">
        <p><strong>Validação factual</strong></p>
        <p>${item.validation_summary || 'Este item ainda não possui validação factual detalhada.'}</p>
        <p><strong>Notas</strong></p>
        <p>${item.validation_notes || '—'}</p>
      </div>
      <div class="detail-block">
        <p><strong>Metadados</strong></p>
        <p>Data da previsão: ${item.prediction_date || 'não informada'}<br/>Horizonte: ${item.target_timeframe || 'não informado'}<br/>Confiança: ${item.confidence || '—'}<br/>Validação: ${item.validation_confidence || '—'}</p>
      </div>
      <div class="detail-block">
        <p><strong>Fontes externas</strong></p>
        <div class="source-list">
          ${(item.sources || []).map((url) => `<a class="linkish" href="${url}" target="_blank" rel="noreferrer">${url}</a>`).join('') || '<span>Sem fontes anexadas.</span>'}
        </div>
      </div>
      <div class="detail-block">
        <p><strong>Embasamento bibliográfico</strong></p>
        <p>${item.bibliographic_grounding_summary || 'Sem embasamento bibliográfico associado.'}</p>
        <p><strong>Argumento bibliográfico</strong></p>
        <p>${item.bibliographic_argument || 'Sem argumento bibliográfico detalhado.'}</p>
        <div class="source-list">
          ${(item.bibliographic_refs || []).map((ref) => `<div><strong>${ref.author}</strong>, <em>${ref.title}</em> (${ref.year}).<br/><span>${ref.why}</span><br/><span style="color:var(--muted)">${ref.path}</span></div>`).join('') || '<span>Sem referências bibliográficas anexadas.</span>'}
        </div>
      </div>
    </div>
  `;
  el('detailDialog').showModal();
}

function computeCounter(items, key) {
  return items.reduce((acc, item) => {
    const value = item[key] || 'Outros';
    acc[value] = (acc[value] || 0) + 1;
    return acc;
  }, {});
}

function sortItems(items) {
  const copy = [...items];
  copy.sort((a, b) => {
    if (state.sort === 'theme') return (a.normalized_theme || '').localeCompare(b.normalized_theme || '', 'pt-BR');
    if (state.sort === 'title') return a.title.localeCompare(b.title, 'pt-BR');
    if (state.sort === 'confidence') return (a.confidence || '').localeCompare(b.confidence || '', 'pt-BR');
    return (a.effective_status || '').localeCompare(b.effective_status || '', 'pt-BR') || a.title.localeCompare(b.title, 'pt-BR');
  });
  return copy;
}

function applyFilters() {
  const items = state.data.predictions.filter((item) => {
    const haystack = normalize([
      item.prediction_text,
      item.title,
      item.normalized_theme,
      item.evidence_quote,
      item.bibliographic_argument,
      item.bibliographic_grounding_summary,
    ].join(' '));
    if (state.search && !haystack.includes(normalize(state.search))) return false;
    if (state.status !== 'all' && item.effective_status !== state.status) return false;
    if (state.originalStatus !== 'all' && item.status !== state.originalStatus) return false;
    if (state.theme !== 'all' && item.normalized_theme !== state.theme) return false;
    if (state.validated === 'validated' && !item.has_validation) return false;
    if (state.validated === 'not_validated' && item.has_validation) return false;
    if (state.bibliography === 'with_bibliography' && !item.has_bibliographic_grounding) return false;
    if (state.bibliography === 'without_bibliography' && item.has_bibliographic_grounding) return false;
    return true;
  });

  state.filtered = sortItems(items);
  renderMetrics(state.filtered);
  renderBars('statusBars', computeCounter(state.filtered, 'effective_status'));
  renderBars('themeBars', computeCounter(state.filtered, 'normalized_theme'));

  const topVideos = Object.values(state.filtered.reduce((acc, item) => {
    acc[item.video_id] ??= { title: item.title, url: item.video_url, count: 0, validated: 0, bibliography: 0 };
    acc[item.video_id].count += 1;
    acc[item.video_id].validated += item.has_validation ? 1 : 0;
    acc[item.video_id].bibliography += item.has_bibliographic_grounding ? 1 : 0;
    return acc;
  }, {})).sort((a, b) => b.count - a.count).slice(0, 8);

  renderVideoList('topVideos', topVideos, (video) => `
    <div class="video-item">
      <strong><a class="linkish" href="${video.url}" target="_blank" rel="noreferrer">${video.title}</a></strong>
      <div class="video-meta"><span>${video.count} previsões</span><span>${video.validated} validadas</span><span>${video.bibliography} com bibliografia</span></div>
    </div>
  `);

  const mismatches = state.filtered.filter((item) => item.has_validation && item.effective_status !== item.status).slice(0, 8);
  renderVideoList('mismatchList', mismatches, (item) => `
    <div class="video-item">
      <strong>${item.title}</strong>
      <p>${item.prediction_text}</p>
      <div class="video-meta"><span>${item.status}</span><span>→ ${item.effective_status}</span></div>
    </div>
  `);

  renderTable(state.filtered);
}

function init() {
  state.data = window.PREDICTIONS_EXPLORER_DATA;
  if (!state.data) {
    document.body.innerHTML = '<main style="padding:40px;color:#2f2418;font-family:Georgia,serif">Dataset não carregado.</main>';
    return;
  }

  renderHero(state.data.summary);
  fillSelect(el('statusFilter'), unique(state.data.predictions.map((item) => item.effective_status)), 'Todos');
  fillSelect(el('originalStatusFilter'), unique(state.data.predictions.map((item) => item.status)), 'Todos');
  fillSelect(el('themeFilter'), unique(state.data.predictions.map((item) => item.normalized_theme)), 'Todos');

  el('searchInput').addEventListener('input', (e) => { state.search = e.target.value; applyFilters(); });
  el('statusFilter').addEventListener('change', (e) => { state.status = e.target.value; applyFilters(); });
  el('originalStatusFilter').addEventListener('change', (e) => { state.originalStatus = e.target.value; applyFilters(); });
  el('themeFilter').addEventListener('change', (e) => { state.theme = e.target.value; applyFilters(); });
  el('validatedFilter').addEventListener('change', (e) => { state.validated = e.target.value; applyFilters(); });
  el('bibliographyFilter').addEventListener('change', (e) => { state.bibliography = e.target.value; applyFilters(); });
  el('sortFilter').addEventListener('change', (e) => { state.sort = e.target.value; applyFilters(); });
  el('resetFilters').addEventListener('click', () => {
    state.search = '';
    state.status = 'all';
    state.originalStatus = 'all';
    state.theme = 'all';
    state.validated = 'all';
    state.bibliography = 'all';
    state.sort = 'effective_status';
    el('searchInput').value = '';
    el('statusFilter').value = 'all';
    el('originalStatusFilter').value = 'all';
    el('themeFilter').value = 'all';
    el('validatedFilter').value = 'all';
    el('bibliographyFilter').value = 'all';
    el('sortFilter').value = 'effective_status';
    applyFilters();
  });
  el('closeDialog').addEventListener('click', () => el('detailDialog').close());

  applyFilters();
}

init();
