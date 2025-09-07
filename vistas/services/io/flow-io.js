/**
 * FlowRunner - Flow I/O
 * Manejo de importación y exportación de flujos JSON
 */

import { state } from '../state.js';
import { registry } from '../registry.js';
import * as nodeView from '../nodes/view.js';
import * as viewport from '../viewport.js';
import { scheduleEdges, scheduleCanvasSize } from '../edges/scheduler.js';
import { renderPropsPanel } from '../ui/properties.js';
import toast from '../ui/toast.js';
import errorHandler from '../ui/error-handler.js';

let uiConsole = null;

/**
 * Inicializa el módulo I/O
 */
export async function init() {
  // Obtener referencia a la consola si está disponible
  const consoleModule = await import('../ui/console.js').catch(() => null);
  if (consoleModule) {
    // La consola se configura en app.js, aquí solo obtenemos referencia si es necesario
  }
  
  console.log('💾 Módulo Flow I/O iniciado');
}

/**
 * Exporta el flujo actual a JSON
 * @param {string} nombrePersonalizado - Nombre personalizado para el archivo
 */
export function exportJSON(nombrePersonalizado = 'flujo') {
  try {
    const data = buildFlowJSON();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `${nombrePersonalizado}.json`;
    a.click();
    
    URL.revokeObjectURL(url);
    
    console.log(`💾 Flujo exportado: ${nombrePersonalizado}.json`);
    toast.success('Flujo exportado', `Archivo ${nombrePersonalizado}.json descargado`);
    
  } catch (error) {
    console.error('Error exportando flujo:', error);
    toast.error('Error de exportación', error.message);
    errorHandler.reportError(error, { action: 'exportJSON', nombrePersonalizado });
  }
}

/**
 * Importa un flujo desde texto JSON
 * @param {string} text - Contenido JSON del flujo
 */
export function importJSON(text) {
  try {
    // Validar que el texto no esté vacío
    if (!text || typeof text !== 'string' || text.trim() === '') {
      throw new Error('Archivo JSON vacío o inválido');
    }
    
    // Intentar parsear el JSON
    let json;
    try {
      json = JSON.parse(text);
    } catch (parseError) {
      throw new Error(`JSON mal formateado: ${parseError.message}`);
    }
    
    // Validar estructura básica
    if (!json || typeof json !== 'object') {
      throw new Error('El archivo no contiene un objeto JSON válido');
    }
    
    if (!Array.isArray(json.steps)) {
      throw new Error('El flujo no contiene una lista de pasos válida');
    }
    
    const loadingId = toast.loading('Importando flujo...', 'Cargando nodos y conexiones');
    
    setTimeout(() => {
      try {
        loadFlowJSON(json);
        toast.hide(loadingId);
        console.log('💾 Flujo importado correctamente');
        
      } catch (loadError) {
        toast.hide(loadingId);
        toast.error('Error al cargar flujo', loadError.message);
        console.error('Error al cargar flujo:', loadError.message);
      }
    }, 200);
    
  } catch (e) {
    toast.error('JSON inválido', 'El archivo no tiene un formato válido');
    console.error('JSON inválido:', e.message);
  }
}

/**
 * Limpia el canvas
 * @param {boolean} ask - Mostrar confirmación
 */
export function clearCanvas(ask = true) {
  if (ask && state.steps.length > 0) {
    if (!confirm('¿Limpiar el canvas? Se perderán todos los nodos.')) {
      return;
    }
  }
  
  // Limpiar estado
  state.steps = [];
  state.edges = [];
  state.selectedId = null;
  state.clearResults();
  
  // Limpiar DOM
  const lienzo = document.getElementById('lienzo');
  if (lienzo) {
    lienzo.innerHTML = '';
  }
  
  // Limpiar panel de propiedades
  renderPropsPanel(null, null);
  
  // Actualizar UI
  viewport.updateCanvasHint();
  viewport.updateCanvasSize();
  scheduleEdges();
  
  console.log('🧹 Canvas limpiado');
  toast.info('Canvas limpiado', 'Todos los nodos han sido eliminados');
}

/**
 * Construye el JSON del flujo actual
 * @returns {Object} Datos del flujo en formato JSON
 */
