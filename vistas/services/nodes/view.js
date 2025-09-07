/**
 * FlowRunner - Node View
 * Creación, montaje y gestión visual de nodos
 */

import { state } from '../state.js';
import { registry } from '../registry.js';
import { scheduleEdges } from '../edges/scheduler.js';
import * as viewport from '../viewport.js';
import * as nodePorts from './ports.js';
import { renderPropsPanel } from '../ui/properties.js';

// Constante de auto-centrado
const AUTO_CENTER_ON_SELECT = true;

/**
 * Crea un nuevo nodo en el canvas
 * @param {Object} def - Definición del tipo de nodo
 * @param {number} x - Posición X
 * @param {number} y - Posición Y
 * @returns {Object} El paso creado
 */
export function createNode(def, x, y) {
  const step = {
    id: nextId(def.id),
    typeId: def.id,
    label: def.nombre,
    pos: { x: Math.round(x), y: Math.round(y) },
    props: { ...defaultProps(def.schema) },
  };

  state.steps.push(step);
  const nodeEl = mountNode(step, def);
  
  // Auto-seleccionar y centrar el nuevo nodo
  selectStep(step.id);
  if (AUTO_CENTER_ON_SELECT) {
    viewport.centerOnStep(step.id, true);
  }
  
  // Actualizar canvas
  viewport.updateCanvasSize();
  viewport.updateCanvasHint();
  
  console.log(`➕ Nodo creado: ${step.id} (${def.nombre}) en (${x}, ${y})`);
  return step;
}

/**
 * Monta un nodo en el DOM
 * @param {Object} step - Datos del paso
 * @param {Object} def - Definición del tipo
 * @returns {Element} Elemento DOM del nodo
 */
export function mountNode(step, def) {
  const lienzo = document.getElementById('lienzo');
  if (!lienzo) {
    throw new Error('No se encontró el elemento lienzo');
  }

  // Crear elemento del nodo
  const nodeEl = document.createElement('div');
  nodeEl.id = step.id;
  nodeEl.className = 'node';
  
  // Aplicar sistema de formas unificado
  applyNodeShape(nodeEl, step.typeId, def);
  
  // Aplicar clases por categoría
  if (def.categoria) {
    nodeEl.classList.add(`node--${def.categoria}`);
  }
  
  // Posicionar
  nodeEl.style.left = `${step.pos.x}px`;
  nodeEl.style.top = `${step.pos.y}px`;

  // Crear estructura interna
  nodeEl.innerHTML = `
    <div class="node-header">
      <div class="node-title">${step.label}</div>
      <button class="node-close" type="button">&times;</button>
    </div>
    <div class="node-body">
      <div class="node-summary"></div>
    </div>
    <div class="ports">
      <div class="port port-in W" data-port="W" data-direction="in"></div>
      <div class="port port-in N" data-port="N" data-direction="in"></div>
      <div class="port port-out E" data-port="E" data-direction="out"></div>
      <div class="port port-out S" data-port="S" data-direction="out"></div>
    </div>
  `;

  // Event listeners
  setupNodeEvents(nodeEl, step);
  
  // Configurar drag
  enableDrag(nodeEl, step);
  
  // Configurar puertos
  nodePorts.setupPorts(nodeEl, step);
  
  // Actualizar resumen
  refreshNodeSummary(step);
  
  // Agregar al lienzo
  lienzo.appendChild(nodeEl);
  
  return nodeEl;
}

/**
 * Aplica el sistema de formas unificado al nodo
 * @param {Element} element - Elemento del nodo
 * @param {string} actionId - ID de la acción
 * @param {Object} def - Definición del tipo
 */
function applyNodeShape(element, actionId, def) {
  if (!actionId || !element) return;
  
  // Limpiar clases anteriores
  element.classList.remove('node--decision', 'node--loop', 'node--inicio', 'node--cierre');
  
  // Sistema de mapeo moderno basado en actionId
  const SHAPE_MAPPING = {
    // Decisiones (rombo)
    'condicional_si': 'node--decision',
    'condicional_multiple': 'node--decision', 
    'switch': 'node--decision',
    'decision': 'node--decision',
    'si_entonces': 'node--decision',
    
    // Loops (hexágono con marca)
    'bucle_mientras': 'node--loop',
    'bucle_for_lista': 'node--loop',
    'bucle_for_rango': 'node--loop',
    'repetir_hasta': 'node--loop',
    'loop_mientras': 'node--loop',
    'while': 'node--loop',
    'for': 'node--loop',
    'loop_para': 'node--loop',
    
    // Inicio/Cierre (píldoras)
    'inicio': 'node--inicio',
    'fin': 'node--cierre',
    'start': 'node--inicio',
    'end': 'node--cierre'
  };
  
  const shapeClass = SHAPE_MAPPING[actionId];
  if (shapeClass) {
    element.classList.add(shapeClass);
    element.dataset.nodeShape = shapeClass.replace('node--', '');
  }
  
  // Data attributes para CSS targeting
  element.dataset.typeId = actionId;
  element.dataset.categoria = def?.categoria || 'proceso';
}

/**
 * Configura los event listeners del nodo
 * @param {Element} nodeEl - Elemento del nodo
 * @param {Object} step - Datos del paso
 */
function setupNodeEvents(nodeEl, step) {
  // Click en el nodo para seleccionar
  nodeEl.addEventListener('click', (e) => {
    if (e.target.closest('.node-close')) return; // No seleccionar si se hace clic en cerrar
    selectStep(step.id);
  });
  
  // Botón de cerrar
  const closeBtn = nodeEl.querySelector('.node-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      deleteStep(step.id);
    });
  }
}

/**
 * Habilita el drag & drop para un nodo
 * @param {Element} nodeEl - Elemento del nodo
 * @param {Object} step - Datos del paso
 */
