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

  root.querySelector('#btnImport').addEventListener('click', () => file.click());
  root.querySelector('#btnExport').addEventListener('click', () => onExport?.());
  root.querySelector('#btnClearAll').addEventListener('click', () => onClear?.());

  file.addEventListener('change', async () => {
    const f = file.files?.[0];
    if (!f) return;
    const text = await f.text();
    onImport?.(text);
    file.value = '';
  });
}
