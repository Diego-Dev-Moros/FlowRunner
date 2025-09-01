import { state } from '../state.js';
import { setNodeStatus } from '../nodes.js';
import { runFunction } from './handlers.js';

let abortFlag = false;

export async function runFlow(consoleUI, registry) {
  abortFlag = false;
  const g = buildGraph(state.steps, state.edges);

  // detecta ciclos
  if (g.cycle) {
    consoleUI.err('El flujo contiene ciclos; por ahora se requiere DAG.');
    return;
  }

  // Orden topológico (Kahn)
  const order = g.topo;
  for (const step of order) {
    if (abortFlag) { consoleUI.err('Ejecución detenida por el usuario.'); break; }
    setNodeStatus(step.id, 'running');
    consoleUI.stepStart(step);

    try {
      const def = registry.byId.get(step.defId);
      const res = await runFunction(def.id, step.props || {});
      setNodeStatus(step.id, 'ok');
      consoleUI.stepEnd(step, res);
    } catch (e) {
      setNodeStatus(step.id, 'error');
      consoleUI.stepFail(step, e);
      // corta toda la ejecución ante errores
      break;
    }
  }
}

export function stopFlow() { abortFlag = true; }

// Helpers
function buildGraph(steps, edges) {
  const byId = new Map(steps.map(s => [s.id, s]));
  const indeg = new Map(steps.map(s => [s.id, 0]));
  const adj = new Map(steps.map(s => [s.id, []]));

  for (const e of edges) {
    if (!byId.has(e.from.step) || !byId.has(e.to.step)) continue;
    adj.get(e.from.step).push(e.to.step);
    indeg.set(e.to.step, (indeg.get(e.to.step) || 0) + 1);
  }

  // nodos de inicio: indeg 0 (o de categoría 'inicio' priorizados)
  const q = [];
  const startNodes = steps.filter(s => s.categoria === 'inicio');
  const startSet = new Set(startNodes.map(s => s.id));
  for (const s of steps) {
    if (startSet.size ? startSet.has(s.id) : indeg.get(s.id) === 0) q.push(s.id);
  }

  const topo = [];
  const indegCopy = new Map(indeg);
  while (q.length) {
    const id = q.shift();
    const step = byId.get(id);
    topo.push(step);
    for (const v of adj.get(id) || []) {
      indegCopy.set(v, indegCopy.get(v) - 1);
      if (indegCopy.get(v) === 0) q.push(v);
    }
  }

  const cycle = topo.length !== steps.length;
  return { topo, cycle };
}
