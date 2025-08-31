# modules/funciones/extras.py
from __future__ import annotations
from typing import Dict, Any, List, Tuple, Set, Optional, Callable
from dataclasses import dataclass, field
import traceback

# Importar tus módulos
from modules.funciones.archivos import lectura as mod_lectura
from modules.funciones.archivos import escritura as mod_escritura
from modules.funciones.navegador import navegador as mod_nav

# ==============================
# Contexto de ejecución
# ==============================
class ContextoEjecucion:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.contadores = {"csv": 0, "excel": 0, "txt": 0}
        self.driver = None  # navegador Selenium

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

    # Si no se cubrieron todos (ciclo), fallback al orden original
    if len(ordered_ids) != len(steps):
        return steps
    return [id_to_step[i] for i in ordered_ids]

# ==============================
# Dispatcher (typeId → callable)
# ==============================
def build_dispatcher() -> Dict[str, Callable[[ContextoEjecucion, Dict[str, Any]], Any]]:
    def not_implemented(ctx: ContextoEjecucion, props: Dict[str, Any]):
        print(f"[WARN] Acción no implementada: props={props}")
        return None

    return {
        # --- Lectura ---
        'leer_csv': lambda ctx, p: ctx.asignar_variable('csv', mod_lectura.leer_csv(p['ruta'])),
        'leer_excel': lambda ctx, p: ctx.asignar_variable('excel', mod_lectura.leer_excel(p['ruta'], p['hoja'])),
        'leer_txt': lambda ctx, p: ctx.asignar_variable('txt', mod_lectura.leer_txt_delimitado(p['ruta'], p['delimitador'])),

        # --- Escritura ---
        'escribir_csv': lambda ctx, p: mod_escritura.escribir_csv(ctx.obtener_variable(p['variable']), p['ruta']),
        'escribir_excel': lambda ctx, p: mod_escritura.escribir_excel(ctx.obtener_variable(p['variable']), p['ruta']),
        'escribir_txt': lambda ctx, p: mod_escritura.escribir_txt(ctx.obtener_variable(p['variable']), p['ruta'], p.get('delimitador', ',')),

        # --- Navegador ---
        'abrir_pagina': lambda ctx, p: _open_and_store_driver(ctx, p['url']),
        'cambiar_pagina': lambda ctx, p: mod_nav.cambiar_pagina_web_selenium(_require_driver(ctx), p['url']),
        'cerrar_navegador': lambda ctx, p: _close_and_clear_driver(ctx),
        'maximizar_app': lambda ctx, p: mod_nav.maximizar_navegador(_require_driver(ctx)),

        # --- Placeholders / por implementar ---
        'abrir_documento': not_implemented,
        'iniciar_app': not_implemented,
        'hacer_clic': not_implemented,
        'escribir_texto': not_implemented,
        'copiar_pegar': not_implemented,
        'ordenar_info': not_implemented,
        'cerrar_documento': not_implemented,
        'cerrar_app': not_implemented,
        'exportar_json': lambda ctx, p: None,   # el front ya exporta
        'ejecutar_flujo': lambda ctx, p: None,  # redundante
        'finalizar_todo': lambda ctx, p: ctx.cerrar()
    }

def _open_and_store_driver(ctx: ContextoEjecucion, url: str):
    if ctx.driver:
        try:
            mod_nav.cambiar_pagina_web_selenium(ctx.driver, url)
            return ctx.driver
        except Exception:
            pass
    ctx.driver = mod_nav.abrir_pagina_web_selenium(url)
    return ctx.driver

def _require_driver(ctx: ContextoEjecucion):
    if not ctx.driver:
        raise RuntimeError("No hay navegador abierto. Agregá un paso 'Abrir página web' antes.")
    return ctx.driver

def _close_and_clear_driver(ctx: ContextoEjecucion):
    if ctx.driver:
        try:
            mod_nav.cerrar_navegador_selenium(ctx.driver)
        except Exception:
            pass
    ctx.driver = None

# ==============================
# Motor principal de ejecución
# ==============================
def run_flow(flow: Dict[str, Any], notifier=None) -> Dict[str, Any]:
    """
    Ejecuta un flujo {steps:[...], edges:[...]}.
    notifier: callable(dict) → e.g. eel.notify_progress
    """
    ctx = ContextoEjecucion()
    dispatch = build_dispatcher()

    steps = flow.get('steps', [])
    edges = flow.get('edges', [])

    # Orden de ejecución: edges (topológico) o steps tal cual
    ordered_steps = topological_order(steps, edges)
    results: List[Dict[str, Any]] = []

    try:
        for step in ordered_steps:
            sid = step.get('id')
            tid = step.get('typeId')
            nombre = step.get('nombre', tid)
            props = step.get('props', {})

            if notifier:
                notifier({'stepId': sid, 'message': f"Ejecutando {nombre} ({tid})..."})

            fn = dispatch.get(tid)
            if not fn:
                raise NotImplementedError(f"Tipo de acción no soportado: {tid}")

            out = fn(ctx, props)

            results.append({
                'id': sid,
                'typeId': tid,
                'nombre': nombre,
                'output': str(out)[:500] if out is not None else None
            })

            if notifier:
                notifier({'stepId': sid, 'message': f"Completado {nombre}"})

        # Finalizar si había 'finalizar_todo'
        # (el propio step lo haría, pero por seguridad cerramos al final)
        ctx.cerrar()

        return {
            'ok': True,
            'results': results,
            'variables': ctx.listar_variables()
        }
    except Exception as ex:
        err = ''.join(traceback.format_exc())
        try:
            ctx.cerrar()
        except Exception:
            pass
        return {
            'ok': False,
            'error': str(ex),
            'traceback': err,
            'partial_results': results
        }
