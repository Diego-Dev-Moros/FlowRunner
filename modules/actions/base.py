# modules/actions/base.py
"""
Clases base y utilidades comunes para todas las acciones.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from modules.core import FlowContext


class BaseAction(ABC):
    """
    Clase base abstracta para todas las acciones.
    """
    
    @abstractmethod
    def execute(self, context: FlowContext, **params) -> Dict[str, Any]:
        """
        Ejecuta la acción con los parámetros dados.
        
        Args:
            context: Contexto de ejecución del flujo
            **params: Parámetros específicos de la acción
            
        Returns:
            Dict con 'ok' boolean y opcionalmente 'error', 'result', 'variables'
        """
        pass


def success_result(result: Any = None, variables: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Crea un resultado exitoso estándar.
    """
    response = {"ok": True}
    if result is not None:
        response["result"] = result
    if variables:
        response["variables"] = variables
    return response


def error_result(error: str) -> Dict[str, Any]:
    """
    Crea un resultado de error estándar.
    """
    return {"ok": False, "error": error}


def validate_required_params(params: Dict[str, Any], required: list) -> Optional[str]:
    """
    Valida que los parámetros requeridos estén presentes.
    
    Returns:
        None si todo está bien, mensaje de error si falta algo
    """
    missing = []
    for param in required:
        if param not in params or params[param] is None or params[param] == '':
            missing.append(param)
    
    if missing:
        return f"Parámetros requeridos faltantes: {', '.join(missing)}"
    
    return None
