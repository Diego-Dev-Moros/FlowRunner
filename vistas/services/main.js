// vistas/services/main.js
import { state } from './state.js';
import * as registry from './registry.js';
import { renderPropsPanel } from './ui/properties.js';
import { setupTopbar } from './ui/topbar.js';
import { setupConsole } from './ui/console.js';
import { renderToolbar } from './ui/toolbar.js';
import * as edges from './edges.js';

document.addEventListener('DOMContentLoaded', init);

let uiConsole;
let zoom = 1;                 // 0.5 .. 2
let isSpacePanning = false;
let panStart = null;

async function init() {
  // Topbar
  setupTopbar({
    onExport: () => exportJSON(),
    onImport: (text) => importJSON(text),
    onClear:  () => clearCanvas(true),
  });

  // Toolbar (catálogo izq.)
  await renderToolbar();

  // Console
  uiConsole = setupConsole({
    onRun:   runFlow,
    onStop:  stopFlow,
    onClear: () => state.clearResults(),
  });

  // Arrastre desde catálogo
  setupCanvasDnd();

  // Pan / Zoom
  setupPanZoom();

  // Redibujar edges en scroll/resize
  const ws = getWorkspace();
  ws.addEventListener('scroll', edges.renderEdges);
  window.addEventListener('resize', () => {
    updateCanvasSize();        // por si cambia tamaño visible
    edges.renderEdges();
  });

  // Si Python/Eel manda notificaciones de progreso
  if (window.eel && typeof window.eel.expose === 'function') {
    window.eel.expose(onProgress, 'notify_progress');
  }

  updateCanvasHint();
  updateCanvasSize();
  edges.renderEdges();
}

/* =========================
   DnD desde el catálogo
   ========================= */
function setupCanvasDnd() {
  const ws = getWorkspace();
  ws.addEventListener('dragover', (ev) => ev.preventDefault());
  ws.addEventListener('drop', (ev) => {
    ev.preventDefault();
    const typeId = ev.dataTransfer.getData('text/plain');
    if (!typeId) return;

    const def = registry.getDefById(typeId);
    if (!def) return;

    // Posición real con scroll y compensación de zoom
    const rect = ws.getBoundingClientRect();
    const x = ((ev.clientX - rect.left) + ws.scrollLeft) / zoom;
    const y = ((ev.clientY - rect.top)  + ws.scrollTop)  / zoom;

    createNode(def, x, y);
  });
}

/* =========================
   Pan / Zoom
   ========================= */
function setupPanZoom() {
  const ws = getWorkspace();
  const lienzo = document.getElementById('lienzo');
  const svg    = document.getElementById('svgEdges');

  // Zoom con Ctrl + rueda
  ws.addEventListener('wheel', (ev) => {
    if (!ev.ctrlKey) return;          // solo con CTRL
    ev.preventDefault();
    const dir = ev.deltaY < 0 ? 1.1 : 0.9;
    setZoom(clamp(zoom * dir, 0.5, 2));
  }, { passive:false });

  // Pan con SPACE + arrastrar
  window.addEventListener('keydown', (e) => { if (e.code === 'Space') isSpacePanning = true; }, { passive:true });
  window.addEventListener('keyup',   (e) => { if (e.code === 'Space') isSpacePanning = false; }, { passive:true });

  ws.addEventListener('mousedown', (e) => {
    // solo pan cuando apretás Space y clic en el fondo (no sobre un nodo)
    if (!isSpacePanning || e.target.closest('.node')) return;
    e.preventDefault();
    panStart = { x: e.clientX, y: e.clientY, sx: ws.scrollLeft, sy: ws.scrollTop };
    ws.style.cursor = 'grabbing';
    window.addEventListener('mousemove', onPanMove);
    window.addEventListener('mouseup', onPanUp);
  });

  function onPanMove(e) {
    if (!panStart) return;
    ws.scrollLeft = panStart.sx - (e.clientX - panStart.x);
    ws.scrollTop  = panStart.sy - (e.clientY - panStart.y);
  }
  function onPanUp() {
    ws.style.cursor = '';
    panStart = null;
    window.removeEventListener('mousemove', onPanMove);
    window.removeEventListener('mouseup', onPanUp);
  }

  // aplica zoom a ambas capas
  function setZoom(z) {
    zoom = z;
    lienzo.style.transform = `scale(${zoom})`;
    svg.style.transform    = `scale(${zoom})`;
    // edges y nodos se escalan parejos → no hace falta recomputar inmediatamente
  }

  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
}

