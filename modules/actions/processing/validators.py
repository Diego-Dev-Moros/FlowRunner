# modules/actions/processing/validators.py
"""
Acciones de validación de datos para FlowRunner.
Incluye validación de tipos, rangos, nulos y integridad de datos.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
from modules.core.decorators import action
from modules.core.context import FlowContext
import re
from datetime import datetime


@action(
    category="procesamiento",
    name="Validar Datos",
    description="Valida la calidad e integridad de los datos en un DataFrame",
    schema=[
        {
            "key": "dataframe_var",
            "label": "Variable DataFrame",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable que contiene el DataFrame"
        },
        {
            "key": "validaciones",
            "label": "Tipos de validación",
            "type": "text",
            "required": True,
            "description": "Validaciones a realizar: nulos,duplicados,tipos,rangos,patterns (separadas por coma)"
        },
        {
            "key": "columnas_especificas",
            "label": "Columnas específicas",
            "type": "text", 
            "required": False,
            "description": "Columnas específicas a validar (todas si está vacío, separadas por coma)"
        },
        {
            "key": "configuracion",
            "label": "Configuración de validación",
            "type": "text",
            "required": False,
            "description": "Config JSON: {\"col1\":{\"tipo\":\"int\",\"min\":0,\"max\":100}}"
        },
        {
            "key": "resultado_var",
            "label": "Variable resultado",
            "type": "text", 
            "required": True,
            "description": "Nombre de la variable donde guardar el reporte de validación"
        }
    ]
)
def validar_datos(context: FlowContext, dataframe_var: str, validaciones: str,
                 resultado_var: str, columnas_especificas: str = None,
                 configuracion: str = None) -> Dict[str, Any]:
    """
    Valida la calidad e integridad de datos en un DataFrame.
    """
    try:
        # Obtener el DataFrame
        df = context.get_variable(dataframe_var)
        if df is None:
            return {"success": False, "error": f"Variable '{dataframe_var}' no encontrada"}
            
        if not isinstance(df, pd.DataFrame):
            return {"success": False, "error": f"Variable '{dataframe_var}' no es un DataFrame"}
        
        # Procesar validaciones solicitadas
        validaciones_lista = [v.strip() for v in validaciones.split(',')]
        
        # Seleccionar columnas
        if columnas_especificas:
            target_cols = [col.strip() for col in columnas_especificas.split(',')]
            missing_cols = [col for col in target_cols if col not in df.columns]
            if missing_cols:
                return {"success": False, "error": f"Columnas no encontradas: {missing_cols}"}
        else:
            target_cols = list(df.columns)
        
        # Procesar configuración si existe
        config = {}
        if configuracion:
            try:
                import json
                config = json.loads(configuracion)
            except json.JSONDecodeError:
                return {"success": False, "error": "Configuración JSON inválida"}
        
        # Inicializar reporte de validación
        reporte = {
            "resumen": {
                "total_filas": len(df),
                "total_columnas": len(df.columns),
                "columnas_validadas": len(target_cols),
                "validaciones_realizadas": validaciones_lista
            },
            "detalles": {},
            "problemas": [],
            "recomendaciones": []
        }
        
        # VALIDACIÓN 1: Valores nulos
        if "nulos" in validaciones_lista:
            nulos_info = {}
            for col in target_cols:
                nulos_count = df[col].isnull().sum()
                nulos_percent = (nulos_count / len(df)) * 100
                nulos_info[col] = {
                    "cantidad_nulos": int(nulos_count),
                    "porcentaje_nulos": round(nulos_percent, 2)
                }
                
                if nulos_percent > 50:
                    reporte["problemas"].append(f"Columna '{col}': {nulos_percent:.1f}% valores nulos")
                elif nulos_percent > 10:
                    reporte["recomendaciones"].append(f"Columna '{col}': {nulos_percent:.1f}% valores nulos - considerar limpieza")
                    
            reporte["detalles"]["valores_nulos"] = nulos_info
        
        # VALIDACIÓN 2: Duplicados
        if "duplicados" in validaciones_lista:
            duplicados_total = df.duplicated().sum()
            duplicados_percent = (duplicados_total / len(df)) * 100
            
            reporte["detalles"]["duplicados"] = {
                "filas_duplicadas": int(duplicados_total),
                "porcentaje_duplicadas": round(duplicados_percent, 2)
            }
            
            if duplicados_percent > 5:
                reporte["problemas"].append(f"Dataset tiene {duplicados_percent:.1f}% filas duplicadas")
        
        # VALIDACIÓN 3: Tipos de datos
        if "tipos" in validaciones_lista:
            tipos_info = {}
            for col in target_cols:
                dtype_actual = str(df[col].dtype)
                unique_count = df[col].nunique()
                
                tipos_info[col] = {
                    "tipo_actual": dtype_actual,
                    "valores_unicos": int(unique_count),
                    "es_numerico": pd.api.types.is_numeric_dtype(df[col]),
                    "es_datetime": pd.api.types.is_datetime64_any_dtype(df[col]),
                    "es_categorico": pd.api.types.is_categorical_dtype(df[col])
                }
                
                # Validar contra configuración si existe
                if col in config and "tipo" in config[col]:
                    tipo_esperado = config[col]["tipo"]
                    if tipo_esperado == "int" and not pd.api.types.is_integer_dtype(df[col]):
                        reporte["problemas"].append(f"Columna '{col}': tipo esperado entero, encontrado {dtype_actual}")
                    elif tipo_esperado == "float" and not pd.api.types.is_float_dtype(df[col]):
                        reporte["problemas"].append(f"Columna '{col}': tipo esperado decimal, encontrado {dtype_actual}")
                    elif tipo_esperado == "string" and not pd.api.types.is_string_dtype(df[col]) and not pd.api.types.is_object_dtype(df[col]):
                        reporte["problemas"].append(f"Columna '{col}': tipo esperado texto, encontrado {dtype_actual}")
                        
            reporte["detalles"]["tipos_datos"] = tipos_info
        
        # VALIDACIÓN 4: Rangos (solo para columnas numéricas)
        if "rangos" in validaciones_lista:
            rangos_info = {}
            for col in target_cols:
                if pd.api.types.is_numeric_dtype(df[col]):
                    col_min = df[col].min()
                    col_max = df[col].max()
                    col_mean = df[col].mean()
                    
                    rangos_info[col] = {
                        "minimo": float(col_min) if not pd.isna(col_min) else None,
                        "maximo": float(col_max) if not pd.isna(col_max) else None,
                        "promedio": float(col_mean) if not pd.isna(col_mean) else None
                    }
                    
                    # Validar contra configuración si existe
                    if col in config:
                        if "min" in config[col] and col_min < config[col]["min"]:
                            reporte["problemas"].append(f"Columna '{col}': valor mínimo {col_min} menor que esperado {config[col]['min']}")
                        if "max" in config[col] and col_max > config[col]["max"]:
                            reporte["problemas"].append(f"Columna '{col}': valor máximo {col_max} mayor que esperado {config[col]['max']}")
                    
                    # Detectar outliers (valores fuera de 3 desviaciones estándar)
                    std_val = df[col].std()
                    if not pd.isna(std_val) and std_val > 0:
                        outliers = df[(np.abs(df[col] - col_mean) > 3 * std_val)][col]
                        if len(outliers) > 0:
                            rangos_info[col]["outliers_detectados"] = len(outliers)
                            if len(outliers) > len(df) * 0.05:  # Más del 5%
                                reporte["recomendaciones"].append(f"Columna '{col}': {len(outliers)} outliers detectados")
                    
            if rangos_info:
                reporte["detalles"]["rangos_numericos"] = rangos_info
        
        # VALIDACIÓN 5: Patrones (para columnas de texto)
        if "patterns" in validaciones_lista:
            patterns_info = {}
            for col in target_cols:
                if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]):
                    # Análisis básico de patrones
                    sample_values = df[col].dropna().head(100).astype(str)
                    
                    patterns_info[col] = {
                        "longitud_promedio": round(sample_values.str.len().mean(), 2),
                        "longitud_minima": int(sample_values.str.len().min()) if len(sample_values) > 0 else 0,
                        "longitud_maxima": int(sample_values.str.len().max()) if len(sample_values) > 0 else 0,
                        "contiene_numeros": sample_values.str.contains(r'\d').any() if len(sample_values) > 0 else False,
                        "contiene_especiales": sample_values.str.contains(r'[^a-zA-Z0-9\s]').any() if len(sample_values) > 0 else False,
                        "posibles_emails": sample_values.str.contains(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$').sum() if len(sample_values) > 0 else 0
                    }
                    
            if patterns_info:
                reporte["detalles"]["patrones_texto"] = patterns_info
        
        # Generar score de calidad general
        problemas_criticos = len(reporte["problemas"])
        recomendaciones_count = len(reporte["recomendaciones"])
        
        if problemas_criticos == 0 and recomendaciones_count == 0:
            calidad_score = 100
            calidad_nivel = "EXCELENTE"
        elif problemas_criticos == 0:
            calidad_score = max(85, 100 - recomendaciones_count * 5)
            calidad_nivel = "BUENA"
        elif problemas_criticos <= 2:
            calidad_score = max(60, 80 - problemas_criticos * 10 - recomendaciones_count * 3)
            calidad_nivel = "REGULAR" 
        else:
            calidad_score = max(20, 60 - problemas_criticos * 8 - recomendaciones_count * 2)
            calidad_nivel = "DEFICIENTE"
        
        reporte["resumen"]["calidad_score"] = calidad_score
        reporte["resumen"]["calidad_nivel"] = calidad_nivel
        reporte["resumen"]["problemas_criticos"] = problemas_criticos
        reporte["resumen"]["recomendaciones"] = recomendaciones_count
        
        # Guardar resultado
        context.set_variable(resultado_var, reporte)
        
        return {
            "success": True,
            "message": f"Validación completada: {calidad_nivel} ({calidad_score}%) - {problemas_criticos} problemas, {recomendaciones_count} recomendaciones",
            "calidad_score": calidad_score,
            "calidad_nivel": calidad_nivel,
            "problemas_encontrados": problemas_criticos,
            "recomendaciones": recomendaciones_count,
            "validaciones_realizadas": validaciones_lista
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error validando datos: {str(e)}"}
