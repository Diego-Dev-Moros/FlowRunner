# config.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class StepSpec:
    """
    Especifica cómo invocar una acción a partir de un nodo del flujo.
    - callable_path: ruta 'paquete.modulo:funcion' a importar dinámicamente.
    - param_map: mapea nombre_parametro_funcion -> clave_en_props (del nodo).
                 Si terminás una clave con '?' se considera opcional.
                 Ej.: {'nombre_variable': 'variable', 'ruta_destino': 'ruta'}
    - inject: lista de parámetros a inyectar automáticamente si la función los acepta.
              Soportados: 'driver', 'contexto'
    - provides: si la función devuelve un recurso a guardar en el runtime.
                Soportado: 'driver' (p. ej., abrir navegador retorna driver)
    - clear_driver: si True, tras ejecutar la función se setea driver=None
                    (útil para cerrar navegador)
    - description: opcional, para documentación/logs
    """
    callable_path: str
    param_map: Dict[str, str] = field(default_factory=dict)
    inject: List[str] = field(default_factory=list)
    provides: Optional[str] = None
    clear_driver: bool = False
    description: str = ""


# --------------------------------------------------------------------
# MAPEO: typeId (del front/JSON)  ->  StepSpec (callable + binding)
# Ajustá los módulos/funciones según tu código real.
# En este ejemplo, asumimos que todas están en modules/funciones/extras.py
# --------------------------------------------------------------------
ACTION_SPECS: Dict[str, StepSpec] = {
    # ===== Navegador / Selenium =====
    'abrir_pagina': StepSpec(
        callable_path='modules.funciones.extras:abrir_pagina_web_selenium',
        param_map={'url': 'url'},         # función espera (url)
        inject=[],                        # no inyecta driver, crea uno nuevo adentro
        provides='driver',                # retorna driver
        description='Abre una página y retorna un driver'
    ),
    'cambiar_pagina': StepSpec(
        callable_path='modules.funciones.extras:cambiar_pagina_web_selenium',
        # firma: (driver, nueva_url)
        param_map={'nueva_url': 'url'},
        inject=['driver'],
        description='Cambia la URL en el driver existente'
    ),
    'cerrar_navegador': StepSpec(
        callable_path='modules.funciones.extras:cerrar_navegador_selenium',
        # firma: (driver)
        param_map={},
        inject=['driver'],
        clear_driver=True,
        description='Cierra el navegador y limpia el driver'
    ),
    'maximizar_app': StepSpec(
        callable_path='modules.funciones.extras:maximizar_navegador',
        # firma: (driver)
        param_map={},
        inject=['driver'],
        description='Maximiza la ventana del navegador'
    ),
    # (Si más adelante agregás en el front un "minimizar_app", ya queda listo)
    'minimizar_app': StepSpec(
        callable_path='modules.funciones.extras:minimizar_navegador',
        param_map={},
        inject=['driver'],
        description='Minimiza la ventana del navegador'
    ),

    # ===== Lectura =====
    'leer_csv': StepSpec(
        callable_path='modules.funciones.extras:leer_csv',
        # firma: (ruta_csv, contexto, nombre_personalizado=None)
        param_map={
            'ruta_csv': 'ruta',
            'nombre_personalizado': 'nombre_personalizado?'   # opcional
        },
        inject=['contexto'],
        description='Lee CSV y guarda resultado en contexto'
    ),
    'leer_excel': StepSpec(
        callable_path='modules.funciones.extras:leer_excel',
        # firma: (ruta_excel, hoja, contexto, nombre_personalizado=None)
        param_map={
            'ruta_excel': 'ruta',
            'hoja': 'hoja',
            'nombre_personalizado': 'nombre_personalizado?'
        },
        inject=['contexto'],
        description='Lee Excel y guarda resultado en contexto'
    ),
    'leer_txt': StepSpec(
        callable_path='modules.funciones.extras:leer_txt_delimitado',
        # firma: (ruta_txt, delimitador, contexto, nombre_personalizado=None)
        param_map={
            'ruta_txt': 'ruta',
            'delimitador': 'delimitador',
            'nombre_personalizado': 'nombre_personalizado?'
        },
        inject=['contexto'],
        description='Lee TXT delimitado y guarda resultado en contexto'
    ),

    # ===== Escritura =====
    'escribir_csv': StepSpec(
        callable_path='modules.funciones.extras:escribir_csv',
        # firma: (nombre_variable, ruta_destino, contexto)
        param_map={
            'nombre_variable': 'variable',
            'ruta_destino': 'ruta'
        },
        inject=['contexto'],
        description='Escribe variable/array del contexto a CSV'
    ),
    'escribir_excel': StepSpec(
        callable_path='modules.funciones.extras:escribir_excel',
        # firma: (nombre_variable, ruta_destino, contexto)
        param_map={
            'nombre_variable': 'variable',
            'ruta_destino': 'ruta'
        },
        inject=['contexto'],
        description='Escribe variable/array del contexto a Excel'
    ),
    'escribir_txt': StepSpec(
        callable_path='modules.funciones.extras:escribir_txt',
        # firma: (nombre_variable, ruta_destino, delimitador, contexto)
        param_map={
            'nombre_variable': 'variable',
            'ruta_destino': 'ruta',
            'delimitador': 'delimitador'
        },
        inject=['contexto'],
        description='Escribe variable/array del contexto a TXT delimitado'
    ),

    # ===== Otras básicas del front (no ejecutan lógica en Python) =====
    # 'exportar_json': no corresponde ejecutar algo aquí
    # 'ejecutar_flujo': representa al runner, no una acción dentro del flujo
    # 'finalizar_todo': si querés, podés mapear a una función de limpieza
}