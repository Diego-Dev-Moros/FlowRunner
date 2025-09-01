# modules/config.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class StepSpec:
    """
    Especifica cómo invocar una acción a partir de un nodo del flujo.
    - callable_path: 'paquete.modulo:funcion'
    - param_map: mapea nombre_parametro_funcion -> clave_en_props (del nodo).
                 Si la clave finaliza en '?' es opcional.
    - inject: ['driver', 'contexto'] para inyección automática
    - provides: 'driver' si la función devuelve un driver a conservar
    - clear_driver: True si se debe limpiar el driver tras ejecutar
    """
    callable_path: str
    param_map: Dict[str, str] = field(default_factory=dict)
    inject: List[str] = field(default_factory=list)
    provides: Optional[str] = None
    clear_driver: bool = False
    description: str = ""

# --------------------------------------------------------------------
# MAPEO: typeId -> StepSpec   (callables en modules.funciones.extras)
# --------------------------------------------------------------------
ACTION_SPECS: Dict[str, StepSpec] = {
    # ===== Control / Básicas =====
    'pausa': StepSpec(
        callable_path='modules.funciones.extras:pausa',
        param_map={'segundos': 'segundos?', 'ms': 'ms?'},
        inject=['contexto'],
        description='Pausa en segundos o ms'
    ),
    'variable_set': StepSpec(
        callable_path='modules.funciones.extras:variable_set',
        param_map={'nombre': 'nombre', 'valor': 'valor'},
        inject=['contexto'],
        description='Guardar variable en contexto'
    ),
    'variable_get': StepSpec(
        callable_path='modules.funciones.extras:variable_get',
        param_map={'nombre': 'nombre'},
        inject=['contexto'],
        description='Leer variable del contexto'
    ),

    # ===== Diálogos =====
    'dialogo_seleccionar_archivo': StepSpec(
        callable_path='modules.funciones.extras:dialogo_seleccionar_archivo',
        param_map={'titulo': 'titulo?', 'guardar_en': 'guardar_en'},
        inject=['contexto'],
        description='Abrir diálogo de archivo y guardar ruta'
    ),
    'dialogo_seleccionar_carpeta': StepSpec(
        callable_path='modules.funciones.extras:dialogo_seleccionar_carpeta',
        param_map={'titulo': 'titulo?', 'guardar_en': 'guardar_en'},
        inject=['contexto'],
        description='Abrir diálogo de carpeta y guardar ruta'
    ),

    # ===== Lectura =====
    'leer_csv': StepSpec(
        callable_path='modules.funciones.extras:leer_csv',
        param_map={'ruta_csv': 'ruta', 'nombre_personalizado': 'nombre_personalizado?'},
        inject=['contexto'],
        description='Lee CSV y guarda DataFrame en contexto'
    ),
    'leer_excel': StepSpec(
        callable_path='modules.funciones.extras:leer_excel',
        param_map={'ruta_excel': 'ruta', 'hoja': 'hoja', 'nombre_personalizado': 'nombre_personalizado?'},
        inject=['contexto'],
        description='Lee Excel (hoja) y guarda DataFrame'
    ),
    'leer_txt': StepSpec(
        callable_path='modules.funciones.extras:leer_txt_delimitado',
        param_map={'ruta_txt': 'ruta', 'delimitador': 'delimitador', 'nombre_personalizado': 'nombre_personalizado?'},
        inject=['contexto'],
        description='Lee TXT delimitado y guarda DataFrame'
    ),
    'excel_leer_rango': StepSpec(
        callable_path='modules.funciones.extras:excel_leer_rango',
        param_map={
            'ruta': 'ruta', 'hoja': 'hoja',
            'rango': 'rango?', 'columnas': 'columnas?', 'nombre_personalizado': 'nombre_personalizado?'
        },
        inject=['contexto'],
        description='Lee rango A1:D100 o columnas por nombre'
    ),

    # ===== Escritura =====
    'escribir_csv': StepSpec(
        callable_path='modules.funciones.extras:escribir_csv',
        param_map={'nombre_variable': 'variable', 'ruta_destino': 'ruta'},
        inject=['contexto'],
        description='Escribe variable/array del contexto a CSV'
    ),
    'escribir_excel': StepSpec(
        callable_path='modules.funciones.extras:escribir_excel',
        param_map={
            'nombre_variable': 'variable',
            'ruta_destino': 'ruta',
            'hoja': 'hoja?',
            'modo': 'modo?',
            'inicio_celda': 'inicio_celda?',
            'incluir_cabeceras': 'incluir_cabeceras?'
        },
        inject=['contexto'],
        description='Escribe a Excel (sobrescribir o append)'
    ),
    'excel_crear_hoja': StepSpec(
        callable_path='modules.funciones.extras:excel_crear_hoja',
        param_map={'ruta': 'ruta', 'nombre_hoja': 'nombre_hoja', 'si_existe': 'si_existe?'},
        description='Crea hoja nueva en libro Excel'
    ),

    # ===== Archivos / Carpetas =====
    'archivo_mover': StepSpec(
        callable_path='modules.funciones.extras:archivo_mover',
        param_map={'origen': 'origen', 'destino': 'destino', 'si_existe': 'si_existe?'},
        description='Mover archivo'
    ),
    'archivo_copiar': StepSpec(
        callable_path='modules.funciones.extras:archivo_copiar',
        param_map={'origen': 'origen', 'destino': 'destino', 'si_existe': 'si_existe?'},
        description='Copiar archivo'
    ),
    'archivo_borrar': StepSpec(
        callable_path='modules.funciones.extras:archivo_borrar',
        param_map={'ruta': 'ruta'},
        description='Borrar archivo/carpeta'
    ),
    'carpeta_crear': StepSpec(
        callable_path='modules.funciones.extras:carpeta_crear',
        param_map={'ruta': 'ruta'},
        description='Crear carpeta'
    ),
    'carpeta_listar': StepSpec(
        callable_path='modules.funciones.extras:carpeta_listar',
        param_map={'ruta': 'ruta', 'patron': 'patron?', 'nombre_personalizado': 'nombre_personalizado?'},
        inject=['contexto'],
        description='Listar archivos por patrón'
    ),

    # ===== Navegador / Selenium (si lo usas) =====
    'abrir_pagina': StepSpec(
        callable_path='modules.funciones.extras:abrir_pagina_web_selenium',
        param_map={'url': 'url'},
        provides='driver',
        description='Abre navegador y retorna driver'
    ),
    'cambiar_pagina': StepSpec(
        callable_path='modules.funciones.extras:cambiar_pagina_web_selenium',
        param_map={'nueva_url': 'url'},
        inject=['driver'],
        description='Cambia URL en driver'
    ),
    'cerrar_navegador': StepSpec(
        callable_path='modules.funciones.extras:cerrar_navegador_selenium',
        param_map={},
        inject=['driver'],
        clear_driver=True,
        description='Cierra navegador y limpia driver'
    ),
    'maximizar_app': StepSpec(
        callable_path='modules.funciones.extras:maximizar_navegador',
        param_map={},
        inject=['driver'],
        description='Maximiza ventana de navegador'
    ),
    'minimizar_app': StepSpec(
        callable_path='modules.funciones.extras:minimizar_navegador',
        param_map={},
        inject=['driver'],
        description='Minimiza ventana de navegador'
    ),
}
ENABLED_TYPES = {
    # ejemplo: habilitadas
    'leer_csv','leer_excel','leer_txt','excel_leer_rango',
    'escribir_csv','escribir_excel','excel_crear_hoja',
    'archivo_mover','archivo_copiar','archivo_borrar',
    'carpeta_crear','carpeta_listar',
    'pausa','variable_set','variable_get',
    # agrega o quita según necesites. Si esta lista está vacía, se asume "todas habilitadas".
}
