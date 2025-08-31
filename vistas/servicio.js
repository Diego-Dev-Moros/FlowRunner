/* =========================================================================
   Orquestador Low-code - Lógica de UI (con visualización de edges en SVG)
   - Render de funciones como botones arrastrables
   - Drag & Drop al lienzo para crear nodos
   - Selección y edición de propiedades
   - Exportación/Importación de JSON con steps y edges
   - Reconexión automática de edges al eliminar nodos
   - Visualización de conexiones (SVG con flechas)
   - Anclajes inteligentes: izquierda/derecha y arriba/abajo
   - Categorías dinámicas en la barra lateral (incluye Lectura/Escritura)
   - Hooks a Eel (Python)
   ========================================================================= */

(() => {
  // Config opcional
  const AUTOCONNECT_NEW_NODES = true;

  // Colores (coinciden con estilos PwC)
  const COLOR_EDGE = '#FF6600'; // naranja PwC
  const COLOR_EDGE_HALO = 'rgba(255,102,0,0.12)';

  // Títulos por categoría (para crear secciones dinámicas en la barra)
  const CAT_TITLES = {
    inicio: 'Acciones de Inicio',
    proceso: 'Acciones de Proceso',
    cierre: 'Acciones de Cierre',
    basicas: 'Funciones Básicas',
    lectura: 'Acciones de Lectura',
    escritura: 'Acciones de Escritura'
  };

  // ---------------------------
  // Catálogo de funciones (metadatos)
  // ---------------------------
  const FUNCTION_CATALOG = [
    // Acciones de Inicio
    {
      id: 'abrir_pagina',
      nombre: 'Abrir página web',
      categoria: 'inicio',
      descripcion: 'Abre una URL en el navegador predeterminado.',
      schema: [{ key: 'url', label: 'URL', type: 'url', required: true, placeholder: 'https://...' }]
    },
    {
      id: 'cambiar_pagina',
      nombre: 'Cambiar página web',
      categoria: 'inicio',
      descripcion: 'Navega a otra URL en la pestaña activa.',
      schema: [{ key: 'url', label: 'Nueva URL', type: 'url', required: true, placeholder: 'https://...' }]
    },
    {
      id: 'abrir_documento',
      nombre: 'Abrir documento',
      categoria: 'inicio',
      descripcion: 'Abre un archivo local (doc, txt, pdf).',
      schema: [{ key: 'ruta', label: 'Ruta del archivo', type: 'text', required: true, placeholder: 'C:\\ruta\\archivo.pdf' }]
    },
    {
      id: 'iniciar_app',
      nombre: 'Iniciar aplicación',
      categoria: 'inicio',
      descripcion: 'Ejecuta una aplicación (se puede seleccionar con diálogo).',
      schema: [
        { key: 'ejecutable', label: 'Ruta ejecutable', type: 'text', required: true, placeholder: 'C:\\Program Files\\app\\app.exe' },
        { key: 'args', label: 'Argumentos (opcional)', type: 'text', required: false, placeholder: '--modo=seguro' }
      ]
    },

    // Acciones de Proceso
    {
      id: 'maximizar_app',
      nombre: 'Maximizar aplicación',
      categoria: 'proceso',
      descripcion: 'Maximiza la ventana de la aplicación objetivo.',
      schema: [{ key: 'titulo', label: 'Título de ventana (opcional)', type: 'text', required: false, placeholder: 'Nombre de la ventana' }]
    },
    {
      id: 'hacer_clic',
      nombre: 'Hacer clic',
      categoria: 'proceso',
      descripcion: 'Realiza un clic en un punto o elemento.',
      schema: [
        { key: 'selector', label: 'Selector/Elemento (opcional)', type: 'text', required: false, placeholder: '#btnEnviar / XPath / texto' },
        { key: 'x', label: 'X (px)', type: 'number', required: false, placeholder: '100' },
        { key: 'y', label: 'Y (px)', type: 'number', required: false, placeholder: '200' },
        { key: 'tipo', label: 'Tipo', type: 'select', required: true, options: ['izquierdo','derecho','doble'] }
      ]
    },
    {
      id: 'escribir_texto',
      nombre: 'Escribir texto / Teclas',
      categoria: 'proceso',
      descripcion: 'Escribe texto o envía combinación de teclas.',
      schema: [
        { key: 'modo', label: 'Modo', type: 'select', required: true, options: ['texto','hotkeys'] },
        { key: 'contenido', label: 'Texto o Hotkeys', type: 'text', required: true, placeholder: 'Hola mundo / CTRL+V' }
      ]
    },
    {
      id: 'copiar_pegar',
      nombre: 'Copiar y pegar',
      categoria: 'proceso',
      descripcion: 'Copia y pega entre aplicaciones.',
      schema: [
        { key: 'origen', label: 'Origen (selector/ventana)', type: 'text', required: false },
        { key: 'destino', label: 'Destino (selector/ventana)', type: 'text', required: false }
      ]
    },
    {
      id: 'ordenar_info',
      nombre: 'Ordenar información',
      categoria: 'proceso',
      descripcion: 'Ordena datos según criterio.',
      schema: [
        { key: 'criterio', label: 'Criterio', type: 'select', required: true, options: ['asc','desc','alfabético','numérico'] },
        { key: 'columna', label: 'Columna/Campo', type: 'text', required: false }
      ]
    },

    // Acciones de Cierre
    {
      id: 'cerrar_navegador',
      nombre: 'Cerrar navegador',
      categoria: 'cierre',
      descripcion: 'Cierra el navegador o una URL específica.',
      schema: [{ key: 'url', label: 'URL específica (opcional)', type: 'url', required: false }]
    },
    {
      id: 'cerrar_documento',
      nombre: 'Cerrar documento',
      categoria: 'cierre',
      descripcion: 'Cierra el archivo en uso.',
      schema: [{ key: 'forzar', label: 'Forzar cierre', type: 'select', required: true, options: ['no','sí'] }]
    },
    {
      id: 'cerrar_app',
      nombre: 'Cerrar aplicación',
      categoria: 'cierre',
      descripcion: 'Cierra la aplicación objetivo.',
      schema: [{ key: 'titulo', label: 'Título de ventana (opcional)', type: 'text', required: false }]
    },

    // Funciones Básicas
    { id: 'exportar_json', nombre: 'Exportar flujo (JSON/XML)', categoria: 'basicas', descripcion: 'Exporta el flujo actual.', schema: [] },
    { id: 'ejecutar_flujo', nombre: 'Ejecutar flujo', categoria: 'basicas', descripcion: 'Ejecuta el JSON generado.', schema: [] },
    { id: 'finalizar_todo', nombre: 'Finalizar (cerrar todo)', categoria: 'basicas', descripcion: 'Finaliza y limpia recursos.', schema: [] },

    // === NUEVAS: Acciones de Lectura ===
    {
      id: 'leer_csv',
      nombre: 'Leer CSV',
      categoria: 'lectura',
      descripcion: 'Lee un archivo CSV.',
      schema: [
        { key: 'ruta', label: 'Ruta del CSV', type: 'text', required: true, placeholder: 'C:\\ruta\\datos.csv' }
      ]
    },
    {
      id: 'leer_excel',
      nombre: 'Leer Excel',
      categoria: 'lectura',
      descripcion: 'Lee un archivo Excel.',
      schema: [
        { key: 'ruta', label: 'Ruta del Excel', type: 'text', required: true, placeholder: 'C:\\ruta\\datos.xlsx' },
        { key: 'hoja', label: 'Nombre de la hoja', type: 'text', required: true, placeholder: 'Hoja1' }
      ]
    },
    {
      id: 'leer_txt',
      nombre: 'Leer TXT',
      categoria: 'lectura',
      descripcion: 'Lee un archivo de texto con delimitador.',
      schema: [
        { key: 'ruta', label: 'Ruta del TXT', type: 'text', required: true, placeholder: 'C:\\ruta\\datos.txt' },
        { key: 'delimitador', label: 'Delimitador', type: 'text', required: true, placeholder: ', ; - | \\t' }
      ]
    },

    // === NUEVAS: Acciones de Escritura ===
    {
      id: 'escribir_csv',
      nombre: 'Escribir CSV',
      categoria: 'escritura',
      descripcion: 'Escribe un array/variable a CSV.',
      schema: [
        { key: 'variable', label: 'Variable/Array', type: 'text', required: true, placeholder: 'mi_array' },
        { key: 'ruta', label: 'Ruta de salida', type: 'text', required: true, placeholder: 'C:\\ruta\\salida.csv' }
      ]
    },
    {
      id: 'escribir_excel',
      nombre: 'Escribir Excel',
      categoria: 'escritura',
      descripcion: 'Escribe un array/variable a Excel.',
      schema: [
        { key: 'variable', label: 'Variable/Array', type: 'text', required: true, placeholder: 'mi_array' },
        { key: 'ruta', label: 'Ruta de salida', type: 'text', required: true, placeholder: 'C:\\ruta\\salida.xlsx' }
      ]
    },
    {
      id: 'escribir_txt',
      nombre: 'Escribir TXT',
      categoria: 'escritura',
      descripcion: 'Escribe un array/variable a TXT con delimitador.',
      schema: [
        { key: 'variable', label: 'Variable/Array', type: 'text', required: true, placeholder: 'mi_array' },
        { key: 'ruta', label: 'Ruta de salida', type: 'text', required: true, placeholder: 'C:\\ruta\\salida.txt' },
        { key: 'delimitador', label: 'Delimitador', type: 'text', required: true, placeholder: ', ; - | \\t' }
      ]
    }
  ];

  // ---------------------------
  // Estado del lienzo
  // ---------------------------
  const state = {
    nodes: [],         // {id, typeId, nombre, x, y, props:{}}
    edges: [],         // [{from:'N1', to:'N2'}]
    selectedId: null,  // id del nodo seleccionado
    counter: 1,
    lastCreatedId: null,
    bulkDeleting: false
  };

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  const els = {
    lists: {
      inicio: $('#listInicio'),
      proceso: $('#listProceso'),
      cierre: $('#listCierre'),
      basicas: $('#listBasicas'),
    },
    sidebar: $('.sidebar'),
    search: $('#searchFuncs'),
    canvas: $('#canvas'),
    propsForm: $('#propsForm'),
    selectionInfo: $('#selectionInfo'),
    hint: $('.canvas-hint'),
    btnExport: $('#btnExport'),
    btnRun: $('#btnRun'),
    btnCancel: $('#btnCancel'),
    btnPause: $('#btnPause'),
    btnClear: $('#btnClear'),
  };

  // ---------------------------
  // Capa SVG para edges
  // ---------------------------
  let svgEdges = null;

  function ensureEdgesLayer() {
    if (svgEdges && svgEdges.parentNode === els.canvas) return;
    svgEdges = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svgEdges.classList.add('edges-layer');
    Object.assign(svgEdges.style, {
      position: 'absolute',
      left: '0',
      top: '0',
      overflow: 'visible',
      pointerEvents: 'none',
      zIndex: '0'
    });

    // Marker (flecha)
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
    marker.setAttribute('id', 'arrowhead');
    marker.setAttribute('orient', 'auto');
    marker.setAttribute('markerWidth', '10');
    marker.setAttribute('markerHeight', '7');
    marker.setAttribute('refX', '10');
    marker.setAttribute('refY', '3.5');

    const arrowPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    arrowPath.setAttribute('d', 'M 0 0 L 10 3.5 L 0 7 z');
    arrowPath.setAttribute('fill', COLOR_EDGE);
    marker.appendChild(arrowPath);
    defs.appendChild(marker);

    svgEdges.appendChild(defs);

    const gHalo = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    gHalo.setAttribute('id', 'edges-halo');
    svgEdges.appendChild(gHalo);

    const gLines = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    gLines.setAttribute('id', 'edges-lines');
    svgEdges.appendChild(gLines);

    els.canvas.insertBefore(svgEdges, els.canvas.firstChild);
    resizeEdgesLayer();
  }

  function resizeEdgesLayer() {
    if (!svgEdges) return;
    let maxRight = els.canvas.clientWidth;
    let maxBottom = els.canvas.clientHeight;

    state.nodes.forEach(n => {
      const el = document.getElementById(n.id);
      if (!el) return;
      const right = el.offsetLeft + el.offsetWidth;
      const bottom = el.offsetTop + el.offsetHeight;
      if (right > maxRight) maxRight = right;
      if (bottom > maxBottom) maxBottom = bottom;
    });

    const margin = 200;
    const w = Math.max(maxRight + margin, els.canvas.clientWidth);
    const h = Math.max(maxBottom + margin, els.canvas.clientHeight);

    svgEdges.setAttribute('width', w);
    svgEdges.setAttribute('height', h);
    svgEdges.setAttribute('viewBox', `0 0 ${w} ${h}`);
  }

  function getNodeBox(id) {
    const el = document.getElementById(id);
    if (!el) return null;
    const x = el.offsetLeft;
    const y = el.offsetTop;
    const w = el.offsetWidth;
    const h = el.offsetHeight;
    return {
      x, y, w, h,
      cx: x + w / 2,
      cy: y + h / 2,
      left: { x: x, y: y + h / 2 },
      right: { x: x + w, y: y + h / 2 },
      top: { x: x + w / 2, y: y },
      bottom: { x: x + w / 2, y: y + h }
    };
  }

  // ==== NUEVO: ruteo con posibles anclajes horizontal (L/R) o vertical (T/B) ====
  function routeBetween(a, b) {
    // Elegimos orientación por el mayor componente de distancia
    const dx = b.cx - a.cx;
    const dy = b.cy - a.cy;

    // Factor de curvatura según distancia
    const dist = Math.hypot(dx, dy);
    const k = Math.max(40, dist * 0.25);

    let start, end, c1, c2;

    if (Math.abs(dx) >= Math.abs(dy)) {
      // Preferencia horizontal
      if (dx >= 0) {
        start = a.right; // sale por derecha de A
        end = b.left;    // entra por izquierda de B
        c1 = { x: start.x + k, y: start.y };
        c2 = { x: end.x - k, y: end.y };
      } else {
        start = a.left;  // sale por izquierda de A
        end = b.right;   // entra por derecha de B
        c1 = { x: start.x - k, y: start.y };
        c2 = { x: end.x + k, y: end.y };
      }
    } else {
      // Preferencia vertical
      if (dy >= 0) {
        start = a.bottom; // sale por abajo de A
        end = b.top;      // entra por arriba de B
        c1 = { x: start.x, y: start.y + k };
        c2 = { x: end.x, y: end.y - k };
      } else {
        start = a.top;    // sale por arriba de A
        end = b.bottom;   // entra por abajo de B
        c1 = { x: start.x, y: start.y - k };
        c2 = { x: end.x, y: end.y + k };
      }
    }

    return {
      d: `M ${start.x} ${start.y} C ${c1.x} ${c1.y}, ${c2.x} ${c2.y}, ${end.x} ${end.y}`
    };
  }

  function renderEdges() {
    ensureEdgesLayer();
    resizeEdgesLayer();
    if (!svgEdges) return;

    const gHalo = svgEdges.querySelector('#edges-halo');
    const gLines = svgEdges.querySelector('#edges-lines');
    gHalo.innerHTML = '';
    gLines.innerHTML = '';

    state.edges.forEach(e => {
      const fromBox = getNodeBox(e.from);
      const toBox = getNodeBox(e.to);
      if (!fromBox || !toBox) return;

      const { d } = routeBetween(fromBox, toBox);

      // Halo suave
      const halo = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      halo.setAttribute('d', d);
      halo.setAttribute('fill', 'none');
      halo.setAttribute('stroke', COLOR_EDGE_HALO);
      halo.setAttribute('stroke-width', '10');
      halo.setAttribute('stroke-linecap', 'round');
      halo.setAttribute('stroke-linejoin', 'round');
      gHalo.appendChild(halo);

      // Línea con flecha
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', d);
      path.setAttribute('fill', 'none');
      path.setAttribute('stroke', COLOR_EDGE);
      path.setAttribute('stroke-width', '2.5');
      path.setAttribute('stroke-linecap', 'round');
      path.setAttribute('stroke-linejoin', 'round');
      path.setAttribute('marker-end', 'url(#arrowhead)');
      gLines.appendChild(path);
    });
  }

  // ---------------------------
  // Helpers de aristas (edges)
  // ---------------------------
  function hasEdge(from, to) {
    return state.edges.some(e => e.from === from && e.to === to);
  }

  function addEdge(from, to) {
    if (!from || !to || from === to) return;
    if (!state.nodes.find(n => n.id === from)) return;
    if (!state.nodes.find(n => n.id === to)) return;
    if (hasEdge(from, to)) return;
    state.edges.push({ from, to });
    renderEdges();
  }

  function removeEdgesTouching(nodeId) {
    const prevLen = state.edges.length;
    state.edges = state.edges.filter(e => e.from !== nodeId && e.to !== nodeId);
    if (state.edges.length !== prevLen) renderEdges();
  }

  function predecessors(nodeId) {
    return state.edges.filter(e => e.to === nodeId).map(e => e.from);
  }

  function successors(nodeId) {
    return state.edges.filter(e => e.from === nodeId).map(e => e.to);
  }

  function rewireOnDelete(nodeId) {
    const preds = predecessors(nodeId);
    const succs = successors(nodeId);

    // Quitar aristas del nodo a eliminar
    state.edges = state.edges.filter(e => e.from !== nodeId && e.to !== nodeId);

    if (preds.length && succs.length) {
      if (preds.length === 1 && succs.length === 1) {
        if (preds[0] !== succs[0]) state.edges.push({ from: preds[0], to: succs[0] });
      } else {
        // Emparejar por posición Y
        const byY = id => (state.nodes.find(n => n.id === id)?.y ?? 0);
        const spreds = [...preds].sort((a,b) => byY(a) - byY(b));
        const ssuccs = [...succs].sort((a,b) => byY(a) - byY(b));
        const len = Math.min(spreds.length, ssuccs.length);
        for (let i = 0; i < len; i++) {
          if (spreds[i] !== ssuccs[i]) state.edges.push({ from: spreds[i], to: ssuccs[i] });
        }
      }
    }

    renderEdges();
  }

  // ---------------------------
  // Render de botones de funciones (categorías dinámicas)
  // ---------------------------
  function titleCase(s) {
    return (s || '').toString().replace(/[_-]+/g, ' ').replace(/\w\S*/g, t => t.charAt(0).toUpperCase() + t.slice(1));
  }

  function ensureCategoryContainer(categoria) {
    // Si ya existe (predefinido en HTML) o fue creado, retornarlo
    if (els.lists[categoria]) return els.lists[categoria];

    // Crear sección dinámica
    const section = document.createElement('section');
    section.className = 'func-group';

    const h3 = document.createElement('h3');
    h3.textContent = CAT_TITLES[categoria] || titleCase(categoria);
    section.appendChild(h3);

    const list = document.createElement('div');
    list.className = 'func-list';
    list.id = `list_${categoria}`;
    section.appendChild(list);

    // Insertar al final de la barra lateral
    els.sidebar.appendChild(section);

    // Registrar en el map para futuros renders
    els.lists[categoria] = list;
    return list;
  }

  function renderFunctionButtons(filter = '') {
    const q = filter.trim().toLowerCase();

    // Limpiar todas las listas conocidas
    Object.values(els.lists).forEach(g => { if (g) g.innerHTML = ''; });

    FUNCTION_CATALOG.forEach(fn => {
      const matches = !q || fn.nombre.toLowerCase().includes(q) || fn.descripcion.toLowerCase().includes(q);
      if (!matches) return;

      // Asegurar contenedor de categoría (dinámico si hace falta)
      const container = ensureCategoryContainer(fn.categoria);
      if (!container) return;

      const btn = document.createElement('button');
      btn.className = 'func-btn';
      btn.textContent = fn.nombre;
      btn.setAttribute('draggable', 'true');
      btn.dataset.typeId = fn.id;

      btn.addEventListener('dragstart', (ev) => {
        ev.dataTransfer.setData('text/plain', fn.id);
      });

      container.appendChild(btn);
    });
  }

  // ---------------------------
  // Lienzo: Drag & Drop para crear nodos
  // ---------------------------
  function setupCanvasDnD() {
    els.canvas.addEventListener('dragover', (ev) => {
      ev.preventDefault();
      els.canvas.classList.add('dragging');
    });
    els.canvas.addEventListener('dragleave', () => {
      els.canvas.classList.remove('dragging');
    });
    els.canvas.addEventListener('drop', (ev) => {
      ev.preventDefault();
      els.canvas.classList.remove('dragging');

      const typeId = ev.dataTransfer.getData('text/plain');
      if (!typeId) return;

      const rect = els.canvas.getBoundingClientRect();
      const x = ev.clientX - rect.left + els.canvas.scrollLeft;
      const y = ev.clientY - rect.top + els.canvas.scrollTop;

      addNode(typeId, x, y);
    });

    // Ajustes al scroll (SVG puede necesitar crecer)
    els.canvas.addEventListener('scroll', () => {
      resizeEdgesLayer();
      renderEdges();
    });
  }

  function addNode(typeId, x, y) {
    const meta = FUNCTION_CATALOG.find(f => f.id === typeId);
    if (!meta) return;
    const id = `N${state.counter++}`;

    const node = {
      id,
      typeId,
      nombre: meta.nombre,
      x: Math.max(16, x - 100),
      y: Math.max(16, y - 20),
      props: defaultPropsFromSchema(meta.schema)
    };
    state.nodes.push(node);

    // Auto-encadenado: último creado → este nuevo
    if (AUTOCONNECT_NEW_NODES && state.lastCreatedId && state.lastCreatedId !== id) {
      addEdge(state.lastCreatedId, id);
    }
    state.lastCreatedId = id;

    renderNode(node);
    updateHint();
    selectNode(id);
    renderEdges();
  }

  function defaultPropsFromSchema(schema) {
    const out = {};
    (schema || []).forEach(f => {
      if (f.type === 'select' && Array.isArray(f.options) && f.options.length) {
        out[f.key] = f.options[0];
      } else {
        out[f.key] = '';
      }
    });
    return out;
  }

  function renderNode(node) {
    // Crear elemento base si no existe
    let el = document.getElementById(node.id);
    if (!el) {
      el = document.createElement('div');
      el.className = 'node';
      el.id = node.id;

      const header = document.createElement('div');
      header.className = 'node-header';
      header.innerHTML = `
        <span class="node-type">${node.nombre}</span>
        <span class="badge">ID: ${node.id}</span>
      `;

      const body = document.createElement('div');
      body.className = 'node-body';
      body.innerHTML = `<div>${describeNode(node)}</div>`;

      el.appendChild(header);
      el.appendChild(body);
      els.canvas.appendChild(el);

      // Selección
      el.addEventListener('mousedown', (e) => {
        if (!e.target.closest('.node-header') && !e.target.closest('.node-body')) return;
        selectNode(node.id);
      });

      // Drag interno (mover dentro del lienzo)
      enableNodeMove(el, node);
    }

    el.style.left = `${node.x}px`;
    el.style.top = `${node.y}px`;

    // actualizar resumen
    const body = el.querySelector('.node-body > div');
    if (body) body.textContent = describeNode(node);

    // estilo de selección
    el.classList.toggle('selected', state.selectedId === node.id);

    // Ajustar capa de edges (por si el nodo expandió límites)
    resizeEdgesLayer();
  }

  function describeNode(node) {
    const meta = FUNCTION_CATALOG.find(f => f.id === node.typeId);
    if (!meta) return '';
    const keys = Object.keys(node.props || {});
    if (!keys.length) return meta.descripcion || '';
    const preview = keys
      .filter(k => node.props[k] !== '')
      .slice(0, 3)
      .map(k => `${k}: ${node.props[k]}`)
      .join(' | ');
    return preview || meta.descripcion || '';
  }

  function enableNodeMove(el, node) {
    const header = el.querySelector('.node-header');
    let dragging = false;
    let startX = 0, startY = 0, baseX = 0, baseY = 0;

    header.addEventListener('mousedown', (e) => {
      dragging = true;
      startX = e.clientX;
      startY = e.clientY;
      baseX = node.x;
      baseY = node.y;
      document.body.style.userSelect = 'none';
      e.preventDefault();
    });

    window.addEventListener('mousemove', (e) => {
      if (!dragging) return;
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      node.x = Math.max(8, baseX + dx);
      node.y = Math.max(8, baseY + dy);
      renderNode(node);
      renderEdges(); // actualizar líneas mientras se arrastra
    });

    window.addEventListener('mouseup', () => {
      if (!dragging) return;
      dragging = false;
      document.body.style.userSelect = '';
      renderEdges(); // ajuste final
    });
  }

  function updateHint() {
    els.hint.style.display = state.nodes.length ? 'none' : 'flex';
  }

  // ---------------------------
  // Selección y panel de propiedades
  // ---------------------------
  function selectNode(id) {
    state.selectedId = id;
    state.nodes.forEach(n => {
      const el = document.getElementById(n.id);
      if (el) el.classList.toggle('selected', n.id === id);
    });
    renderProps();
  }

  function renderProps() {
    const node = state.nodes.find(n => n.id === state.selectedId);
    els.propsForm.innerHTML = '';
    if (!node) {
      els.selectionInfo.textContent = 'Ningún nodo seleccionado';
      return;
    }

    const meta = FUNCTION_CATALOG.find(f => f.id === node.typeId);
    els.selectionInfo.textContent = `${node.nombre} — ${node.id}`;

    // Campos dinámicos
    (meta.schema || []).forEach(field => {
      const row = document.createElement('div');
      row.className = 'form-row';

      const label = document.createElement('label');
      label.textContent = field.label + (field.required ? ' *' : '');
      label.htmlFor = `${node.id}_${field.key}`;

      let input;
      if (field.type === 'select') {
        input = document.createElement('select');
        (field.options || []).forEach(opt => {
          const o = document.createElement('option');
          o.value = opt; o.textContent = opt;
          input.appendChild(o);
        });
      } else if (field.type === 'textarea') {
        input = document.createElement('textarea');
      } else {
        input = document.createElement('input');
        input.type = field.type || 'text';
        if (field.placeholder) input.placeholder = field.placeholder;
      }
      input.id = `${node.id}_${field.key}`;
      input.value = node.props[field.key] ?? '';

      input.addEventListener('input', () => {
        node.props[field.key] = input.value;
        renderNode(node); // refresh resumen
        renderEdges();     // por si el tamaño cambió
      });

      row.appendChild(label);
      row.appendChild(input);

      if (field.required) {
        const help = document.createElement('div');
        help.className = 'form-help';
        help.textContent = 'Campo requerido';
        row.appendChild(help);
      }

      els.propsForm.appendChild(row);
    });

    // Posición (sólo lectura)
    const posRow = document.createElement('div');
    posRow.className = 'form-row';
    posRow.innerHTML = `
      <label>Posición</label>
      <div class="form-help">x: ${Math.round(node.x)} px, y: ${Math.round(node.y)} px</div>
    `;
    els.propsForm.appendChild(posRow);

    // Eliminar nodo
    const delRow = document.createElement('div');
    delRow.className = 'form-row';
    const delBtn = document.createElement('button');
    delBtn.type = 'button';
    delBtn.className = 'btn btn-danger';
    delBtn.textContent = 'Eliminar este nodo';
    delBtn.addEventListener('click', () => {
      deleteNode(node.id); // con rewire y re-render de edges
    });
    delRow.appendChild(delBtn);
    els.propsForm.appendChild(delRow);
  }

  function deleteNode(id, { rewire = true } = {}) {
    const idx = state.nodes.findIndex(n => n.id === id);
    if (idx >= 0) {
      // 1) Reconectar edges antes de borrar el nodo (salvo borrado masivo)
      if (rewire && !state.bulkDeleting) {
        rewireOnDelete(id);
      } else {
        // Si no rewire, sólo removemos edges tocando el nodo
        removeEdgesTouching(id);
      }

      // 2) elimina el DOM del nodo
      const el = document.getElementById(id);
      if (el && el.parentNode) el.parentNode.removeChild(el);

      // 3) quita el nodo del estado
      state.nodes.splice(idx, 1);

      // actualizar lastCreatedId si era éste
      if (state.lastCreatedId === id) {
        state.lastCreatedId = state.nodes.length ? state.nodes[state.nodes.length - 1].id : null;
      }

      // 4) limpiar selección y UI
      if (!state.bulkDeleting) {
        state.selectedId = null;
        renderProps();
        updateHint();
      }

      // 5) redibujar edges
      renderEdges();
    }
  }

  // Deseleccionar al hacer clic en fondo
  els.canvas.addEventListener('mousedown', (e) => {
    if (e.target === els.canvas || e.target.classList.contains('canvas-hint')) {
      state.selectedId = null;
      renderProps();
      state.nodes.forEach(n => {
        const el = document.getElementById(n.id);
        if (el) el.classList.remove('selected');
      });
    }
  });

  // ---------------------------
  // Exportar / Ejecutar / Limpiar / Cancelar / Pausar
  // ---------------------------
  function buildFlowJSON() {
    const sequence = [...state.nodes].sort((a, b) => (a.y - b.y) || (a.x - b.x));
    const steps = sequence.map(n => ({
      id: n.id,
      typeId: n.typeId,
      nombre: n.nombre,
      position: { x: Math.round(n.x), y: Math.round(n.y) },
      props: n.props
    }));

    let edges = state.edges.slice();
    if (!edges.length && steps.length > 1) {
      edges = steps.slice(0, -1).map((s, i) => ({ from: s.id, to: steps[i + 1].id }));
    }

    return {
      version: '1.0.0',
      generatedAt: new Date().toISOString(),
      steps,
      edges
    };
  }

  function downloadJSON(data, filename = 'flujo.json') {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  els.btnExport.addEventListener('click', async () => {
    const flow = buildFlowJSON();
    downloadJSON(flow);
    if (window.eel && typeof window.eel.export_flow === 'function') {
      try { await window.eel.export_flow(flow)(); } catch (e) { console.warn('export_flow error:', e); }
    }
  });

  els.btnRun.addEventListener('click', async () => {
    const flow = buildFlowJSON();
    if (window.eel && typeof window.eel.run_flow === 'function') {
      try {
        els.btnRun.disabled = true;
        const result = await window.eel.run_flow(flow)(); // 👈 Capturamos la respuesta
        console.log('Resultado del flujo:', result);

        if (result.ok) {
          alert(`✅ Flujo completado.\nVariables creadas: ${result.variables.join(', ')}`);
        } else {
          alert(`❌ Error: ${result.error}\nRevisá la consola para más detalles.`);
          console.error(result.traceback);
        }
      } catch (e) {
        console.error('run_flow error:', e);
        alert('Ocurrió un error al ejecutar el flujo.');
      } finally {
        els.btnRun.disabled = false;
      }
    } else {
      console.log('RUN (simulado):', flow);
      try {
        els.btnRun.disabled = true;
        const result = await window.eel.run_flow(flow)(); // 👈 Capturamos la respuesta
        console.log('Resultado del flujo:', result);

        if (result.ok) {
          alert(`✅ Flujo completado.\nVariables creadas: ${result.variables.join(', ')}`);
        } else {
          alert(`❌ Error: ${result.error}\nRevisá la consola para más detalles.`);
          console.error(result.traceback);
        }
      } catch (e) {
        console.error('run_flow error:', e);
        alert('Ocurrió un error al ejecutar el flujo.');
      } finally {
        els.btnRun.disabled = false;
      }
      alert('Ejecución simulada (conectá Eel.run_flow en Python).');
    }
  });

  els.btnCancel.addEventListener('click', async () => {
    if (window.eel && typeof window.eel.cancel_run === 'function') {
      try { await window.eel.cancel_run()(); } catch (e) { console.warn('cancel_run error:', e); }
    } else {
      alert('Cancelar: pendiente de conectar con Python (eel.cancel_run).');
    }
  });

  els.btnPause.addEventListener('click', async () => {
    if (window.eel && typeof window.eel.pause_run === 'function') {
      try { await window.eel.pause_run()(); } catch (e) { console.warn('pause_run error:', e); }
    } else {
      alert('Pausar: pendiente de definición e integración (eel.pause_run).');
    }
  });

  els.btnClear.addEventListener('click', () => {
    if (!confirm('¿Borrar todos los nodos del lienzo?')) return;

    state.bulkDeleting = true;
    const ids = state.nodes.map(n => n.id);
    state.edges = [];
    renderEdges();
    ids.forEach(id => deleteNode(id, { rewire: false }));
    state.bulkDeleting = false;

    state.counter = 1;
    state.selectedId = null;
    state.lastCreatedId = null;
    renderProps();
    updateHint();
  });

  // ---------------------------
  // Búsqueda de funciones
  // ---------------------------
  els.search.addEventListener('input', (e) => {
    renderFunctionButtons(e.target.value);
  });

  // ---------------------------
  // Eel -> JS (exponer si se requiere actualizar UI desde Python)
  // ---------------------------
  if (window.eel && typeof window.eel.expose === 'function') {
    window.eel.expose(loadFlowFromPython, 'load_flow');
    window.eel.expose(notifyRunProgress, 'notify_progress');
  }

  function loadFlowFromPython(flow) {
    // Limpiar lienzo (sin reconectar)
    els.btnClear.click();

    const steps = (flow && Array.isArray(flow.steps)) ? flow.steps : [];
    steps.forEach(step => {
      const meta = FUNCTION_CATALOG.find(f => f.id === step.typeId);
      if (!meta) return;
      const id = step.id || `N${state.counter++}`;
      const node = {
        id,
        typeId: step.typeId,
        nombre: step.nombre || meta.nombre,
        x: step.position?.x ?? 40,
        y: step.position?.y ?? 40,
        props: Object.assign(defaultPropsFromSchema(meta.schema), step.props || {})
      };
      state.nodes.push(node);
      renderNode(node);
      state.lastCreatedId = id;
    });

    const incomingEdges = Array.isArray(flow?.edges) ? flow.edges : [];
    state.edges = incomingEdges
      .filter(e => e && e.from && e.to)
      .filter(e => state.nodes.find(n => n.id === e.from) && state.nodes.find(n => n.id === e.to));

    renderEdges();
    updateHint();
    state.selectedId = null;
    renderProps();
  }

  function notifyRunProgress(payload) {
    console.log('Progreso:', payload);
    if (payload?.stepId) {
      const el = document.getElementById(payload.stepId);
      if (el) {
        el.animate(
          [
            { boxShadow: '0 0 0 0 rgba(255,102,0,0)' },
            { boxShadow: '0 0 0 6px rgba(255,102,0,.35)' },
            { boxShadow: '0 0 0 0 rgba(255,102,0,0)' }
          ],
          { duration: 550, iterations: 1, easing: 'ease-out' }
        );
      }
    }
  }

  // ---------------------------
  // Init
  // ---------------------------
  renderFunctionButtons();
  setupCanvasDnD();
  ensureEdgesLayer();
  updateHint();
  renderEdges();

  window.addEventListener('resize', () => {
    resizeEdgesLayer();
    renderEdges();
  });

})();