import { state } from './state.js';

let pendingConn = null;

export function createNode(step, { onMove, onRemove, getDef }) {
  const lienzo = document.getElementById('lienzo');

  const el = document.createElement('div');
  el.className = 'node';
  el.dataset.stepId = step.id;
  el.style.left = `${step.pos.x}px`;
  el.style.top  = `${step.pos.y}px`;
  el.innerHTML = `
    <div class="node-header">
      <span class="node-title">${step.label}</span>
      <button class="node-close" title="Eliminar">×</button>
    </div>
    <div class="node-body">
      <div class="node-summary" data-role="summary"></div>
      <div class="node-actions"><button class="btn-mini clear-params">Limpiar params</button></div>
    </div>
    <div class="ports ports-in">
      ${step.ports.in.map(p => `<div class="port port-in" data-port="${p}" title="${p}"></div>`).join('')}
    </div>
    <div class="ports ports-out">
      ${step.ports.out.map(p => `<div class="port port-out" data-port="${p}" title="${p}"></div>`).join('')}
    </div>
  `;
  lienzo.appendChild(el);

  // actualizar resumen inicial
  updateNodeSummary(step, getDef?.(step.defId));

  // selección
  el.addEventListener('mousedown', (e) => {
    if (e.target.closest('.node-close, .port')) return;
    selectNode(step.id);
  });

  // drag nodo
  let dragging = false, dx = 0, dy = 0;
  const header = el.querySelector('.node-header');
  header.addEventListener('mousedown', (e) => {
    dragging = true;
    const rect = el.getBoundingClientRect();
    dx = e.clientX - rect.left;
    dy = e.clientY - rect.top;
    e.preventDefault();
  });
  window.addEventListener('mousemove', (e) => {
    if (!dragging) return;
    const canvasRect = lienzo.getBoundingClientRect();
    step.pos.x = e.clientX - canvasRect.left - dx;
    step.pos.y = e.clientY - canvasRect.top  - dy;
    el.style.left = `${step.pos.x}px`;
    el.style.top  = `${step.pos.y}px`;
    onMove?.();
  });
  window.addEventListener('mouseup', () => dragging = false);

  // eliminar
  el.querySelector('.node-close').addEventListener('click', () => {
    el.remove();
    onRemove?.(step.id);
  });

  // limpiar params
  el.querySelector('.clear-params').addEventListener('click', () => {
    const def = getDef?.(step.defId);
    (def?.schema || []).forEach(f => { step.props[f.key] = ''; });
    updateNodeSummary(step, def);
    document.dispatchEvent(new CustomEvent('node:propsCleared', { detail: { stepId: step.id }}));
  });

  // conexiones
  el.querySelectorAll('.port-out').forEach(po => {
    po.addEventListener('click', (e) => {
      e.stopPropagation();
      pendingConn = { step: step.id, port: po.dataset.port };
      toggleTargets(true);
    });
  });
  el.querySelectorAll('.port-in').forEach(pi => {
    pi.addEventListener('click', (e) => {
      e.stopPropagation();
      if (!pendingConn) return;
      const to = { step: step.id, port: pi.dataset.port };
      if (pendingConn.step !== to.step) {
        state.addEdge({ ...pendingConn }, to);
        onMove?.();
      }
      pendingConn = null;
      toggleTargets(false);
    });
  });

  lienzo.addEventListener('click', cancelPendingIfAny);
  window.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape' && pendingConn) {
      pendingConn = null;
      toggleTargets(false);
    }
  });

  function cancelPendingIfAny(ev) {
    const isPort = ev.target?.classList?.contains('port');
    if (!isPort && pendingConn) {
      pendingConn = null;
      toggleTargets(false);
    }
  }
  function toggleTargets(on) {
    document.querySelectorAll('.port-in').forEach(p => p.classList.toggle('target', on));
    document.body.classList.toggle('connecting', on);
  }

  return el;
}

export function updateNodeSummary(step, def){
  const el = document.querySelector(`.node[data-step-id="${step.id}"]`);
  if (!el) return;
  const s = el.querySelector('[data-role="summary"]');
  const total = (def?.schema || []).length;
  const filled = (def?.schema || []).filter(f => (step.props?.[f.key] ?? '') !== '').length;
  if (!total) {
    s.textContent = 'Sin parámetros.';
  } else {
    s.innerHTML = `Parámetros: <span class="${filled>0?'ok':''}">${filled}/${total}</span>`;
  }
}

export function setNodeStatus(stepId, status) {
  const el = document.querySelector(`.node[data-step-id="${stepId}"]`);
  if (!el) return;
  el.classList.remove('status-running', 'status-ok', 'status-error');
  if (status) el.classList.add(`status-${status}`);
}

export function selectNode(stepId) {
  state.setSelected(stepId);
  document.querySelectorAll('.node').forEach(n => n.classList.remove('selected'));
  const el = document.querySelector(`.node[data-step-id="${stepId}"]`);
  if (el) el.classList.add('selected');
  document.dispatchEvent(new CustomEvent('node:selected', { detail: { stepId } }));
}