function buildFlowJSON() {
  return {
    version: '1.0.0',
    generatedAt: new Date().toISOString(),
    name: 'Flujo FlowRunner',
    description: 'Flujo creado con FlowRunner',
    steps: state.steps.map(s => ({
      id: s.id,
      typeId: s.typeId,
      type: s.typeId, // Agregar propiedad 'type' que espera el backend
      nombre: s.label,
      position: { x: Math.round(s.pos.x), y: Math.round(s.pos.y) },
      props: s.props || {},
    })),
    edges: state.edges.map(e => ({ 
      id: e.id || generateEdgeId(),
      from: e.from.step, 
      to: e.to.step 
    })),
  };
}

/**
 * Carga un flujo desde datos JSON
 * @param {Object} data - Datos del flujo
 */
function loadFlowJSON(data) {
  try {
    clearCanvas(false);

    const steps = Array.isArray(data?.steps) ? data.steps : [];
    let validSteps = 0;
    let invalidSteps = 0;
    
    steps.forEach((s, index) => {
      // Validación mejorada del paso
      if (!s || typeof s !== 'object') {
        const error = `Paso inválido en posición ${index}: no es un objeto válido`;
        console.warn(error);
        errorHandler.reportWarning(error, { stepIndex: index, step: s });
        invalidSteps++;
        return;
      }
      
      // Manejar compatibilidad: typeId o type
      let typeId = s.typeId || s.type;
      if (!typeId || typeof typeId !== 'string') {
        const error = `Paso inválido en posición ${index}: typeId/type faltante o inválido`;
        console.warn(error);
        errorHandler.reportWarning(error, { stepIndex: index, stepId: s.id, typeId: s.typeId, type: s.type });
        invalidSteps++;
        return;
      }
      
      const def = registry.getDefById(typeId);
      if (!def) {
        const error = `Definición no encontrada para typeId: ${typeId}`;
        console.warn(error);
        errorHandler.reportWarning(error, { stepId: s.id, typeId: typeId });
        invalidSteps++;
        return;
      }
      
      const step = {
        id: s.id || `step_${Date.now()}_${Math.random().toString(36).slice(2,7)}`,
        typeId: typeId,
        label: s.nombre || def.nombre || s.typeId,
        pos: {
          x: s.position?.x ?? s.pos?.x ?? s.x ?? (100 + (validSteps * 200)),
          y: s.position?.y ?? s.pos?.y ?? s.y ?? (100 + (validSteps * 80))
        },
        props: { ...defaultProps(def.schema), ...(s.props || {}) },
      };
      
      state.steps.push(step);
      nodeView.mountNode(step, def);
      validSteps++;
    });

    // Reportar estadísticas de importación
    const totalSteps = validSteps + invalidSteps;
    if (totalSteps > 0) {
      const message = `Flujo importado: ${validSteps} pasos válidos, ${invalidSteps} pasos inválidos de ${totalSteps} total`;
      console.log(message);
      
      if (invalidSteps > 0) {
        toast.warning('Flujo con errores', `⚠️ ${invalidSteps} pasos no pudieron cargarse`);
      }
    }

    // Reconstruir edges
    const edgesIn = Array.isArray(data?.edges) ? data.edges : [];
    state.edges = edgesIn
      .filter(e => e && e.from && e.to)
      .map(e => ({
        id: e.id || generateEdgeId(),
        from: { step: e.from, port: 'out' }, 
        to: { step: e.to, port: 'in' }
      }));

    // Actualización visual
    scheduleCanvasSize();
    scheduleEdges();
    viewport.updateCanvasHint();
    state.selectedId = null;
    renderPropsPanel(null, null);

    // Forzar actualización visual y centrar
    setTimeout(() => {
      viewport.updateCanvasSize();
      scheduleEdges();
      if (state.steps.length) {
        viewport.centerOnFirstStep(state.steps);
        console.log(`✅ Flujo cargado: ${state.steps.length} nodos, ${state.edges.length} conexiones`);
      }
    }, 100);
    
  } catch (error) {
    const errorMsg = `Error al cargar flujo: ${error.message}`;
    console.error(errorMsg, error);
    errorHandler.reportError(error, { action: 'loadFlowJSON', data: data });
    toast.error('Error al cargar flujo', error.message);
    throw error;
  }
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
 * Genera un ID único para una conexión
 * @returns {string} ID único
 */
function generateEdgeId() {
  const timestamp = Date.now();
  const random = Math.random().toString(36).slice(2, 7);
  return `edge_${timestamp}_${random}`;
}

/**
 * Establece la referencia a la consola UI
 * @param {Object} console - Referencia a la consola
 */
export function setUIConsole(console) {
  uiConsole = console;
}
