# modules/core/executor.py
"""
Motor de ejecución mejorado para FlowRunner.
Maneja la ejecución de flujos con el nuevo sistema de registro.
"""

import json
import inspect
import time
from typing import Dict, Any, List, Callable, Optional
from .context import FlowContext
from .registry import ActionRegistry, ActionSpec
from modules.utils.logging import FlowLogger


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
            
            flow_name = flow.get('name', 'flujo_sin_nombre')
            start_time = time.time()
            
            # Log inicio de flujo
            FlowLogger.log_flow_start(flow_name)
            
            # Auto-descubrir acciones si no se ha hecho
            ActionRegistry.auto_discover_actions()
            
            steps = flow.get('steps', [])
            edges = flow.get('edges', [])
            
            if not steps:
                error_msg = "No hay pasos en el flujo"
                FlowLogger.log_error(error_msg, context={"flow": flow_name})
                return {"ok": False, "error": error_msg}
            
            # Ordenar pasos según edges (topological sort)
            ordered_steps = self._sort_steps_by_edges(steps, edges)
            
            print(f"[EXECUTOR] Iniciando flujo con {len(ordered_steps)} pasos")
            FlowLogger.log_user(f"Flujo '{flow_name}' iniciado con {len(ordered_steps)} pasos")
            
            # Ejecutar cada paso
            for i, step in enumerate(ordered_steps):
                if self.should_stop:
                    FlowLogger.log_user("Flujo detenido por usuario")
                    break
                    
                self.context.current_step = step.get('id', f'step_{i}')
                
                # Notificar progreso
                self._notify_progress(step['id'], f"Ejecutando: {step.get('type', 'unknown')}")
                
                # Ejecutar el paso
                result = self._execute_step(step)
                
                if not result.get('ok', False):
                    error_msg = result.get('error', 'Error desconocido')
                    self._notify_progress(step['id'], f"Error: {error_msg}", "error")
                    
                    # Log error de paso
                    FlowLogger.log_error(f"Error en paso {step.get('type')}", 
                                       context={"step_id": step.get('id'), "error": error_msg})
                    
                    duration = time.time() - start_time
                    FlowLogger.log_flow_end(flow_name, success=False, duration=duration)
                    return result
                
                # Mostrar variables si hay preview
                if result.get('variables'):
                    self._notify_progress(step['id'], "Completado", "success", 
                                        {"variables": result.get('variables')})
            
            duration = time.time() - start_time
            FlowLogger.log_flow_end(flow_name, success=True, duration=duration)
            
            return {
                "ok": True, 
                "variables": list(self.context.list_variables().keys()),
                "message": f"Flujo completado exitosamente ({len(ordered_steps)} pasos)"
            }
            
        except Exception as e:
            error_msg = f"Error ejecutando flujo: {str(e)}"
            print(f"[EXECUTOR] {error_msg}")
            FlowLogger.log_error("Error crítico en executor", exception=e)
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
            error_msg = f"Acción no encontrada: {step_type}"
            FlowLogger.log_error(error_msg, action_id=step_type)
            return {"ok": False, "error": error_msg}
        
        try:
            # Preparar parámetros
            props = step.get('props', {})
            params = self._prepare_parameters(action_spec, props)
            
            # Log inicio de acción
            FlowLogger.log_action_start(step_type, props)
            
            # Ejecutar la función
            start_time = time.time()
            result = action_spec.callable_func(**params)
            duration = time.time() - start_time
            
            # Procesar resultado
            processed_result = self._process_step_result(result, action_spec)
            
            # Log fin de acción
            success = processed_result.get('ok', False)
            FlowLogger.log_action_end(step_type, success, {
                "duration": duration,
                "result": processed_result
            })
            
            return processed_result
            
        except Exception as e:
            error_msg = f"Error en paso {step_type}: {str(e)}"
            print(f"[EXECUTOR] {error_msg}")
            FlowLogger.log_error(error_msg, exception=e, action_id=step_type)
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
