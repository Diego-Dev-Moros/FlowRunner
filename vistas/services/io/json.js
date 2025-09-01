import { state } from '../state.js';
import { createNode } from '../nodes.js';
import { redrawEdges } from '../edges.js';
import { updateHint } from '../canvas.js';

/** Exporta el estado actual a JSON (string) */
export function exportJSON() {
  const steps = state.steps.map(s => ({
    id: s.id,
    defId: s.defId,
    label: s.label,
    categoria: s.categoria,
    position: { x: Math.round(s.pos.x), y: Math.round(s.pos.y) },
    props: s.props || {}
  }));

  const edges = state.edges.map(e => ({
    id: e.id,
    from: e.from,   // {step, port}
    to:   e.to
  }));

  return JSON.stringify({
    version: '1.0.0',
    generatedAt: new Date().toISOString(),
    steps, edges
  }, null, 2);
}

/** Limpia DOM y estado */
function clearDOMAndState() {
  document.querySelectorAll('#lienzo .node').forEach(n => n.remove());
  state.steps = [];
  state.edges = [];
  state.results = {};
  state.seq = 1;
  state.selectedStepId = null;
  state.lastStepId = null;

  const svg = document.getElementById('svgEdges');
  while (svg.firstChild) svg.removeChild(svg.firstChild);
}

/** Importa un JSON y reconstruye el lienzo */
export function importJSON(text, registry) {
  let data = typeof text === 'string' ? JSON.parse(text) : text;
  if (!data || !Array.isArray(data.steps)) throw new Error('JSON inválido');

  clearDOMAndState();

  // pasos
  let maxNum = 0;
  for (const s of data.steps) {
    const def = registry.byId.get(s.defId);
    if (!def) continue;
    const id = s.id || `step_${state.seq++}`;
    const step = {
      id,
      defId: s.defId,
      label: s.label || def.nombre,
      categoria: def.categoria,
      pos: { x: s.position?.x ?? 40, y: s.position?.y ?? 40 },
      props: s.props || {},
      ports: { in: ['W','N'], out: ['E','S'] },
    };
    state.steps.push(step);
    createNode(step, {
      onMove: redrawEdges,
      onRemove: (sid) => { state.removeStep(sid); redrawEdges(); updateHint(); },
      getDef: (id) => registry.byId.get(id)
    });

    // mantener secuencia ordenada si el id es "step_#"
    const m = /^step_(\d+)$/.exec(id);
    if (m) maxNum = Math.max(maxNum, parseInt(m[1], 10));
    state.lastStepId = id;
  }
  state.seq = Math.max(state.seq, maxNum + 1);

  // edges
  if (Array.isArray(data.edges)) {
    for (const e of data.edges) {
      if (!e?.from?.step || !e?.to?.step) continue;
      state.edges.push({
        id: e.id || `edge_${Date.now()}_${Math.random().toString(36).slice(2,7)}`,
        from: e.from, to: e.to
      });
    }
  }

  redrawEdges();
  updateHint();
}
