/**
 * FlowRunner - Node Ports
 * Manejo de puertos de conexión y pending connections
 */

import { state } from '../state.js';
import { scheduleEdges } from '../edges/scheduler.js';

// Estado de conexión pendiente
let pendingConnection = null;

/**
 * Configura los puertos de un nodo
 * @param {Element} nodeEl - Elemento del nodo
 * @param {Object} step - Datos del paso
 */
export function setupPorts(nodeEl, step) {
  const ports = nodeEl.querySelectorAll('.port');
  
  ports.forEach(port => {
    const direction = port.dataset.direction;
    const portName = port.dataset.port;
    
    if (direction === 'out') {
      port.addEventListener('click', (e) => {
        e.stopPropagation();
        handleOutPortClick(step.id, portName);
      });
    } else if (direction === 'in') {
      port.addEventListener('click', (e) => {
        e.stopPropagation();
        handleInPortClick(step.id, portName);
      });
    }
    
    // Efectos visuales en hover
    port.addEventListener('mouseenter', () => {
      port.style.transform = getPortTransform(portName, 1.3);
    });
    
    port.addEventListener('mouseleave', () => {
      if (!port.classList.contains('target')) {
        port.style.transform = getPortTransform(portName, 1);
      }
    });
  });
}

/**
 * Obtiene el transform apropiado para un puerto según su posición
 * @param {string} portName - Nombre del puerto (W, E, N, S)
 * @param {number} scale - Factor de escala
 * @returns {string} Transform CSS
 */
function getPortTransform(portName, scale) {
  const transforms = {
    'W': `translateY(-50%) scale(${scale})`,
    'E': `translateY(-50%) scale(${scale})`,
    'N': `translateX(-50%) scale(${scale})`,
    'S': `translateX(-50%) scale(${scale})`
  };
  
  return transforms[portName] || `scale(${scale})`;
}

/**
 * Maneja el clic en un puerto de salida
 * @param {string} stepId - ID del paso origen
 * @param {string} portName - Nombre del puerto
 */
function handleOutPortClick(stepId, portName) {
  if (pendingConnection) {
    // Cancelar conexión pendiente
    clearPendingConnection();
    return;
  }
  
  // Iniciar nueva conexión
  pendingConnection = {
    from: { step: stepId, port: portName },
    to: null
  };
  
  // Resaltar puertos de entrada disponibles
  highlightTargetPorts(stepId);
  
  console.log(`🔗 Iniciando conexión desde: ${stepId}:${portName}`);
}

/**
 * Maneja el clic en un puerto de entrada
 * @param {string} stepId - ID del paso destino  
 * @param {string} portName - Nombre del puerto
 */
function handleInPortClick(stepId, portName) {
  if (!pendingConnection) return;
  
  // Completar la conexión
  const fromStep = pendingConnection.from.step;
  const fromPort = pendingConnection.from.port;
  
  if (fromStep === stepId) {
    // No permitir auto-conexión
    console.warn('No se permite conectar un nodo consigo mismo');
    clearPendingConnection();
    return;
  }
  
  // Verificar si ya existe esta conexión
  const existingEdge = state.edges.find(e => 
    e.from.step === fromStep && e.to.step === stepId
  );
  
  if (existingEdge) {
    console.warn('Ya existe una conexión entre estos nodos');
    clearPendingConnection();
    return;
  }
  
  // Crear la nueva conexión
  addEdge(fromStep, stepId, fromPort, portName);
  clearPendingConnection();
  
  console.log(`✅ Conexión creada: ${fromStep}:${fromPort} -> ${stepId}:${portName}`);
}

/**
 * Agrega una nueva conexión (edge) de forma segura
 * @param {string} fromStepId - ID del paso origen
 * @param {string} toStepId - ID del paso destino
 * @param {string} fromPort - Puerto origen
 * @param {string} toPort - Puerto destino
 */
