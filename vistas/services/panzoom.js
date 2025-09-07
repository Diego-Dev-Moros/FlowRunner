/**
 * FlowRunner - Pan & Zoom
 * Manejo de zoom (Ctrl+rueda) y pan (Space+arrastrar)
 */

import { scheduleEdges } from './edges/scheduler.js';

// Estado del módulo
let zoom = 1;
let isSpacePanning = false;
let panStart = null;

// Referencias DOM
let workspace = null;
let lienzo = null;
let svgEdges = null;

/**
 * Inicializa el sistema de pan y zoom
 */
export async function init() {
  console.log('🎯 Iniciando módulo PanZoom...');
  
  // Obtener referencias DOM
  workspace = document.getElementById('workspace');
  lienzo = document.getElementById('lienzo');
  svgEdges = document.getElementById('svgEdges');
  
  if (!workspace || !lienzo || !svgEdges) {
    throw new Error('Elementos DOM requeridos no encontrados para PanZoom');
  }
  
  setupZoom();
  setupPan();
  
  console.log('✅ PanZoom iniciado');
}

/**
 * Configurar zoom con Ctrl + rueda
 */
function setupZoom() {
  workspace.addEventListener('wheel', (ev) => {
    if (!ev.ctrlKey) return; // Solo con CTRL
    
    ev.preventDefault();
    ev.stopPropagation();
    
    const dir = ev.deltaY < 0 ? 1.1 : 0.9;
    const newZoom = clamp(zoom * dir, 0.5, 2);
    setZoom(newZoom);
  }, { passive: false });
}

/**
 * Configurar pan con Space + arrastrar
 */
function setupPan() {
  // Detectar tecla Space
  window.addEventListener('keydown', (e) => { 
    if (e.code === 'Space') {
      isSpacePanning = true;
      workspace.style.cursor = 'grab';
    }
  }, { passive: true });
  
  window.addEventListener('keyup', (e) => { 
    if (e.code === 'Space') {
      isSpacePanning = false;
      workspace.style.cursor = '';
    }
  }, { passive: true });

  // Pan con mouse
  workspace.addEventListener('mousedown', (e) => {
    // Solo pan cuando se presiona Space y clic en el fondo (no sobre un nodo)
    if (!isSpacePanning || e.target.closest('.node')) return;
    
    e.preventDefault();
    panStart = { 
      x: e.clientX, 
      y: e.clientY, 
      sx: workspace.scrollLeft, 
      sy: workspace.scrollTop 
    };
    
    workspace.style.cursor = 'grabbing';
    window.addEventListener('mousemove', onPanMove);
    window.addEventListener('mouseup', onPanUp);
  });
}

/**
 * Handler de movimiento durante el pan
 */
function onPanMove(e) {
  if (!panStart) return;
  
  workspace.scrollLeft = panStart.sx - (e.clientX - panStart.x);
  workspace.scrollTop = panStart.sy - (e.clientY - panStart.y);
}

/**
 * Handler de fin de pan
 */
function onPanUp() {
  workspace.style.cursor = isSpacePanning ? 'grab' : '';
  panStart = null;
  window.removeEventListener('mousemove', onPanMove);
  window.removeEventListener('mouseup', onPanUp);
}

/**
 * Aplica zoom a ambas capas con transform-origin: 0 0
 * @param {number} z - Factor de zoom (0.5 a 2)
 */
function setZoom(z) {
  zoom = z;
  lienzo.style.transform = `scale(${zoom})`;
  svgEdges.style.transform = `scale(${zoom})`;
  
  // Programar redibujado de edges
  scheduleEdges();
  
  console.log(`🔍 Zoom actualizado: ${Math.round(zoom * 100)}%`);
}

/**
 * Clamp: limita un valor entre min y max
 * @param {number} value - Valor a limitar
 * @param {number} min - Mínimo
 * @param {number} max - Máximo
 * @returns {number} Valor limitado
 */
function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

/**
 * Obtiene el factor de zoom actual
 * @returns {number} Factor de zoom
 */
export function getZoom() {
  return zoom;
}

/**
 * Establece el zoom programáticamente
 * @param {number} newZoom - Nuevo factor de zoom
 */
export function setZoomLevel(newZoom) {
  const clampedZoom = clamp(newZoom, 0.5, 2);
  setZoom(clampedZoom);
}

/**
 * Resetea el zoom al 100%
 */
export function resetZoom() {
  setZoom(1);
}

// Exportar estado para debugging
export { zoom };
