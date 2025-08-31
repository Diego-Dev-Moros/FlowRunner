# index.py
import os, json, eel
from modules.funciones.extras import run_flow as engine_run_flow  # 👈 renombrado

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
    result = engine_run_flow(flow, notifier=_notify)  # 👈 usamos el motor renombrado
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

if __name__ == '__main__':
    eel.start('vistas/servicio.html', size=(1280, 800), host='localhost', port=8000, block=True)