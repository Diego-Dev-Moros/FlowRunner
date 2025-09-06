# modules/core/__init__.py
"""
Core del sistema FlowRunner.
Maneja el registro automático de acciones, contexto y ejecución.
"""

from .context import FlowContext
from .executor import FlowExecutor
from .registry import ActionRegistry
from .decorators import action, require_context, provide_driver

__all__ = [
    'FlowContext',
    'FlowExecutor', 
    'ActionRegistry',
    'action',
    'require_context',
    'provide_driver'
]
