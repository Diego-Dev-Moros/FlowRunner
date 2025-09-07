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
  // � PROCESAMIENTO DE DATOS AVANZADO
  // =========================
  {
    id: 'filtrar_dataframe',
    nombre: 'Filtrar DataFrame',
    categoria: 'procesamiento',
    descripcion: 'Filtra un DataFrame usando condiciones especificadas',
    schema: [
      { key: 'dataframe_var', label: 'Variable DataFrame', type: 'text', required: true, placeholder: 'mi_dataframe' },
      { key: 'columna', label: 'Columna a filtrar', type: 'text', required: true, placeholder: 'nombre_columna' },
      { key: 'operador', label: 'Operador', type: 'select', required: true, options: [
        { value: '==', label: 'Igual a' },
        { value: '!=', label: 'Diferente de' },
        { value: '>', label: 'Mayor que' },
        { value: '>=', label: 'Mayor o igual que' },
        { value: '<', label: 'Menor que' },
        { value: '<=', label: 'Menor o igual que' },
        { value: 'contains', label: 'Contiene texto' },
        { value: 'startswith', label: 'Comienza con' },
        { value: 'endswith', label: 'Termina con' },
        { value: 'isnull', label: 'Es nulo' },
        { value: 'notnull', label: 'No es nulo' }
      ]},
      { key: 'valor', label: 'Valor de comparación', type: 'text', required: false, placeholder: 'valor' },
      { key: 'resultado_var', label: 'Variable resultado', type: 'text', required: true, placeholder: 'df_filtrado' }
    ]
  },
  {
    id: 'transformar_columnas',
    nombre: 'Transformar Columnas',
    categoria: 'procesamiento',
    descripcion: 'Aplica transformaciones a columnas del DataFrame',
    schema: [
      { key: 'dataframe_var', label: 'Variable DataFrame', type: 'text', required: true, placeholder: 'mi_dataframe' },
      { key: 'columna', label: 'Columna a transformar', type: 'text', required: true, placeholder: 'nombre_columna' },
      { key: 'transformacion', label: 'Tipo de transformación', type: 'select', required: true, options: [
        { value: 'upper', label: 'Mayúsculas' },
        { value: 'lower', label: 'Minúsculas' },
        { value: 'title', label: 'Título (Primera Mayúscula)' },
        { value: 'strip', label: 'Quitar espacios' },
        { value: 'replace', label: 'Reemplazar texto' },
        { value: 'numeric', label: 'Convertir a numérico' },
        { value: 'datetime', label: 'Convertir a fecha' },
        { value: 'multiply', label: 'Multiplicar por valor' },
        { value: 'add', label: 'Sumar valor' }
      ]},
      { key: 'parametro1', label: 'Parámetro 1', type: 'text', required: false, placeholder: 'valor1' },
      { key: 'parametro2', label: 'Parámetro 2', type: 'text', required: false, placeholder: 'valor2' },
      { key: 'nueva_columna', label: 'Nueva columna', type: 'text', required: false, placeholder: 'nueva_col' }
    ]
  },
  {
    id: 'agrupar_datos',
    nombre: 'Agrupar Datos',
    categoria: 'procesamiento',
    descripcion: 'Agrupa datos por columnas y calcula estadísticas',
    schema: [
      { key: 'dataframe_var', label: 'Variable DataFrame', type: 'text', required: true, placeholder: 'mi_dataframe' },
      { key: 'columnas_grupo', label: 'Columnas para agrupar', type: 'text', required: true, placeholder: 'col1,col2' },
      { key: 'columna_agregacion', label: 'Columna para agregar', type: 'text', required: true, placeholder: 'valor_columna' },
      { key: 'funcion_agregacion', label: 'Función de agregación', type: 'select', required: true, options: [
        { value: 'count', label: 'Contar' },
        { value: 'sum', label: 'Sumar' },
        { value: 'mean', label: 'Promedio' },
        { value: 'median', label: 'Mediana' },
        { value: 'min', label: 'Mínimo' },
        { value: 'max', label: 'Máximo' },
        { value: 'std', label: 'Desviación estándar' },
        { value: 'var', label: 'Varianza' }
      ]},
      { key: 'resultado_var', label: 'Variable resultado', type: 'text', required: true, placeholder: 'datos_agrupados' }
    ]
  },
  {
    id: 'eliminar_duplicados',
    nombre: 'Eliminar Duplicados',
    categoria: 'procesamiento',
    descripcion: 'Elimina filas duplicadas del DataFrame',
    schema: [
      { key: 'dataframe_var', label: 'Variable DataFrame', type: 'text', required: true, placeholder: 'mi_dataframe' },
      { key: 'columnas', label: 'Columnas para comparar', type: 'text', required: false, placeholder: 'col1,col2' },
      { key: 'mantener', label: 'Registro a mantener', type: 'select', required: true, options: [
        { value: 'first', label: 'Primer registro' },
        { value: 'last', label: 'Último registro' },
        { value: 'false', label: 'Eliminar todos los duplicados' }
      ]}
    ]
  },
  {
    id: 'ordenar_avanzado',
    nombre: 'Ordenar Avanzado',
    categoria: 'procesamiento',
    descripcion: 'Ordena DataFrame por múltiples columnas',
    schema: [
      { key: 'dataframe_var', label: 'Variable DataFrame', type: 'text', required: true, placeholder: 'mi_dataframe' },
      { key: 'columnas', label: 'Columnas para ordenar', type: 'text', required: true, placeholder: 'col1,col2' },
      { key: 'orden', label: 'Orden de clasificación', type: 'select', required: true, options: [
        { value: 'asc', label: 'Ascendente' },
        { value: 'desc', label: 'Descendente' }
      ]},
      { key: 'nulos_al_final', label: 'Valores nulos al final', type: 'select', required: true, options: [
        { value: 'true', label: 'Sí' },
        { value: 'false', label: 'No' }
      ]}
    ]
  },
  {
    id: 'pivotar_tabla',
    nombre: 'Crear Tabla Pivote',
    categoria: 'procesamiento',
    descripcion: 'Crea una tabla pivote a partir del DataFrame',
    schema: [
      { key: 'dataframe_var', label: 'Variable DataFrame', type: 'text', required: true, placeholder: 'mi_dataframe' },
      { key: 'columna_indice', label: 'Columna índice', type: 'text', required: true, placeholder: 'columna_fila' },
      { key: 'columna_columnas', label: 'Columna para columnas', type: 'text', required: true, placeholder: 'columna_cols' },
      { key: 'columna_valores', label: 'Columna de valores', type: 'text', required: true, placeholder: 'valores' },
      { key: 'funcion_agregacion', label: 'Función de agregación', type: 'select', required: true, options: [
        { value: 'sum', label: 'Sumar' },
        { value: 'mean', label: 'Promedio' },
        { value: 'count', label: 'Contar' },
        { value: 'min', label: 'Mínimo' },
        { value: 'max', label: 'Máximo' }
      ]},
      { key: 'resultado_var', label: 'Variable resultado', type: 'text', required: true, placeholder: 'tabla_pivote' }
    ]
  },
  {
    id: 'calcular_estadisticas',
    nombre: 'Calcular Estadísticas',
    categoria: 'procesamiento',
    descripcion: 'Calcula estadísticas descriptivas completas',
    schema: [
      { key: 'dataframe_var', label: 'Variable DataFrame', type: 'text', required: true, placeholder: 'mi_dataframe' },
      { key: 'columnas', label: 'Columnas a analizar', type: 'text', required: false, placeholder: 'col1,col2' },
      { key: 'estadisticas', label: 'Estadísticas específicas', type: 'text', required: false, placeholder: 'count,mean,std' },
      { key: 'formato_salida', label: 'Formato de salida', type: 'select', required: true, options: [
        { value: 'dataframe', label: 'DataFrame' },
        { value: 'dict', label: 'Diccionario' },
        { value: 'resumen', label: 'Resumen de texto' }
      ]},
      { key: 'resultado_var', label: 'Variable resultado', type: 'text', required: true, placeholder: 'estadisticas' }
    ]
  },
  {
    id: 'normalizar_datos',
    nombre: 'Normalizar Datos',
    categoria: 'procesamiento',
    descripcion: 'Normaliza columnas numéricas usando diferentes métodos',
    schema: [
      { key: 'dataframe_var', label: 'Variable DataFrame', type: 'text', required: true, placeholder: 'mi_dataframe' },
      { key: 'columnas', label: 'Columnas a normalizar', type: 'text', required: false, placeholder: 'col1,col2' },
      { key: 'metodo', label: 'Método de normalización', type: 'select', required: true, options: [
        { value: 'zscore', label: 'Z-Score (media=0, std=1)' },
        { value: 'minmax', label: 'Min-Max (0-1)' },
        { value: 'robust', label: 'Robusto (mediana y MAD)' },
        { value: 'unit', label: 'Vector unitario (norma=1)' }
      ]},
      { key: 'sufijo', label: 'Sufijo para nuevas columnas', type: 'text', required: false, placeholder: '_norm' }
    ]
  },
  {
    id: 'unir_datasets',
    nombre: 'Unir Datasets',
    categoria: 'procesamiento',
    descripcion: 'Une dos DataFrames usando diferentes tipos de JOIN',
    schema: [
      { key: 'dataframe_izq_var', label: 'DataFrame izquierdo', type: 'text', required: true, placeholder: 'df1' },
      { key: 'dataframe_der_var', label: 'DataFrame derecho', type: 'text', required: true, placeholder: 'df2' },
      { key: 'columna_izq', label: 'Columna de unión izquierda', type: 'text', required: true, placeholder: 'id' },
      { key: 'columna_der', label: 'Columna de unión derecha', type: 'text', required: false, placeholder: 'id' },
      { key: 'tipo_join', label: 'Tipo de JOIN', type: 'select', required: true, options: [
        { value: 'inner', label: 'INNER - Solo registros que coinciden' },
        { value: 'left', label: 'LEFT - Todos los registros del izquierdo' },
        { value: 'right', label: 'RIGHT - Todos los registros del derecho' },
        { value: 'outer', label: 'OUTER - Todos los registros de ambos' }
      ]},
      { key: 'sufijos', label: 'Sufijos para columnas duplicadas', type: 'text', required: false, placeholder: '_x,_y' },
      { key: 'resultado_var', label: 'Variable resultado', type: 'text', required: true, placeholder: 'df_unido' }
    ]
  },
  {
    id: 'concatenar_datasets',
    nombre: 'Concatenar Datasets',
    categoria: 'procesamiento',
    descripcion: 'Concatena múltiples DataFrames vertical u horizontalmente',
    schema: [
      { key: 'dataframes_vars', label: 'Variables DataFrames', type: 'text', required: true, placeholder: 'df1,df2,df3' },
      { key: 'direccion', label: 'Dirección de concatenación', type: 'select', required: true, options: [
        { value: 'vertical', label: 'Vertical (apilar filas)' },
        { value: 'horizontal', label: 'Horizontal (unir columnas)' }
      ]},
      { key: 'ignorar_indices', label: 'Ignorar índices originales', type: 'select', required: true, options: [
        { value: 'true', label: 'Sí - crear nuevo índice' },
        { value: 'false', label: 'No - mantener índices originales' }
      ]},
      { key: 'etiquetas', label: 'Etiquetas para identificar origen', type: 'text', required: false, placeholder: 'tabla1,tabla2' },
      { key: 'resultado_var', label: 'Variable resultado', type: 'text', required: true, placeholder: 'df_concatenado' }
    ]
  },
  {
    id: 'validar_datos',
    nombre: 'Validar Datos',
    categoria: 'procesamiento',
    descripcion: 'Valida la calidad e integridad de los datos',
    schema: [
      { key: 'dataframe_var', label: 'Variable DataFrame', type: 'text', required: true, placeholder: 'mi_dataframe' },
      { key: 'validaciones', label: 'Tipos de validación', type: 'text', required: true, placeholder: 'nulos,duplicados,tipos' },
      { key: 'columnas_especificas', label: 'Columnas específicas', type: 'text', required: false, placeholder: 'col1,col2' },
      { key: 'configuracion', label: 'Configuración JSON', type: 'text', required: false, placeholder: '{"col1":{"tipo":"int","min":0}}' },
      { key: 'resultado_var', label: 'Variable resultado', type: 'text', required: true, placeholder: 'reporte_validacion' }
    ]
  },

  // =========================
  // 🔄 CONTROL Y DECISIONES 
  // =========================
  {
    id: 'condicional_si',
    nombre: 'Condición Si/Entonces',
    categoria: 'logica',
    descripcion: 'Ejecuta acciones diferentes según una condición (if/else).',
    schema: [
      { key: 'condicion', label: 'Condición', type: 'text', required: true, placeholder: 'edad >= 18' },
      { key: 'variable_resultado', label: 'Variable resultado', type: 'text', required: false, placeholder: 'es_mayor' }
    ]
  },
  {
    id: 'bucle_mientras',
    nombre: 'Repetir Mientras',
    categoria: 'logica',
    descripcion: 'Repite acciones mientras se cumpla una condición (while loop).',
    schema: [
      { key: 'condicion', label: 'Condición', type: 'text', required: true, placeholder: 'contador < 10' },
      { key: 'max_iteraciones', label: 'Máximo iteraciones', type: 'number', required: false, placeholder: '100' }
    ]
  },
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
  },

  // =========================
  // 🎮 CONTROL DE FLUJO AVANZADO (Phase 2)
  // =========================
  {
    id: 'bucle_for_rango',
    nombre: 'Bucle For con Rango',
    categoria: 'control',
    descripcion: 'Ejecuta un bucle for con un rango numérico específico',
    schema: [
      { key: 'variable_contador', label: 'Variable contador', type: 'text', required: true, placeholder: 'i' },
      { key: 'inicio', label: 'Valor inicial', type: 'number', required: true, placeholder: '1' },
      { key: 'fin', label: 'Valor final', type: 'number', required: true, placeholder: '10' },
      { key: 'paso', label: 'Incremento', type: 'number', required: false, placeholder: '1' },
      { key: 'max_iteraciones', label: 'Máximo iteraciones', type: 'number', required: false, placeholder: '1000' }
    ]
  },
  {
    id: 'bucle_for_lista',
    nombre: 'Bucle For sobre Lista',
    categoria: 'control',
    descripcion: 'Itera sobre elementos de una lista o array',
    schema: [
      { key: 'variable_elemento', label: 'Variable elemento', type: 'text', required: true, placeholder: 'item' },
      { key: 'variable_indice', label: 'Variable índice', type: 'text', required: false, placeholder: 'idx' },
      { key: 'lista_variable', label: 'Lista/Variable', type: 'text', required: true, placeholder: 'mi_lista' },
      { key: 'max_iteraciones', label: 'Máximo iteraciones', type: 'number', required: false, placeholder: '1000' }
    ]
  },
  {
    id: 'repetir_hasta',
    nombre: 'Repetir Hasta',
    categoria: 'control',
    descripcion: 'Repite hasta que se cumpla una condición',
    schema: [
      { key: 'variable_condicion', label: 'Variable condición', type: 'text', required: true, placeholder: 'contador' },
      { key: 'valor_objetivo', label: 'Valor objetivo', type: 'text', required: true, placeholder: '10' },
      { key: 'operador', label: 'Operador', type: 'select', required: true, options: ['==','!=','>=','<=','>','<','contains','not_contains'] },
      { key: 'max_iteraciones', label: 'Máximo iteraciones', type: 'number', required: false, placeholder: '100' },
      { key: 'delay_ms', label: 'Delay (ms)', type: 'number', required: false, placeholder: '100' }
    ]
  },
  {
    id: 'interrumpir_flujo',
    nombre: 'Interrumpir Flujo',
    categoria: 'control',
    descripcion: 'Interrumpe o controla el flujo de ejecución',
    schema: [
      { key: 'tipo_interrupcion', label: 'Tipo', type: 'select', required: true, options: ['break','continue','return','exit'] },
      { key: 'condicion_variable', label: 'Variable condición', type: 'text', required: false, placeholder: 'estado' },
      { key: 'condicion_valor', label: 'Valor condición', type: 'text', required: false, placeholder: 'true' },
      { key: 'mensaje_salida', label: 'Mensaje', type: 'text', required: false, placeholder: 'Flujo interrumpido' }
    ]
  },
  {
    id: 'condicional_multiple',
    nombre: 'Condición Múltiple (Switch)',
    categoria: 'control',
    descripcion: 'Evalúa múltiples condiciones tipo switch/case',
    schema: [
      { key: 'variable_evaluacion', label: 'Variable a evaluar', type: 'text', required: true, placeholder: 'estado' },
      { key: 'casos', label: 'Casos (JSON)', type: 'text', required: true, placeholder: '{"caso1": "accion1", "default": "accion_default"}' },
      { key: 'comparacion_estricta', label: 'Comparación estricta', type: 'select', required: true, options: ['true','false'] },
      { key: 'resultado_variable', label: 'Variable resultado', type: 'text', required: true, placeholder: 'resultado' }
    ]
  },
  {
    id: 'condicional_and_or',
    nombre: 'Condición AND/OR',
    categoria: 'control',
    descripcion: 'Evalúa condiciones complejas con AND/OR',
    schema: [
      { key: 'condicion_1', label: 'Condición 1', type: 'text', required: true, placeholder: 'edad >= 18' },
      { key: 'condicion_2', label: 'Condición 2', type: 'text', required: true, placeholder: 'activo == true' },
      { key: 'operador', label: 'Operador lógico', type: 'select', required: true, options: ['and','or','xor'] },
      { key: 'resultado_variable', label: 'Variable resultado', type: 'text', required: true, placeholder: 'es_valido' }
    ]
  },
  {
    id: 'esperar_condicion',
    nombre: 'Esperar Condición',
    categoria: 'control',
    descripcion: 'Espera hasta que se cumpla una condición específica',
    schema: [
      { key: 'condicion_espera', label: 'Condición', type: 'text', required: true, placeholder: 'proceso_completado == true' },
      { key: 'timeout_segundos', label: 'Timeout (seg)', type: 'number', required: true, placeholder: '30' },
      { key: 'intervalo_verificacion', label: 'Intervalo verificación (seg)', type: 'number', required: false, placeholder: '1' },
      { key: 'accion_timeout', label: 'Acción timeout', type: 'select', required: true, options: ['error','continue','return_false'] }
    ]
  },
  {
    id: 'try_catch_finally',
    nombre: 'Try-Catch-Finally',
    categoria: 'control',
    descripcion: 'Manejo de errores con bloques try/catch/finally',
    schema: [
      { key: 'accion_catch', label: 'Acción en catch', type: 'select', required: true, options: ['continue','stop','retry','log_only'] },
      { key: 'variable_error', label: 'Variable error', type: 'text', required: false, placeholder: 'ultimo_error' },
      { key: 'error_esperado', label: 'Tipo error esperado', type: 'select', required: false, options: ['any','variable_not_found','type_error','value_error','file_not_found'] },
      { key: 'max_reintentos', label: 'Máximo reintentos', type: 'number', required: false, placeholder: '3' },
      { key: 'delay_reintento', label: 'Delay reintento (ms)', type: 'number', required: false, placeholder: '1000' }
    ]
  },
  {
    id: 'validar_variable',
    nombre: 'Validar Variable',
    categoria: 'control',
    descripcion: 'Valida el contenido de una variable',
    schema: [
      { key: 'nombre_variable', label: 'Variable a validar', type: 'text', required: true, placeholder: 'email' },
      { key: 'tipo_validacion', label: 'Tipo validación', type: 'select', required: true, options: ['email','telefono','numero','texto','fecha','url','regex'] },
      { key: 'patron_regex', label: 'Patrón regex', type: 'text', required: false, placeholder: '^[A-Za-z]+$' },
      { key: 'es_obligatoria', label: 'Es obligatoria', type: 'select', required: true, options: ['true','false'] },
      { key: 'resultado_variable', label: 'Variable resultado', type: 'text', required: true, placeholder: 'es_valido' }
    ]
  },
  {
    id: 'delay_dinamico',
    nombre: 'Delay Dinámico',
    categoria: 'control',
    descripcion: 'Pausa con duración calculada dinámicamente',
    schema: [
      { key: 'tipo_delay', label: 'Tipo de delay', type: 'select', required: true, options: ['fijo','variable','aleatorio','progresivo','exponencial'] },
      { key: 'valor_base', label: 'Valor base (seg)', type: 'number', required: true, placeholder: '1' },
      { key: 'variable_multiplicador', label: 'Variable multiplicador', type: 'text', required: false, placeholder: 'factor' },
      { key: 'min_delay', label: 'Delay mínimo (seg)', type: 'number', required: false, placeholder: '0.1' },
      { key: 'max_delay', label: 'Delay máximo (seg)', type: 'number', required: false, placeholder: '300' }
    ]
  },
  {
    id: 'esperar_hasta_hora',
    nombre: 'Esperar Hasta Hora',
    categoria: 'control',
    descripcion: 'Espera hasta una hora específica del día',
    schema: [
      { key: 'hora_objetivo', label: 'Hora objetivo', type: 'text', required: true, placeholder: '14:30:00' },
      { key: 'fecha_objetivo', label: 'Fecha objetivo', type: 'text', required: false, placeholder: '2025-12-25' },
      { key: 'accion_si_pasado', label: 'Acción si ya pasó', type: 'select', required: true, options: ['siguiente_dia','error','continuar'] }
    ]
  },
  {
    id: 'programar_ejecucion',
    nombre: 'Programar Ejecución',
    categoria: 'control',
    descripcion: 'Programa la ejecución para un momento específico',
    schema: [
      { key: 'tipo_programacion', label: 'Tipo programación', type: 'select', required: true, options: ['una_vez','intervalo','diario','semanal','condicional'] },
      { key: 'momento_inicial', label: 'Momento inicial', type: 'text', required: false, placeholder: '2025-12-25 14:30:00 o +30m' },
      { key: 'intervalo', label: 'Intervalo', type: 'text', required: false, placeholder: '30s, 5m, 2h, 1d' },
      { key: 'max_ejecuciones', label: 'Máximo ejecuciones', type: 'number', required: false, placeholder: '10' },
      { key: 'variable_contador', label: 'Variable contador', type: 'text', required: false, placeholder: 'ejecuciones' }
    ]
  }
];
