/**
 * FlowRunner - Viewport
 * Manejo de centrado, hints del canvas y tamaño del canvas
 */

import { getZoom } from './panzoom.js';
import { scheduleCanvasSize } from './edges/scheduler.js';
import { state } from './state.js';

// Referencias DOM
let workspace = null;
let lienzo = null;
let svgEdges = null;

/**
 * Inicializa el módulo viewport
 */
export async function init() {
  console.log('📐 Iniciando módulo Viewport...');
  
  // Obtener referencias DOM
  workspace = document.getElementById('workspace');
  lienzo = document.getElementById('lienzo');
  svgEdges = document.getElementById('svgEdges');
  
  if (!workspace || !lienzo || !svgEdges) {
    throw new Error('Elementos DOM requeridos no encontrados para Viewport');
  }
  
  // Configurar listeners de resize y scroll
  const ws = workspace;
  ws.addEventListener('scroll', () => {
    // scheduleEdges ya se maneja en el scheduler
  }, { passive: true });
  
  window.addEventListener('resize', () => {
    scheduleCanvasSize();
  }, { passive: true });
  
  console.log('✅ Viewport iniciado');
}

/**
 * Centra la vista en un nodo específico
 * @param {string} stepId - ID del paso a centrar
 * @param {boolean} smooth - Usar animación suave (por defecto true)
 */
export function centerOnStep(stepId, smooth = true) {
  const ws = workspace;
  const el = document.getElementById(stepId);
  if (!ws || !el) {
    console.warn(`No se pudo centrar en el nodo: ${stepId}`);
    return;
  }

  // Coordenadas del contenido (sin zoom)
  const nodeLeft = el.offsetLeft;
  const nodeTop = el.offsetTop;
  const nodeW = el.offsetWidth;
  const nodeH = el.offsetHeight;

  const zoom = getZoom();
  const viewW = ws.clientWidth / zoom; // Viewport expresado en coords del contenido
  const viewH = ws.clientHeight / zoom;

  const cx = nodeLeft + nodeW / 2;
  const cy = nodeTop + nodeH / 2;

  const left = Math.max(0, cx - viewW / 2);
  const top = Math.max(0, cy - viewH / 2);

  if (smooth) {
    // Animación suave personalizada
    smoothScrollTo(ws, left, top);
  } else {
    ws.scrollLeft = left;
    ws.scrollTop = top;
  }
  
  console.log(`🎯 Centrando en nodo: ${stepId} (${Math.round(left)}, ${Math.round(top)})`);
}

/**
 * Animación suave de scroll
 * @param {Element} element - Elemento a animar
 * @param {number} targetLeft - Posición izquierda objetivo
 * @param {number} targetTop - Posición superior objetivo
 */
function smoothScrollTo(element, targetLeft, targetTop) {
  const startLeft = element.scrollLeft;
  const startTop = element.scrollTop;
  const deltaLeft = targetLeft - startLeft;
  const deltaTop = targetTop - startTop;
  
  const duration = 500; // ms
  const startTime = performance.now();
  
  function animate(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // Easing function (ease-out)
    const easedProgress = 1 - Math.pow(1 - progress, 3);
    
    element.scrollLeft = startLeft + deltaLeft * easedProgress;
    element.scrollTop = startTop + deltaTop * easedProgress;
    
    if (progress < 1) {
      requestAnimationFrame(animate);
    }
  }
  
  requestAnimationFrame(animate);
}

/**
 * Actualiza el hint del canvas (mensaje cuando está vacío)
 */
export function updateCanvasHint() {
  const el = document.querySelector('.canvas-hint');
  if (!el) return;
  
  const hasSteps = state.steps && state.steps.length > 0;
  el.style.display = hasSteps ? 'none' : 'flex';
  
  if (!hasSteps) {
    el.textContent = 'Arrastra funciones desde la izquierda para crear tu flujo';
  }
}

/**
 * Actualiza el tamaño del canvas según los nodos existentes
 */
export function updateCanvasSize() {
  const marginX = 400;
  const marginY = 300;
  
  // Calcular dimensiones necesarias basado en posiciones de nodos
  const maxX = state.steps.reduce((m, s) => {
    const x = s.pos?.x || s.x || 0;
    return Math.max(m, x + 260); // 260 = ancho aprox del nodo
  }, 800);
  
  const maxY = state.steps.reduce((m, s) => {
    const y = s.pos?.y || s.y || 0;
    return Math.max(m, y + 160); // 160 = alto aprox del nodo
  }, 600);

  const totalWidth = maxX + marginX;
  const totalHeight = maxY + marginY;

  // Aplicar a lienzo
  lienzo.style.width = `${totalWidth}px`;
  lienzo.style.height = `${totalHeight}px`;

  // Aplicar a SVG
  if (svgEdges) {
    svgEdges.setAttribute('width', totalWidth);
    svgEdges.setAttribute('height', totalHeight);
    svgEdges.setAttribute('viewBox', `0 0 ${totalWidth} ${totalHeight}`);
  }
  
  console.log(`📏 Canvas redimensionado: ${totalWidth}x${totalHeight}`);
}

/**
 * Centra automáticamente en el primer nodo después de cargar un flujo
 * @param {Array} steps - Lista de pasos del flujo
 */
export function centerOnFirstStep(steps) {
  if (steps && steps.length > 0) {
    setTimeout(() => {
      centerOnStep(steps[0].id, true);
    }, 200); // Pequeño delay para que el DOM se actualice
  }
}

/**
 * Obtiene las coordenadas del centro actual del viewport
 * @returns {Object} Coordenadas {x, y}
 */
export function getViewportCenter() {
  const zoom = getZoom();
  const viewW = workspace.clientWidth / zoom;
  const viewH = workspace.clientHeight / zoom;
  
  return {
    x: workspace.scrollLeft + viewW / 2,
    y: workspace.scrollTop + viewH / 2
  };
}

/**
 * Verifica si un nodo está visible en el viewport
 * @param {string} stepId - ID del paso
 * @returns {boolean} true si está visible
 */
export function isNodeVisible(stepId) {
  const el = document.getElementById(stepId);
  if (!el) return false;
  
  const rect = el.getBoundingClientRect();
  const wsRect = workspace.getBoundingClientRect();
  
  return (
    rect.left < wsRect.right &&
    rect.right > wsRect.left &&
    rect.top < wsRect.bottom &&
    rect.bottom > wsRect.top
  );
}
