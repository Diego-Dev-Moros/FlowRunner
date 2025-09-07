/**
 * FlowRunner - Aplicación principal
 * Bootstrap y orquestación de módulos
 */

import { setupTopbar } from './ui/topbar.js';
import { setupConsole } from './ui/console.js';
import { renderToolbar } from './ui/toolbar.js';
import * as panzoom from './panzoom.js';
import * as viewport from './viewport.js';
import * as bridge from './runtime/bridge.js';
import * as flowIO from './io/flow-io.js';
import { setupCanvasDnd } from './nodes/dnd.js';
import { state } from './state.js';

/**
 * Inicializa la aplicación FlowRunner
 */
async function init() {
  console.log('🚀 Iniciando FlowRunner...');
  
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
    const uiConsole = setupConsole({
      onRun: bridge.runFlow,
      onStop: bridge.stopFlow,
      onClear: () => state.clearResults(),
    });

    // 4. Inicializar módulos principales
    await panzoom.init();
    await viewport.init();
    await bridge.init();
    await flowIO.init();

    // 5. Configurar drag & drop desde catálogo
    setupCanvasDnd();

    // 6. Configurar atajos de teclado globales
    setupKeyboardShortcuts();

    // 7. Estado inicial
    viewport.updateCanvasHint();
    viewport.updateCanvasSize();

    console.log('✅ FlowRunner iniciado correctamente');
    
  } catch (error) {
    console.error('❌ Error iniciando FlowRunner:', error);
    throw error;
  }
}

/**
 * Configura atajos de teclado globales
 */
function setupKeyboardShortcuts() {
  window.addEventListener('keydown', (e) => {
    // F: Centrar nodo seleccionado
    if (e.key.toLowerCase() === 'f' && state.selectedId) {
      viewport.centerOnStep(state.selectedId, true);
    }
    
    // Escape: Deseleccionar nodo
    if (e.key === 'Escape' && state.selectedId) {
      // TODO: Implementar deselección
      console.log('Deseleccionando nodo...');
    }
  });
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', init);

export { init };
