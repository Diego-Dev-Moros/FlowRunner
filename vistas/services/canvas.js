import { state } from './state.js';
import { createNode, selectNode } from './nodes.js';
import { redrawEdges } from './edges.js';
import { AUTOCONNECT_NEW_NODES } from './config.js';

let registryRef;

export function initCanvas(registry) {
  registryRef = registry;
  const lienzo = document.getElementById('lienzo');
  const svg = document.getElementById('svgEdges');

  svg.setAttribute('width', lienzo.clientWidth);
  svg.setAttribute('height', lienzo.clientHeight);

  lienzo.addEventListener('dragover', ev => ev.preventDefault());
  lienzo.addEventListener('drop', ev => {
    ev.preventDefault();
    const defId = ev.dataTransfer.getData('text/defId');
    if (!defId) return;
    const def = registryRef.byId.get(defId);
    const rect = lienzo.getBoundingClientRect();
    const pos = { x: ev.clientX - rect.left, y: ev.clientY - rect.top };

    const step = state.addStep(def, pos);
    createNode(step, {
      onMove: redrawEdges,
      onRemove: handleRemove,
      getDef: (id) => registryRef.byId.get(id)
    });
    selectNode(step.id);

    if (AUTOCONNECT_NEW_NODES && state.lastStepId && state.lastStepId !== step.id) {
      const prevId = state.lastStepId;
      state.addEdge({ step: prevId, port: 'E' }, { step: step.id, port: 'W' });
    }
    state.lastStepId = step.id;

    redrawEdges();
    updateHint();
  });

  window.addEventListener('resize', () => {
    svg.setAttribute('width', lienzo.clientWidth);
    svg.setAttribute('height', lienzo.clientHeight);
    redrawEdges();
  });

  updateHint();
}

export function updateHint(){
  const ws = document.getElementById('workspace');
  if (!ws) return;
  if (state.steps.length) ws.classList.add('has-steps');
  else ws.classList.remove('has-steps');
}

function handleRemove(stepId) {
  state.removeStep(stepId);
  redrawEdges();
  updateHint();
}
