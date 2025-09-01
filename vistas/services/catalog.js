// ---------------------------
// Catálogo de funciones (metadatos)
// ---------------------------
export const FUNCTION_CATALOG = [
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

// Acciones de Lectura
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

//  Acciones de Escritura
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