function enableDrag(nodeEl, step) {
  const header = nodeEl.querySelector('.node-header');
  if (!header) return;

  let isDragging = false;
  let startX, startY, startLeft, startTop;

  header.addEventListener('mousedown', (e) => {
    if (e.target.classList.contains('node-close')) return;
    
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    startLeft = step.pos.x;
    startTop = step.pos.y;
    
    header.style.cursor = 'grabbing';
    
    // Seleccionar el nodo al comenzar a arrastrarlo
    selectStep(step.id);
    
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    
    e.preventDefault();
  });

  function onMouseMove(e) {
    if (!isDragging) return;
    
    const deltaX = e.clientX - startX;
    const deltaY = e.clientY - startY;
    
    step.pos.x = startLeft + deltaX;
    step.pos.y = startTop + deltaY;
    
    nodeEl.style.left = `${step.pos.x}px`;
    nodeEl.style.top = `${step.pos.y}px`;
    
    // Usar scheduler para optimizar rendimiento durante el drag
    scheduleEdges();
  }

  function onMouseUp() {
    if (!isDragging) return;
    
    isDragging = false;
    header.style.cursor = 'move';
    
    window.removeEventListener('mousemove', onMouseMove);
    window.removeEventListener('mouseup', onMouseUp);
    
    // Actualización final
    viewport.updateCanvasSize();
    scheduleEdges();
  }
}

/**
 * Selecciona un paso y actualiza la UI
 * @param {string} stepId - ID del paso a seleccionar
 */
export function selectStep(stepId) {
  // Limpiar selección anterior
  document.querySelectorAll('.node.selected').forEach(el => {
    el.classList.remove('selected');
  });
  
  // Seleccionar nuevo nodo
  const nodeEl = document.getElementById(stepId);
  if (nodeEl) {
    nodeEl.classList.add('selected');
  }
  
  // Actualizar estado
  state.selectedId = stepId;
  
  // Actualizar panel de propiedades
  const step = state.steps.find(s => s.id === stepId);
  if (step) {
    const def = registry.getDefById(step.typeId);
    renderPropsPanel(step, def);
  }
  
  // Auto-centrar si está habilitado
  if (AUTO_CENTER_ON_SELECT && stepId) {
    viewport.centerOnStep(stepId, true);
  }
  
  console.log(`🎯 Nodo seleccionado: ${stepId}`);
}

/**
 * Actualiza el resumen visual del nodo
 * @param {Object} step - Datos del paso
 */
export function refreshNodeSummary(step) {
  const nodeEl = document.getElementById(step.id);
  if (!nodeEl) return;
  
  const summaryEl = nodeEl.querySelector('.node-summary');
  if (!summaryEl) return;
  
  // Generar resumen basado en props
  let summary = '';
  if (step.props) {
    const props = Object.entries(step.props).slice(0, 2); // Mostrar máximo 2 props
    summary = props.map(([key, value]) => {
      const shortValue = String(value).length > 20 ? String(value).substring(0, 20) + '...' : value;
      return `<div class="prop-line"><strong>${key}:</strong> ${shortValue}</div>`;
    }).join('');
  }
  
  summaryEl.innerHTML = summary || '<em class="text-muted">Sin configuración</em>';
}

/**
 * Elimina un paso del canvas
 * @param {string} stepId - ID del paso a eliminar
 */
export function deleteStep(stepId) {
  // Confirmar eliminación
  if (!confirm('¿Eliminar este nodo?')) return;
  
  // Eliminar del estado
  const stepIndex = state.steps.findIndex(s => s.id === stepId);
  if (stepIndex > -1) {
    state.steps.splice(stepIndex, 1);
  }
  
  // Eliminar edges relacionados
  state.edges = state.edges.filter(e => e.from.step !== stepId && e.to.step !== stepId);
  
  // Eliminar del DOM
  const nodeEl = document.getElementById(stepId);
  if (nodeEl) {
    nodeEl.remove();
  }
  
  // Limpiar selección si era el nodo seleccionado
  if (state.selectedId === stepId) {
    state.selectedId = null;
    renderPropsPanel(null, null);
  }
  
  // Actualizar UI
  viewport.updateCanvasHint();
  viewport.updateCanvasSize();
  scheduleEdges();
  
  console.log(`🗑️ Nodo eliminado: ${stepId}`);
}

/**
 * Genera propiedades por defecto basadas en el schema
 * @param {Array} schema - Schema del tipo de nodo
 * @returns {Object} Propiedades por defecto
 */
function defaultProps(schema = []) {
  const out = {};
  schema.forEach(f => {
    if (f.type === 'select' && Array.isArray(f.options) && f.options.length) {
      out[f.key] = f.options[0];
    } else {
      out[f.key] = '';
    }
  });
  return out;
}

/**
 * Genera el siguiente ID único para un nodo
 * @param {string} prefix - Prefijo del ID
 * @returns {string} ID único
 */
function nextId(prefix) {
  const n = (state.__counter = (state.__counter || 0) + 1);
  return `N${n}_${prefix}`;
}

/**
 * Actualiza una propiedad de un paso
 * @param {Object} step - El paso
 * @param {string} key - Clave de la propiedad
 * @param {any} value - Nuevo valor
 */
export function onPropChange(step, key, value) {
  if (!step || !step.props) return;
  
  step.props[key] = value;
  refreshNodeSummary(step);
  
  console.log(`📝 Propiedad actualizada: ${step.id}.${key} = ${value}`);
}

/**
 * Obtiene todos los nodos visibles en el viewport
 * @returns {Array} Lista de IDs de nodos visibles
 */
export function getVisibleNodes() {
  return state.steps
    .filter(step => viewport.isNodeVisible(step.id))
    .map(step => step.id);
}
