import toast from './toast.js';

export function setupTopbar({ onExport, onImport, onClear }) {
  const root = document.getElementById('topbar');
  if (!root) return;

  root.innerHTML = `
    <div class="brand">
      <div class="brand-dot"></div>
      <div>
        <h1>FlowRunner</h1>
        <div class="sub">Orquestador low-code</div>
      </div>
    </div>
    <div class="actions">
      <button id="btnClearAll" class="btn btn-secondary">Limpiar lienzo</button>
      <button id="btnImport" class="btn btn-secondary">Importar JSON</button>
      <button id="btnExport" class="btn btn-primary">Exportar JSON</button>
    </div>
  `;

  const file = document.createElement('input');
  file.type = 'file';
  file.accept = 'application/json,.json';
  file.style.display = 'none';
  root.appendChild(file);

  root.querySelector('#btnImport').addEventListener('click', () => {
    // Info toast eliminado - abrir directamente
    file.click();
  });
  
  root.querySelector('#btnExport').addEventListener('click', () => {
    // Pedir nombre al usuario
    const nombreFlujo = prompt('Nombre del flujo a exportar:', 'mi_flujo') || 'flujo_sin_nombre';
    
    const exportingId = toast.loading('📤 Exportando...', `Generando ${nombreFlujo}.json`);
    setTimeout(() => {
      onExport?.(nombreFlujo);
      toast.hide(exportingId);
      // Success toast eliminado para export
    }, 300);
  });
  
  root.querySelector('#btnClearAll').addEventListener('click', () => {
    // Toast warning y borrado automático
    toast.warning('🧹 Lienzo limpiado', 'Todos los nodos han sido eliminados', {
      duration: 3000
    });
    onClear?.();
    toast.hideAll();
  });

  file.addEventListener('change', async () => {
    const f = file.files?.[0];
    if (!f) return;
    
    try {
      const text = await f.text();
      onImport?.(text);
    } catch (error) {
      toast.error('Error al leer archivo', 'No se pudo procesar el archivo seleccionado');
    }
    
    file.value = '';
  });
}
