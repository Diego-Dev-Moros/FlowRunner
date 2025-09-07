// vistas/services/edges.js
import { state } from './state.js';

let svg;

function hostLayer() {
  return document.getElementById('workspace');
}

function ensureLayer() {
  const host = hostLayer();
  if (!host) return;
  if (!svg) {
    svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.id = 'svgEdges';
    svg.style.position = 'absolute';
    svg.style.inset = '0';
    svg.style.pointerEvents = 'none';
    svg.style.zIndex = '0';

    const defs = document.createElementNS('http://www.w3.org/2000/svg','defs');
    const marker = document.createElementNS('http://www.w3.org/2000/svg','marker');
    marker.setAttribute('id','arrowhead');
    marker.setAttribute('orient','auto');
    marker.setAttribute('markerWidth','10');
    marker.setAttribute('markerHeight','7');
    marker.setAttribute('refX','10');
    marker.setAttribute('refY','3.5');
    const arrow = document.createElementNS('http://www.w3.org/2000/svg','path');
    arrow.setAttribute('d','M 0 0 L 10 3.5 L 0 7 z');
    arrow.setAttribute('fill','#FF6600');
    marker.appendChild(arrow);
    defs.appendChild(marker);
    svg.appendChild(defs);

    const g = document.createElementNS('http://www.w3.org/2000/svg','g');
    g.setAttribute('id','edges');
    svg.appendChild(g);

    host.appendChild(svg);
  }
}

function findNodeEl(stepId) {
  return document.getElementById(stepId) ||
         document.querySelector(`.node[data-step-id="${stepId}"]`);
}

function getBox(stepId) {
  const el = findNodeEl(stepId);
  if (!el) return null;
  const rect = el.getBoundingClientRect();
  const host = hostLayer();
  const hostRect = host.getBoundingClientRect();
  const x = rect.left - hostRect.left + host.scrollLeft;
  const y = rect.top  - hostRect.top  + host.scrollTop;
  const w = rect.width, h = rect.height;
  return {
    x, y, w, h,
    left:  { x,       y: y + h/2 },
    right: { x: x+w,  y: y + h/2 },
    top:   { x: x+w/2,y },
    bottom:{ x: x+w/2,y: y + h }
  };
}

function pathLR(a, b) {
  const dx = b.right.x - a.right.x;
  const dy = b.right.y - a.right.y;
  const k  = Math.max(40, Math.hypot(dx,dy) * 0.25);

  let s, t, c1, c2;
  if (Math.abs(dx) >= Math.abs(dy)) {
    s = a.right; t = b.left;
    c1 = { x: s.x + k, y: s.y };
    c2 = { x: t.x - k, y: t.y };
  } else {
    s = a.bottom; t = b.top;
    c1 = { x: s.x, y: s.y + k };
    c2 = { x: t.x, y: t.y - k };
  }
  return `M ${s.x} ${s.y} C ${c1.x} ${c1.y}, ${c2.x} ${c2.y}, ${t.x} ${t.y}`;
}

export function renderEdges() {
  ensureLayer();
  if (!svg) return;

  const host = hostLayer();
  if (!host) return;
  
  // Validar dimensiones antes de usarlas
  const width = Math.max(host.scrollWidth || 0, host.clientWidth || 0, 800);
  const height = Math.max(host.scrollHeight || 0, host.clientHeight || 0, 600);
  
  svg.setAttribute('width', width);
  svg.setAttribute('height', height);
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);

  const g = svg.querySelector('#edges');
  g.innerHTML = '';

  state.edges.forEach(e => {
    const A = getBox(e.from.step);
    const B = getBox(e.to.step);
    if (!A || !B) return;

    const d = pathLR(A, B);

    const halo = document.createElementNS('http://www.w3.org/2000/svg','path');
    halo.setAttribute('d', d);
    halo.setAttribute('fill','none');
    halo.setAttribute('stroke','rgba(255,102,0,.12)');
    halo.setAttribute('stroke-width','10');
    halo.setAttribute('stroke-linecap','round');
    g.appendChild(halo);

    const p = document.createElementNS('http://www.w3.org/2000/svg','path');
    p.setAttribute('d', d);
    p.setAttribute('fill','none');
    p.setAttribute('stroke','#FF6600');
    p.setAttribute('stroke-width','2.5');
    p.setAttribute('stroke-linecap','round');
    p.setAttribute('marker-end','url(#arrowhead)');
    g.appendChild(p);
  });
}
