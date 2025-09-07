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
            message=f"[FRONTEND] {error_data.get('message', 'Error desconocido')}",
            error_type=error_data.get('type', 'frontend_error'),
            context={
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
        logger.log_user_activity(
            f"[FRONTEND WARNING] {warning_data.get('message', 'Warning desconocido')}",
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
        # Usar el nuevo registry para obtener todos los tipos registrados
        return ActionRegistry.get_enabled_types()
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

    # HOTFIX #4: Recuperar modo app con secuencia optimizada
    print("[INFO] Iniciando FlowRunner...")
    
    # Usar el nuevo sistema de configuración de navegador
    browser_config = create_browser_config()
    print(f"[INFO] Navegadores detectados: {list(browser_config.detected_browsers.keys())}")
    
    success, mode_used = browser_config.launch_app(page, host, port, size)
    
    if success:
        if mode_used.endswith('-app'):
            print(f"[SUCCESS] ✅ FlowRunner iniciado en modo aplicación: {mode_used}")
        elif mode_used in ['chrome', 'edge']:
            print(f"[SUCCESS] ✅ FlowRunner iniciado en modo pestaña: {mode_used}")
        elif mode_used == 'server-only':
            print(f"[SUCCESS] ✅ Servidor iniciado. Abrir manualmente: http://{host}:{port}/{page}")
            print("[INFO] 💡 Tip: Instala Chrome o Edge para modo aplicación automático")
    else:
        print("[ERROR] ❌ No se pudo iniciar FlowRunner")
        print("[INFO] Verifica que Chrome/Edge estén instalados o accede manualmente al servidor")
        input("Presiona Enter para salir...")
