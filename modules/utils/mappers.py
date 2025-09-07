"""
Mappers y utilidades para la configuración del sistema FlowRunner.
Centraliza la lógica de mapeo entre backend y frontend.
"""

from modules.core.registry import ActionRegistry


# Configuración global que se puede modificar
_ACTION_CONFIG = None

def get_action_config():
    """
    Configuración central de todas las acciones disponibles y su estado.
    Aquí se define TODO el mapeo backend->frontend y qué está habilitado.
    
    Returns:
        dict: Configuración completa de acciones
    """
    global _ACTION_CONFIG
    if _ACTION_CONFIG is None:
        _ACTION_CONFIG = {
            # === DATOS ===
            'variable_set': {'enabled': True, 'backend_id': 'variable_set'},
            'variable_get': {'enabled': True, 'backend_id': 'variable_get'},
            'variables_listar': {'enabled': True, 'backend_id': 'variables_listar'},
            'ordenar_info': {'enabled': True, 'backend_id': 'ordenar_info'},
            
            # === LECTURA ===
            'leer_csv': {'enabled': True, 'backend_id': 'leer_csv_action'},
            'excel_leer_rango': {'enabled': True, 'backend_id': 'excel_leer_rango_action'},
            'carpeta_listar': {'enabled': True, 'backend_id': 'carpeta_listar_action'},
            
            # === ESCRITURA ===
            'escribir_csv': {'enabled': True, 'backend_id': 'escribir_csv_action'},
            'escribir_excel': {'enabled': True, 'backend_id': 'escribir_excel_action'},
            'escribir_txt': {'enabled': True, 'backend_id': 'escribir_txt_action'},
            
            # === ARCHIVOS ===
            'carpeta_crear': {'enabled': True, 'backend_id': 'crear_carpeta_action'},
            'archivo_mover': {'enabled': True, 'backend_id': 'mover_archivo_action'},
            'archivo_copiar': {'enabled': True, 'backend_id': 'copiar_archivo_action'},
            'archivo_borrar': {'enabled': True, 'backend_id': 'eliminar_archivo_action'},
            
            # === DIALOGOS ===
            'dialogo_seleccionar_archivo': {'enabled': True, 'backend_id': 'dialogo_seleccionar_archivo'},
            'dialogo_seleccionar_carpeta': {'enabled': True, 'backend_id': 'dialogo_seleccionar_carpeta'},
            
            # === NAVEGACIÓN WEB (DESHABILITADAS) ===
            'abrir_pagina': {'enabled': False, 'backend_id': 'abrir_pagina_action'},
            'cambiar_pagina': {'enabled': False, 'backend_id': 'cambiar_pagina_action'},
            'maximizar_navegador': {'enabled': False, 'backend_id': 'maximizar_navegador_action'},
            'cerrar_navegador': {'enabled': False, 'backend_id': 'cerrar_navegador_action'},
            
            # === CONTROL BÁSICO ===
            'pausa': {'enabled': True, 'backend_id': 'pausa'},
            'condicional_si': {'enabled': True, 'backend_id': 'condicional_si'},
            'bucle_mientras': {'enabled': True, 'backend_id': 'bucle_mientras'},
            
            # === CONTROL DE FLUJO AVANZADO (Phase 2) ===
            'bucle_for_rango': {'enabled': True, 'backend_id': 'bucle_for_rango'},
            'bucle_for_lista': {'enabled': True, 'backend_id': 'bucle_for_lista'},
            'repetir_hasta': {'enabled': True, 'backend_id': 'repetir_hasta'},
            'interrumpir_flujo': {'enabled': True, 'backend_id': 'interrumpir_flujo'},
            'condicional_multiple': {'enabled': True, 'backend_id': 'condicional_multiple'},
            'condicional_and_or': {'enabled': True, 'backend_id': 'condicional_and_or'},
            'esperar_condicion': {'enabled': True, 'backend_id': 'esperar_condicion'},
            'try_catch_finally': {'enabled': True, 'backend_id': 'try_catch_finally'},
            'validar_variable': {'enabled': True, 'backend_id': 'validar_variable'},
            'delay_dinamico': {'enabled': True, 'backend_id': 'delay_dinamico'},
            'esperar_hasta_hora': {'enabled': True, 'backend_id': 'esperar_hasta_hora'},
            'programar_ejecucion': {'enabled': True, 'backend_id': 'programar_ejecucion'},
            
            # === PROCESAMIENTO AVANZADO (Phase 1) ===
            'filtrar_dataframe': {'enabled': True, 'backend_id': 'filtrar_dataframe'},
            'transformar_columnas': {'enabled': True, 'backend_id': 'transformar_columnas'},
            'agrupar_datos': {'enabled': True, 'backend_id': 'agrupar_datos'},
            'eliminar_duplicados': {'enabled': True, 'backend_id': 'eliminar_duplicados'},
            'ordenar_avanzado': {'enabled': True, 'backend_id': 'ordenar_avanzado'},
            'pivotar_tabla': {'enabled': True, 'backend_id': 'pivotar_tabla'},
            'calcular_estadisticas': {'enabled': True, 'backend_id': 'calcular_estadisticas'},
            'normalizar_datos': {'enabled': True, 'backend_id': 'normalizar_datos'},
            'unir_datasets': {'enabled': True, 'backend_id': 'unir_datasets'},
            'concatenar_datasets': {'enabled': True, 'backend_id': 'concatenar_datasets'},
            'validar_datos': {'enabled': True, 'backend_id': 'validar_datos'},
            
            # === FINALIZACION ===
            'finalizar_todo': {'enabled': True, 'backend_id': 'finalizar_todo_action'},
        }
    return _ACTION_CONFIG


