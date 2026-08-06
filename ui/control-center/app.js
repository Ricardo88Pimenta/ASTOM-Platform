'use strict';

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

const state = {
  data: null,
  view: 'overview',
  componentQuery: '',
  componentStatus: 'all',
  rating: 0,
  density: localStorage.getItem('astom-density') || 'comfortable',
  reduceMotion: localStorage.getItem('astom-reduce-motion') === 'true'
};

const statusTone = (value = '') => {
  const normalized = String(value).toLowerCase();
  if (['presente', 'compatível', 'aprovado', 'apto'].some(item => normalized.includes(item))) return 'status-good';
  if (['ausente', 'divergente', 'indisponível', 'fora do alvo'].some(item => normalized.includes(item))) return 'status-warn';
  if (['bloqueado', 'falha', 'erro'].some(item => normalized.includes(item))) return 'status-bad';
  return 'status-info';
};

const labelSummary = {
  presentes: 'Presentes',
  ausentes_obrigatorios: 'Obrigatórios ausentes',
  opcionais_ausentes: 'Opcionais ausentes',
  versoes_divergentes: 'Versões divergentes',
  detectores_indisponiveis: 'Detectores indisponíveis'
};

function escapeText(value) {
  return value == null ? '—' : String(value);
}

function formatDate(value) {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '';
  return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short' }).format(date);
}

function setNotice(message = '', isError = false) {
  const notice = $('#notice');
  notice.hidden = !message;
  notice.textContent = message;
  notice.classList.toggle('status-info', !isError);
}

function badge(text, tone) {
  const element = document.createElement('span');
  element.className = `badge ${tone || statusTone(text)}`;
  element.textContent = escapeText(text);
  return element;
}

function renderOverview() {
  const data = state.data;
  const planner = data.planner || {};
  const recovery = data.recovery || {};
  const homologation = data.homologation || {};
  const profile = planner.profile || {};

  $('#homologation-current').textContent = homologation.current || 'H1';
  $('#homologation-next').textContent = homologation.next || 'H2';
  $('#homologation-message').textContent = homologation.message || 'Avaliação de interface em andamento.';
  $('#profile-title').textContent = profile.title || 'Perfil não identificado';
  $('#profile-id').textContent = profile.id || '—';
  $('#recovery-gate').textContent = recovery.gate || 'Gate não identificado';
  $('#recovery-gate').className = `gate-value ${statusTone(recovery.gate)}`;

  const summaryGrid = $('#summary-grid');
  summaryGrid.replaceChildren();
  const summary = planner.summary || {};
  Object.entries(labelSummary).forEach(([key, title]) => {
    const card = document.createElement('div');
    card.className = 'summary-card';
    const label = document.createElement('span');
    label.textContent = title;
    const value = document.createElement('strong');
    value.textContent = Number.isFinite(summary[key]) ? summary[key] : 0;
    card.append(label, value);
    summaryGrid.append(card);
  });

  const targetGrid = $('#target-grid');
  targetGrid.replaceChildren();
  (planner.target || []).forEach(item => {
    const card = document.createElement('article');
    card.className = 'target-card';
    const name = document.createElement('span');
    name.className = 'target-name';
    name.textContent = item.criterion;
    const detected = document.createElement('strong');
    detected.textContent = item.detected;
    card.append(name, detected, badge(item.status));
    targetGrid.append(card);
  });
}

function filteredComponents() {
  const components = state.data?.planner?.components || [];
  const query = state.componentQuery.trim().toLowerCase();
  return components.filter(item => {
    const haystack = [item.identificador, item.descricao, item.tipo, item.categoria, item.estado, item.fonte]
      .join(' ').toLowerCase();
    const queryMatch = !query || haystack.includes(query);
    const statusMatch = state.componentStatus === 'all' || item.estado === state.componentStatus;
    return queryMatch && statusMatch;
  });
}

function renderComponents() {
  const body = $('#components-body');
  body.replaceChildren();
  const components = filteredComponents();

  components.forEach(item => {
    const row = document.createElement('tr');
    const componentCell = document.createElement('td');
    const componentName = document.createElement('div');
    componentName.className = 'component-name';
    const strong = document.createElement('strong');
    strong.textContent = item.identificador;
    const small = document.createElement('small');
    small.textContent = item.descricao;
    componentName.append(strong, small);
    componentCell.append(componentName);

    const values = [item.tipo, item.categoria];
    row.append(componentCell);
    values.forEach(value => {
      const cell = document.createElement('td');
      cell.textContent = escapeText(value);
      row.append(cell);
    });
    const statusCell = document.createElement('td');
    statusCell.append(badge(item.estado));
    row.append(statusCell);
    [item.versao, item.fonte].forEach(value => {
      const cell = document.createElement('td');
      cell.textContent = escapeText(value);
      row.append(cell);
    });
    body.append(row);
  });

  const total = state.data?.planner?.components?.length || 0;
  $('#component-count').textContent = `${components.length} de ${total} componentes exibidos.`;
}

function renderRecovery() {
  const recovery = state.data?.recovery || {};
  const gate = recovery.gate || 'não identificado';
  const gateBadge = $('#recovery-badge');
  gateBadge.className = `badge ${statusTone(gate)}`;
  gateBadge.textContent = gate;

  const list = $('#recovery-checks');
  list.replaceChildren();
  (recovery.checks || []).forEach(item => {
    const row = document.createElement('div');
    row.className = 'check-row';
    const description = document.createElement('strong');
    description.textContent = item.descricao;
    const detected = document.createElement('span');
    detected.textContent = item.detectado;
    row.append(description, detected, badge(item.estado));
    list.append(row);
  });
}

