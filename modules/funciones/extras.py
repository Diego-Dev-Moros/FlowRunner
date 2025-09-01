# modules/funciones/extras.py
from __future__ import annotations
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
import traceback

# Acciones modulares
from modules.funciones.acciones import fs as act_fs
from modules.funciones.acciones import io_read as act_read
from modules.funciones.acciones import io_write as act_write
from modules.funciones.acciones import web as act_web
from modules.funciones.acciones import control as act_ctl

# Para cerrar navegador si quedó abierto
from modules.funciones.navegador import navegador as mod_nav


# ==============================
# Contexto de ejecución
# ==============================
class ContextoEjecucion:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        # contadores para prefijos
        self.contadores = {
            "csv": 0,
            "excel": 0,
            "txt": 0,
            "carpeta": 0,
            "lista": 0,
        }
        self.driver = None  # para Selenium, si lo usas

    def asignar_variable(self, tipo: str, valor: Any, nombre_personalizado: Optional[str] = None) -> str:
        if nombre_personalizado:
            nombre = nombre_personalizado
        else:
            self.contadores[tipo] = self.contadores.get(tipo, 0) + 1
            nombre = f"{tipo}_{self.contadores[tipo]}"
        self.variables[nombre] = valor
        return nombre

    def obtener_variable(self, nombre: str):
        return self.variables.get(nombre)

    def listar_variables(self):
        return list(self.variables.keys())

    def cerrar(self):
        # Cierra recursos (navegador, etc.)
        try:
            if self.driver:
                mod_nav.cerrar_navegador_selenium(self.driver)
        except Exception:
            pass
        self.driver = None


