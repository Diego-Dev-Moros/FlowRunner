// /vistas/services/ui/properties.js
export function renderPropsPanel(step, def, { onChange } = {}) {
  const root = document.getElementById('props');
  root.innerHTML = '';
  if (!step || !def) {
    root.innerHTML = `<div class="props-empty">Selecciona un nodo para editar sus propiedades.</div>`;
    return;
  }

  const title = document.createElement('h3');
  title.textContent = `Propiedades: ${step.label}`;
  root.appendChild(title);

  (def.schema || []).forEach(field => {
    const wrap = document.createElement('div');
    wrap.className = 'props-group';

    const lab = document.createElement('label');
    lab.textContent = field.label + (field.required ? ' *' : '');
    wrap.appendChild(lab);

    let input;
    if (field.type === 'select') {
      input = document.createElement('select');
      (field.options || []).forEach(opt => {
        const o = document.createElement('option');
        o.value = opt; o.textContent = opt;
        input.appendChild(o);
      });
    } else {
      input = document.createElement('input');
      input.type = field.type === 'number' ? 'number'
                 : field.type === 'url'    ? 'url'
                 : 'text';
      if (field.placeholder) input.placeholder = field.placeholder;
    }

    // valor actual
    if (step.props && step.props[field.key] != null) {
      input.value = step.props[field.key];
    }

    input.addEventListener('input', () => {
      step.props[field.key] = (field.type === 'number')
        ? (input.value === '' ? '' : Number(input.value))
        : input.value;
      onChange?.(step, field);
    });

    wrap.appendChild(input);
    root.appendChild(wrap);
  });
}
