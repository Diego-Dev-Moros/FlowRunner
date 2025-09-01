// vistas/services/nodes.js
import { state } from './state.js';

let pendingConn = null;

function hostLayer() {
  // Usa #lienzo si existe (capa de nodos). Si no, cae en #workspace.
  return document.getElementById('lienzo') || document.getElementById('workspace');
}

export function createNode(step, { onMove, onRemove, getDef }) {
  const host = hostLayer();
  if (!host) throw new Error('No se encontró #lienzo ni #workspace para montar nodos');

  const el = document.createElement('div');
  el.className = 'node';
  el.id = step.id;                    // ← necesario para edges.js
  el.dataset.stepId = step.id;        // helper
  el.style.left = `${step.pos.x}px`;
  el.style.top  = `${step.pos.y}px`;
  el.innerHTML = `
    <div class="node-header">
      <span class="node-title">${step.label}</span>
      <button class="node-close" title="Eliminar">×</button>
    </div>
    <div class="node-body">
      <div class="node-summary" data-role="summary"></div>
      <div class="node-actions">
        <button class="btn-mini clear-params">Limpiar params</button>
      </div>
    </div>
    <div class="ports ports-in">
      ${step.ports.in.map(p => `<div class="port port-in" data-port="${p}" title="${p}"></div>`).join('')}
    </div>
    <div class="ports ports-out">
      ${step.ports.out.map(p => `<div class="port port-out" data-port="${p}" title="${p}"></div>`).join('')}
    </div>
  `;
  host.appendChild(el);

  // Resumen inicial
  updateNodeSummary(step, getDef?.(step.defId));

  // ===== Selección (clic en el nodo salvo puertos/botones) =====
  el.addEventListener('mousedown', (e) => {
    if (e.target.closest('.node-close, .port, .btn-mini')) return;
    selectNode(step.id);
  });

  // ===== DRAG súper simple y estable (con scroll) =====
  const header = el.querySelector('.node-header');
  let dragging = false;
  let startMouseX = 0, startMouseY = 0;
  let baseX = 0, baseY = 0;
  let startScrollLeft = 0, startScrollTop = 0;

  function onMouseMove(ev) {
    if (!dragging) return;
    const dx = (ev.clientX - startMouseX) + (host.scrollLeft - startScrollLeft);
    const dy = (ev.clientY - startMouseY) + (host.scrollTop  - startScrollTop);
    step.pos.x = Math.max(8, baseX + dx);
    step.pos.y = Math.max(8, baseY + dy);
    el.style.left = `${step.pos.x}px`;
    el.style.top  = `${step.pos.y}px`;
    onMove?.(); // ← redibuja edges
  }

  function onMouseUp() {
    if (!dragging) return;
    dragging = false;
    document.body.style.userSelect = '';
    window.removeEventListener('mousemove', onMouseMove);
    window.removeEventListener('mouseup', onMouseUp);
    onMove?.();
  }

  header.addEventListener('mousedown', (ev) => {
    ev.preventDefault();
    dragging = true;
    startMouseX = ev.clientX;
    startMouseY = ev.clientY;
    baseX = step.pos.x;
    baseY = step.pos.y;
    startScrollLeft = host.scrollLeft;
    startScrollTop  = host.scrollTop;
    document.body.style.userSelect = 'none';
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
  });

  // ===== Eliminar =====
  el.querySelector('.node-close').addEventListener('click', (e) => {
    e.stopPropagation();
    el.remove();
    onRemove?.(step.id);
  });

  // ===== Limpiar params =====
  el.querySelector('.clear-params').addEventListener('click', (e) => {
    e.stopPropagation();
    const def = getDef?.(step.defId);
    (def?.schema || []).forEach(f => { step.props[f.key] = ''; });
    updateNodeSummary(step, def);
    document.dispatchEvent(new CustomEvent('node:propsCleared', { detail: { stepId: step.id }}));
  });

  // ===== Conexiones =====
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

  function toggleTargets(on) {
    document.querySelectorAll('.port-in').forEach(p => p.classList.toggle('target', on));
    document.body.classList.toggle('connecting', on);
  }

  // cancelar conexión con clic vacío o Escape
  (document.getElementById('workspace') || document).addEventListener('click', (ev) => {
    if (ev.target?.classList?.contains('port')) return;
    if (pendingConn) {
      pendingConn = null;
      toggleTargets(false);
    }
  });

  window.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape' && pendingConn) {
      pendingConn = null;
      toggleTargets(false);
    }
  });

  return el;
}

export function updateNodeSummary(step, def) {
  const el = document.getElementById(step.id) ||
             document.querySelector(`.node[data-step-id="${step.id}"]`);
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
  const el = document.getElementById(stepId) ||
             document.querySelector(`.node[data-step-id="${stepId}"]`);
  if (!el) return;
  el.classList.remove('status-running', 'status-ok', 'status-error');
  if (status) el.classList.add(`status-${status}`);
}

export function selectNode(stepId) {
  state.setSelected(stepId);
  document.querySelectorAll('.node').forEach(n => n.classList.remove('selected'));
  const el = document.getElementById(stepId) ||
             document.querySelector(`.node[data-step-id="${stepId}"]`);
  if (el) el.classList.add('selected');
  document.dispatchEvent(new CustomEvent('node:selected', { detail: { stepId } }));
}
