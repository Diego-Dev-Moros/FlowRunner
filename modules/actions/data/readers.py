# modules/actions/data/readers.py
"""
Acciones de lectura de datos desde archivos.
"""

from typing import Dict, Any
from modules.core import action, FlowContext
from modules.actions.base import success_result, error_result, validate_required_params
from modules.utils.data_io import leer_excel, leer_csv as _leer_csv, excel_leer_rango, carpeta_listar as _carpeta_listar


@action(
    category='lectura',
    name='Leer datos de Excel',
    description='Lee un rango (A1:D100) o columnas específicas.',
    schema=[
        {'key': 'ruta', 'label': 'Ruta del Excel', 'type': 'text', 'required': True, 'placeholder': 'C:\\ruta\\datos.xlsx'},
        {'key': 'hoja', 'label': 'Hoja', 'type': 'text', 'required': True, 'placeholder': 'Hoja1'},
        {'key': 'rango', 'label': 'Rango (A1:D100)', 'type': 'text', 'required': True},
        {'key': 'nombre_personalizado', 'label': 'Nombre variable (opcional)', 'type': 'text', 'required': False}
    ]
)
def excel_leer_rango_action(context: FlowContext, ruta: str, hoja: str, rango: str, 
                           nombre_personalizado: str = "") -> Dict[str, Any]:
    """
    Lee datos de un archivo Excel usando rango específico.
    """
    try:
        error = validate_required_params({'ruta': ruta, 'hoja': hoja, 'rango': rango}, 
                                       ['ruta', 'hoja', 'rango'])
        if error:
            return error_result(error)
        
        # Usar la función existente
        datos = excel_leer_rango(ruta, hoja, rango)
        
        if datos is None:
            return error_result(f"No se pudieron leer datos de {ruta}")
        
        # Guardar en variable
        var_name = nombre_personalizado or "datos_excel"
        context.set_variable(var_name, datos)
        
        return success_result(
            f"Leídos datos de Excel: {len(datos)} filas",
            variables={var_name: f"DataFrame con {len(datos)} filas"}
        )
        
    except Exception as e:
        return error_result(f"Error leyendo Excel: {str(e)}")


@action(
    category='lectura',
    name='Leer datos de CSV',
    description='Lee datos de un archivo CSV.',
    schema=[
        {'key': 'ruta', 'label': 'Ruta del CSV', 'type': 'text', 'required': True, 'placeholder': 'C:\\ruta\\datos.csv'},
        {'key': 'nombre_personalizado', 'label': 'Nombre variable (opcional)', 'type': 'text', 'required': False}
    ]
)
def leer_csv_action(context: FlowContext, ruta: str, nombre_personalizado: str = "") -> Dict[str, Any]:
    """
    Lee datos de un archivo CSV.
    """
    try:
        if not ruta:
            return error_result("Ruta del archivo requerida")
        
        # Usar la función existente
        datos = _leer_csv(ruta)
        
        if datos is None:
            return error_result(f"No se pudieron leer datos de {ruta}")
        
        # Guardar en variable
        var_name = nombre_personalizado or "datos_csv"
        context.set_variable(var_name, datos)
        
        return success_result(
            f"Leídos datos de CSV: {len(datos)} filas",
            variables={var_name: f"DataFrame con {len(datos)} filas"}
        )
        
    except Exception as e:
        return error_result(f"Error leyendo CSV: {str(e)}")


@action(
    category='lectura',
    name='Ver archivos de carpeta',
    description='Lista archivos de una carpeta con patrón opcional.',
    schema=[
        {'key': 'ruta', 'label': 'Ruta de carpeta', 'type': 'text', 'required': True},
        {'key': 'patron', 'label': 'Patrón (ej. *.xlsx)', 'type': 'text', 'required': False, 'placeholder': '*.xlsx'},
        {'key': 'nombre_personalizado', 'label': 'Nombre variable (opcional)', 'type': 'text', 'required': False}
    ]
)
def carpeta_listar_action(context: FlowContext, ruta: str, patron: str = "*", 
                         nombre_personalizado: str = "") -> Dict[str, Any]:
    """
    Lista archivos en una carpeta.
    """
    try:
        if not ruta:
            return error_result("Ruta de carpeta requerida")
        
        # Usar la función existente
        archivos = _carpeta_listar(ruta, patron or "*")
        
        if archivos is None:
            return error_result(f"No se pudo acceder a la carpeta {ruta}")
        
        # Guardar en variable
        var_name = nombre_personalizado or "lista_archivos"
        context.set_variable(var_name, archivos)
        
        return success_result(
            f"Encontrados {len(archivos)} archivos en {ruta}",
            variables={var_name: archivos}
        )
        
    except Exception as e:
        return error_result(f"Error listando carpeta: {str(e)}")
