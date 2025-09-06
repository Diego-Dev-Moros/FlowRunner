// vistas/services/catalog.js
// Catálogo maestro. El filtrado por habilitación lo hace registry/bootstrapFlags
// usando get_enabled_types() del backend.

export const FUNCTION_CATALOG = [
  // =========================
  // 🚀 INICIO & CONFIGURACIÓN
  // =========================
  {
    id: 'abrir_pagina',
    nombre: 'Abrir página web',
    categoria: 'inicio',
    descripcion: 'Abre una URL en el navegador predeterminado.',
    schema: [
      { key: 'url', label: 'URL', type: 'url', required: true, placeholder: 'https://...' }
    ]
  },
  {
    id: 'abrir_documento',
    nombre: 'Abrir documento',
    categoria: 'inicio',
    descripcion: 'Abre un archivo local (doc, txt, pdf).',
    schema: [
      { key: 'ruta', label: 'Ruta del archivo', type: 'text', required: true, placeholder: 'C:\\ruta\\archivo.pdf' }
    ]
  },
  {
    id: 'iniciar_app',
    nombre: 'Iniciar aplicación',
    categoria: 'inicio',
    descripcion: 'Ejecuta una aplicación.',
    schema: [
      { key: 'ejecutable', label: 'Ruta ejecutable', type: 'text', required: true, placeholder: 'C:\\Program Files\\app\\app.exe' },
      { key: 'args',        label: 'Argumentos (opcional)', type: 'text', required: false, placeholder: '--modo=seguro' }
    ]
  },
  {
    id: 'maximizar_app',
    nombre: 'Maximizar aplicación',
    categoria: 'inicio',
    descripcion: 'Maximiza la ventana de la aplicación objetivo.',
    schema: [
      { key: 'titulo', label: 'Título de ventana (opcional)', type: 'text', required: false }
    ]
  },

  // =========================
  // 🌐 NAVEGACIÓN WEB
  // =========================
  {
    id: 'cambiar_pagina',
    nombre: 'Cambiar página web',
    categoria: 'navegacion',
    descripcion: 'Navega a otra URL en la pestaña activa.',
    schema: [
      { key: 'url', label: 'Nueva URL', type: 'url', required: true, placeholder: 'https://...' }
    ]
  },
  {
    id: 'hacer_clic',
    nombre: 'Hacer clic',
    categoria: 'navegacion',
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
    categoria: 'navegacion',
    descripcion: 'Escribe texto o envía combinación de teclas.',
    schema: [
      { key: 'modo', label: 'Modo', type: 'select', required: true, options: ['texto','hotkeys'] },
      { key: 'contenido', label: 'Texto o Hotkeys', type: 'text', required: true, placeholder: 'Hola mundo / CTRL+V' }
    ]
  },
  {
    id: 'copiar_pegar',
    nombre: 'Copiar y pegar',
    categoria: 'navegacion',
    descripcion: 'Copia y pega entre aplicaciones.',
    schema: [
      { key: 'origen', label: 'Origen (selector/ventana)', type: 'text', required: false },
      { key: 'destino', label: 'Destino (selector/ventana)', type: 'text', required: false }
    ]
  },

  // =========================
  // 📖 LEER INFORMACIÓN
  // =========================
  {
    id: 'excel_leer_rango',
    nombre: 'Leer datos de Excel',
    categoria: 'lectura',
    descripcion: 'Lee un rango (A1:D100) o columnas específicas.',
    schema: [
      { key: 'ruta',  label: 'Ruta del Excel', type: 'text', required: true,  placeholder: 'C:\\ruta\\datos.xlsx' },
      { key: 'hoja',  label: 'Hoja',           type: 'text', required: true,  placeholder: 'Hoja1' },
      { key: 'rango', label: 'Rango (A1:D100)', type: 'text', required: true },
      { key: 'nombre_personalizado', label: 'Nombre variable (opcional)', type: 'text', required: false }
    ]
  },
  {
    id: 'carpeta_listar',
    nombre: 'Ver archivos de carpeta',
    categoria: 'lectura',
    descripcion: 'Lista archivos de una carpeta con patrón opcional.',
    schema: [
      { key: 'ruta',   label: 'Ruta de carpeta', type: 'text', required: true },
      { key: 'patron', label: 'Patrón (ej. *.xlsx)', type: 'text', required: false, placeholder: '*.xlsx' },
      { key: 'nombre_personalizado', label: 'Nombre variable (opcional)', type: 'text', required: false }
    ]
  },

  // =========================
  // 📊 PROCESAR DATOS
  // =========================
  {
    id: 'ordenar_info',
    nombre: 'Ordenar información',
    categoria: 'datos',
    descripcion: 'Ordena datos según criterio.',
    schema: [
      { key: 'criterio', label: 'Criterio', type: 'select', required: true, options: ['asc','desc','alfabético','numérico'] },
      { key: 'columna', label: 'Columna/Campo', type: 'text', required: false }
    ]
  },
  {
    id: 'variable_set',
    nombre: 'Crear/Actualizar variable',
    categoria: 'datos',
    descripcion: 'Crea/actualiza una variable del flujo.',
    schema: [
      { key: 'variable', label: 'Nombre variable', type: 'text', required: true,  placeholder: 'mi_var' },
      { key: 'valor',    label: 'Valor (texto)',   type: 'text', required: true,  placeholder: '123 | Hola | true' }
    ]
  },
  {
    id: 'variable_get',
    nombre: 'Usar variable',
    categoria: 'datos',
    descripcion: 'Lee una variable del flujo.',
    schema: [
      { key: 'variable', label: 'Nombre variable', type: 'text', required: true, placeholder: 'mi_var' }
    ]
  },

  // =========================
  // 🔄 CONTROL Y DECISIONES (preparado para futuras funciones)
  // =========================
  {
    id: 'pausa',
    nombre: 'Hacer una pausa',
    categoria: 'logica',
    descripcion: 'Detiene la ejecución por algunos segundos.',
    schema: [
      { key: 'segundos', label: 'Segundos', type: 'number', required: true, placeholder: '1' }
    ]
  },

  // =========================
  // 💾 GUARDAR INFORMACIÓN
  // =========================
  {
    id: 'escribir_csv',
    nombre: 'Guardar como CSV',
    categoria: 'escritura',
    descripcion: 'Escribe una variable a CSV.',
    schema: [
      { key: 'variable', label: 'Variable/Array', type: 'text', required: true, placeholder: 'mi_array' },
      { key: 'ruta',     label: 'Ruta de salida',  type: 'text', required: true, placeholder: 'C:\\ruta\\salida.csv' }
    ]
  },
  {
    id: 'escribir_excel',
    nombre: 'Guardar como Excel',
    categoria: 'escritura',
    descripcion: 'Escribe una variable a Excel.',
    schema: [
      { key: 'variable', label: 'Variable/Array', type: 'text', required: true, placeholder: 'mi_array' },
      { key: 'ruta',     label: 'Ruta de salida',  type: 'text', required: true, placeholder: 'C:\\ruta\\salida.xlsx' }
    ]
  },
  {
    id: 'escribir_txt',
    nombre: 'Guardar como TXT',
    categoria: 'escritura',
    descripcion: 'Escribe una variable a TXT con delimitador.',
    schema: [
      { key: 'variable',    label: 'Variable/Array', type: 'text', required: true, placeholder: 'mi_array' },
      { key: 'ruta',        label: 'Ruta de salida',  type: 'text', required: true, placeholder: 'C:\\ruta\\salida.txt' },
      { key: 'delimitador', label: 'Delimitador',     type: 'text', required: true, placeholder: ', ; - | \\t' }
    ]
  },
  {
    id: 'excel_escribir_rango',
    nombre: 'Actualizar Excel existente',
    categoria: 'escritura',
    descripcion: 'Escribe en un rango o agrega filas al final.',
    schema: [
      { key: 'variable',    label: 'Variable origen', type: 'text', required: true, placeholder: 'mi_array' },
      { key: 'ruta',        label: 'Ruta del Excel',  type: 'text', required: true, placeholder: 'C:\\ruta\\datos.xlsx' },
      { key: 'hoja',        label: 'Hoja',            type: 'text', required: true, placeholder: 'Hoja1' },
      { key: 'modo',        label: 'Modo',            type: 'select', required: true, options: ['sobrescribir','append'] },
      { key: 'inicio_celda',label: 'Inicio celda (ej. A1)', type: 'text', required: false, placeholder: 'A1' }
    ]
  },
  {
    id: 'excel_crear_hoja',
    nombre: 'Crear hoja en Excel',
    categoria: 'escritura',
    descripcion: 'Crea una hoja en un libro existente.',
    schema: [
      { key: 'ruta',        label: 'Ruta del Excel', type: 'text', required: true, placeholder: 'C:\\ruta\\datos.xlsx' },
      { key: 'nombre_hoja', label: 'Nombre de hoja', type: 'text', required: true, placeholder: 'NuevaHoja' },
      { key: 'si_existe',   label: 'Si existe',      type: 'select', required: true, options: ['reemplazar','renombrar','error'] }
    ]
  },

  // =========================
  // 📁 GESTIÓN DE ARCHIVOS
  // =========================
  {
    id: 'archivo_mover',
    nombre: 'Mover archivo',
    categoria: 'archivos',
    descripcion: 'Mueve un archivo de origen a destino.',
    schema: [
      { key: 'origen',   label: 'Origen',   type: 'text', required: true },
      { key: 'destino',  label: 'Destino',  type: 'text', required: true },
      { key: 'si_existe',label: 'Si existe',type: 'select', required: true, options: ['sobrescribir','renombrar','omitir'] }
    ]
  },
  {
    id: 'archivo_copiar',
    nombre: 'Copiar archivo',
    categoria: 'archivos',
    descripcion: 'Copia un archivo a destino.',
    schema: [
      { key: 'origen',   label: 'Origen',   type: 'text', required: true },
      { key: 'destino',  label: 'Destino',  type: 'text', required: true },
      { key: 'si_existe',label: 'Si existe',type: 'select', required: true, options: ['sobrescribir','renombrar','omitir'] }
    ]
  },
  {
    id: 'archivo_borrar',
    nombre: 'Eliminar archivo',
    categoria: 'archivos',
    descripcion: 'Elimina un archivo.',
    schema: [
      { key: 'origen', label: 'Ruta a borrar', type: 'text', required: true }
    ]
  },
  {
    id: 'carpeta_crear',
    nombre: 'Crear carpeta',
    categoria: 'archivos',
    descripcion: 'Crea una carpeta (mkdir -p).',
    schema: [
      { key: 'ruta', label: 'Ruta de carpeta', type: 'text', required: true }
    ]
  },

  // =========================
  // 💬 PREGUNTAR AL USUARIO
  // =========================
  {
    id: 'dialogo_seleccionar_archivo',
    nombre: 'Elegir archivo',
    categoria: 'dialogos',
    descripcion: 'Abre un diálogo para elegir archivo y guarda la ruta.',
    schema: [
      { key: 'filtro',  label: 'Filtro (ej. *.xlsx;*.csv)', type: 'text', required: false },
      { key: 'nombre_personalizado', label: 'Nombre variable (opcional)', type: 'text', required: false }
    ]
  },
  {
    id: 'dialogo_seleccionar_carpeta',
    nombre: 'Elegir carpeta',
    categoria: 'dialogos',
    descripcion: 'Abre un diálogo para elegir carpeta y guarda la ruta.',
    schema: [
      { key: 'nombre_personalizado', label: 'Nombre variable (opcional)', type: 'text', required: false }
    ]
  },

  // =========================
  // ⚙️ HERRAMIENTAS DEL SISTEMA
  // =========================
  {
    id: 'exportar_json',
    nombre: 'Exportar flujo (JSON/XML)',
    categoria: 'sistema',
    descripcion: 'Exporta el flujo actual.',
    schema: []
  },
  {
    id: 'ejecutar_flujo',
    nombre: 'Ejecutar flujo',
    categoria: 'sistema',
    descripcion: 'Ejecuta el JSON generado.',
    schema: []
  },

  // =========================
  // 🏁 FINALIZACIÓN
  // =========================
  {
    id: 'cerrar_navegador',
    nombre: 'Cerrar navegador',
    categoria: 'finalizacion',
    descripcion: 'Cierra el navegador o una URL específica.',
    schema: [
      { key: 'url', label: 'URL específica (opcional)', type: 'url', required: false }
    ]
  },
  {
    id: 'cerrar_documento',
    nombre: 'Cerrar documento',
    categoria: 'finalizacion',
    descripcion: 'Cierra el archivo en uso.',
    schema: [
      { key: 'forzar', label: 'Forzar cierre', type: 'select', required: true, options: ['no','sí'] }
    ]
  },
  {
    id: 'cerrar_app',
    nombre: 'Cerrar aplicación',
    categoria: 'finalizacion',
    descripcion: 'Cierra la aplicación objetivo.',
    schema: [
      { key: 'titulo', label: 'Título de ventana (opcional)', type: 'text', required: false }
    ]
  },
  {
    id: 'finalizar_todo',
    nombre: 'Finalizar flujo',
    categoria: 'finalizacion',
    descripcion: 'Finaliza y limpia recursos.',
    schema: []
  }
];
