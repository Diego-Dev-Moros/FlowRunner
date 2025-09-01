import { CAT_TITLES } from '../config.js';

const storeKey = (cat) => `fr.collapsed.${cat}`;

export function renderSidebar(registry) {
  const side = document.getElementById('sidebar');
  side.innerHTML = '';

  const defaultCollapsed = true; // 👈 arranca todo colapsado

  for (const [cat, defs] of registry.byCat.entries()) {
    const wrap = document.createElement('section');
    wrap.className = 'cat';

    // Si no hay preferencia guardada, usamos el default (=colapsado)
    const pref = localStorage.getItem(storeKey(cat));
    const startCollapsed = (pref === null) ? defaultCollapsed : pref === '1';
    if (startCollapsed) wrap.classList.add('cat-collapsed');

    const h = document.createElement('h4');
    const title = registry.catTitles?.[cat] || CAT_TITLES?.[cat] || cat;
    h.innerHTML = `<span class="chev"></span>${title}`;
    h.addEventListener('click', () => {
      wrap.classList.toggle('cat-collapsed');
      localStorage.setItem(storeKey(cat), wrap.classList.contains('cat-collapsed') ? '1' : '0');
    });
    wrap.appendChild(h);

    const ul = document.createElement('div');
    ul.className = 'tool-list';

    defs.forEach(def => {
      const btn = document.createElement('button');
      btn.className = 'tool-item';
      btn.textContent = def.nombre;
      btn.title = def.descripcion || '';
      btn.draggable = true;
      btn.addEventListener('dragstart', ev => {
        ev.dataTransfer.setData('text/defId', def.id);
      });
      ul.appendChild(btn);
    });

    wrap.appendChild(ul);
    side.appendChild(wrap);
  }
}
