# modules/funciones/acciones/fs.py
from __future__ import annotations
from typing import Optional, List
import os
import glob
import shutil


def carpeta_listar(ctx, ruta: str, patron: str = "*", nombre_personalizado: Optional[str] = None):
    """
    Lista archivos/carpetas según patrón y guarda el resultado en el contexto.
    - Guarda con prefijo 'carpeta_' (p.ej. 'carpeta_1')
    - Devuelve dict con preview para UI.
    """
    ruta = os.path.expanduser(ruta or ".")
    patron = patron or "*"

    # Asegura ruta válida (si no existe, lista vacía)
    if not os.path.exists(ruta):
        paths: List[str] = []
    else:
        paths = sorted(glob.glob(os.path.join(ruta, patron)))

    nombre_var = ctx.asignar_variable("carpeta", paths, nombre_personalizado)
    # Por compatibilidad con lógicas existentes
    ctx.variables["last_list"] = nombre_var

    # Preview para la UI (primeros 10 elementos)
    sample = paths[:10]
    return {
        "variable": nombre_var,
        "count": len(paths),
        "sample": sample,
    }


def carpeta_crear(_ctx, ruta: str):
    """Crea carpeta si no existe (idempotente)."""
    ruta = os.path.expanduser(ruta or ".")
    os.makedirs(ruta, exist_ok=True)
    return {"created": True, "path": ruta}


def archivo_mover(_ctx, origen: str, destino: str, si_existe: str = "sobrescribir"):
    """
    Mueve archivo.
    si_existe: sobrescribir | renombrar | omitir
    """
    origen = os.path.expanduser(origen or "")
    destino = os.path.expanduser(destino or "")
    if not origen or not os.path.exists(origen):
        raise FileNotFoundError(f"Origen no existe: {origen}")
    if not destino:
        raise ValueError("Destino vacío.")

    # Crear carpeta destino
    ddir = destino if os.path.isdir(destino) else os.path.dirname(destino)
    if ddir:
        os.makedirs(ddir, exist_ok=True)

    dst = _resolver_conflicto(destino, si_existe)
    if dst is None:
        return {"moved": False, "reason": "omitido", "dest": destino}

    shutil.move(origen, dst)
    return {"moved": True, "from": origen, "to": dst}


def archivo_copiar(_ctx, origen: str, destino: str, si_existe: str = "sobrescribir"):
    origen = os.path.expanduser(origen or "")
    destino = os.path.expanduser(destino or "")
    if not origen or not os.path.exists(origen):
        raise FileNotFoundError(f"Origen no existe: {origen}")
    if not destino:
        raise ValueError("Destino vacío.")

    ddir = destino if os.path.isdir(destino) else os.path.dirname(destino)
    if ddir:
        os.makedirs(ddir, exist_ok=True)

    dst = _resolver_conflicto(destino, si_existe)
    if dst is None:
        return {"copied": False, "reason": "omitido", "dest": destino}

    shutil.copy2(origen, dst)
    return {"copied": True, "from": origen, "to": dst}


def archivo_borrar(_ctx, ruta: str):
    ruta = os.path.expanduser(ruta or "")
    if not ruta:
        raise ValueError("Ruta vacía.")
    if os.path.isdir(ruta):
        shutil.rmtree(ruta, ignore_errors=True)
        return {"deleted_dir": True, "path": ruta}
    if os.path.exists(ruta):
        os.remove(ruta)
        return {"deleted": True, "path": ruta}
    return {"deleted": False, "reason": "no_exists", "path": ruta}


def _resolver_conflicto(destino: str, modo: str):
    """
    - sobrescribir: usa destino tal cual (y si existe, lo reemplaza)
    - renombrar: genera destino (1), (2), ... si ya existe
    - omitir: si ya existe, retorna None
    """
    if modo not in {"sobrescribir", "renombrar", "omitir"}:
        modo = "sobrescribir"

    if not os.path.exists(destino):
        return destino

    if modo == "sobrescribir":
        return destino
    if modo == "omitir":
        return None
    # renombrar
    base, ext = os.path.splitext(destino)
    i = 1
    while True:
        cand = f"{base} ({i}){ext}"
        if not os.path.exists(cand):
            return cand
        i += 1
