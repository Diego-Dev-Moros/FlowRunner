# modules/funciones/acciones/web.py
from __future__ import annotations
from typing import Any, Dict

try:
    from modules.funciones.navegador import navegador as mod_nav
except Exception:
    mod_nav = None

def abrir_pagina(url: str):
    if not mod_nav:
        raise RuntimeError("Navegador no disponible.")
    drv = mod_nav.abrir_pagina_web_selenium(url)
    return {"status": "OK", "message": f"Abrir {url}", "preview": "", "driver": drv}

def cambiar_pagina(driver: Any, url: str):
    if not mod_nav:
        raise RuntimeError("Navegador no disponible.")
    mod_nav.cambiar_pagina_web_selenium(driver, url)
    return {"status": "OK", "message": f"URL -> {url}", "preview": ""}

def cerrar_navegador(driver: Any):
    if not mod_nav:
        raise RuntimeError("Navegador no disponible.")
    mod_nav.cerrar_navegador_selenium(driver)
    return {"status": "OK", "message": "Navegador cerrado", "preview": ""}

def maximizar(driver: Any):
    if not mod_nav:
        raise RuntimeError("Navegador no disponible.")
    mod_nav.maximizar_navegador(driver)
    return {"status": "OK", "message": "Ventana maximizada", "preview": ""}
