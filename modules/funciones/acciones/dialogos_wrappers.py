# modules/funciones/acciones/dialogos_wrappers.py
from __future__ import annotations
from typing import Any, Dict, Optional

try:
    from modules.funciones import dialogos as sys_dialogs
except Exception:
    sys_dialogs = None

def seleccionar_archivo(titulo: Optional[str] = None, guardar_en: str = "archivo_seleccionado",
                        contexto: Dict[str, Any] | None = None):
    path = ""
    if sys_dialogs:
        try:
            path = sys_dialogs.seleccionar_archivo(titulo or "Seleccionar archivo")
        except Exception:
            path = ""
    if contexto is not None:
        contexto[guardar_en] = path
    return {"status": "OK", "message": path or "cancelado", "preview": path}

def seleccionar_carpeta(titulo: Optional[str] = None, guardar_en: str = "carpeta_seleccionada",
                        contexto: Dict[str, Any] | None = None):
    path = ""
    if sys_dialogs:
        try:
            path = sys_dialogs.seleccionar_carpeta(titulo or "Seleccionar carpeta")
        except Exception:
            path = ""
    if contexto is not None:
        contexto[guardar_en] = path
    return {"status": "OK", "message": path or "cancelado", "preview": path}
