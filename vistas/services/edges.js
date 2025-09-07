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
    // HOTFIX #3: Transform origin para zoom correcto
    svg.style.transformOrigin = '0 0';

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
  
  // HOTFIX #2: Optimización robusta - priorizar offset cuando sea confiable
  const host = hostLayer();
  let x, y, w, h;
  
  // Verificación más robusta de offsetParent
  const hasValidOffset = el.offsetParent !== null && 
                        el.offsetLeft !== 0 || el.offsetTop !== 0 || 
                        el.offsetWidth > 0 && el.offsetHeight > 0;
  
  if (hasValidOffset && host === el.offsetParent) {
    // Método optimizado: usar offset directo (sin reflow)
    x = el.offsetLeft;
    y = el.offsetTop;
    w = el.offsetWidth;
    h = el.offsetHeight;
  } else {
    // Fallback: getBoundingClientRect con caché de hostRect
    if (!getBox._hostRectCache || performance.now() - getBox._hostRectTime > 16) {
      getBox._hostRectCache = host.getBoundingClientRect();
      getBox._hostRectTime = performance.now();
    }
    
    const rect = el.getBoundingClientRect();
    const hostRect = getBox._hostRectCache;
    
    x = rect.left - hostRect.left + host.scrollLeft;
    y = rect.top - hostRect.top + host.scrollTop;
    w = rect.width;
    h = rect.height;
  }
  
  // Cálculo optimizado de anchor points
  const halfW = w * 0.5;
  const halfH = h * 0.5;
  
  return {
    x, y, w, h,
    left:  { x, y: y + halfH },
    right: { x: x + w, y: y + halfH },
    top:   { x: x + halfW, y },
    bottom:{ x: x + halfW, y: y + h }
  };
}

// Cache estático para optimización
getBox._hostRectCache = null;
getBox._hostRectTime = 0;

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
  svg.setAttribute('width', host.scrollWidth);
  svg.setAttribute('height', host.scrollHeight);
  svg.setAttribute('viewBox', `0 0 ${host.scrollWidth} ${host.scrollHeight}`);

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
    // HOTFIX #3: Vector-effect para grosor constante en zoom
    halo.setAttribute('vector-effect','non-scaling-stroke');
    halo.setAttribute('shape-rendering','geometricPrecision');
    g.appendChild(halo);

    const p = document.createElementNS('http://www.w3.org/2000/svg','path');
    p.setAttribute('d', d);
    p.setAttribute('fill','none');
    p.setAttribute('stroke','#FF6600');
    p.setAttribute('stroke-width','2.5');
    p.setAttribute('stroke-linecap','round');
    p.setAttribute('marker-end','url(#arrowhead)');
    // HOTFIX #3: Vector-effect para grosor constante en zoom
    p.setAttribute('vector-effect','non-scaling-stroke');
    p.setAttribute('shape-rendering','geometricPrecision');
    g.appendChild(p);
  });
}
