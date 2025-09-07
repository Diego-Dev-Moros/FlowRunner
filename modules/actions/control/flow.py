# modules/actions/control/flow.py
"""
Acciones de control de flujo básicas.
"""

import time
from typing import Dict, Any
from modules.core import action, FlowContext
from modules.actions.base import success_result, error_result, validate_required_params


@action(
    category='logica',
    name='Hacer una pausa', 
    description='Detiene la ejecución por algunos segundos.',
    schema=[
        {'key': 'segundos', 'label': 'Segundos', 'type': 'number', 'required': True, 'placeholder': '1'}
    ]
)
def pausa(context: FlowContext, segundos: float = 1.0) -> Dict[str, Any]:
    """
    Pausa la ejecución por el número de segundos especificado.
    """
    try:
        # Convertir a float si es string
        if isinstance(segundos, str):
            segundos = float(segundos)
            
        if segundos <= 0:
            return error_result("Los segundos deben ser mayor que 0")
        
        print(f"[PAUSA] Esperando {segundos} segundos...")
        time.sleep(float(segundos))
        
        return success_result(f"Pausa de {segundos} segundos completada")
        
    except Exception as e:
        return error_result(f"Error en pausa: {str(e)}")


# TODO: Implementar en el futuro
@action(
    category='logica',
    name='Si... entonces', 
    description='Ejecuta acciones condicionalmente.',
    schema=[
        {'key': 'condicion', 'label': 'Condición', 'type': 'text', 'required': True, 'placeholder': '$variable == "valor"'},
        {'key': 'verdadero', 'label': 'Acciones si verdadero', 'type': 'textarea', 'required': False},
        {'key': 'falso', 'label': 'Acciones si falso', 'type': 'textarea', 'required': False}
    ]
)
def condicional_si(context: FlowContext, condicion: str, 
                   verdadero: str = "", falso: str = "") -> Dict[str, Any]:
    """
    Ejecuta acciones condicionalmente (implementación futura).
    """
    return error_result("Condicionales aún no implementados - próximamente")


@action(
    category='logica',
    name='Repetir mientras',
    description='Repite acciones mientras se cumpla una condición.',
    schema=[
        {'key': 'condicion', 'label': 'Condición', 'type': 'text', 'required': True},
        {'key': 'max_iteraciones', 'label': 'Máximo iteraciones', 'type': 'number', 'required': False, 'placeholder': '100'}
    ]
)
def bucle_mientras(context: FlowContext, condicion: str, 
                  max_iteraciones: int = 100) -> Dict[str, Any]:
    """
    Bucle while (implementación futura).
    """
    return error_result("Bucles aún no implementados - próximamente")
