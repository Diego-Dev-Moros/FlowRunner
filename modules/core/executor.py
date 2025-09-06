# modules/core/executor.py
"""
Motor de ejecución mejorado para FlowRunner.
Maneja la ejecución de flujos con el nuevo sistema de registro.
"""

import json
import inspect
from typing import Dict, Any, List, Callable, Optional
from .context import FlowContext
from .registry import ActionRegistry, ActionSpec


class FlowExecutor:
    """
    Ejecutor de flujos mejorado que usa el registry automático.
    """
    
    def __init__(self, notifier: Optional[Callable] = None):
        self.context = FlowContext()
        self.notifier = notifier or (lambda x: None)
        self.is_running = False
        self.should_stop = False
    
    def execute_flow(self, flow: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta un flujo completo.
        
        Args:
            flow: Diccionario con la definición del flujo
            
        Returns:
            Resultado de la ejecución
        """
        try:
            self.is_running = True
            self.should_stop = False
            
            # Auto-descubrir acciones si no se ha hecho
            ActionRegistry.auto_discover_actions()
            
            steps = flow.get('steps', [])
            edges = flow.get('edges', [])
            
            if not steps:
                return {"ok": False, "error": "No hay pasos en el flujo"}
            
            # Ordenar pasos según edges (topological sort)
            ordered_steps = self._sort_steps_by_edges(steps, edges)
            
            print(f"[EXECUTOR] Iniciando flujo con {len(ordered_steps)} pasos")
            
            # Ejecutar cada paso
            for i, step in enumerate(ordered_steps):
                if self.should_stop:
                    break
                    
                self.context.current_step = step.get('id', f'step_{i}')
                
                # Notificar progreso
                self._notify_progress(step['id'], f"Ejecutando: {step.get('type', 'unknown')}")
                
                # Ejecutar el paso
                result = self._execute_step(step)
                
                if not result.get('ok', False):
                    error_msg = result.get('error', 'Error desconocido')
                    self._notify_progress(step['id'], f"Error: {error_msg}", "error")
                    return result
                
                # Mostrar variables si hay preview
                if result.get('variables'):
                    self._notify_progress(step['id'], "Completado", "success", 
                                        {"variables": result.get('variables')})
            
            return {
                "ok": True, 
                "variables": list(self.context.list_variables().keys()),
                "message": f"Flujo completado exitosamente ({len(ordered_steps)} pasos)"
            }
            
        except Exception as e:
            error_msg = f"Error ejecutando flujo: {str(e)}"
            print(f"[EXECUTOR] {error_msg}")
            return {"ok": False, "error": error_msg}
            
        finally:
            self.is_running = False
            self.context.cleanup()
    
    def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta un paso individual.
        """
        step_type = step.get('type')
        if not step_type:
            return {"ok": False, "error": "Paso sin tipo definido"}
        
        # Buscar la acción en el registry
        action_spec = ActionRegistry.get_action(step_type)
        if not action_spec:
            return {"ok": False, "error": f"Acción no encontrada: {step_type}"}
        
        try:
            # Preparar parámetros
            props = step.get('props', {})
            params = self._prepare_parameters(action_spec, props)
            
            # Ejecutar la función
            result = action_spec.callable_func(**params)
            
            # Procesar resultado
            return self._process_step_result(result, action_spec)
            
        except Exception as e:
            error_msg = f"Error en paso {step_type}: {str(e)}"
            print(f"[EXECUTOR] {error_msg}")
            return {"ok": False, "error": error_msg}
    
    def _prepare_parameters(self, action_spec: ActionSpec, props: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepara los parámetros para llamar a la función.
        """
        params = {}
        
        # Obtener la signatura de la función
        sig = inspect.signature(action_spec.callable_func)
        
        for param_name, param in sig.parameters.items():
            # Inyección automática del contexto
            if param_name == 'context' or param_name == 'contexto':
                params[param_name] = self.context
                continue
            
            # Inyección automática de drivers
            if param_name == 'driver' and 'driver' in self.context.drivers:
                params[param_name] = self.context.get_driver('driver')
                continue
            
            # Mapear desde props
            if param_name in props and props[param_name] != '':
                value = props[param_name]
                
                # Resolver variables si es necesario
                if isinstance(value, str) and value.startswith('$'):
                    var_name = value[1:]  # remover $
                    value = self.context.get_variable(var_name, value)
                
                params[param_name] = value
            elif param.default is not inspect.Parameter.empty:
                # Usar valor por defecto si está disponible
                continue
            else:
                # Parámetro requerido no encontrado
                print(f"[EXECUTOR] Parámetro requerido no encontrado: {param_name}")
        
        return params
    
    def _process_step_result(self, result: Any, action_spec: ActionSpec) -> Dict[str, Any]:
        """
        Procesa el resultado de un paso.
        """
        # Si la función devuelve un driver, guardarlo
        if action_spec.provides and result:
            self.context.set_driver(action_spec.provides, result)
        
        # Si debe limpiar driver después
        if action_spec.clear_driver:
            self.context.clear_all_drivers()
        
        # Formatear resultado
        if isinstance(result, dict) and 'ok' in result:
            return result
        
        # Resultado simple, convertir a formato estándar
        return {"ok": True, "result": result}
    
    def _sort_steps_by_edges(self, steps: List[Dict], edges: List[Dict]) -> List[Dict]:
        """
        Ordena los pasos según las conexiones (edges).
        """
        # Por ahora usar ordenamiento simple por ID
        # TODO: Implementar topological sort real
        return sorted(steps, key=lambda x: x.get('id', ''))
    
    def _notify_progress(self, step_id: str, message: str, 
                        level: str = "info", preview: Dict = None) -> None:
        """
        Notifica progreso al frontend.
        """
        payload = {
            "stepId": step_id,
            "message": message,
            "level": level
        }
        
        if preview:
            payload["preview"] = preview
        
        self.notifier(payload)
    
    def stop(self) -> None:
        """
        Detiene la ejecución del flujo.
        """
        self.should_stop = True
