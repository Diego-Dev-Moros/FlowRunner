/**
 * FlowRunner - Node Drag & Drop
 * Manejo de drag & drop desde el catálogo al canvas
 */

import { registry } from '../registry.js';
import { getZoom } from '../panzoom.js';
import * as nodeView from './view.js';

/**
 * Configura el drag & drop desde el catálogo al canvas
 */
export function setupCanvasDnd() {
  const workspace = document.getElementById('workspace');
  
  if (!workspace) {
    console.error('No se encontró el workspace para configurar DnD');
    return;
  }
  
  // Permitir drop en el workspace
  workspace.addEventListener('dragover', handleDragOver);
  workspace.addEventListener('drop', handleDrop);
  
  console.log('🎯 Drag & Drop configurado para el canvas');
}

/**
 * Maneja el evento dragover para permitir el drop
 * @param {DragEvent} ev - Evento de drag over
 */
function handleDragOver(ev) {
  ev.preventDefault(); // Necesario para permitir el drop
  
  // Opcional: cambiar cursor o estilo visual
  ev.dataTransfer.dropEffect = 'copy';
}

/**
 * Maneja el evento drop para crear nodos
 * @param {DragEvent} ev - Evento de drop
 */
function handleDrop(ev) {
  ev.preventDefault();
  
  const typeId = ev.dataTransfer.getData('text/plain');
  if (!typeId) {
    console.warn('No se recibió typeId en el drop');
    return;
  }

  const def = registry.getDefById(typeId);
  if (!def) {
    console.error(`No se encontró definición para typeId: ${typeId}`);
    return;
  }

  // Calcular posición real considerando scroll y zoom
  const rect = ev.currentTarget.getBoundingClientRect();
  const zoom = getZoom();
  
  const x = ((ev.clientX - rect.left) + ev.currentTarget.scrollLeft) / zoom;
  const y = ((ev.clientY - rect.top) + ev.currentTarget.scrollTop) / zoom;
  
  // Crear el nodo
  try {
    nodeView.createNode(def, x, y);
    console.log(`✅ Nodo creado via DnD: ${def.nombre} en (${Math.round(x)}, ${Math.round(y)})`);
  } catch (error) {
    console.error('Error creando nodo via DnD:', error);
  }
}

/**
 * Configura un elemento para ser draggable desde el catálogo
 * @param {Element} element - Elemento draggable
 * @param {string} typeId - ID del tipo de nodo
 */
export function makeDraggable(element, typeId) {
  element.draggable = true;
  element.addEventListener('dragstart', (ev) => {
    ev.dataTransfer.setData('text/plain', typeId);
    ev.dataTransfer.effectAllowed = 'copy';
    
    // Opcional: cambiar estilo del elemento siendo arrastrado
    element.style.opacity = '0.5';
  });
  
  element.addEventListener('dragend', (ev) => {
    // Restaurar estilo
    element.style.opacity = '1';
  });
}

/**
 * Obtiene la posición ajustada para drop considerando zoom y scroll
 * @param {DragEvent} ev - Evento de drop
 * @param {Element} container - Contenedor target
 * @returns {Object} Coordenadas {x, y}
 */
export function getAdjustedDropPosition(ev, container) {
  const rect = container.getBoundingClientRect();
  const zoom = getZoom();
  
  return {
    x: ((ev.clientX - rect.left) + container.scrollLeft) / zoom,
    y: ((ev.clientY - rect.top) + container.scrollTop) / zoom
  };
}