/* =========================
   Nodos
   ========================= */
function createNode(def, x = 80, y = 80) {
  const id = nextId(def.id);
  const step = {
    id,
    typeId: def.id,
    label: def.nombre || def.id,
    x: Math.max(16, x - 100),
    y: Math.max(16, y - 20),
    props: defaultProps(def.schema),
  };

  state.steps.push(step);
  mountNode(step, def);
  selectStep(step.id);

  // autoconectar con el anterior si existe
  if (state.__lastCreated && state.__lastCreated !== step.id) {
    addEdge(state.__lastCreated, step.id);
  }
  state.__lastCreated = step.id;

  updateCanvasSize();
  edges.renderEdges();
  updateCanvasHint();
}

function mountNode(step, def) {
  const el = document.createElement('div');
  el.className = 'node';
  el.id = step.id;
  el.style.left = `${step.x}px`;
  el.style.top  = `${step.y}px`;

  // Header
  const header = document.createElement('div');
  header.className = 'node-header';

  const title = document.createElement('div');
  title.className = 'node-title';
  title.textContent = step.label;

  const close = document.createElement('button');
  close.className = 'node-close';
  close.innerHTML = '×';
  close.addEventListener('click', (e) => {
    e.stopPropagation();
    deleteStep(step.id);
  });

  header.appendChild(title);
  header.appendChild(close);

  // Body
  const body = document.createElement('div');
  body.className = 'node-body';

  const paramsLine = document.createElement('div');
  paramsLine.className = 'badge';
  body.appendChild(paramsLine);

  const btnClear = document.createElement('button');
  btnClear.type = 'button';
  btnClear.textContent = 'Limpiar params';
  btnClear.className = 'btn btn-secondary';
  btnClear.style.marginTop = '6px';
  btnClear.style.padding = '4px 8px';
  btnClear.style.fontSize = '12px';
  btnClear.addEventListener('click', (e) => {
    e.stopPropagation();
    step.props = defaultProps(def.schema);
    refreshNodeSummary(step, def);
    if (state.selectedId === step.id) {
      renderPropsPanel(step, def, { onChange: onPropChange });
    }
  });
  body.appendChild(btnClear);

  // Puertos
  const ports = document.createElement('div');
  ports.className = 'ports';
  const pIn  = document.createElement('div'); pIn.className  = 'port port-in';
  const pOut = document.createElement('div'); pOut.className = 'port port-out';

  pOut.addEventListener('click', (e) => {
    e.stopPropagation();
    state.__edgeFrom = { step: step.id, port: 'out' };
    pOut.classList.add('target');
    setTimeout(() => pOut.classList.remove('target'), 300);
  });

  pIn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (state.__edgeFrom && state.__edgeFrom.step !== step.id) {
      addEdge(state.__edgeFrom.step, step.id);
      state.__edgeFrom = null;
    }
  });

  ports.appendChild(pIn);
  ports.appendChild(pOut);

  el.appendChild(header);
  el.appendChild(body);
  el.appendChild(ports);
  document.getElementById('lienzo').appendChild(el);

  el.addEventListener('mousedown', () => selectStep(step.id));
  enableDrag(el, step);
  refreshNodeSummary(step, def);
}

function refreshNodeSummary(step, def) {
  const el = document.getElementById(step.id);
  if (!el) return;

  const req = (def.schema || []).filter(s => s.required).length;
  const filled = (def.schema || []).filter(s => {
    const v = step.props?.[s.key];
    return v !== undefined && v !== null && String(v) !== '';
  }).length;

  const badge = el.querySelector('.badge');
  if (badge) badge.textContent = `Parámetros: ${filled}/${req || (def.schema || []).length}`;
}