function addEdge(fromStepId, toStepId, fromPort = 'out', toPort = 'in') {
  if (fromStepId === toStepId) {
    console.warn('No se permite auto-conexión');
    return;
  }
  
  // Verificar que no existe ya
  const exists = state.edges.some(e => 
    e.from.step === fromStepId && e.to.step === toStepId
  );
  
  if (exists) {
    console.warn('La conexión ya existe');
    return;
  }
  
  // Crear nueva conexión
  const newEdge = {
    id: generateEdgeId(),
    from: { step: fromStepId, port: fromPort },
    to: { step: toStepId, port: toPort }
  };
  
  state.edges.push(newEdge);
  
  // Programar redibujado
  scheduleEdges();
  
  return newEdge;
}

/**
 * Resalta los puertos de entrada disponibles para conexión
 * @param {string} excludeStepId - ID del paso a excluir (origen)
 */
function highlightTargetPorts(excludeStepId) {
  // Limpiar targets anteriores
  document.querySelectorAll('.port.target').forEach(port => {
    port.classList.remove('target');
    port.style.transform = getPortTransform(port.dataset.port, 1);
  });
  
  // Resaltar puertos de entrada disponibles
  document.querySelectorAll('.port[data-direction="in"]').forEach(port => {
    const nodeEl = port.closest('.node');
    if (nodeEl && nodeEl.id !== excludeStepId) {
      port.classList.add('target');
      port.style.transform = getPortTransform(port.dataset.port, 1.4);
    }
  });
}

/**
 * Limpia la conexión pendiente y los resaltados
 */
function clearPendingConnection() {
  pendingConnection = null;
  
  // Limpiar todos los resaltados
  document.querySelectorAll('.port.target').forEach(port => {
    port.classList.remove('target');
    port.style.transform = getPortTransform(port.dataset.port, 1);
  });
  
  console.log('🔗 Conexión pendiente cancelada');
}

/**
 * Genera un ID único para una conexión
 * @returns {string} ID único
 */
function generateEdgeId() {
  const timestamp = Date.now();
  const random = Math.random().toString(36).slice(2, 7);
  return `edge_${timestamp}_${random}`;
}

/**
 * Elimina todas las conexiones de un nodo
 * @param {string} stepId - ID del paso
 */
export function removeNodeConnections(stepId) {
  const initialCount = state.edges.length;
  
  state.edges = state.edges.filter(e => 
    e.from.step !== stepId && e.to.step !== stepId
  );
  
  const removedCount = initialCount - state.edges.length;
  
  if (removedCount > 0) {
    scheduleEdges();
    console.log(`🗑️ ${removedCount} conexiones eliminadas del nodo: ${stepId}`);
  }
}

/**
 * Obtiene todas las conexiones de un nodo
 * @param {string} stepId - ID del paso
 * @returns {Object} Conexiones entrantes y salientes
 */
export function getNodeConnections(stepId) {
  const incoming = state.edges.filter(e => e.to.step === stepId);
  const outgoing = state.edges.filter(e => e.from.step === stepId);
  
  return { incoming, outgoing };
}

/**
 * Verifica si dos nodos están conectados
 * @param {string} fromStepId - ID del paso origen
 * @param {string} toStepId - ID del paso destino
 * @returns {boolean} true si están conectados
 */
export function areNodesConnected(fromStepId, toStepId) {
  return state.edges.some(e => 
    e.from.step === fromStepId && e.to.step === toStepId
  );
}

/**
 * Obtiene el estado actual del sistema de puertos para debugging
 * @returns {Object} Estado del sistema
 */
export function getPortsState() {
  return {
    hasPendingConnection: pendingConnection !== null,
    pendingConnection: pendingConnection ? { ...pendingConnection } : null,
    totalConnections: state.edges.length,
    targetPorts: document.querySelectorAll('.port.target').length
  };
}

// Exportar funciones principales
export { addEdge, clearPendingConnection };