def enable_actions(*action_ids):
    """
    Función auxiliar para habilitar acciones específicas.
    
    Args:
        *action_ids: IDs de acciones a habilitar
    """
    config = get_action_config()
    for action_id in action_ids:
        if action_id in config:
            config[action_id]['enabled'] = True
            print(f"[ACTIONS] Habilitada: {action_id}")
        else:
            print(f"[ACTIONS] WARNING: Acción no encontrada: {action_id}")


def disable_actions(*action_ids):
    """
    Función auxiliar para deshabilitar acciones específicas.
    
    Args:
        *action_ids: IDs de acciones a deshabilitar
    """
    config = get_action_config()
    for action_id in action_ids:
        if action_id in config:
            config[action_id]['enabled'] = False
            print(f"[ACTIONS] Deshabilitada: {action_id}")
        else:
            print(f"[ACTIONS] WARNING: Acción no encontrada: {action_id}")


def get_enabled_types():
    """
    Obtiene los tipos habilitados para el frontend con mapeo de IDs.
    Mantiene la separación entre backend y frontend.
    
    Returns:
        list: Lista de IDs de acciones habilitadas para el frontend
    """
    # Obtener todas las acciones registradas
    ActionRegistry.auto_discover_actions()  # Forzar auto-descubrimiento
    all_backend_actions = list(ActionRegistry._actions.keys())
    
    # Obtener configuración
    config = get_action_config()
    
    # Filtrar solo las acciones habilitadas que existen en el backend
    frontend_ids = []
    for frontend_id, settings in config.items():
        if not settings['enabled']:
            continue
            
        backend_id = settings['backend_id']
        if backend_id in all_backend_actions:
            frontend_ids.append(frontend_id)
        # else:
        #     print(f"[WARNING] Acción {frontend_id} -> {backend_id} no encontrada en backend")
    
    # Ordenar alfabéticamente para consistencia
    frontend_ids.sort()
    
    print(f"[ENABLED_TYPES] Total backend: {len(all_backend_actions)}, Habilitadas frontend: {len(frontend_ids)}")
    print(f"[ENABLED_TYPES] IDs enviados al frontend: {frontend_ids}")
    
    return frontend_ids


def get_action_icon_type(action_id):
    """
    Determina el tipo de icono para una acción basado en su ID.
    
    Args:
        action_id (str): ID de la acción
        
    Returns:
        str: Tipo de icono ('triangle', 'circle', 'square', etc.)
    """
    # Funciones de control - triángulos
    if any(keyword in action_id for keyword in ['condicional', 'bucle', 'repetir', 'try_catch', 'validar_variable']):
        return 'triangle'
    
    # Funciones de tiempo - rombo
    elif any(keyword in action_id for keyword in ['pausa', 'delay', 'esperar', 'programar']):
        return 'diamond'
    
    # Funciones de datos - círculos
    elif any(keyword in action_id for keyword in ['variable', 'leer', 'escribir', 'datos']):
        return 'circle'
    
    # Funciones de archivos - cuadrados
    elif any(keyword in action_id for keyword in ['archivo', 'carpeta', 'dialogo']):
        return 'square'
    
    # Funciones de procesamiento - hexágonos
    elif any(keyword in action_id for keyword in ['filtrar', 'transformar', 'agrupar', 'calcular', 'normalizar']):
        return 'hexagon'
    
    # Por defecto - círculo
    else:
        return 'circle'


# =============================================================================
# EJEMPLOS DE USO PARA HABILITAR/DESHABILITAR ACCIONES
# =============================================================================

def enable_web_actions():
    """Habilita todas las acciones web (navegación)"""
    enable_actions('abrir_pagina', 'cambiar_pagina', 'maximizar_navegador', 'cerrar_navegador')

def disable_web_actions():
    """Deshabilita todas las acciones web (navegación)"""
    disable_actions('abrir_pagina', 'cambiar_pagina', 'maximizar_navegador', 'cerrar_navegador')

def enable_advanced_processing():
    """Habilita solo procesamiento avanzado"""
    enable_actions('filtrar_dataframe', 'transformar_columnas', 'agrupar_datos', 
                  'calcular_estadisticas', 'normalizar_datos', 'unir_datasets')

def enable_basic_only():
    """Habilita solo funciones básicas"""
    config = get_action_config()
    # Deshabilitar todo primero
    for action_id in config.keys():
        disable_actions(action_id)
    
    # Habilitar solo básicas
    enable_actions('variable_set', 'variable_get', 'pausa', 'condicional_si', 'bucle_mientras',
                  'leer_csv', 'escribir_csv', 'carpeta_crear', 'dialogo_seleccionar_archivo')
