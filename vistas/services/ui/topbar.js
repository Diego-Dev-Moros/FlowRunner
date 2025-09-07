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
    toast.info('📂 Seleccionar archivo', 'Elige un archivo JSON para importar');
    file.click();
  });
  
  root.querySelector('#btnExport').addEventListener('click', () => {
    const exportingId = toast.loading('📤 Exportando...', 'Generando archivo JSON');
    setTimeout(() => {
      onExport?.();
      toast.hide(exportingId);
      toast.success('✅ Flujo exportado', 'Archivo JSON descargado correctamente');
    }, 300);
  });
  
  root.querySelector('#btnClearAll').addEventListener('click', () => {
    toast.warning('🧹 Limpiar lienzo', '¿Estás seguro? Se perderán todos los nodos', {
      duration: 0,
      action: () => {
        onClear?.();
        toast.hideAll();
      }
    });
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
