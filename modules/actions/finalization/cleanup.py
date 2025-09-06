# modules/actions/finalization/cleanup.py
"""
Acciones de finalización y limpieza.
"""

from typing import Dict, Any
from modules.core import action, FlowContext
from modules.actions.base import success_result, error_result
from modules.utils.web_automation import cerrar_navegador


@action(
    category='finalizacion',
    name='Cerrar navegador',
    description='Cierra el navegador y limpia los recursos.',
    schema=[],
    clear_driver=True
)
def cerrar_navegador_action(context: FlowContext) -> Dict[str, Any]:
    """
    Cierra el navegador actual.
    """
    try:
        driver = context.get_driver()
        if driver:
            cerrar_navegador(driver)
            context.clear_driver()
            return success_result("Navegador cerrado")
        else:
            return success_result("No hay navegador que cerrar")
        
    except Exception as e:
        return error_result(f"Error cerrando navegador: {str(e)}")


@action(
    category='finalizacion',
    name='Finalizar todo',
    description='Finaliza la ejecución y limpia todos los recursos.',
    schema=[]
)
def finalizar_todo_action(context: FlowContext) -> Dict[str, Any]:
    """
    Limpia todos los recursos y finaliza la ejecución.
    """
    try:
        # Cerrar navegador si existe
        driver = context.get_driver()
        if driver:
            cerrar_navegador(driver)
            context.clear_driver()
        
        # Limpiar variables (opcional)
        variables_count = len(context.variables)
        
        return success_result(
            f"Ejecución finalizada. Limpiadas {variables_count} variables y recursos."
        )
        
    except Exception as e:
        return error_result(f"Error finalizando: {str(e)}")
