import { CAT_TITLES } from './config.js';
import { FUNCTION_CATALOG } from './catalog.js';
import { buildRegistry } from './registry.js';
import { state } from './state.js';
import { renderSidebar } from './ui/toolbar.js';
import { initCanvas, updateHint } from './canvas.js';
import { exportJSON, importJSON } from './io/json.js';
import { setupConsole } from './ui/console.js';
import { runFlow, stopFlow } from './runtime/runner.js';
import { renderPropsPanel } from './ui/properties.js';
import { setupTopbar } from './ui/topbar.js';
import { updateNodeSummary } from './nodes.js';

function download(filename, dataStr) {
  const blob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename; a.click();
  URL.revokeObjectURL(url);
}

function clearCanvas() {
  // borra DOM y estado (versión local a main)
  document.querySelectorAll('#lienzo .node').forEach(n => n.remove());
  state.steps = [];
  state.edges = [];
  state.seq = 1;
  state.selectedStepId = null;
  state.lastStepId = null;

  const svg = document.getElementById('svgEdges');
  while (svg.firstChild) svg.removeChild(svg.firstChild);

  // props out
  const props = document.getElementById('props');
  props.innerHTML = '<div class="props-empty">Selecciona un nodo para editar sus propiedades.</div>';

  updateHint();
}

document.addEventListener('DOMContentLoaded', () => {
  const registry = buildRegistry(FUNCTION_CATALOG, CAT_TITLES);

  // Topbar: Importar, Exportar, Limpiar
  setupTopbar({
    onExport: () => {
      const json = exportJSON();
      download('flujo.json', json);
      if (window.eel?.export_flow) window.eel.export_flow(JSON.parse(json))().catch(()=>{});
    },
    onImport: (text) => {
      try {
        importJSON(text, registry);
        renderPropsPanel(null, null); // limpio panel
      } catch (e) {
        alert('JSON inválido'); console.error(e);
      }
    },
    onClear: () => {
      if (confirm('¿Borrar todos los nodos y conexiones?')) clearCanvas();
    }
  });

  renderSidebar(registry);
  initCanvas(registry);

  const con = setupConsole({
    onRun:  () => runFlow(con, registry),
    onStop: () => stopFlow(),
    onClear: () => {}
  });
  window._flowConsole = con;

  // Propiedades al seleccionar nodo
  document.addEventListener('node:selected', (e) => {
    const step = state.getStep(e.detail.stepId);
    const def  = registry.byId.get(step?.defId);
    renderPropsPanel(step, def, {
      onChange: () => updateNodeSummary(step, def)
    });
  });

  // refrescar panel cuando se limpian params desde el nodo
  document.addEventListener('node:propsCleared', (e) => {
    const step = state.getStep(e.detail.stepId);
    const def  = registry.byId.get(step?.defId);
    renderPropsPanel(step, def, {
      onChange: () => updateNodeSummary(step, def)
    });
  });

  // helpers consola
  window.FlowRunner = {
    exportJSON: () => exportJSON(),
    importJSON: (text) => importJSON(text, registry),
    state,
    run: () => runFlow(con, registry),
    stop: stopFlow,
    clear: clearCanvas
  };

  // Eel -> consola
  function notify_progress(payload) {
    try {
      const { type, message } = payload || {};
      const text = (message != null) ? message : JSON.stringify(payload);
      const c = window._flowConsole;
      if (!c) return;
      if (type === 'ok')      c.ok(text);
      else if (type === 'err') c.err(text);
      else                     c.log(text);
    } catch (e) { console && console.warn('notify_progress error:', e); }
  }
  if (window.eel && typeof window.eel.expose === 'function') {
    window.eel.expose(notify_progress, 'notify_progress');
  }
});
