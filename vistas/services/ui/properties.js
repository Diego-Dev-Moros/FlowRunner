// vistas/services/ui/properties.js
import { state } from '../state.js';

export function renderPropsPanel(step, def, { onChange } = {}) {
  const root = document.getElementById('props');
  root.innerHTML = '';

  if (!step || !def) {
    root.innerHTML = '<div class="props-empty">Selecciona un nodo para editar sus propiedades.</div>';
    return;
  }

  const h = document.createElement('h3');
  h.textContent = `Propiedades: ${step.label}`;
  root.appendChild(h);

  // Descripción de la función (si existe)
  if (def.descripcion) {
    const desc = document.createElement('div');
    desc.className = 'form-help';
    desc.style.margin = '-4px 0 8px';
    desc.style.color = '#666';
    desc.textContent = def.descripcion;
    root.appendChild(desc);
  }

  // Campos dinámicos
  (def.schema || []).forEach(field => {
    const g = document.createElement('div');
    g.className = 'props-group';

    const lab = document.createElement('label');
    lab.textContent = field.label + (field.required ? ' *' : '');
    g.appendChild(lab);

    let input;
    if (field.type === 'select') {
      input = document.createElement('select');
      (field.options || []).forEach(opt => {
        const o = document.createElement('option'); o.value = opt; o.textContent = opt;
        input.appendChild(o);
      });
    } else if (field.type === 'textarea') {
      input = document.createElement('textarea');
    } else {
      input = document.createElement('input');
      input.type = field.type || 'text';
      if (field.placeholder) input.placeholder = field.placeholder;
    }

    input.value = step.props?.[field.key] ?? '';
    input.addEventListener('input', () => {
      step.props[field.key] = input.value;
      onChange?.(step, field.key, input.value);
    });

    g.appendChild(input);
    root.appendChild(g);
  });

  // Resultado / Estado
  const res = state.results[step.id];
  const rg = document.createElement('div');
  rg.className = 'props-group';
  const lbl = document.createElement('label');
  lbl.textContent = 'Resultado';
  rg.appendChild(lbl);

  const pre = document.createElement('pre');
  pre.style.maxHeight = '240px';
  pre.style.overflow = 'auto';
  pre.style.background = '#f8f8f8';
  pre.style.border = '1px solid #e5e5e5';
  pre.style.borderRadius = '8px';
  pre.style.padding = '8px';
  pre.textContent = res?.preview || '(sin resultado aún)';
  rg.appendChild(pre);

  const status = document.createElement('div');
  status.className = 'form-help';
  status.textContent = res ? `[${res.status}] ${res.message || ''}` : '[S/I] sin ejecutar';
  rg.appendChild(status);

  root.appendChild(rg);
}
