# modules/actions/files/operations.py
"""
Operaciones de gestión de archivos.
"""

from typing import Dict, Any
from modules.core import action, FlowContext
from modules.actions.base import success_result, error_result, validate_required_params
from modules.utils.data_io import crear_carpeta, mover_archivo, copiar_archivo, eliminar_archivo


@action(
    category='archivos',
    name='Crear carpeta',
    description='Crea una nueva carpeta.',
    schema=[
        {'key': 'ruta', 'label': 'Ruta de carpeta', 'type': 'text', 'required': True, 'placeholder': 'C:\\Nueva_Carpeta'}
    ]
)
def crear_carpeta_action(context: FlowContext, ruta: str) -> Dict[str, Any]:
    """
    Crea una carpeta nueva.
    """
    try:
        error = validate_required_params({'ruta': ruta}, ['ruta'])
        if error:
            return error_result(error)
        
        crear_carpeta(ruta)
        return success_result(f"Carpeta creada: {ruta}")
        
    except Exception as e:
        return error_result(f"Error creando carpeta: {str(e)}")


@action(
    category='archivos',
    name='Mover archivo',
    description='Mueve un archivo de un lugar a otro.',
    schema=[
        {'key': 'origen', 'label': 'Archivo origen', 'type': 'text', 'required': True, 'placeholder': 'C:\\archivo.txt'},
        {'key': 'destino', 'label': 'Destino', 'type': 'text', 'required': True, 'placeholder': 'C:\\nueva_ubicacion\\archivo.txt'},
        {'key': 'si_existe', 'label': 'Si existe', 'type': 'select', 'required': False, 'options': ['sobrescribir', 'renombrar', 'saltar'], 'default': 'sobrescribir'}
    ]
)
def mover_archivo_action(context: FlowContext, origen: str, destino: str, si_existe: str = "sobrescribir") -> Dict[str, Any]:
    """
    Mueve un archivo.
    """
    try:
        error = validate_required_params({'origen': origen, 'destino': destino}, ['origen', 'destino'])
        if error:
            return error_result(error)
        
        mover_archivo(origen, destino, si_existe)
        return success_result(f"Archivo movido: {origen} → {destino}")
        
    except Exception as e:
        return error_result(f"Error moviendo archivo: {str(e)}")


@action(
    category='archivos',
    name='Copiar archivo',
    description='Copia un archivo a otra ubicación.',
    schema=[
        {'key': 'origen', 'label': 'Archivo origen', 'type': 'text', 'required': True, 'placeholder': 'C:\\archivo.txt'},
        {'key': 'destino', 'label': 'Destino', 'type': 'text', 'required': True, 'placeholder': 'C:\\copia\\archivo.txt'},
        {'key': 'si_existe', 'label': 'Si existe', 'type': 'select', 'required': False, 'options': ['sobrescribir', 'renombrar', 'saltar'], 'default': 'sobrescribir'}
    ]
)
def copiar_archivo_action(context: FlowContext, origen: str, destino: str, si_existe: str = "sobrescribir") -> Dict[str, Any]:
    """
    Copia un archivo.
    """
    try:
        error = validate_required_params({'origen': origen, 'destino': destino}, ['origen', 'destino'])
        if error:
            return error_result(error)
        
        copiar_archivo(origen, destino, si_existe)
        return success_result(f"Archivo copiado: {origen} → {destino}")
        
    except Exception as e:
        return error_result(f"Error copiando archivo: {str(e)}")


@action(
    category='archivos',
    name='Eliminar archivo',
    description='Elimina un archivo.',
    schema=[
        {'key': 'ruta', 'label': 'Ruta del archivo', 'type': 'text', 'required': True, 'placeholder': 'C:\\archivo_a_eliminar.txt'}
    ]
)
def eliminar_archivo_action(context: FlowContext, ruta: str) -> Dict[str, Any]:
    """
    Elimina un archivo.
    """
    try:
        error = validate_required_params({'ruta': ruta}, ['ruta'])
        if error:
            return error_result(error)
        
        eliminar_archivo(ruta)
        return success_result(f"Archivo eliminado: {ruta}")
        
    except Exception as e:
        return error_result(f"Error eliminando archivo: {str(e)}")
