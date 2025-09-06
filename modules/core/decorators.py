# modules/core/decorators.py
"""
Decoradores para el registro automático y manejo de acciones.
"""

import functools
from typing import Dict, Any, List, Optional, Callable
from .registry import ActionRegistry


def action(category: str, name: str, description: str = "", 
          schema: List[Dict] = None, 
          provides: Optional[str] = None,
          clear_driver: bool = False):
    """
    Decorador para registrar automáticamente una acción.
    
    Args:
        category: Categoría de la acción (inicio, navegacion, datos, etc.)
        name: Nombre display de la acción
        description: Descripción para el usuario
        schema: Esquema de parámetros para el frontend
        provides: Si retorna un recurso a mantener (ej: 'driver')
        clear_driver: Si debe limpiar el driver después
    """
    def decorator(func: Callable):
        # Registro automático
        ActionRegistry.register_action(
            id=func.__name__,
            category=category,
            name=name, 
            description=description,
            schema=schema or [],
            callable_func=func,
            provides=provides,
            clear_driver=clear_driver
        )
        
        return func
    return decorator


def require_context(func: Callable):
    """
    Decorador que inyecta automáticamente el contexto del flujo.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # El contexto se inyecta automáticamente por el executor
        return func(*args, **kwargs)
    
    wrapper._requires_context = True
    return wrapper


def provide_driver(driver_type: str):
    """
    Decorador para marcar funciones que proporcionan un driver.
    
    Args:
        driver_type: Tipo de driver ('selenium', 'browser', etc.)
    """
    def decorator(func: Callable):
        func._provides_driver = driver_type
        return func
    return decorator


def require_driver(driver_type: str):
    """
    Decorador para marcar funciones que requieren un driver específico.
    """
    def decorator(func: Callable):
        func._requires_driver = driver_type
        return func
    return decorator
