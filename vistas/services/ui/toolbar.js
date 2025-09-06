// vistas/services/ui/toolbar.js
import * as registry from '../registry.js';
import { CATEGORY_ORDER, CAT_TITLES } from '../config.js';

/**
 * Renderiza la barra lateral con grupos colapsables mejorados.
 * Muestra SOLO las acciones habilitadas (según backend → registry.bootstrapFlags()).
 */
export async function renderToolbar() {
  const sidebar = document.getElementById('sidebar');
  if (!sidebar) return;

  // Limpia y carga flags de habilitación
  sidebar.innerHTML = '';
  await registry.bootstrapFlags();

  const groups = registry.listByCategory(); // solo habilitadas

  // Usar el nuevo orden de categorías
  const catKeys = CATEGORY_ORDER.filter(cat => groups[cat] && groups[cat].length > 0);

  catKeys.forEach(cat => {
    const defs = groups[cat] || [];
    if (!defs.length) return;

    const section = document.createElement('section');
    section.className = 'func-group';

    // Header colapsable mejorado
    const header = document.createElement('div');
    header.className = 'sidebar-header';
    Object.assign(header.style, {
      cursor: 'pointer',
      userSelect: 'none',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: '10px 12px',
      borderRadius: '6px',
      transition: 'background-color 0.2s ease'
    });

    // Efecto hover
    header.addEventListener('mouseenter', () => {
      header.style.backgroundColor = '#f5f5f5';
    });
    header.addEventListener('mouseleave', () => {
      header.style.backgroundColor = '';
    });

    const caret = document.createElement('span');
    caret.textContent = '▸';
    caret.style.color = '#666';
    caret.style.flex = '0 0 auto';
    caret.style.fontSize = '14px';
    caret.style.transition = 'transform 0.2s ease';

    const h = document.createElement('h2');
    h.textContent = CAT_TITLES[cat] || cat.charAt(0).toUpperCase() + cat.slice(1);
    h.style.margin = '0';
    h.style.fontSize = '14px';
    h.style.fontWeight = '600';
    h.style.color = '#333';
    h.style.flex = '1';

    const count = document.createElement('span');
    count.textContent = `(${defs.length})`;
    count.style.color = '#888';
    count.style.fontSize = '12px';
    count.style.marginLeft = 'auto';

    const list = document.createElement('div');
    list.className = 'tool-list';
    list.style.display = 'none'; // todas colapsadas al inicio
    list.style.marginTop = '8px';

    header.addEventListener('click', () => {
      const isOpen = list.style.display !== 'none';
      list.style.display = isOpen ? 'none' : 'grid';
      caret.textContent = isOpen ? '▸' : '▾';
      caret.style.transform = isOpen ? 'rotate(0deg)' : 'rotate(90deg)';
    });

    header.appendChild(caret);
    header.appendChild(h);
    header.appendChild(count);
    section.appendChild(header);
    section.appendChild(list);
    sidebar.appendChild(section);

    // Items (botones arrastrables mejorados)
    defs.forEach(def => {
      const btn = document.createElement('button');
      btn.className = 'tool-item';
      btn.type = 'button';
      btn.innerHTML = `
        <div class="tool-item-content">
          <span class="tool-name">${def.nombre || def.id}</span>
          ${def.descripcion ? `<span class="tool-desc">${def.descripcion}</span>` : ''}
        </div>
      `;
      btn.draggable = true;
      btn.dataset.type = def.id;
      btn.title = def.descripcion || def.nombre || def.id;

      btn.addEventListener('dragstart', (ev) => {
        ev.dataTransfer.setData('text/plain', def.id);
        btn.style.opacity = '0.5';
      });

      btn.addEventListener('dragend', () => {
        btn.style.opacity = '';
      });

      list.appendChild(btn);
    });
  });
}


