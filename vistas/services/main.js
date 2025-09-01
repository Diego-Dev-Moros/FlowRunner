// vistas/services/main.js
import { state } from './state.js';
import * as registry from './registry.js';
import { renderToolbar } from './ui/toolbar.js';
import { renderPropsPanel } from './ui/properties.js';
import { setupTopbar } from './ui/topbar.js';
import { setupConsole } from './ui/console.js';
import * as edges from './edges.js';
import { createNode, selectNode } from './nodes.js';

let con; // consola (API devuelta por setupConsole)

document.addEventListener('DOMContentLoaded', init);

async function init() {
  // 1) Topbar + Consola (con tus setup*)
  con = setupConsole({
    onRun: runFlow,
    onStop: () => con?.log('Detener (placeholder)'),
    onClear: () => {}
  });

  setupTopbar({
    onExport: exportFlow,
    onImport: importFlowText,
    onClear: () => {
      if (!confirm('¿Limpiar lienzo?')) return;
      clearAll();
    }
  });

  // 2) Flags (habilitadas) → toolbar
  await registry.bootstrapFlags();
  await renderToolbar();

  // 3) DnD en lienzo
  setupCanvasDnd();

  // 4) Edges + autosize
  edges.renderEdges();
  updateCanvasHint();
  autosizeCanvas();

  const ws = getWorkspace();
  ws.addEventListener('scroll', edges.renderEdges);
  window.addEventListener('resize', () => { edges.renderEdges(); autosizeCanvas(); });
}

/* ───────── Canvas / DnD ───────── */
function setupCanvasDnd() {
  const ws = getWorkspace();
  ws.addEventListener('dragover', (ev) => ev.preventDefault());
  ws.addEventListener('drop', (ev) => {
    ev.preventDefault();
    const typeId = ev.dataTransfer.getData('text/plain') || ev.dataTransfer.getData('text/defId');
    if (!typeId) return;

    const def = registry.getDefById(typeId);
    if (!def) return;

    const rect = ws.getBoundingClientRect();
    const x = ev.clientX - rect.left + ws.scrollLeft;
    const y = ev.clientY - rect.top  + ws.scrollTop;

    addNewNode(def, { x, y });
  });
}

function addNewNode(def, pos) {
  const id = nextId(def.id);
  const step = {
    id,
    defId: def.id,
    label: def.nombre || def.id,
    categoria: def.categoria || 'proceso',
    pos: { x: Math.max(16, pos.x - 100), y: Math.max(16, pos.y - 20) },
    props: defaultProps(def.schema),
    ports: { in: ['W','N'], out: ['E','S'] },
  };
  state.steps.push(step);
  mountStep(step);
  selectNode(step.id);

  if (state.__lastCreated && state.__lastCreated !== step.id) {
    state.edges.push({ from: { step: state.__lastCreated, port:'out' }, to: { step: step.id, port: 'in' } });
  }
  state.__lastCreated = step.id;

  edges.renderEdges();
  updateCanvasHint();
  autosizeCanvas();
}

function mountStep(step) {
  const def = registry.getDefById(step.defId);

  createNode(step, {
    onMove: () => { edges.renderEdges(); autosizeCanvas(); },
    onRemove: (id) => {
      // Reencadenado lógico (prev → next)
      const preds = state.edges.filter(e => e.to.step === id).map(e => e.from.step);
      const succs = state.edges.filter(e => e.from.step === id).map(e => e.to.step);

      state.edges = state.edges.filter(e => e.from.step !== id && e.to.step !== id);
      state.steps  = state.steps.filter(s => s.id !== id);

      if (preds.length && succs.length) {
        if (preds.length === 1 && succs.length === 1) {
          state.edges.push({ from:{ step: preds[0], port:'out' }, to:{ step: succs[0], port:'in' } });
        } else {
          preds.forEach(p => succs.forEach(s => {
            if (!state.edges.some(e => e.from.step===p && e.to.step===s)) {
              state.edges.push({ from:{ step:p, port:'out' }, to:{ step:s, port:'in' } });
            }
          }));
        }
      }

      edges.renderEdges();
      updateCanvasHint();
      autosizeCanvas();
    },
    getDef: (id) => registry.getDefById(id)
  });

  // Refrescar panel de propiedades al seleccionar
  document.addEventListener('node:selected', ev => {
    const st = state.getStep?.(ev.detail.stepId) || state.steps.find(s => s.id === ev.detail.stepId);
    const df = st ? registry.getDefById(st.defId) : null;
    renderPropsPanel(st || null, df || null, { onChange: () => {} });
  });
}

/* ───────── Import / Export ───────── */
function exportFlow() {
  const data = state.toJSON ? state.toJSON() : buildFlowJSON();
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url  = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = 'flujo.json'; a.click();
  URL.revokeObjectURL(url);
  con?.ok('Flujo exportado');
}

function importFlowText(text) {
  try {
    const json = JSON.parse(text);
    importFlow(json);
    con?.ok('Flujo importado');
  } catch (e) {
    con?.err(`Importar: ${e?.message || e}`);
  }
}

