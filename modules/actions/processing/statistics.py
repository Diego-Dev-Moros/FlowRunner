# modules/actions/processing/statistics.py
"""
Acciones de estadísticas y análisis de datos para FlowRunner.
Incluye cálculos estadísticos y normalización de datos.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
from modules.core.decorators import action
from modules.core.context import FlowContext


@action(
    category="procesamiento",
    name="Calcular Estadísticas",
    description="Calcula estadísticas descriptivas de columnas numéricas",
    schema=[
        {
            "key": "dataframe_var",
            "label": "Variable DataFrame",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable que contiene el DataFrame"
        },
        {
            "key": "columnas",
            "label": "Columnas a analizar",
            "type": "text",
            "required": False,
            "description": "Columnas específicas a analizar (todas las numéricas si está vacío, separadas por coma)"
        },
        {
            "key": "estadisticas",
            "label": "Estadísticas a calcular",
            "type": "text",
            "required": False,
            "description": "Estadísticas específicas: count,mean,std,min,25%,50%,75%,max (todas si está vacío, separadas por coma)"
        },
        {
            "key": "resultado_var",
            "label": "Variable resultado",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable donde guardar las estadísticas"
        },
        {
            "key": "formato_salida",
            "label": "Formato de salida",
            "type": "select",
            "required": True,
            "options": [
                {"value": "dataframe", "label": "DataFrame"},
                {"value": "dict", "label": "Diccionario"},
                {"value": "resumen", "label": "Resumen de texto"}
            ],
            "description": "Formato para guardar las estadísticas"
        }
    ]
)
def calcular_estadisticas(context: FlowContext, dataframe_var: str, resultado_var: str,
                         columnas: str = None, estadisticas: str = None,
                         formato_salida: str = "dataframe") -> Dict[str, Any]:
    """
    Calcula estadísticas descriptivas de un DataFrame.
    """
    try:
        # Obtener el DataFrame
        df = context.get_variable(dataframe_var)
        if df is None:
            return {"success": False, "error": f"Variable '{dataframe_var}' no encontrada"}
            
        if not isinstance(df, pd.DataFrame):
            return {"success": False, "error": f"Variable '{dataframe_var}' no es un DataFrame"}
        
        # Seleccionar columnas
        if columnas:
            target_cols = [col.strip() for col in columnas.split(',')]
            missing_cols = [col for col in target_cols if col not in df.columns]
            if missing_cols:
                return {"success": False, "error": f"Columnas no encontradas: {missing_cols}"}
            df_analysis = df[target_cols]
        else:
            # Solo columnas numéricas
            df_analysis = df.select_dtypes(include=[np.number])
            
        if df_analysis.empty:
            return {"success": False, "error": "No hay columnas numéricas para analizar"}
        
        # Calcular estadísticas
        if estadisticas:
            stats_list = [stat.strip() for stat in estadisticas.split(',')]
            # Validar estadísticas disponibles
            available_stats = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
            invalid_stats = [stat for stat in stats_list if stat not in available_stats]
            if invalid_stats:
                return {"success": False, "error": f"Estadísticas no válidas: {invalid_stats}"}
            
            stats_result = df_analysis.describe().loc[stats_list]
        else:
            stats_result = df_analysis.describe()
        
        # Formatear resultado según la salida solicitada
        if formato_salida == "dataframe":
            result = stats_result
        elif formato_salida == "dict":
            result = stats_result.to_dict()
        elif formato_salida == "resumen":
            # Crear resumen textual
            resumen_lines = []
            resumen_lines.append("=== ESTADÍSTICAS DESCRIPTIVAS ===")
            resumen_lines.append(f"Análisis de {len(df_analysis.columns)} columnas:")
            resumen_lines.append("")
            
            for col in df_analysis.columns:
                resumen_lines.append(f"COLUMNA: {col}")
                col_stats = stats_result[col]
                for stat_name, value in col_stats.items():
                    if pd.isna(value):
                        resumen_lines.append(f"  {stat_name}: N/A")
                    else:
                        resumen_lines.append(f"  {stat_name}: {value:.4f}")
                resumen_lines.append("")
                
            result = "\n".join(resumen_lines)
        
        # Guardar resultado
        context.set_variable(resultado_var, result)
        
        return {
            "success": True,
            "message": f"Estadísticas calculadas para {len(df_analysis.columns)} columnas en '{resultado_var}'",
            "columnas_analizadas": list(df_analysis.columns),
            "estadisticas_calculadas": list(stats_result.index) if hasattr(stats_result, 'index') else "resumen",
            "formato": formato_salida
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error calculando estadísticas: {str(e)}"}


@action(
    category="procesamiento", 
    name="Normalizar Datos",
    description="Normaliza columnas numéricas usando diferentes métodos",
    schema=[
        {
            "key": "dataframe_var",
            "label": "Variable DataFrame",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable que contiene el DataFrame"
        },
        {
            "key": "columnas",
            "label": "Columnas a normalizar",
            "type": "text",
            "required": False,
            "description": "Columnas específicas a normalizar (todas las numéricas si está vacío, separadas por coma)"
        },
        {
            "key": "metodo",
            "label": "Método de normalización",
            "type": "select",
            "required": True,
            "options": [
                {"value": "zscore", "label": "Z-Score (media=0, std=1)"},
                {"value": "minmax", "label": "Min-Max (0-1)"},
                {"value": "robust", "label": "Robusto (mediana y MAD)"},
                {"value": "unit", "label": "Vector unitario (norma=1)"}
            ],
            "description": "Método de normalización a aplicar"
        },
        {
            "key": "sufijo",
            "label": "Sufijo para nuevas columnas",
            "type": "text",
            "required": False,
            "description": "Sufijo para nuevas columnas normalizadas (si está vacío, reemplaza originales)"
        }
    ]
)
def normalizar_datos(context: FlowContext, dataframe_var: str, metodo: str,
                    columnas: str = None, sufijo: str = None) -> Dict[str, Any]:
    """
    Normaliza columnas numéricas de un DataFrame usando diferentes métodos.
    """
    try:
        # Obtener el DataFrame
        df = context.get_variable(dataframe_var)
        if df is None:
            return {"success": False, "error": f"Variable '{dataframe_var}' no encontrada"}
            
        if not isinstance(df, pd.DataFrame):
            return {"success": False, "error": f"Variable '{dataframe_var}' no es un DataFrame"}
        
        # Crear copia del DataFrame
        df_result = df.copy()
        
        # Seleccionar columnas a normalizar
        if columnas:
            target_cols = [col.strip() for col in columnas.split(',')]
            missing_cols = [col for col in target_cols if col not in df.columns]
            if missing_cols:
                return {"success": False, "error": f"Columnas no encontradas: {missing_cols}"}
        else:
            # Solo columnas numéricas
            target_cols = list(df.select_dtypes(include=[np.number]).columns)
            
        if not target_cols:
            return {"success": False, "error": "No hay columnas numéricas para normalizar"}
        
        normalized_cols = []
        
        # Aplicar normalización según el método
        for col in target_cols:
            # Verificar que la columna es numérica
            if not pd.api.types.is_numeric_dtype(df[col]):
                continue
                
            # Nombre de la nueva columna
            new_col_name = f"{col}_{sufijo}" if sufijo else col
            
            # Obtener datos numéricos (sin NaN)
            col_data = df[col].dropna()
            
            if col_data.empty:
                continue
                
            if metodo == "zscore":
                # Z-score: (x - mean) / std
                mean_val = col_data.mean()
                std_val = col_data.std()
                if std_val == 0:
                    df_result[new_col_name] = 0  # Si std=0, todos los valores son iguales
                else:
                    df_result[new_col_name] = (df[col] - mean_val) / std_val
                    
            elif metodo == "minmax":
                # Min-Max: (x - min) / (max - min)
                min_val = col_data.min()
                max_val = col_data.max()
                if min_val == max_val:
                    df_result[new_col_name] = 0  # Si todos iguales
                else:
                    df_result[new_col_name] = (df[col] - min_val) / (max_val - min_val)
                    
            elif metodo == "robust":
                # Robust: (x - median) / MAD
                median_val = col_data.median()
                mad_val = np.median(np.abs(col_data - median_val))
                if mad_val == 0:
                    df_result[new_col_name] = 0
                else:
                    df_result[new_col_name] = (df[col] - median_val) / mad_val
                    
            elif metodo == "unit":
                # Vector unitario: x / ||x||
                norm_val = np.linalg.norm(col_data.values)
                if norm_val == 0:
                    df_result[new_col_name] = 0
                else:
                    df_result[new_col_name] = df[col] / norm_val
            
            normalized_cols.append(new_col_name)
        
        if not normalized_cols:
            return {"success": False, "error": "No se pudieron normalizar las columnas especificadas"}
        
        # Guardar resultado
        context.set_variable(dataframe_var, df_result)
        
        return {
            "success": True,
            "message": f"Normalizadas {len(normalized_cols)} columnas usando método '{metodo}'",
            "columnas_normalizadas": normalized_cols,
            "metodo_aplicado": metodo,
            "columnas_originales": target_cols
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error normalizando datos: {str(e)}"}
