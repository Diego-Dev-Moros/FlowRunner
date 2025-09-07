/**
 * FlowRunner - Edge View
 * Renderizado optimizado de conexiones SVG entre nodos
 */

import { state } from '../state.js';

// Referencias SVG
let svg = null;

/**
 * Obtiene el contenedor workspace
 * @returns {Element} Elemento workspace
 */
function getWorkspace() {
  return document.getElementById('workspace');
}

/**
 * Asegura que la capa SVG existe y está configurada
 */
function ensureLayer() {
  const host = getWorkspace();
  if (!host) return;
  
  if (!svg) {
    svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.id = 'svgEdges';
    svg.style.position = 'absolute';
    svg.style.inset = '0';
    svg.style.pointerEvents = 'none';
    svg.style.zIndex = '1'; // Por encima del lienzo pero debajo de nodos
    svg.style.transformOrigin = '0 0'; // HOTFIX: Transform origin para zoom correcto

    // Crear definiciones (marcadores de flechas)
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
    marker.setAttribute('id', 'arrowhead');
    marker.setAttribute('orient', 'auto');
    marker.setAttribute('markerWidth', '10');
    marker.setAttribute('markerHeight', '7');
    marker.setAttribute('refX', '10');
    marker.setAttribute('refY', '3.5');
    
    const arrow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    arrow.setAttribute('d', 'M 0 0 L 10 3.5 L 0 7 z');
    arrow.setAttribute('fill', '#FF6600');
    
    marker.appendChild(arrow);
    defs.appendChild(marker);
    svg.appendChild(defs);

    // Grupo contenedor para los edges
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('id', 'edges');
    svg.appendChild(g);

    host.appendChild(svg);
    
    console.log('📐 Capa SVG de edges inicializada');
  }
}

/**
 * Encuentra el elemento DOM de un nodo
 * @param {string} stepId - ID del paso
 * @returns {Element|null} Elemento del nodo
 */
function findNodeElement(stepId) {
  return document.getElementById(stepId) ||
         document.querySelector(`.node[data-step-id="${stepId}"]`);
}

/**
 * Calcula la caja de colisión optimizada de un nodo con caching
 * @param {string} stepId - ID del paso
 * @returns {Object|null} Caja con puntos de anclaje
 */
function getNodeBox(stepId) {
  const el = findNodeElement(stepId);
  if (!el) return null;
  
  const host = getWorkspace();
  let x, y, w, h;
  
  // HOTFIX #2: Optimización robusta - priorizar offset cuando sea confiable
  const hasValidOffset = el.offsetParent !== null && 
                        (el.offsetLeft !== 0 || el.offsetTop !== 0 || 
                         (el.offsetWidth > 0 && el.offsetHeight > 0));
  
  if (hasValidOffset && host === el.offsetParent) {
    // Método optimizado: usar offset directo (sin reflow)
    x = el.offsetLeft;
    y = el.offsetTop;
    w = el.offsetWidth;
    h = el.offsetHeight;
  } else {
    // Fallback: getBoundingClientRect con caché de hostRect por frame
    if (!getNodeBox._hostRectCache || performance.now() - getNodeBox._hostRectTime > 16) {
      getNodeBox._hostRectCache = host.getBoundingClientRect();
      getNodeBox._hostRectTime = performance.now();
    }
    
    const rect = el.getBoundingClientRect();
    const hostRect = getNodeBox._hostRectCache;
    
    x = rect.left - hostRect.left + host.scrollLeft;
    y = rect.top - hostRect.top + host.scrollTop;
    w = rect.width;
    h = rect.height;
  }
  
  // Cálculo optimizado de puntos de anclaje
  const halfW = w * 0.5;
  const halfH = h * 0.5;
  
  return {
    x, y, w, h,
    left:   { x, y: y + halfH },
    right:  { x: x + w, y: y + halfH },
    top:    { x: x + halfW, y },
    bottom: { x: x + halfW, y: y + h }
  };
}

// Cache estático para optimización por frame
getNodeBox._hostRectCache = null;
getNodeBox._hostRectTime = 0;

