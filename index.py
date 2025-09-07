# index.py
import os
import json
import eel
from modules.core import FlowExecutor, ActionRegistry
import modules.actions  # Esto iniciará el auto-registro
from modules.browser_config import create_browser_config
from modules.utils.logging import FlowLogger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
eel.init(BASE_DIR, allowed_extensions=['.js', '.html', '.css'])

# Inicializar logger
logger = FlowLogger()

def _notify(payload):
    try:
        eel.notify_progress(payload)
    except Exception:
        pass

@eel.expose
def log_frontend_error(error_data):
    """Log errores del frontend al sistema de logging"""
    try:
        logger.log_error(
            error=f"[FRONTEND] {error_data.get('message', 'Error desconocido')}",
            context={
                'error_type': error_data.get('type', 'frontend_error'),
                'filename': error_data.get('filename'),
                'line': error_data.get('line'),
                'column': error_data.get('column'),
                'stack': error_data.get('stack'),
                'url': error_data.get('url'),
                'timestamp': error_data.get('timestamp')
            }
        )
        return True
    except Exception as e:
        print(f"Error al registrar error del frontend: {e}")
        return False

@eel.expose
def log_frontend_warning(warning_data):
    """Log warnings del frontend al sistema de logging"""
    try:
        logger.log_user(
            f"[FRONTEND WARNING] {warning_data.get('message', 'Warning desconocido')}",
            level="WARNING",
            context={
                'type': warning_data.get('type', 'frontend_warning'),
                'url': warning_data.get('url'),
                'timestamp': warning_data.get('timestamp')
            }
        )
        return True
    except Exception as e:
        print(f"Error al registrar warning del frontend: {e}")
        return False

def _notify(payload):
    try:
        eel.notify_progress(payload)
    except Exception:
        pass

@eel.expose
def run_flow(flow):
    print('RUN_FLOW <-', json.dumps(flow, indent=2, ensure_ascii=False))
    
    # Usar el nuevo executor
    executor = FlowExecutor(notifier=_notify)
    result = executor.execute_flow(flow)
    
    print('RUN_FLOW ->', json.dumps(result, indent=2, ensure_ascii=False))
    return result

@eel.expose
def export_flow(flow):
    out = os.path.join(BASE_DIR, 'flujo_exportado.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(flow, f, ensure_ascii=False, indent=2)
    print(f'Flujo exportado a: {out}')
    return True

@eel.expose
def cancel_run():
    print('CANCEL_RUN solicitado (pendiente)')
    return True

@eel.expose
def pause_run():
    print('PAUSE_RUN (pendiente)')
    return True

@eel.expose
def get_enabled_types():
    try:
        # Asegurar que el auto-descubrimiento esté completo
        if not ActionRegistry._initialized:
            ActionRegistry.auto_discover_actions()
        
        # ENABLED_TYPES: Whitelist de acciones habilitadas para producción
        # Estos IDs deben coincidir EXACTAMENTE con los IDs del catálogo frontend
        ENABLED_TYPES = {
            # === DATOS BÁSICOS ===
            'variable_set', 'variable_get', 'ordenar_info',
            
            # === LECTURA ===
            'excel_leer_rango', 'carpeta_listar',
            
            # === ESCRITURA ===
            'escribir_csv', 'escribir_excel', 'escribir_txt',
            
            # === ARCHIVOS ===
            'carpeta_crear', 'archivo_mover', 'archivo_copiar', 'archivo_borrar',
            
            # === DIALOGOS ===
            'dialogo_seleccionar_archivo', 'dialogo_seleccionar_carpeta',
            
            # === CONTROL BÁSICO ===
            'pausa',
            
            # === CONTROL DE FLUJO AVANZADO (Phase 2) ===
            'bucle_for_rango', 'bucle_for_lista', 'repetir_hasta', 'interrumpir_flujo',
            'condicional_multiple', 'condicional_and_or', 'esperar_condicion',
            'try_catch_finally', 'validar_variable',
            'delay_dinamico', 'esperar_hasta_hora', 'programar_ejecucion',
            
            # === PROCESAMIENTO AVANZADO (Phase 1) ===
            'filtrar_dataframe', 'transformar_columnas', 'agrupar_datos', 
            'eliminar_duplicados', 'ordenar_avanzado', 'pivotar_tabla',
            'calcular_estadisticas', 'normalizar_datos', 'unir_datasets',
            'concatenar_datasets', 'validar_datos',
            
            # === FINALIZACION ===
            'finalizar_todo'
        }
        
        # Obtener todas las acciones registradas
        all_actions = ActionRegistry.get_enabled_types()
        
        # El catálogo frontend usa IDs diferentes que el backend
        # Necesitamos mapear los IDs del backend a los del frontend
        BACKEND_TO_FRONTEND_MAP = {
            # Variables  
            'variables_listar': 'ordenar_info',  # aproximación
            
            # Lectura
            'excel_leer_rango_action': 'excel_leer_rango',
            'carpeta_listar_action': 'carpeta_listar',
            
            # Escritura
            'escribir_csv_action': 'escribir_csv',
            'escribir_excel_action': 'escribir_excel', 
            'escribir_txt_action': 'escribir_txt',
            
            # Archivos
            'crear_carpeta_action': 'carpeta_crear',
            'mover_archivo_action': 'archivo_mover',
            'copiar_archivo_action': 'archivo_copiar',
            'eliminar_archivo_action': 'archivo_borrar',
            
            # Finalización
            'finalizar_todo_action': 'finalizar_todo'
        }
        
        # Convertir IDs de backend a frontend cuando sea necesario
        frontend_actions = []
        processed_ids = set()  # Para evitar duplicados
        
        for backend_id in all_actions:
            frontend_id = BACKEND_TO_FRONTEND_MAP.get(backend_id, backend_id)
            if frontend_id in ENABLED_TYPES and frontend_id not in processed_ids:
                frontend_actions.append(frontend_id)
                processed_ids.add(frontend_id)
        
        # También incluir los que ya coinciden directamente
        for action in all_actions:
            if action in ENABLED_TYPES and action not in processed_ids:
                frontend_actions.append(action)
                processed_ids.add(action)
        
        print(f"[ENABLED_TYPES] Total backend: {len(all_actions)}, Habilitadas frontend: {len(frontend_actions)}")
        print(f"[ENABLED_TYPES] IDs enviados al frontend: {sorted(frontend_actions)}")
        
        return frontend_actions
        
    except Exception as e:
        print(f"Error obteniendo tipos habilitados: {e}")
        # Fallback: devolver lista vacía
        return []

# -------------------------
# Configuración de navegador modularizada
# -------------------------

if __name__ == '__main__':
    page = 'vistas/servicio.html'
    host = 'localhost'
    port = 8000
    size = (1280, 800)

    # Usar el nuevo sistema de configuración de navegador
    browser_config = create_browser_config()
    
    print("[INFO] Iniciando FlowRunner...")
    print(f"[INFO] Navegadores detectados: {list(browser_config.detected_browsers.keys())}")
    
    success, mode_used = browser_config.launch_app(page, host, port, size)
    
    if success:
        if mode_used.endswith('-app'):
            print(f"[SUCCESS] FlowRunner iniciado en modo aplicación: {mode_used}")
        elif mode_used in ['chrome', 'edge']:
            print(f"[SUCCESS] FlowRunner iniciado en modo pestaña: {mode_used}")
        elif mode_used == 'server-only':
            print(f"[SUCCESS] Servidor iniciado. Abrir manualmente: http://{host}:{port}/{page}")
    else:
        print("[ERROR] No se pudo iniciar FlowRunner")
        input("Presiona Enter para salir...")
