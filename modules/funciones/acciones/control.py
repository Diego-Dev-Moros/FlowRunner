# modules/funciones/acciones/control.py
from __future__ import annotations
from typing import Any, Dict, Optional
import time

def pausa(segundos: Optional[float] = None, ms: Optional[int] = None, contexto: Dict[str, Any] | None = None):
    secs = float(segundos) if segundos is not None else (float(ms or 0) / 1000.0)
    if secs < 0: secs = 0.0
    time.sleep(secs)
    return {"status": "OK", "message": f"Pausa {secs:.2f}s", "preview": ""}

def variable_set(nombre: str, valor: Any, contexto: Dict[str, Any]):
    contexto[nombre] = valor
    return {"status": "OK", "message": f"Set {nombre}", "preview": str(valor)}

def variable_get(nombre: str, contexto: Dict[str, Any]):
    val = contexto.get(nombre)
    return {"status": "OK", "message": f"Get {nombre} -> {val}", "preview": str(val)}
