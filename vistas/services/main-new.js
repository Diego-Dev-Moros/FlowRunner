/**
 * FlowRunner - Main (Orquestador Ligero)
 * Punto de entrada principal que coordina todos los módulos
 * Reducido de 833 líneas a ~150 líneas
 */

import { setupTopbar } from './ui/topbar.js';
import { setupConsole } from './ui/console.js';
import { renderToolbar } from './ui/toolbar.js';
import * as panzoom from './panzoom.js';
import * as viewport from './viewport.js';
import * as bridge from './runtime/bridge.js';
import * as flowIO from './io/flow-io.js';
import { setupCanvasDnd } from './nodes/dnd.js';
import { scheduleEdges } from './edges/scheduler.js';
import { state } from './state.js';

// Referencias globales
let uiConsole = null;

/**
 * Inicializa la aplicación FlowRunner
 */
async function init() {
  console.log('🚀 Iniciando FlowRunner - Versión Refactorizada...');
  
  try {
    // 1. Configurar topbar con handlers
    setupTopbar({
      onExport: (nombrePersonalizado) => flowIO.exportJSON(nombrePersonalizado),
      onImport: (text) => flowIO.importJSON(text),
      onClear: () => flowIO.clearCanvas(true),
    });

    // 2. Renderizar toolbar (catálogo izquierda)
    await renderToolbar();

    // 3. Configurar consola con handlers
    uiConsole = setupConsole({
      onRun: bridge.runFlow,
      onStop: bridge.stopFlow,
      onClear: () => state.clearResults(),
    });

    // 4. Inicializar módulos principales
    await panzoom.init();
    await viewport.init();
    await bridge.init();
    await flowIO.init();

    // 5. Conectar consola con otros módulos
    bridge.setUIConsole(uiConsole);
    flowIO.setUIConsole(uiConsole);

    // 6. Configurar drag & drop desde catálogo
    setupCanvasDnd();

    // 7. Configurar listeners globales
    setupGlobalListeners();

    // 8. Estado inicial
    viewport.updateCanvasHint();
    viewport.updateCanvasSize();
    scheduleEdges();

    console.log('✅ FlowRunner iniciado correctamente - Modo Refactorizado');
    
  } catch (error) {
    console.error('❌ Error iniciando FlowRunner:', error);
    throw error;
  }
}

/**
 * Configura listeners globales de la aplicación
 */
function setupGlobalListeners() {
  // Atajo F: Centrar nodo seleccionado
  window.addEventListener('keydown', (e) => {
    if (e.key.toLowerCase() === 'f' && state.selectedId) {
      viewport.centerOnStep(state.selectedId, true);
    }
  });

  // Redibujar edges en eventos de scroll/resize
  const workspace = document.getElementById('workspace');
  if (workspace) {
    workspace.addEventListener('scroll', scheduleEdges, { passive: true });
  }
  
  window.addEventListener('resize', () => {
    viewport.updateCanvasSize();
    scheduleEdges();
  }, { passive: true });
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', init);

// Exportar función de inicialización para uso externo si es necesario
export { init };
