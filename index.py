# index.py
import os
import json
import eel
from modules.core import FlowExecutor, ActionRegistry
import modules.actions  # Esto iniciará el auto-registro
from modules.browser_config import create_browser_config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
eel.init(BASE_DIR, allowed_extensions=['.js', '.html', '.css'])

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
