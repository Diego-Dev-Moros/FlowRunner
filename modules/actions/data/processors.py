# modules/actions/data/processors.py
"""
Acciones de procesamiento de datos y manejo de variables.
"""

from typing import Dict, Any, Union
from modules.core import action, FlowContext
from modules.actions.base import success_result, error_result, validate_required_params


@action(
    category='datos',
    name='Crear/Actualizar variable',
    description='Crea o actualiza una variable del flujo.',
    schema=[
        {'key': 'variable', 'label': 'Nombre variable', 'type': 'text', 'required': True, 'placeholder': 'mi_var'},
        {'key': 'valor', 'label': 'Valor', 'type': 'text', 'required': True, 'placeholder': '123 | Hola | true'}
    ]
)
def variable_set(context: FlowContext, variable: str, valor: str) -> Dict[str, Any]:
    """
    Establece una variable en el contexto del flujo.
    """
    try:
        error = validate_required_params({'variable': variable, 'valor': valor}, ['variable', 'valor'])
        if error:
            return error_result(error)
        
        # Convertir valor según el tipo
        processed_value = _convert_value(valor)
        
        context.set_variable(variable, processed_value)
        
        return success_result(
            f"Variable '{variable}' establecida con valor: {processed_value}",
            variables={variable: processed_value}
        )
        
    except Exception as e:
        return error_result(f"Error estableciendo variable: {str(e)}")


@action(
    category='datos',
    name='Usar variable',
    description='Lee una variable del flujo.',
    schema=[
        {'key': 'variable', 'label': 'Nombre variable', 'type': 'text', 'required': True, 'placeholder': 'mi_var'}
    ]
)
def variable_get(context: FlowContext, variable: str) -> Dict[str, Any]:
    """
    Obtiene el valor de una variable del contexto.
    """
    try:
        if not variable:
            return error_result("Nombre de variable requerido")
        
        if not context.has_variable(variable):
            return error_result(f"Variable '{variable}' no encontrada")
        
        value = context.get_variable(variable)
        
        return success_result(
            f"Variable '{variable}': {value}",
            variables={variable: value}
        )
        
    except Exception as e:
        return error_result(f"Error leyendo variable: {str(e)}")


@action(
    category='datos',
    name='Listar variables',
    description='Muestra todas las variables actuales del flujo.',
    schema=[]
)
def variables_listar(context: FlowContext) -> Dict[str, Any]:
    """
    Lista todas las variables disponibles en el contexto.
    """
    try:
        variables = context.list_variables()
        
        if not variables:
            return success_result("No hay variables definidas")
        
        return success_result(
            f"Variables actuales: {list(variables.keys())}",
            variables=variables
        )
        
    except Exception as e:
        return error_result(f"Error listando variables: {str(e)}")


@action(
    category='datos',
    name='Ordenar información',
    description='Ordena datos según criterio.',
    schema=[
        {'key': 'variable', 'label': 'Variable con datos', 'type': 'text', 'required': True, 'placeholder': 'mi_lista'},
        {'key': 'criterio', 'label': 'Criterio', 'type': 'select', 'required': True, 'options': ['asc', 'desc', 'alfabético', 'numérico']},
        {'key': 'columna', 'label': 'Columna/Campo', 'type': 'text', 'required': False}
    ]
)
def ordenar_info(context: FlowContext, variable: str, criterio: str, columna: str = None) -> Dict[str, Any]:
    """
    Ordena datos almacenados en una variable.
    """
    try:
        error = validate_required_params({'variable': variable, 'criterio': criterio}, ['variable', 'criterio'])
        if error:
            return error_result(error)
        
        if not context.has_variable(variable):
            return error_result(f"Variable '{variable}' no encontrada")
        
        data = context.get_variable(variable)
        
        if not isinstance(data, list):
            return error_result(f"La variable '{variable}' debe contener una lista")
        
        try:
            if criterio == 'asc':
                sorted_data = sorted(data)
            elif criterio == 'desc':
                sorted_data = sorted(data, reverse=True)
            elif criterio == 'alfabético':
                sorted_data = sorted(data, key=lambda x: str(x).lower())
            elif criterio == 'numérico':
                sorted_data = sorted(data, key=lambda x: float(x) if str(x).replace('.', '').isdigit() else 0)
            else:
                return error_result(f"Criterio no válido: {criterio}")
            
            # Guardar resultado ordenado
            result_var = f"{variable}_ordenado"
            context.set_variable(result_var, sorted_data)
            
            return success_result(
                f"Datos ordenados por {criterio}. Guardado en '{result_var}'",
                variables={result_var: sorted_data}
            )
            
        except Exception as sort_error:
            return error_result(f"Error ordenando datos: {str(sort_error)}")
        
    except Exception as e:
        return error_result(f"Error en ordenar_info: {str(e)}")


def _convert_value(value_str: str) -> Union[str, int, float, bool]:
    """
    Convierte un string a su tipo más apropiado.
    """
    # Intentar boolean
    if value_str.lower() in ('true', 'verdadero', 'sí', 'si'):
        return True
    if value_str.lower() in ('false', 'falso', 'no'):
        return False
    
    # Intentar número
    try:
        if '.' in value_str:
            return float(value_str)
        return int(value_str)
    except ValueError:
        pass
    
    # Devolver como string
    return value_str