function renderMeta() {
  const source = state.data.source === 'live' ? 'Dados reais — leitura local' : 'Dados de demonstração';
  $('#source-label').textContent = source;
  $('#generated-at').textContent = formatDate(state.data.generated_at);
}

function renderAll() {
  renderOverview();
  renderComponents();
  renderRecovery();
  renderMeta();
}

async function loadState(showLoading = true) {
  if (showLoading) $('#loading').hidden = false;
  setNotice();
  try {
    const response = await fetch('/api/state', { cache: 'no-store', headers: { Accept: 'application/json' } });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.message || `Falha HTTP ${response.status}`);
    state.data = payload;
    renderAll();
    toast('Dados ASTOM atualizados.');
  } catch (error) {
    setNotice(`Não foi possível carregar os dados: ${error.message}`, true);
  } finally {
    $('#loading').hidden = true;
  }
}

function switchView(view) {
  state.view = view;
  $$('.nav-item').forEach(button => {
    const active = button.dataset.view === view;
    button.classList.toggle('is-active', active);
    if (active) button.setAttribute('aria-current', 'page');
    else button.removeAttribute('aria-current');
  });
  $$('[data-view-panel]').forEach(panel => {
    const active = panel.dataset.viewPanel === view;
    panel.hidden = !active;
    panel.classList.toggle('is-active', active);
  });
  $('#conteudo').focus({ preventScroll: true });
}

function updateClock() {
  const now = new Date();
  $('#clock').textContent = new Intl.DateTimeFormat('pt-BR', { weekday: 'short', hour: '2-digit', minute: '2-digit' }).format(now);
  $('#preview-clock').textContent = new Intl.DateTimeFormat('pt-BR', { hour: '2-digit', minute: '2-digit' }).format(now);
}

function toggleLauncher(open) {
  const launcher = $('#launcher');
  launcher.classList.toggle('is-open', open);
  launcher.setAttribute('aria-hidden', String(!open));
  if (open) $('#launcher-search').focus();
  else $('#open-launcher').focus();
}

function applyPreferences() {
  const preview = $('#workspace-preview');
  preview.classList.toggle('is-compact', state.density === 'compact');
  $$('[data-density]').forEach(button => button.classList.toggle('is-active', button.dataset.density === state.density));
  $('#motion-toggle').checked = state.reduceMotion;
  document.body.classList.toggle('reduce-motion', state.reduceMotion);
}

function toast(message) {
  const element = $('#toast');
  element.textContent = message;
  element.hidden = false;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => { element.hidden = true; }, 2600);
}
toast.timer = null;

function exportFeedback() {
  const checks = $$('#test-checklist input').map(input => ({ id: input.value, approved: input.checked }));
  const payload = {
    schema_version: 1,
    type: 'astom-interface-feedback',
    generated_at: new Date().toISOString(),
    interface_version: state.data?.astom_version || '0.2.0-dev',
    data_source: state.data?.source || 'unknown',
    viewport: { width: window.innerWidth, height: window.innerHeight },
    preferences: { density: state.density, reduce_motion: state.reduceMotion },
    checklist: checks,
    rating: state.rating,
    notes: $('#feedback-notes').value.trim()
  };
  const blob = new Blob([`${JSON.stringify(payload, null, 2)}\n`], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `astom-interface-feedback-${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  toast('Resultado exportado localmente.');
}

function bindEvents() {
  $$('.nav-item').forEach(button => button.addEventListener('click', () => switchView(button.dataset.view)));
  $('#refresh-button').addEventListener('click', () => loadState(false));
  $('#component-filter').addEventListener('input', event => { state.componentQuery = event.target.value; renderComponents(); });
  $('#status-filter').addEventListener('change', event => { state.componentStatus = event.target.value; renderComponents(); });
  $('#open-launcher').addEventListener('click', () => toggleLauncher(true));
  $('#close-launcher').addEventListener('click', () => toggleLauncher(false));
  $('#launcher-search').addEventListener('input', event => {
    const query = event.target.value.trim().toLowerCase();
    $$('#launcher-grid button').forEach(button => { button.hidden = query && !button.dataset.app.toLowerCase().includes(query); });
  });
  $$('[data-density]').forEach(button => button.addEventListener('click', () => {
    state.density = button.dataset.density;
    localStorage.setItem('astom-density', state.density);
    applyPreferences();
  }));
  $('#motion-toggle').addEventListener('change', event => {
    state.reduceMotion = event.target.checked;
    localStorage.setItem('astom-reduce-motion', String(state.reduceMotion));
    applyPreferences();
  });
  $$('#rating-buttons button').forEach(button => button.addEventListener('click', () => {
    state.rating = Number(button.dataset.rating);
    $$('#rating-buttons button').forEach(item => item.classList.toggle('is-active', item === button));
  }));
  $('#export-feedback').addEventListener('click', exportFeedback);
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && $('#launcher').classList.contains('is-open')) toggleLauncher(false);
    if (event.key === '/' && state.view === 'components' && document.activeElement?.tagName !== 'INPUT') {
      event.preventDefault();
      $('#component-filter').focus();
    }
  });
}

function initialize() {
  bindEvents();
  applyPreferences();
  updateClock();
  setInterval(updateClock, 30000);
  loadState();
}

document.addEventListener('DOMContentLoaded', initialize);