function enableDrag(el, step) {
  const header = el.querySelector('.node-header');
  let dragging = false;
  let sx = 0, sy = 0, bx = 0, by = 0;

  const onMouseMove = (e) => {
    if (!dragging) return;
    // Compensar zoom para que el desplazamiento sea 1:1 visual
    const dx = (e.clientX - sx) / zoom;
    const dy = (e.clientY - sy) / zoom;
    step.x = Math.max(8, bx + dx);
    step.y = Math.max(8, by + dy);
    el.style.left = `${step.x}px`;
    el.style.top  = `${step.y}px`;
    updateCanvasSize();
    edges.renderEdges();
  };

  const onMouseUp = () => {
    if (!dragging) return;
    dragging = false;
    document.body.style.userSelect = '';
    window.removeEventListener('mousemove', onMouseMove);
    window.removeEventListener('mouseup', onMouseUp);
    updateCanvasSize();
    edges.renderEdges();
  };

  header.addEventListener('mousedown', (e) => {
    e.preventDefault();
    dragging = true;
    sx = e.clientX; sy = e.clientY;
    bx = step.x;    by = step.y;
    document.body.style.userSelect = 'none';
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
  });
}

function selectStep(stepId) {
  state.selectedId = stepId;
  document.querySelectorAll('.node').forEach(n => {
    n.classList.toggle('selected', n.id === stepId);
  });

  const step = state.steps.find(s => s.id === stepId);
  const def  = step ? registry.getDefById(step.typeId) : null;
  renderPropsPanel(step || null, def || null, { onChange: onPropChange });
}

function onPropChange(step, key, value) {
  const def = registry.getDefById(step.typeId);
  refreshNodeSummary(step, def);
}

function deleteStep(stepId) {
  // Reconectar linearmente (A->X->B => A->B)
  const preds = state.edges.filter(e => e.to.step === stepId).map(e => e.from.step);
  const succs = state.edges.filter(e => e.from.step === stepId).map(e => e.to.step);

  state.edges = state.edges.filter(e => e.from.step !== stepId && e.to.step !== stepId);
  state.steps = state.steps.filter(s => s.id !== stepId);

  const el = document.getElementById(stepId);
  if (el && el.parentNode) el.parentNode.removeChild(el);

  if (preds.length && succs.length) {
    preds.forEach(p => succs.forEach(s => addEdge(p, s)));
  }

  if (state.selectedId === stepId) {
    state.selectedId = null;
    renderPropsPanel(null, null);
  }

  updateCanvasSize();
  edges.renderEdges();
  updateCanvasHint();
}

function addEdge(fromStepId, toStepId) {
  if (fromStepId === toStepId) return;
  if (state.edges.some(e => e.from.step === fromStepId && e.to.step === toStepId)) return;
  state.edges.push({ from: { step: fromStepId, port: 'out' }, to: { step: toStepId, port: 'in' } });
  edges.renderEdges();
}

/* =========================
   Topbar: Import / Export / Clear
   ========================= */
function exportJSON() {
  const data = buildFlowJSON();
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url  = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'flujo.json';
  a.click();
  URL.revokeObjectURL(url);
}

function importJSON(text) {
  try {
    const json = JSON.parse(text);
    loadFlowJSON(json);
    uiConsole?.log('Flujo importado.');
  } catch (e) {
    uiConsole?.err('JSON inválido: ' + e.message);
  }
}

function clearCanvas(ask = true) {
  if (ask && !confirm('¿Limpiar lienzo?')) return;

  document.getElementById('lienzo').querySelectorAll('.node').forEach(n => n.remove());
  state.steps = [];
  state.edges = [];
  state.selectedId = null;
  state.results = {};
  state.__lastCreated = null;

  updateCanvasSize();
  edges.renderEdges();
  updateCanvasHint();
  renderPropsPanel(null, null);
}

/* =========================
   Ejecución
   ========================= */
async function runFlow() {
  const flow = buildFlowJSON();
  uiConsole?.log('Iniciando ejecución...');

  try {
    if (window.eel && typeof window.eel.run_flow === 'function') {
      const res = await window.eel.run_flow(flow)();  // Python debe exponer run_flow
      if (res?.ok) uiConsole?.ok('Ejecución completada.');
      else uiConsole?.err(res?.error || 'Fallo en ejecución.');
    } else {
      // Modo demo sin backend
      await fakeRun(flow);
      uiConsole?.ok('Ejecución simulada completa.');
    }
  } catch (e) {
    uiConsole?.err(e?.message || e);
  }
}

