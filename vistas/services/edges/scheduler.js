/**
 * FlowRunner - Edge Scheduler
 * Sistema de batching con RequestAnimationFrame para optimización de performance
 */

import * as edgesView from './view.js';
import * as viewport from '../viewport.js';

// Estado del scheduler
let _rafEdges = null;
let _rafCanvasSize = null;

/**
 * Programa el redibujado de edges usando requestAnimationFrame
 * Colapsa múltiples llamadas en una sola ejecución por frame
 */
export function scheduleEdges() {
  if (_rafEdges) return; // Ya hay una ejecución programada
  
  _rafEdges = requestAnimationFrame(() => {
    _rafEdges = null;
    
    try {
      edgesView.renderEdges();
    } catch (error) {
      console.error('Error renderizando edges:', error);
    }
  });
}

/**
 * Programa la actualización del tamaño del canvas
 * Colapsa múltiples llamadas en una sola ejecución por frame
 */
export function scheduleCanvasSize() {
  if (_rafCanvasSize) return; // Ya hay una ejecución programada
  
  _rafCanvasSize = requestAnimationFrame(() => {
    _rafCanvasSize = null;
    
    try {
      viewport.updateCanvasSize();
    } catch (error) {
      console.error('Error actualizando tamaño del canvas:', error);
    }
  });
}

/**
 * Programa tanto edges como canvas size (operación completa)
 */
export function scheduleFullUpdate() {
  scheduleEdges();
  scheduleCanvasSize();
}

/**
 * Cancela todas las animaciones programadas
 * Útil para cleanup o cuando se necesita forzar una actualización inmediata
 */
export function cancelScheduled() {
  if (_rafEdges) {
    cancelAnimationFrame(_rafEdges);
    _rafEdges = null;
  }
  
  if (_rafCanvasSize) {
    cancelAnimationFrame(_rafCanvasSize);
    _rafCanvasSize = null;
  }
}

/**
 * Fuerza la ejecución inmediata de todas las operaciones pendientes
 * Cancela las programadas y ejecuta directamente
 */
export function flushScheduled() {
  cancelScheduled();
  
  try {
    edgesView.renderEdges();
    viewport.updateCanvasSize();
  } catch (error) {
    console.error('Error en flush de operaciones programadas:', error);
  }
}

/**
 * Obtiene el estado actual del scheduler para debugging
 * @returns {Object} Estado del scheduler
 */
export function getSchedulerState() {
  return {
    edgesScheduled: _rafEdges !== null,
    canvasSizeScheduled: _rafCanvasSize !== null,
  };
}
