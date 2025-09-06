# modules/actions/dialogs/pickers.py
"""
Acciones de diálogos para selección de archivos y carpetas.
"""

from typing import Dict, Any
from modules.core import action, FlowContext
from modules.actions.base import success_result, error_result
from modules.utils.dialogs import seleccionar_archivo, seleccionar_carpeta


@action(
    category='dialogos',
    name='Elegir archivo',
    description='Abre un diálogo para seleccionar un archivo.',
    schema=[
        {'key': 'titulo', 'label': 'Título del diálogo', 'type': 'text', 'required': False, 'placeholder': 'Seleccionar archivo'},
        {'key': 'tipos', 'label': 'Tipos de archivo', 'type': 'text', 'required': False, 'placeholder': '*.xlsx,*.csv'},
        {'key': 'variable_destino', 'label': 'Variable destino', 'type': 'text', 'required': False, 'placeholder': 'archivo_seleccionado'}
    ]
)
def dialogo_seleccionar_archivo(context: FlowContext, titulo: str = "Seleccionar archivo", 
                               tipos: str = "", variable_destino: str = "archivo_seleccionado") -> Dict[str, Any]:
    """
    Muestra un diálogo para seleccionar archivo y guarda la ruta en una variable.
    """
    try:
        # Convertir tipos de archivo si se especifica
        filetypes = [("Todos", "*.*")]
        if tipos:
            # Parsear tipos como "*.xlsx,*.csv" o "Excel:*.xlsx,CSV:*.csv"
            tipos_list = []
            for tipo in tipos.split(','):
                tipo = tipo.strip()
                if ':' in tipo:
                    nombre, ext = tipo.split(':', 1)
                    tipos_list.append((nombre.strip(), ext.strip()))
                else:
                    tipos_list.append((tipo.replace('*.', '').upper(), tipo))
            filetypes = tipos_list + filetypes
        
        # Mostrar diálogo
        archivo = seleccionar_archivo(titulo, tuple(filetypes))
        
        if archivo:
            # Guardar en variable
            context.set_variable(variable_destino, archivo)
            return success_result(
                f"Archivo seleccionado: {archivo}",
                variables={variable_destino: archivo}
            )
        else:
            return success_result("No se seleccionó archivo")
        
    except Exception as e:
        return error_result(f"Error en diálogo de archivo: {str(e)}")


@action(
    category='dialogos',
    name='Elegir carpeta',
    description='Abre un diálogo para seleccionar una carpeta.',
    schema=[
        {'key': 'titulo', 'label': 'Título del diálogo', 'type': 'text', 'required': False, 'placeholder': 'Seleccionar carpeta'},
        {'key': 'variable_destino', 'label': 'Variable destino', 'type': 'text', 'required': False, 'placeholder': 'carpeta_seleccionada'}
    ]
)
def dialogo_seleccionar_carpeta(context: FlowContext, titulo: str = "Seleccionar carpeta", 
                               variable_destino: str = "carpeta_seleccionada") -> Dict[str, Any]:
    """
    Muestra un diálogo para seleccionar carpeta y guarda la ruta en una variable.
    """
    try:
        # Mostrar diálogo
        carpeta = seleccionar_carpeta(titulo)
        
        if carpeta:
            # Guardar en variable
            context.set_variable(variable_destino, carpeta)
            return success_result(
                f"Carpeta seleccionada: {carpeta}",
                variables={variable_destino: carpeta}
            )
        else:
            return success_result("No se seleccionó carpeta")
        
    except Exception as e:
        return error_result(f"Error en diálogo de carpeta: {str(e)}")
