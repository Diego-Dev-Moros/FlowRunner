// vistas/services/ui/toolbar.js
import * as registry from '../registry.js';

/**
 * Renderiza la barra lateral con grupos colapsables.
 * Muestra SOLO las acciones habilitadas (según backend → registry.bootstrapFlags()).
 */
export async function renderToolbar() {
  const sidebar = document.getElementById('sidebar');
  if (!sidebar) return;

  // Limpia y carga flags de habilitación
  sidebar.innerHTML = '';
  await registry.bootstrapFlags();

  const groups = registry.listByCategory(); // solo habilitadas

  // Orden opcional de categorías
  const order = ['inicio', 'proceso', 'cierre', 'basicas', 'lectura', 'escritura'];
  const catKeys = Object.keys(groups).sort((a, b) => {
    const ia = order.indexOf(a); const ib = order.indexOf(b);
    if (ia === -1 && ib === -1) return a.localeCompare(b);
    if (ia === -1) return 1;
    if (ib === -1) return -1;
    return ia - ib;
  });

  catKeys.forEach(cat => {
    const defs = groups[cat] || [];
    if (!defs.length) return;

    const section = document.createElement('section');
    section.className = 'func-group';

    // Header colapsable
    const header = document.createElement('div');
    header.className = 'sidebar-header';
    Object.assign(header.style, {
      cursor: 'pointer',
      userSelect: 'none',
      display: 'flex',
      alignItems: 'center',
      gap: '6px',
      padding: '6px 0'
    });

    const caret = document.createElement('span');
    caret.textContent = '▸';
    caret.style.color = '#666';
    caret.style.flex = '0 0 auto';

    const h = document.createElement('h2');
    h.textContent = tituloCategoria(cat);
    h.style.margin = '0';
    h.style.fontSize = '1rem';
    h.style.lineHeight = '1.2';

    const list = document.createElement('div');
    list.className = 'tool-list';
    list.style.display = 'none'; // todas colapsadas al inicio

    header.addEventListener('click', () => {
      const isOpen = list.style.display !== 'none';
      list.style.display = isOpen ? 'none' : 'grid';
      caret.textContent = isOpen ? '▸' : '▾';
    });

    header.appendChild(caret);
    header.appendChild(h);
    section.appendChild(header);
    section.appendChild(list);
    sidebar.appendChild(section);

    // Items (botones arrastrables)
    defs.forEach(def => {
      const btn = document.createElement('button');
      btn.className = 'tool-item';
      btn.type = 'button';
      btn.textContent = def.nombre || def.id;
      btn.draggable = true;
      btn.dataset.type = def.id;

      btn.addEventListener('dragstart', (ev) => {
        ev.dataTransfer.setData('text/plain', def.id);
      });

      list.appendChild(btn);
    });
  });
}

function tituloCategoria(key) {
  const map = {
    inicio: 'Acciones de Inicio',
    proceso: 'Acciones de Proceso',
    cierre: 'Acciones de Cierre',
    basicas: 'Funciones Básicas',
    lectura: 'Acciones de Lectura',
    escritura: 'Acciones de Escritura',
  };
  return map[key] || key.charAt(0).toUpperCase() + key.slice(1);
}
