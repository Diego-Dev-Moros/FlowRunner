# index.py
import os
import json
import shutil
import eel
from eel import browsers
from modules.funciones.extras import run_flow as engine_run_flow  # motor de ejecución
import modules.config as appcfg

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
    result = engine_run_flow(flow, notifier=_notify)
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
        enabled = getattr(appcfg, 'ENABLED_TYPES', set()) or set()
        return list(enabled)
    except Exception:
        return []

# -------------------------
# Navegador: CHROME (app) -> EDGE (app) -> normal -> sin navegador
# -------------------------
def _which_browser():
    pf   = os.environ.get('ProgramFiles', r"C:\Program Files")
    pf86 = os.environ.get('ProgramFiles(x86)', r"C:\Program Files (x86)")
    lad  = os.environ.get('LOCALAPPDATA', os.path.expanduser(r"~\AppData\Local"))

    chrome = next((p for p in [
        os.path.join(pf,   r"Google\Chrome\Application\chrome.exe"),
        os.path.join(pf86, r"Google\Chrome\Application\chrome.exe"),
        os.path.join(lad,  r"Google\Chrome\Application\chrome.exe"),
        shutil.which("chrome"),
        shutil.which("chrome.exe"),
    ] if p and os.path.exists(p)), None)

    edge = next((p for p in [
        os.path.join(pf,   r"Microsoft\Edge\Application\msedge.exe"),
        os.path.join(pf86, r"Microsoft\Edge\Application\msedge.exe"),
        shutil.which("msedge"),
        shutil.which("msedge.exe"),
    ] if p and os.path.exists(p)), None)

    return {"chrome": chrome, "edge": edge}

def _register_paths(paths):
    if paths.get("chrome"):
        browsers.set_path('chrome', paths["chrome"])
        browsers.set_path('chrome-app', paths["chrome"])  # modo app
    if paths.get("edge"):
        browsers.set_path('edge', paths["edge"])
        browsers.set_path('edge-app', paths["edge"])      # modo app

if __name__ == '__main__':
    page = 'vistas/servicio.html'
    host = 'localhost'
    port = 8000
    size = (1280, 800)

    paths = _which_browser()
    _register_paths(paths)

    modes = []
    if paths.get("chrome"): modes += ['chrome-app', 'chrome']
    if paths.get("edge"):   modes += ['edge-app',   'edge']
    modes.append(None)  # servir sin abrir navegador

    for mode in modes:
        try:
            if mode is None:
                print(f"[INFO] Sin navegador. Abrí manualmente: http://{host}:{port}/{page}")
            else:
                print(f"[INFO] Intentando abrir en modo: {mode}")
            eel.start(page, mode=mode, size=size, host=host, port=port, block=True)
            break
        except OSError as e:
            print(f"[WARN] Falló {mode}: {e}")
            continue
