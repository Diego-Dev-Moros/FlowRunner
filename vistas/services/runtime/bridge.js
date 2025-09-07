/**
 * FlowRunner - Runtime Bridge
 * Bridge con Python/Eel para ejecución de flujos
 */

import { state } from '../state.js';
import * as flowIO from '../io/flow-io.js';
import { renderPropsPanel } from '../ui/properties.js';
import { formatRunnerError } from './handlers.js';
import toast from '../ui/toast.js';

let uiConsole = null;

/**
 * Inicializa el bridge con Python/Eel
 */
export async function init() {
  // Configurar notify_progress si Eel está disponible
  if (window.eel && typeof window.eel.expose === 'function') {
    window.eel.expose(onProgress, 'notify_progress');
    console.log('🔌 Bridge Eel configurado - notify_progress expuesto');
  } else {
    console.log('⚠️ Eel no disponible - ejecutándose en modo demo');
  }
  
  console.log('🌉 Runtime Bridge iniciado');
}

/**
 * Ejecuta el flujo actual
 */
export async function runFlow() {
  const flow = flowIO.buildFlowJSON();
  const runId = toast.loading('Ejecutando flujo...', 'Iniciando procesamiento');
  
  if (uiConsole) {
    uiConsole.log('Iniciando ejecución...');
  }

  try {
    if (window.eel && typeof window.eel.run_flow === 'function') {
      // Ejecución real con Python
      const res = await window.eel.run_flow(flow)();
      toast.hide(runId);
      
      if (res?.ok) {
        if (uiConsole) {
          uiConsole.ok('Ejecución completada.');
        }
        console.log('✅ Flujo ejecutado correctamente');
      } else {
        toast.error('Error en ejecución', res?.error || 'Fallo en ejecución');
        if (uiConsole) {
          uiConsole.err(res?.error || 'Fallo en ejecución.');
        }
      }
    } else {
      // Modo demo sin backend
      await fakeRun(flow);
      toast.hide(runId);
      if (uiConsole) {
        uiConsole.ok('✅ Demo completado (sin backend Python).');
      }
      console.log('🎭 Ejecución demo completada');
    }
  } catch (error) {
    toast.hide(runId);
    const errorMsg = formatRunnerError(error);
    toast.error('Error de ejecución', errorMsg);
    if (uiConsole) {
      uiConsole.err(`Error: ${errorMsg}`);
    }
    console.error('❌ Error ejecutando flujo:', error);
  }
}

/**
 * Detiene la ejecución del flujo
 */
export function stopFlow() {
  try {
    if (window.eel && typeof window.eel.cancel_run === 'function') {
      window.eel.cancel_run();
      if (uiConsole) {
        uiConsole.log('🛑 Cancelación solicitada');
      }
      console.log('🛑 Flujo cancelado');
    } else {
      if (uiConsole) {
        uiConsole.log('🛑 Detención demo (sin backend)');
      }
      console.log('🛑 Detención demo solicitada');
    }
  } catch (error) {
    console.error('Error deteniendo flujo:', error);
    if (uiConsole) {
      uiConsole.err(`Error deteniendo flujo: ${error.message}`);
    }
  }
}

/**
 * Handler para notificaciones de progreso desde Python
 * @param {Object} payload - Datos del progreso
 */
function onProgress(payload) {
  try {
    console.log('📡 Progreso recibido:', payload);
    
    if (!payload || typeof payload !== 'object') {
      console.warn('Payload de progreso inválido');
      return;
    }

    const { stepId, status, message, preview, error, results } = payload;

    // Log en consola
    if (uiConsole) {
      if (status === 'running') {
        uiConsole.log(`▶️ ${stepId}: ${message || 'Ejecutando...'}`);
      } else if (status === 'completed') {
        uiConsole.ok(`✅ ${stepId}: ${message || 'Completado'}`);
      } else if (status === 'error') {
        uiConsole.err(`❌ ${stepId}: ${error || message || 'Error'}`);
      }
    }

    // Actualizar estado del nodo
    if (stepId) {
      updateNodeStatus(stepId, status);
    }

    // Actualizar resultados si hay preview
    if (preview && stepId) {
      state.results[stepId] = preview;
      
      // Si el nodo está seleccionado, actualizar el panel de propiedades
      if (state.selectedId === stepId) {
        const step = state.steps.find(s => s.id === stepId);
        if (step) {
          const def = registry.getDefById(step.typeId);
          renderPropsPanel(step, def);
        }
      }
    }

    // Manejar resultados globales
    if (results && typeof results === 'object') {
      Object.assign(state.results, results);
    }

  } catch (error) {
    console.error('Error procesando progreso:', error);
  }
}

/**
 * Actualiza el estado visual de un nodo
 * @param {string} stepId - ID del paso
 * @param {string} status - Estado (running, completed, error)
 */
function updateNodeStatus(stepId, status) {
  const nodeEl = document.getElementById(stepId);
  if (!nodeEl) return;

  // Limpiar estados anteriores
  nodeEl.classList.remove('status-running', 'status-ok', 'status-error');

  // Aplicar nuevo estado
  if (status === 'running') {
    nodeEl.classList.add('status-running');
  } else if (status === 'completed') {
    nodeEl.classList.add('status-ok');
    // Remover después de 3 segundos
    setTimeout(() => {
      nodeEl.classList.remove('status-ok');
    }, 3000);
  } else if (status === 'error') {
    nodeEl.classList.add('status-error');
    // Mantener el error visible más tiempo
    setTimeout(() => {
      nodeEl.classList.remove('status-error');
    }, 5000);
  }
}

/**
 * Simulación de ejecución para modo demo
 * @param {Object} flow - Datos del flujo
 */
async function fakeRun(flow) {
  const steps = flow.steps || [];
  
  for (let i = 0; i < steps.length; i++) {
    const step = steps[i];
    
    // Simular progreso
    onProgress({
      stepId: step.id,
      status: 'running',
      message: `Ejecutando ${step.nombre || step.typeId}`
    });
    
    // Simular delay
    await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 1000));
    
    // Simular completado
    onProgress({
      stepId: step.id,
      status: 'completed',
      message: `Completado ${step.nombre || step.typeId}`,
      preview: `Resultado demo para ${step.id}`
    });
  }
  
  if (uiConsole) {
    uiConsole.ok(`✅ Demo completado: ${steps.length} pasos procesados`);
  }
}

/**
 * Establece la referencia a la consola UI
 * @param {Object} console - Referencia a la consola
 */
export function setUIConsole(console) {
  uiConsole = console;
}
