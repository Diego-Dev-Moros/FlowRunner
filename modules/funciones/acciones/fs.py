# modules/funciones/acciones/fs.py
from __future__ import annotations
from typing import Any, Dict, Optional

try:
    from modules.funciones.archivos import gestor as mod_gestor
except Exception:
    mod_gestor = None

def archivo_mover(origen: str, destino: str, si_existe: str = "sobrescribir"):
    if mod_gestor and hasattr(mod_gestor, "archivo_mover"):
        out = mod_gestor.archivo_mover(origen, destino, si_existe)
    else:
        import os, shutil
        d = os.path.dirname(destino)
        if d and not os.path.exists(d): os.makedirs(d, exist_ok=True)
        if os.path.exists(destino):
            if si_existe == "sobrescribir":
                if os.path.isdir(destino): shutil.rmtree(destino)
                else: os.remove(destino)
            elif si_existe == "omitir":
                raise FileExistsError(destino)
            elif si_existe == "renombrar":
                base, ext = os.path.splitext(destino); i = 2
                while os.path.exists(f"{base}_{i}{ext}"): i += 1
                destino = f"{base}_{i}{ext}"
        shutil.move(origen, destino)
        out = destino
    return {"status": "OK", "message": "Archivo movido", "preview": out}

def archivo_copiar(origen: str, destino: str, si_existe: str = "sobrescribir"):
    if mod_gestor and hasattr(mod_gestor, "archivo_copiar"):
        out = mod_gestor.archivo_copiar(origen, destino, si_existe)
    else:
        import os, shutil
        d = os.path.dirname(destino)
        if d and not os.path.exists(d): os.makedirs(d, exist_ok=True)
        if os.path.exists(destino):
            if si_existe == "sobrescribir":
                if os.path.isdir(destino): shutil.rmtree(destino)
                else: os.remove(destino)
            elif si_existe == "omitir":
                raise FileExistsError(destino)
            elif si_existe == "renombrar":
                base, ext = os.path.splitext(destino); i = 2
                while os.path.exists(f"{base}_{i}{ext}"): i += 1
                destino = f"{base}_{i}{ext}"
        shutil.copy2(origen, destino)
        out = destino
    return {"status": "OK", "message": "Archivo copiado", "preview": out}

def archivo_borrar(ruta: str):
    if mod_gestor and hasattr(mod_gestor, "archivo_borrar"):
        mod_gestor.archivo_borrar(ruta)
    else:
        import os, shutil
        if os.path.isdir(ruta): shutil.rmtree(ruta, ignore_errors=True)
        elif os.path.exists(ruta): os.remove(ruta)
    return {"status": "OK", "message": "Archivo/Carpeta borrado", "preview": ""}

def carpeta_crear(ruta: str):
    if mod_gestor and hasattr(mod_gestor, "carpeta_crear"):
        out = mod_gestor.carpeta_crear(ruta, True)
    else:
        import os
        os.makedirs(ruta, exist_ok=True)
        out = ruta
    return {"status": "OK", "message": "Carpeta creada", "preview": out}

def carpeta_listar(ruta: str, patron: str = "*", contexto: Dict[str, Any] | None = None,
                   nombre_personalizado: Optional[str] = None):
    if mod_gestor and hasattr(mod_gestor, "carpeta_listar"):
        lst = mod_gestor.carpeta_listar(ruta, patron)
    else:
        import os, glob
        lst = sorted(glob.glob(os.path.join(ruta, patron)))
    var = nombre_personalizado or "lista_1"
    if contexto is not None:
        # contador simple
        cnts = contexto.setdefault("_contadores", {})
        if nombre_personalizado is None:
            cnts["lista"] = int(cnts.get("lista", 0)) + 1
            var = f"lista_{cnts['lista']}"
        contexto[var] = lst
        contexto["last_list"] = lst
    return {"status": "OK", "message": f"{len(lst)} ítems → {var}", "preview": "\n".join(lst[:50])}
