# modules/actions/processing/joins.py
"""
Acciones para unir y combinar DataFrames en FlowRunner.
Incluye diferentes tipos de joins y concatenaciones.
"""

import pandas as pd
from typing import Dict, List, Any, Optional, Union
from modules.core.decorators import action
from modules.core.context import FlowContext


@action(
    category="procesamiento",
    name="Unir Datasets",
    description="Une dos DataFrames usando diferentes tipos de JOIN",
    schema=[
        {
            "key": "dataframe_izq_var",
            "label": "DataFrame izquierdo",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable que contiene el DataFrame principal"
        },
        {
            "key": "dataframe_der_var", 
            "label": "DataFrame derecho",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable que contiene el DataFrame a unir"
        },
        {
            "key": "columna_izq",
            "label": "Columna de unión izquierda",
            "type": "text",
            "required": True,
            "description": "Columna del DataFrame izquierdo para la unión"
        },
        {
            "key": "columna_der",
            "label": "Columna de unión derecha", 
            "type": "text",
            "required": False,
            "description": "Columna del DataFrame derecho (usa la misma si está vacío)"
        },
        {
            "key": "tipo_join",
            "label": "Tipo de JOIN",
            "type": "select",
            "required": True,
            "options": [
                {"value": "inner", "label": "INNER - Solo registros que coinciden"},
                {"value": "left", "label": "LEFT - Todos los registros del izquierdo"},
                {"value": "right", "label": "RIGHT - Todos los registros del derecho"}, 
                {"value": "outer", "label": "OUTER - Todos los registros de ambos"}
            ],
            "description": "Tipo de unión a realizar"
        },
        {
            "key": "sufijos",
            "label": "Sufijos para columnas duplicadas",
            "type": "text",
            "required": False,
            "description": "Sufijos para columnas duplicadas, formato: '_izq,_der' (por defecto: '_x,_y')"
        },
        {
            "key": "resultado_var",
            "label": "Variable resultado",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable donde guardar el DataFrame unido"
        }
    ]
)
def unir_datasets(context: FlowContext, dataframe_izq_var: str, dataframe_der_var: str,
                 columna_izq: str, tipo_join: str, resultado_var: str,
                 columna_der: str = None, sufijos: str = None) -> Dict[str, Any]:
    """
    Une dos DataFrames usando diferentes tipos de JOIN.
    """
    try:
        # Obtener los DataFrames
        df_izq = context.get_variable(dataframe_izq_var)
        if df_izq is None:
            return {"success": False, "error": f"Variable '{dataframe_izq_var}' no encontrada"}
            
        df_der = context.get_variable(dataframe_der_var)
        if df_der is None:
            return {"success": False, "error": f"Variable '{dataframe_der_var}' no encontrada"}
            
        if not isinstance(df_izq, pd.DataFrame):
            return {"success": False, "error": f"Variable '{dataframe_izq_var}' no es un DataFrame"}
            
        if not isinstance(df_der, pd.DataFrame):
            return {"success": False, "error": f"Variable '{dataframe_der_var}' no es un DataFrame"}
        
        # Verificar columnas de unión
        if columna_izq not in df_izq.columns:
            return {"success": False, "error": f"Columna '{columna_izq}' no existe en DataFrame izquierdo"}
        
        # Si no se especifica columna derecha, usar la misma
        col_der = columna_der if columna_der else columna_izq
        if col_der not in df_der.columns:
            return {"success": False, "error": f"Columna '{col_der}' no existe en DataFrame derecho"}
        
        # Procesar sufijos
        if sufijos:
            try:
                suffix_left, suffix_right = sufijos.split(',')
                suffixes = (suffix_left.strip(), suffix_right.strip())
            except ValueError:
                return {"success": False, "error": "Formato de sufijos inválido. Use formato: '_izq,_der'"}
        else:
            suffixes = ('_x', '_y')
        
        # Realizar el JOIN
        if columna_izq == col_der:
            # Si las columnas tienen el mismo nombre, usar on
            df_result = pd.merge(
                df_izq, df_der,
                on=columna_izq,
                how=tipo_join,
                suffixes=suffixes
            )
        else:
            # Si las columnas tienen nombres diferentes, usar left_on y right_on
            df_result = pd.merge(
                df_izq, df_der,
                left_on=columna_izq,
                right_on=col_der,
                how=tipo_join,
                suffixes=suffixes
            )
        
        # Guardar resultado
        context.set_variable(resultado_var, df_result)
        
        return {
            "success": True,
            "message": f"Datasets unidos con {tipo_join.upper()} JOIN en '{resultado_var}' ({len(df_result)} filas)",
            "filas_izq": len(df_izq),
            "filas_der": len(df_der),
            "filas_resultado": len(df_result),
            "columnas_resultado": len(df_result.columns),
            "tipo_join": tipo_join,
            "columnas_union": f"{columna_izq} = {col_der}"
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error uniendo datasets: {str(e)}"}


@action(
    category="procesamiento",
    name="Concatenar Datasets", 
    description="Concatena múltiples DataFrames verticalmente (filas) u horizontalmente (columnas)",
    schema=[
        {
            "key": "dataframes_vars",
            "label": "Variables DataFrames",
            "type": "text",
            "required": True,
            "description": "Nombres de variables que contienen los DataFrames (separadas por coma)"
        },
        {
            "key": "direccion",
            "label": "Dirección de concatenación",
            "type": "select",
            "required": True,
            "options": [
                {"value": "vertical", "label": "Vertical (apilar filas)"},
                {"value": "horizontal", "label": "Horizontal (unir columnas)"}
            ],
            "description": "Cómo concatenar los DataFrames"
        },
        {
            "key": "ignorar_indices",
            "label": "Ignorar índices originales",
            "type": "select",
            "required": True,
            "options": [
                {"value": "true", "label": "Sí - crear nuevo índice"},
                {"value": "false", "label": "No - mantener índices originales"}
            ],
            "description": "Si crear un nuevo índice o mantener los originales"
        },
        {
            "key": "etiquetas",
            "label": "Etiquetas para identificar origen",
            "type": "text",
            "required": False,
            "description": "Etiquetas para identificar origen de cada DataFrame (separadas por coma)"
        },
        {
            "key": "resultado_var",
            "label": "Variable resultado",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable donde guardar el DataFrame concatenado"
        }
    ]
)
def concatenar_datasets(context: FlowContext, dataframes_vars: str, direccion: str,
                       ignorar_indices: str, resultado_var: str, etiquetas: str = None) -> Dict[str, Any]:
    """
    Concatena múltiples DataFrames vertical u horizontalmente.
    """
    try:
        # Procesar nombres de variables
        var_names = [name.strip() for name in dataframes_vars.split(',')]
        
        # Obtener DataFrames
        dataframes = []
        for var_name in var_names:
            df = context.get_variable(var_name)
            if df is None:
                return {"success": False, "error": f"Variable '{var_name}' no encontrada"}
            if not isinstance(df, pd.DataFrame):
                return {"success": False, "error": f"Variable '{var_name}' no es un DataFrame"}
            dataframes.append(df)
        
        if len(dataframes) < 2:
            return {"success": False, "error": "Se necesitan al menos 2 DataFrames para concatenar"}
        
        # Procesar etiquetas si se proporcionan
        keys = None
        if etiquetas:
            keys = [label.strip() for label in etiquetas.split(',')]
            if len(keys) != len(dataframes):
                return {"success": False, "error": f"Número de etiquetas ({len(keys)}) debe coincidir con número de DataFrames ({len(dataframes)})"}
        
        # Configurar parámetros de concatenación
        axis = 0 if direccion == "vertical" else 1  # 0=filas, 1=columnas
        ignore_index = ignorar_indices == "true"
        
        # Concatenar DataFrames
        df_result = pd.concat(
            dataframes,
            axis=axis,
            ignore_index=ignore_index,
            keys=keys
        )
        
        # Guardar resultado
        context.set_variable(resultado_var, df_result)
        
        # Calcular estadísticas del resultado
        total_filas_orig = sum(len(df) for df in dataframes)
        total_cols_orig = sum(len(df.columns) for df in dataframes)
        
        return {
            "success": True,
            "message": f"Concatenados {len(dataframes)} DataFrames {direccion}mente en '{resultado_var}'",
            "dataframes_concatenados": len(dataframes),
            "direccion": direccion,
            "filas_resultado": len(df_result),
            "columnas_resultado": len(df_result.columns),
            "total_filas_originales": total_filas_orig,
            "total_columnas_originales": total_cols_orig if direccion == "horizontal" else "N/A"
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error concatenando datasets: {str(e)}"}
