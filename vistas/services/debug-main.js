// Debug version - minimal main.js para identificar problemas

console.log('🔧 Debug Main - Iniciando...');

// Test básico de elementos DOM
document.addEventListener('DOMContentLoaded', () => {
  console.log('📋 DOM Ready - Verificando elementos...');
  
  const topbar = document.getElementById('topbar');
  const sidebar = document.getElementById('sidebar');
  const main = document.getElementById('main');
  const workspace = document.getElementById('workspace');
  const consoleEl = document.getElementById('console');
  const props = document.getElementById('props');
  
  console.log('Elements found:', {
    topbar: !!topbar,
    sidebar: !!sidebar,
    main: !!main,
    workspace: !!workspace,
    console: !!consoleEl,
    props: !!props
  });
  
  // Setup básico del topbar
  if (topbar) {
    topbar.innerHTML = `
      <div class="brand">
        <div class="brand-dot"></div>
        <div>
          <h1>FlowRunner</h1>
          <div class="sub">Debug Mode</div>
        </div>
      </div>
      <div class="actions">
        <button class="btn btn-secondary">Limpiar lienzo</button>
        <button class="btn btn-secondary">Importar JSON</button>
        <button class="btn btn-primary">Exportar JSON</button>
      </div>
    `;
    topbar.style.border = '2px solid red'; // Debug visual
    console.log('✅ Topbar configurado');
  }
  
  // Setup básico del sidebar
  if (sidebar) {
    sidebar.innerHTML = `
      <div class="toolbar">
        <h3>🔧 Debug Mode</h3>
        <div class="toolbar-group">
          <div class="draggable">
            <span>🔍 Test Action</span>
          </div>
        </div>
      </div>
    `;
    sidebar.style.border = '2px solid blue'; // Debug visual
    console.log('✅ Sidebar configurado');
  }
  
  // Setup básico del console
  if (consoleEl) {
    consoleEl.innerHTML = `
      <div class="console-header">
        <h4>Flow Console - Debug</h4>
        <div>
          <button class="btn">▶ Test</button>
        </div>
      </div>
      <div class="console-content">
        <div class="console-line info">Debug mode activo</div>
      </div>
    `;
    console.log('✅ Console configurado');
  }
  
  // Setup básico del props
  if (props) {
    props.innerHTML = `
      <h3>Propiedades</h3>
      <div class="form-group">
        <label>Debug Info</label>
        <div style="padding: 0.5rem; background: #f0f0f0; border-radius: 4px;">
          Sistema en modo debug
        </div>
      </div>
    `;
    props.style.border = '2px solid purple'; // Debug visual
    console.log('✅ Props configurado');
  }
  
  // Verificar workspace
  if (workspace) {
    const hint = workspace.querySelector('.canvas-hint');
    if (hint) {
      hint.textContent = 'Debug Mode - Sistema funcionando';
    }
    workspace.style.border = '2px solid green'; // Debug visual
    workspace.style.background = 'rgba(0,255,0,0.1)'; // Fondo verde claro
    console.log('✅ Workspace configurado');
  }
  
  // Debug del main container
  if (main) {
    main.style.border = '2px solid orange'; // Debug visual
    main.style.background = 'rgba(255,165,0,0.1)'; // Fondo naranja claro
    console.log('✅ Main configurado');
  }
  
  console.log('🎉 Debug Main - Completado sin errores');
});