function stopFlow() {
  if (window.eel && typeof window.eel.cancel_flow === 'function') {
    window.eel.cancel_flow()();
  }
  uiConsole?.log('Detener: solicitado.');
}

function onProgress(payload) {
  const { stepId, message, level, preview } = payload || {};
  if (message) uiConsole?.log(message);

  if (stepId && (preview !== undefined)) {
    state.results = state.results || {};
    state.results[stepId] = {
      status: level || 'info',
      message: message || '',
      preview: typeof preview === 'string' ? preview : JSON.stringify(preview, null, 2)
    };
    if (state.selectedId === stepId) {
      const step = state.steps.find(s => s.id === stepId);
      const def  = step ? registry.getDefById(step.typeId) : null;
      renderPropsPanel(step || null, def || null, { onChange: onPropChange });
    }
  }
}


/* =========================
   Serialización
   ========================= */
function buildFlowJSON() {
  return {
    version: '1.0.0',
    generatedAt: new Date().toISOString(),
    steps: state.steps.map(s => ({
      id: s.id,
      typeId: s.typeId,
      nombre: s.label,
      position: { x: Math.round(s.x), y: Math.round(s.y) },
      props: s.props || {},
    })),
    edges: state.edges.map(e => ({ from: e.from.step, to: e.to.step })),
  };
}

function loadFlowJSON(data) {
  clearCanvas(false);

  const steps = Array.isArray(data?.steps) ? data.steps : [];
  steps.forEach(s => {
    const def = registry.getDefById(s.typeId);
    if (!def) return;
    const step = {
      id: s.id,
      typeId: s.typeId,
      label: s.nombre || def.nombre || s.typeId,
      x: s.position?.x ?? 40,
      y: s.position?.y ?? 40,
      props: { ...defaultProps(def.schema), ...(s.props || {}) },
    };
    state.steps.push(step);
    mountNode(step, def);
  });

  const edgesIn = Array.isArray(data?.edges) ? data.edges : [];
  state.edges = edgesIn
    .filter(e => e && e.from && e.to)
    .map(e => ({ from: { step: e.from, port: 'out' }, to: { step: e.to, port: 'in' } }));

  updateCanvasSize();
  edges.renderEdges();
  updateCanvasHint();
  state.selectedId = null;
  renderPropsPanel(null, null);
}

/* =========================
   Helpers
   ========================= */
function defaultProps(schema = []) {
  const out = {};
  schema.forEach(f => {
    if (f.type === 'select' && Array.isArray(f.options) && f.options.length) {
      out[f.key] = f.options[0];
    } else {
      out[f.key] = '';
    }
  });
  return out;
}

function nextId(prefix) {
  const n = (state.__counter = (state.__counter || 0) + 1);
  return `N${n}_${prefix}`;
}

function getWorkspace() {
  return document.getElementById('workspace');
}

function updateCanvasHint() {
  const el = document.querySelector('.canvas-hint');
  if (!el) return;
  el.style.display = state.steps.length ? 'none' : 'flex';
}

function updateCanvasSize() {
  // hace el lienzo desplazable según los nodos
  const lienzo = document.getElementById('lienzo');
  const svg    = document.getElementById('svgEdges');
  const marginX = 400, marginY = 300;

  const maxX = state.steps.reduce((m,s) => Math.max(m, s.x + 260), 800);
  const maxY = state.steps.reduce((m,s) => Math.max(m, s.y + 160), 600);

  lienzo.style.width  = `${maxX + marginX}px`;
  lienzo.style.height = `${maxY + marginY}px`;

  svg.setAttribute('width',  maxX + marginX);
  svg.setAttribute('height', maxY + marginY);
  svg.setAttribute('viewBox', `0 0 ${maxX + marginX} ${maxY + marginY}`);
}

/* Simulador si no hay backend */
async function fakeRun(flow) {
  for (const st of flow.steps) {
    uiConsole?.stepStart(st);
    await new Promise(r => setTimeout(r, 200));
    uiConsole?.stepEnd(st, 'OK');
  }
}
