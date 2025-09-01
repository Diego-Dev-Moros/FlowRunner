import { state } from './state.js';
import { COLOR_EDGE, COLOR_EDGE_HALO } from './config.js';

function portPoint(stepId, port) {
  const el = document.querySelector(`.node[data-step-id="${stepId}"]`);
  if (!el) return { x: 0, y: 0 };
  const r = el.getBoundingClientRect();
  const canvas = document.getElementById('lienzo').getBoundingClientRect();

  const cx = r.left - canvas.left;
  const cy = r.top  - canvas.top;

  switch (port) {
    case 'N': return { x: cx + r.width/2, y: cy };
    case 'S': return { x: cx + r.width/2, y: cy + r.height };
    case 'W': return { x: cx, y: cy + r.height/2 };
    case 'E': return { x: cx + r.width, y: cy + r.height/2 };
    default:  return { x: cx + r.width/2, y: cy + r.height/2 };
  }
}

function pathBetween(a, b) {
  // Curva suave con control en el medio, favoreciendo dirección horizontal
  const dx = Math.abs(b.x - a.x);
  const c1 = { x: a.x + dx * 0.5, y: a.y };
  const c2 = { x: b.x - dx * 0.5, y: b.y };
  return `M ${a.x},${a.y} C ${c1.x},${c1.y} ${c2.x},${c2.y} ${b.x},${b.y}`;
}

export function redrawEdges() {
  const svg = document.getElementById('svgEdges');
  // limpiar
  while (svg.firstChild) svg.removeChild(svg.firstChild);

  // marcador flecha
  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  const marker = document.createElementNS(svg.namespaceURI, 'marker');
  marker.setAttribute('id', 'arrow');
  marker.setAttribute('viewBox', '0 0 10 10');
  marker.setAttribute('refX', '10');
  marker.setAttribute('refY', '5');
  marker.setAttribute('markerWidth', '8');
  marker.setAttribute('markerHeight', '8');
  marker.setAttribute('orient', 'auto-start-reverse');
  const arrowPath = document.createElementNS(svg.namespaceURI, 'path');
  arrowPath.setAttribute('d', 'M 0 0 L 10 5 L 0 10 z');
  arrowPath.setAttribute('fill', COLOR_EDGE);
  marker.appendChild(arrowPath);
  defs.appendChild(marker);
  svg.appendChild(defs);

  // dibujar cada edge
  for (const e of state.edges) {
    const p1 = portPoint(e.from.step, e.from.port);
    const p2 = portPoint(e.to.step,   e.to.port);
    const d = pathBetween(p1, p2);

    // halo
    const halo = document.createElementNS(svg.namespaceURI, 'path');
    halo.setAttribute('d', d);
    halo.setAttribute('stroke', COLOR_EDGE_HALO);
    halo.setAttribute('stroke-width', '10');
    halo.setAttribute('fill', 'none');
    halo.setAttribute('opacity', '1');
    svg.appendChild(halo);

    // línea principal
    const path = document.createElementNS(svg.namespaceURI, 'path');
    path.setAttribute('d', d);
    path.setAttribute('stroke', COLOR_EDGE);
    path.setAttribute('stroke-width', '2');
    path.setAttribute('fill', 'none');
    path.setAttribute('marker-end', 'url(#arrow)');
    svg.appendChild(path);
  }
}
