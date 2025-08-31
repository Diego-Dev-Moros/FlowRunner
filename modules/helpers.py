# modules/helpers.py
from __future__ import annotations
from typing import Dict, Any, List, Tuple, Callable, Optional, Set
from importlib import import_module
from dataclasses import dataclass
import inspect

from config import ACTION_SPECS, StepSpec


@dataclass
class RuntimeState:
    contexto: Dict[str, Any]
    driver: Any = None


# ------------------------ Utilidades ------------------------
def load_callable(path: str) -> Callable:
    """
    Carga una función a partir de 'paquete.modulo:funcion'
    """
    try:
        mod_path, func_name = path.split(':', 1)
        mod = import_module(mod_path)
        func = getattr(mod, func_name)
        if not callable(func):
            raise TypeError(f"'{path}' no es callable.")
        return func
    except Exception as e:
        raise ImportError(f"No se pudo importar callable '{path}': {e}") from e


def topological_order(steps: List[Dict[str, Any]], edges: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Ordena steps según edges (DAG). Si hay ciclo o edges faltantes, cae en orden por aparición.
    """
    if not edges:
        return steps[:]  # sin edges, respeta el orden del array

    id_to_step = {s['id']: s for s in steps}
    graph: Dict[str, Set[str]] = {s['id']: set() for s in steps}
    indeg: Dict[str, int] = {s['id']: 0 for s in steps}

    # construir grafo
    for e in edges:
        f, t = e.get('from'), e.get('to')
        if f in graph and t in graph and t not in graph[f]:
            graph[f].add(t)
            indeg[t] += 1

    # Kahn
    queue = [nid for nid, d in indeg.items() if d == 0]
    order_ids: List[str] = []
    while queue:
        nid = queue.pop(0)
        order_ids.append(nid)
        for neigh in graph[nid]:
            indeg[neigh] -= 1
            if indeg[neigh] == 0:
                queue.append(neigh)

    # Si faltaron nodos (ciclos o edges malos), completar en orden original
    if len(order_ids) != len(steps):
        seen = set(order_ids)
        for s in steps:
            if s['id'] not in seen:
                order_ids.append(s['id'])

    return [id_to_step[i] for i in order_ids if i in id_to_step]


def build_kwargs(spec: StepSpec, node_props: Dict[str, Any], runtime: RuntimeState, func: Callable) -> Dict[str, Any]:
    """
    Crea kwargs para el callable:
    - Mapea props -> argumentos según param_map
    - Inyecta 'driver' y/o 'contexto' si están en spec.inject y el callable los acepta
    - Ignora parámetros opcionales con props faltantes (cuando clave termina en '?')
    """
    sig = inspect.signature(func)
    kwargs: Dict[str, Any] = {}

    # props -> args de función según param_map
    for param_name, prop_key in (spec.param_map or {}).items():
        optional = prop_key.endswith('?')
        prop_key_clean = prop_key[:-1] if optional else prop_key
        if prop_key_clean in node_props and node_props[prop_key_clean] != '':
            kwargs[param_name] = node_props[prop_key_clean]
        else:
            if not optional and param_name in sig.parameters and sig.parameters[param_name].default is inspect._empty:
                raise ValueError(f"Falta prop requerida '{prop_key_clean}' para parámetro '{param_name}'.")

    # Inyecciones
    if 'driver' in (spec.inject or []) and 'driver' in sig.parameters:
        kwargs['driver'] = runtime.driver
        if runtime.driver is None:
            # No hay driver; algunas funciones podrían crearlo internamente, pero normalmente es error
            # No lanzamos excepción aquí; dejamos que la función falle si es necesario
            pass

    if 'contexto' in (spec.inject or []) and 'contexto' in sig.parameters:
        kwargs['contexto'] = runtime.contexto

    return kwargs


# ------------------------ Ejecutor ------------------------
def execute_flow(flow: Dict[str, Any],
                 on_progress: Optional[Callable[[Dict[str, Any]], None]] = None) -> Dict[str, Any]:
    """
    Ejecuta el flow: { steps: [...], edges: [...] }
    Devuelve el 'contexto' resultante.
    """
    steps: List[Dict[str, Any]] = flow.get('steps', []) or []
    edges: List[Dict[str, str]] = flow.get('edges', []) or []

    ordered_steps = topological_order(steps, edges)
    runtime = RuntimeState(contexto={})

    for i, node in enumerate(ordered_steps, start=1):
        type_id = node.get('typeId')
        node_id = node.get('id')
        props = node.get('props', {}) or {}

        spec = ACTION_SPECS.get(type_id)
        if not spec:
            _emit(on_progress, {'stepId': node_id, 'message': f"Saltando acción desconocida: {type_id}", 'level': 'warn'})
            continue

        func = load_callable(spec.callable_path)

        try:
            kwargs = build_kwargs(spec, props, runtime, func)
        except Exception as e:
            _emit(on_progress, {'stepId': node_id, 'message': f"Error preparando args de {type_id}: {e}", 'level': 'error'})
            raise

        _emit(on_progress, {'stepId': node_id, 'message': f"Ejecutando {type_id} ({i}/{len(ordered_steps)})", 'level': 'info'})

        # Llamada
        result = func(**kwargs)

        # Post-proceso: driver
        if spec.provides == 'driver':
            # Si la acción abre/retorna un driver, guardarlo
            runtime.driver = result
        if spec.clear_driver:
            runtime.driver = None

        _emit(on_progress, {'stepId': node_id, 'message': f"Completado {type_id}", 'level': 'success'})

    return runtime.contexto


def _emit(cb: Optional[Callable[[Dict[str, Any]], None]], payload: Dict[str, Any]) -> None:
    if cb:
        try:
            cb(payload)
        except Exception:
            pass