function importFlow(json) {
  // limpiar DOM y estado
  document.getElementById('lienzo').innerHTML = '';
  if (state.loadJSON) state.loadJSON(json);
  else loadFlowFallback(json);

  // reconstruir nodos
  state.steps.forEach(st => mountStep(st));

  edges.renderEdges();
  updateCanvasHint();
  autosizeCanvas();
  renderPropsPanel(null, null);
}

function clearAll() {
  document.getElementById('lienzo').innerHTML = '';
  state.steps = [];
  state.edges = [];
  state.selectedStepId = null;
  state.results = {};
  state.__lastCreated = null;

  edges.renderEdges();
  updateCanvasHint();
  autosizeCanvas();
  renderPropsPanel(null, null);
  con?.clear();
}

/* ───────── Ejecutar (con fallback si no hay backend) ───────── */
async function runFlow() {
  const flow = state.toJSON ? state.toJSON() : buildFlowJSON();
  con?.clear();
  document.querySelectorAll('.node').forEach(n => n.classList.remove('status-running','status-ok','status-error'));
  con?.log('Iniciando ejecución…');

  if (window.eel && typeof window.eel.run_flow === 'function') {
    try {
      const res = await window.eel.run_flow(flow, true)();
      if (res?.results) {
        res.results.forEach(r => {
          const el = document.getElementById(r.id);
          el?.classList.remove('status-running');
          el?.classList.add(res.ok ? 'status-ok' : 'status-error');
          con?.stepEnd({ label: r.nombre || r.id }, r.output ?? 'OK');
        });
      }
      if (!res?.ok) con?.err(res?.error || 'Error en flujo');
      else con?.ok('Ejecución finalizada');
    } catch (e) {
      con?.err(String(e));
    }
  } else {
    // Demo sin backend
    state.steps.forEach((s, i) => {
      setTimeout(() => {
        const el = document.getElementById(s.id);
        el?.classList.add('status-running');
        con?.stepStart({ id: s.id, label: s.label });
      }, i*220);
      setTimeout(() => {
        const el = document.getElementById(s.id);
        el?.classList.remove('status-running'); el?.classList.add('status-ok');
        con?.stepEnd({ id: s.id, label: s.label }, 'OK');
      }, i*220+200);
    });
  }
}

/* ───────── Visual helpers ───────── */
function getWorkspace(){ return document.getElementById('workspace'); }

function updateCanvasHint() {
  const hint = document.querySelector('.canvas-hint');
  if (!hint) return;
  hint.style.display = state.steps.length ? 'none' : 'flex';
}

function autosizeCanvas() {
  const host  = getWorkspace();
  const layer = document.getElementById('lienzo');
  const nodes = Array.from(layer.querySelectorAll('.node'));
  if (!nodes.length) { layer.style.width = '100%'; layer.style.height = '100%'; return; }

  let maxRight = host.clientWidth, maxBottom = host.clientHeight;
  nodes.forEach(n => {
    const r = n.getBoundingClientRect();
    const h = host.getBoundingClientRect();
    const right  = (r.right  - h.left) + host.scrollLeft;
    const bottom = (r.bottom - h.top ) + host.scrollTop;
    if (right  > maxRight)  maxRight  = right;
    if (bottom > maxBottom) maxBottom = bottom;
  });
  maxRight += 200; maxBottom += 200;
  layer.style.width  = `${Math.max(maxRight,  host.clientWidth)}px`;
  layer.style.height = `${Math.max(maxBottom, host.clientHeight)}px`;
}

/* ───────── Utils (fallback) ───────── */
function defaultProps(schema = []) {
  const out = {};
  schema.forEach(f => {
    out[f.key] = (f.type === 'select' && Array.isArray(f.options) && f.options.length)
      ? f.options[0] : '';
  });
  return out;
}
function nextId(prefix){ const n=(state.__counter=(state.__counter||0)+1); return `N${n}_${prefix}`; }

function buildFlowJSON(){
  return {
    version: '1.0.0',
    generatedAt: new Date().toISOString(),
    steps: state.steps.map(s => ({
      id: s.id, typeId: s.defId, nombre: s.label,
      position: { x: Math.round(s.pos.x), y: Math.round(s.pos.y) },
      props: s.props || {}
    })),
    edges: state.edges.map(e => ({ from: e.from.step, to: e.to.step })),
  };
}
function loadFlowFallback(data){
  state.steps = [];
  state.edges = [];
  const steps = Array.isArray(data?.steps) ? data.steps : [];
  steps.forEach(st => {
    state.steps.push({
      id: st.id, defId: st.typeId, label: st.nombre || st.typeId,
      categoria: st.categoria || 'proceso',
      pos: { x: st.position?.x ?? 40, y: st.position?.y ?? 40 },
      props: { ...(st.props || {}) },
      ports: { in: ['W','N'], out: ['E','S'] },
    });
  });
  const valid = new Set(state.steps.map(s => s.id));
  const edgesIn = Array.isArray(data?.edges) ? data.edges : [];
  state.edges = edgesIn.filter(e => e && valid.has(e.from) && valid.has(e.to))
                       .map(e => ({ from:{ step:e.from, port:'out' }, to:{ step:e.to, port:'in' } }));
}
