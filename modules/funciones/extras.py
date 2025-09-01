# modules/funciones/extras.py
from __future__ import annotations
from typing import Any, Dict, List, Optional
import traceback

# acciones por dominio
from modules.funciones.acciones import control as act_ctrl
from modules.funciones.acciones import dialogos_wrappers as act_dlg
from modules.funciones.acciones import io_read as act_read
from modules.funciones.acciones import io_write as act_write
from modules.funciones.acciones import fs as act_fs
try:
    from modules.funciones.acciones import web as act_web
except Exception:
    act_web = None

# ---- lista de acciones web que pueden bloquearse en modo local ----
BLOCKABLE_WEB = {"abrir_pagina","cambiar_pagina","cerrar_navegador","maximizar_app","hacer_clic"}

def topological_order(steps: List[Dict[str, Any]], edges: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    if not edges: return steps
    id_to_step = {s['id']: s for s in steps}
    indeg = {s['id']: 0 for s in steps}
    adj = {s['id']: [] for s in steps}
    for e in edges:
        f, t = e.get('from'), e.get('to')
        if f in id_to_step and t in id_to_step:
            adj[f].append(t); indeg[t] += 1
    from collections import deque
    q = deque([sid for sid, d in indeg.items() if d == 0])
    out_ids = []
    while q:
        u = q.popleft(); out_ids.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    if len(out_ids) != len(steps):  # ciclo → orden original
        return steps
    return [id_to_step[i] for i in out_ids]

def _notify(notifier, step_id: str, typ: str, msg: str, preview: str = "", status: str | None = None):
    if notifier:
        try:
            payload = {"stepId": step_id, "type": typ, "message": msg}
            if preview is not None: payload["preview"] = preview
            if status: payload["status"] = status
            else:
                payload["status"] = "OK" if typ == "ok" else "ERROR" if typ == "err" else "WARNING" if typ == "warn" else "LOG"
            notifier(payload)
        except Exception:
            pass

def run_flow(flow: Dict[str, Any], notifier=None) -> Dict[str, Any]:
    steps = list(flow.get("steps") or [])
    edges = list(flow.get("edges") or [])
    order = topological_order(steps, edges)
    ctx: Dict[str, Any] = {}
    driver = None

    try:
        for step in order:
            sid = step.get("id")
            tid = step.get("typeId")
            props = step.get("props") or {}

            # bloqueo local
            if str(props.get("bloqueado","no")).lower() in ("si","sí","true","1") and tid in BLOCKABLE_WEB:
                _notify(notifier, sid, "warn", f"{tid} bloqueado (modo local).", "")
                continue

            _notify(notifier, sid, "log", f"Ejecutando {tid}...")

            # --- dispatch por typeId ---
            if tid == "pausa":
                res = act_ctrl.pausa(props.get("segundos"), props.get("ms"), ctx)

            elif tid == "variable_set":
                res = act_ctrl.variable_set(props["nombre"], props.get("valor"), ctx)

            elif tid == "variable_get":
                res = act_ctrl.variable_get(props["nombre"], ctx)

            elif tid == "dialogo_seleccionar_archivo":
                res = act_dlg.seleccionar_archivo(props.get("titulo"), props.get("guardar_en","archivo_seleccionado"), ctx)

            elif tid == "dialogo_seleccionar_carpeta":
                res = act_dlg.seleccionar_carpeta(props.get("titulo"), props.get("guardar_en","carpeta_seleccionada"), ctx)

            # ---- Lectura
            elif tid == "leer_csv":
                res = act_read.leer_csv(props["ruta"], ctx, props.get("nombre_personalizado"))

            elif tid == "leer_excel":
                res = act_read.leer_excel(props["ruta"], props["hoja"], ctx, props.get("nombre_personalizado"))

            elif tid == "leer_txt":
                # acepta 'delimitador'
                res = act_read.leer_txt(props["ruta"], props["delimitador"], ctx, props.get("nombre_personalizado"))

            elif tid == "excel_leer_rango":
                res = act_read.excel_leer_rango(
                    props["ruta"], props["hoja"], ctx,
                    props.get("rango"), props.get("columnas"), props.get("nombre_personalizado")
                )

            # ---- Escritura
            elif tid in ("escribir_excel", "excel_escribir"):
                res = act_write.escribir_excel(
                    props["variable"], props["ruta"], ctx,
                    hoja=props.get("hoja","Sheet1"), modo=props.get("modo","sobrescribir"),
                    inicio_celda=props.get("inicio_celda"), incluir_cabeceras=props.get("incluir_cabeceras","sí")
                )

            elif tid == "escribir_csv":
                res = act_write.escribir_csv(props["variable"], props["ruta"], ctx)

            elif tid == "excel_crear_hoja":
                res = act_write.excel_crear_hoja(props["ruta"], props["nombre_hoja"], props.get("si_existe","reemplazar"))

            # ---- Archivos/Carpetas
            elif tid == "archivo_mover":
                res = act_fs.archivo_mover(props["origen"], props["destino"], props.get("si_existe","sobrescribir"))

            elif tid == "archivo_copiar":
                res = act_fs.archivo_copiar(props["origen"], props["destino"], props.get("si_existe","sobrescribir"))

            elif tid == "archivo_borrar":
                res = act_fs.archivo_borrar(props["ruta"])

            elif tid == "carpeta_crear":
                res = act_fs.carpeta_crear(props["ruta"])

            elif tid == "carpeta_listar":
                res = act_fs.carpeta_listar(props["ruta"], props.get("patron","*"), ctx, props.get("nombre_personalizado"))

            # ---- Web/Selenium (opcional)
            elif tid == "abrir_pagina":
                if not act_web: raise RuntimeError("Navegador no disponible.")
                res = act_web.abrir_pagina(props["url"])
                driver = res.get("driver", driver)

            elif tid == "cambiar_pagina":
                if not driver: raise RuntimeError("No hay driver")
                res = act_web.cambiar_pagina(driver, props["url"])

            elif tid == "cerrar_navegador":
                if not driver:
                    res = {"status": "WARNING", "message": "No hay navegador para cerrar", "preview": ""}
                else:
                    res = act_web.cerrar_navegador(driver)
                    driver = None

            elif tid == "maximizar_app":
                if not driver: raise RuntimeError("No hay driver")
                res = act_web.maximizar(driver)

            else:
                res = {"status":"ALERT","message":f"Función no implementada: {tid}","preview":""}

            _notify(notifier, sid, "ok" if res.get("status","OK")=="OK" else "warn", res.get("message","OK"), res.get("preview",""), res.get("status"))

        # fin for
        # cierre suave
        if driver and act_web:
            try:
                act_web.cerrar_navegador(driver)
            except Exception:
                pass
        return {"ok": True, "variables": list(ctx.keys())}

    except Exception as e:
        if driver and act_web:
            try: act_web.cerrar_navegador(driver)
            except Exception: pass
        return {"ok": False, "error": str(e), "traceback": traceback.format_exc(limit=12)}
