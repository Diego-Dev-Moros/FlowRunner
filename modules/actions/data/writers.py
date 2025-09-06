# modules/actions/data/writers.py
"""
Acciones de escritura de datos a archivos.
"""

from typing import Dict, Any
from modules.core import action, FlowContext
from modules.actions.base import success_result, error_result, validate_required_params
from modules.utils.data_io import escribir_csv as _escribir_csv, escribir_excel as _escribir_excel


@action(
    category='escritura',
    name='Escribir CSV',
    description='Escribe datos a un archivo CSV.',
    schema=[
        {'key': 'nombre_variable', 'label': 'Variable con datos', 'type': 'text', 'required': True, 'placeholder': 'datos_excel'},
        {'key': 'ruta_destino', 'label': 'Ruta del archivo CSV', 'type': 'text', 'required': True, 'placeholder': 'C:\\salida\\datos.csv'}
    ]
)
def escribir_csv_action(context: FlowContext, nombre_variable: str, ruta_destino: str) -> Dict[str, Any]:
    """
    Escribe datos de una variable a un archivo CSV.
    """
    try:
        error = validate_required_params({'nombre_variable': nombre_variable, 'ruta_destino': ruta_destino}, 
                                       ['nombre_variable', 'ruta_destino'])
        if error:
            return error_result(error)
        
        # Obtener datos del contexto
        if nombre_variable not in context.variables:
            return error_result(f"Variable '{nombre_variable}' no encontrada")
        
        datos = context.variables[nombre_variable]
        
        # Escribir usando la función consolidada
        _escribir_csv(datos, ruta_destino)
        
        return success_result(f"CSV escrito: {ruta_destino}")
        
    except Exception as e:
        return error_result(f"Error escribiendo CSV: {str(e)}")


@action(
    category='escritura',
    name='Escribir Excel',
    description='Escribe datos a un archivo Excel.',
    schema=[
        {'key': 'nombre_variable', 'label': 'Variable con datos', 'type': 'text', 'required': True, 'placeholder': 'datos_csv'},
        {'key': 'ruta_destino', 'label': 'Ruta del archivo Excel', 'type': 'text', 'required': True, 'placeholder': 'C:\\salida\\datos.xlsx'},
        {'key': 'hoja', 'label': 'Nombre de hoja', 'type': 'text', 'required': False, 'placeholder': 'Hoja1', 'default': 'Hoja1'}
    ]
)
def escribir_excel_action(context: FlowContext, nombre_variable: str, ruta_destino: str, hoja: str = "Hoja1") -> Dict[str, Any]:
    """
    Escribe datos de una variable a un archivo Excel.
    """
    try:
        error = validate_required_params({'nombre_variable': nombre_variable, 'ruta_destino': ruta_destino}, 
                                       ['nombre_variable', 'ruta_destino'])
        if error:
            return error_result(error)
        
        # Obtener datos del contexto
        if nombre_variable not in context.variables:
            return error_result(f"Variable '{nombre_variable}' no encontrada")
        
        datos = context.variables[nombre_variable]
        
        # Escribir usando la función consolidada
        _escribir_excel(datos, ruta_destino, hoja)
        
        return success_result(f"Excel escrito: {ruta_destino}")
        
    except Exception as e:
        return error_result(f"Error escribiendo Excel: {str(e)}")


@action(
    category='escritura',
    name='Escribir TXT',
    description='Escribe datos a un archivo de texto.',
    schema=[
        {'key': 'nombre_variable', 'label': 'Variable con datos', 'type': 'text', 'required': True, 'placeholder': 'datos_procesados'},
        {'key': 'ruta_destino', 'label': 'Ruta del archivo TXT', 'type': 'text', 'required': True, 'placeholder': 'C:\\salida\\datos.txt'},
        {'key': 'delimitador', 'label': 'Delimitador', 'type': 'text', 'required': False, 'placeholder': ',', 'default': ','}
    ]
)
def escribir_txt_action(context: FlowContext, nombre_variable: str, ruta_destino: str, delimitador: str = ",") -> Dict[str, Any]:
    """
    Escribe datos de una variable a un archivo de texto.
    """
    try:
        error = validate_required_params({'nombre_variable': nombre_variable, 'ruta_destino': ruta_destino}, 
                                       ['nombre_variable', 'ruta_destino'])
        if error:
            return error_result(error)
        
        # Obtener datos del contexto
        if nombre_variable not in context.variables:
            return error_result(f"Variable '{nombre_variable}' no encontrada")
        
        datos = context.variables[nombre_variable]
        
        # Escribir usando pandas si es DataFrame
        if hasattr(datos, 'to_csv'):
            _escribir_csv(datos, ruta_destino, sep=delimitador)
        else:
            # Escribir como texto plano
            import os
            os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
            with open(ruta_destino, 'w', encoding='utf-8') as f:
                if isinstance(datos, (list, tuple)):
                    f.write(delimitador.join(map(str, datos)))
                else:
                    f.write(str(datos))
        
        return success_result(f"TXT escrito: {ruta_destino}")
        
    except Exception as e:
        return error_result(f"Error escribiendo TXT: {str(e)}")
