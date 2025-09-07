# modules/actions/processing/__init__.py
"""
Módulo de procesamiento avanzado de datos para FlowRunner.
Incluye transformaciones, estadísticas, joins y validaciones.
"""

from .transforms import *
from .statistics import *
from .joins import *
from .validators import *

__all__ = [
    # Transforms
    'filtrar_dataframe', 'transformar_columnas', 'agrupar_datos',
    'pivotar_tabla', 'eliminar_duplicados', 'ordenar_avanzado',
    
    # Statistics  
    'calcular_estadisticas', 'normalizar_datos',
    
    # Joins
    'unir_datasets',
    
    # Validators
    'validar_datos'
]