# ==============================
# Utilidades de orden (edges)
# ==============================
def topological_order(steps: List[Dict[str, Any]], edges: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Devuelve steps en orden topológico según edges. Si hay ciclo o edges vacíos, retorna steps como vinieron."""
    if not edges:
        return steps
    id_to_step = {s['id']: s for s in steps}
    indeg: Dict[str, int] = {s['id']: 0 for s in steps}
    adj: Dict[str, List[str]] = {s['id']: [] for s in steps}
    for e in edges:
        if e['from'] in id_to_step and e['to'] in id_to_step:
            adj[e['from']].append(e['to'])
            indeg[e['to']] += 1

    from collections import deque
    q = deque([sid for sid, d in indeg.items() if d == 0])
    ordered_ids: List[str] = []
    while q:
        u = q.popleft()
        ordered_ids.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(ordered_ids) != len(steps):
        return steps
    return [id_to_step[i] for i in ordered_ids]


# ==============================
# Dispatcher (typeId → callable)
# ==============================
def build_dispatcher() -> Dict[str, Callable[[ContextoEjecucion, Dict[str, Any]], Any]]:
    def not_impl(_ctx: ContextoEjecucion, _p: Dict[str, Any]):
        return {"_": "not_implemented"}

    return {
        # ---- FS ----
        "carpeta_listar": lambda ctx, p: act_fs.carpeta_listar(
            ctx,
            p.get("ruta", ""),
            p.get("patron", "*"),
            p.get("nombre_personalizado"),
        ),
        "carpeta_crear": lambda ctx, p: act_fs.carpeta_crear(ctx, p.get("ruta", "")),
        "archivo_mover": lambda ctx, p: act_fs.archivo_mover(
            ctx, p.get("origen", ""), p.get("destino", ""), p.get("si_existe", "sobrescribir")
        ),
        "archivo_copiar": lambda ctx, p: act_fs.archivo_copiar(
            ctx, p.get("origen", ""), p.get("destino", ""), p.get("si_existe", "sobrescribir")
        ),
        "archivo_borrar": lambda ctx, p: act_fs.archivo_borrar(ctx, p.get("ruta", "")),

        # ---- Lectura (según tus firmas en io_read) ----
        "leer_csv":   lambda ctx, p: act_read.leer_csv(ctx, p.get("ruta", ""), p.get("nombre_personalizado")),
        "leer_excel": lambda ctx, p: act_read.leer_excel(ctx, p.get("ruta", ""), p.get("hoja", ""), p.get("nombre_personalizado")),
        "leer_txt":   lambda ctx, p: act_read.leer_txt_delimitado(ctx, p.get("ruta", ""), p.get("delimitador", ","), p.get("nombre_personalizado")),

        # ---- Escritura ----
        "escribir_csv":   lambda ctx, p: act_write.escribir_csv(ctx, p.get("variable", ""), p.get("ruta", "")),
        "escribir_txt":   lambda ctx, p: act_write.escribir_txt(ctx, p.get("variable", ""), p.get("ruta", ""), p.get("delimitador", ",")),
        "escribir_excel": lambda ctx, p: act_write.escribir_excel(ctx, p.get("variable", ""), p.get("ruta", ""), p.get("hoja", "Hoja1")),

        # ---- Control ----
        "pausa": lambda _ctx, p: act_ctl.pausa(float(p.get("segundos", 0) or 0)),

        # ---- Web/Selenium si lo usas ----
        "abrir_pagina":     lambda ctx, p: _open_and_store_driver(ctx, p.get("url", "")),
        "cambiar_pagina":   lambda ctx, p: act_web.cambiar_pagina_web_selenium(_require_driver(ctx), p.get("url", "")),
        "cerrar_navegador": lambda ctx, _p: _close_and_clear_driver(ctx),
        "maximizar_app":    lambda ctx, _p: act_web.maximizar_navegador(_require_driver(ctx)),
    }


def _open_and_store_driver(ctx: ContextoEjecucion, url: str):
    if ctx.driver:
        try:
            act_web.cambiar_pagina_web_selenium(ctx.driver, url)
            return ctx.driver
        except Exception:
            pass
    ctx.driver = act_web.abrir_pagina_web_selenium(url)
    return ctx.driver


def _require_driver(ctx: ContextoEjecucion):
    if not ctx.driver:
        raise RuntimeError("No hay navegador abierto. Agregá un paso 'Abrir página web' antes.")
    return ctx.driver


def _close_and_clear_driver(ctx: ContextoEjecucion):
    if ctx.driver:
        try:
            act_web.cerrar_navegador_selenium(ctx.driver)
        except Exception:
            pass
    ctx.driver = None


# ==============================
# Motor principal de ejecución
# ==============================
def run_flow(flow: Dict[str, Any], notifier: Optional[Callable[[Dict[str, Any]], None]] = None) -> Dict[str, Any]:
    """
    Ejecuta un flujo {steps:[...], edges:[...]}.
    'notifier' recibe dicts: {'stepId','message','level','preview?'}
    """
    ctx = ContextoEjecucion()
    dispatch = build_dispatcher()

    steps = flow.get("steps", []) or []
    edges = flow.get("edges", []) or []

    ordered_steps = topological_order(steps, edges)
    results: List[Dict[str, Any]] = []

    try:
        for step in ordered_steps:
            sid = step.get("id")
            tid = step.get("typeId")
            nombre = step.get("nombre", tid)
            props = step.get("props", {}) or {}

            _emit(notifier, {"stepId": sid, "message": f"Ejecutando {nombre}...", "level": "info"})

            fn = dispatch.get(tid)
            if not fn:
                raise NotImplementedError(f"Tipo de acción no soportado: {tid}")

            out = fn(ctx, props)

            # Resultado resumido para retorno
            prev = _safe_preview(out)
            results.append({"id": sid, "typeId": tid, "nombre": nombre, "output": prev})

            # Notificar también preview al front (panel derecho)
            _emit(notifier, {"stepId": sid, "message": f"Completado {nombre}", "level": "success", "preview": prev})

        # Limpieza final
        ctx.cerrar()

        return {"ok": True, "results": results, "variables": ctx.listar_variables()}

    except Exception as ex:
        err = "".join(traceback.format_exc())
        try:
            ctx.cerrar()
        except Exception:
            pass
        return {"ok": False, "error": str(ex), "traceback": err, "partial_results": results}


def _safe_preview(out):
    if out is None:
        return None
    try:
        import json
        s = json.dumps(out, ensure_ascii=False)
    except Exception:
        s = str(out)
    return s[:500] if s else None


def _emit(cb: Optional[Callable[[Dict[str, Any]], None]], payload: Dict[str, Any]) -> None:
    if cb:
        try:
            cb(payload)
        except Exception:
            pass