/**
 * Genera un path SVG curvo entre dos nodos
 * @param {Object} boxA - Caja del nodo origen
 * @param {Object} boxB - Caja del nodo destino
 * @returns {string} Path SVG
 */
function generateCurvePath(boxA, boxB) {
  const dx = boxB.right.x - boxA.right.x;
  const dy = boxB.right.y - boxA.right.y;
  const k = Math.max(40, Math.hypot(dx, dy) * 0.25); // Curvatura adaptativa

  let start, end, control1, control2;
  
  // Determinar la mejor dirección según la distancia
  if (Math.abs(dx) >= Math.abs(dy)) {
    // Conexión horizontal (left-right)
    start = boxA.right;
    end = boxB.left;
    control1 = { x: start.x + k, y: start.y };
    control2 = { x: end.x - k, y: end.y };
  } else {
    // Conexión vertical (top-bottom)
    start = boxA.bottom;
    end = boxB.top;
    control1 = { x: start.x, y: start.y + k };
    control2 = { x: end.x, y: end.y - k };
  }
  
  return `M ${start.x} ${start.y} C ${control1.x} ${control1.y}, ${control2.x} ${control2.y}, ${end.x} ${end.y}`;
}

/**
 * Renderiza todas las conexiones (edges) en el SVG
 * Función principal del módulo
 */
export function renderEdges() {
  ensureLayer();
  if (!svg) return;

  const host = getWorkspace();
  
  // Configurar dimensiones del SVG según el workspace
  svg.setAttribute('width', host.scrollWidth);
  svg.setAttribute('height', host.scrollHeight);
  svg.setAttribute('viewBox', `0 0 ${host.scrollWidth} ${host.scrollHeight}`);

  const edgesGroup = svg.querySelector('#edges');
  edgesGroup.innerHTML = ''; // Limpiar edges previos

  // Renderizar cada edge
  state.edges.forEach((edge, index) => {
    const boxA = getNodeBox(edge.from.step);
    const boxB = getNodeBox(edge.to.step);
    
    if (!boxA || !boxB) {
      console.warn(`Edge ${index}: No se pudieron obtener las cajas de los nodos`);
      return;
    }

    const pathData = generateCurvePath(boxA, boxB);

    // Crear halo (sombra del edge)
    const halo = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    halo.setAttribute('d', pathData);
    halo.setAttribute('fill', 'none');
    halo.setAttribute('stroke', 'rgba(255,102,0,.12)');
    halo.setAttribute('stroke-width', '10');
    halo.setAttribute('stroke-linecap', 'round');
    halo.setAttribute('vector-effect', 'non-scaling-stroke'); // HOTFIX: Grosor constante en zoom
    halo.setAttribute('shape-rendering', 'geometricPrecision');
    edgesGroup.appendChild(halo);

    // Crear línea principal del edge
    const mainPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    mainPath.setAttribute('d', pathData);
    mainPath.setAttribute('fill', 'none');
    mainPath.setAttribute('stroke', '#FF6600');
    mainPath.setAttribute('stroke-width', '2.5');
    mainPath.setAttribute('stroke-linecap', 'round');
    mainPath.setAttribute('marker-end', 'url(#arrowhead)');
    mainPath.setAttribute('vector-effect', 'non-scaling-stroke'); // HOTFIX: Grosor constante en zoom
    mainPath.setAttribute('shape-rendering', 'geometricPrecision');
    edgesGroup.appendChild(mainPath);
  });
  
  console.log(`🔗 ${state.edges.length} edges renderizados`);
}

/**
 * Limpia todos los edges del SVG
 */
export function clearEdges() {
  if (!svg) return;
  
  const edgesGroup = svg.querySelector('#edges');
  if (edgesGroup) {
    edgesGroup.innerHTML = '';
  }
}

/**
 * Obtiene información de debugging del módulo
 * @returns {Object} Estado del módulo
 */
export function getEdgeViewState() {
  return {
    svgInitialized: svg !== null,
    totalEdges: state.edges.length,
    cacheTime: getNodeBox._hostRectTime,
    hasCachedRect: getNodeBox._hostRectCache !== null
  };
}
