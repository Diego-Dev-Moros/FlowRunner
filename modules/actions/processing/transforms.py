# modules/actions/processing/transforms.py
"""
Acciones de transformación de datos para FlowRunner.
Incluye filtrado, transformación de columnas, agrupamiento y más.
"""

import pandas as pd
from typing import Dict, List, Any, Optional, Union
from modules.core.decorators import action
from modules.core.context import FlowContext


@action(
    category="procesamiento", 
    name="Filtrar DataFrame",
    description="Filtra un DataFrame usando condiciones especificadas",
    schema=[
        {
            "key": "dataframe_var",
            "label": "Variable DataFrame", 
            "type": "text",
            "required": True,
            "description": "Nombre de la variable que contiene el DataFrame"
        },
        {
            "key": "columna",
            "label": "Columna a filtrar",
            "type": "text", 
            "required": True,
            "description": "Nombre de la columna para aplicar el filtro"
        },
        {
            "key": "operador",
            "label": "Operador",
            "type": "select",
            "required": True,
            "options": [
                {"value": "==", "label": "Igual a"},
                {"value": "!=", "label": "Diferente de"},
                {"value": ">", "label": "Mayor que"},
                {"value": ">=", "label": "Mayor o igual que"},
                {"value": "<", "label": "Menor que"},
                {"value": "<=", "label": "Menor o igual que"},
                {"value": "contains", "label": "Contiene texto"},
                {"value": "startswith", "label": "Comienza con"},
                {"value": "endswith", "label": "Termina con"},
                {"value": "isnull", "label": "Es nulo"},
                {"value": "notnull", "label": "No es nulo"}
            ],
            "description": "Operador para la condición de filtrado"
        },
        {
            "key": "valor",
            "label": "Valor de comparación",
            "type": "text",
            "required": False,
            "description": "Valor para comparar (no necesario para isnull/notnull)"
        },
        {
            "key": "resultado_var",
            "label": "Variable resultado",
            "type": "text", 
            "required": True,
            "description": "Nombre de la variable donde guardar el DataFrame filtrado"
        }
    ]
)
def filtrar_dataframe(context: FlowContext, dataframe_var: str, columna: str, 
                     operador: str, resultado_var: str, valor: str = None) -> Dict[str, Any]:
    """
    Filtra un DataFrame usando la condición especificada.
    """
    try:
        # Obtener el DataFrame
        df = context.get_variable(dataframe_var)
        if df is None:
            return {"success": False, "error": f"Variable '{dataframe_var}' no encontrada"}
        
        if not isinstance(df, pd.DataFrame):
            return {"success": False, "error": f"Variable '{dataframe_var}' no es un DataFrame"}
        
        # Verificar que la columna existe
        if columna not in df.columns:
            return {"success": False, "error": f"Columna '{columna}' no existe en el DataFrame"}
        
        # Aplicar filtro según el operador
        if operador == "==":
            filtered_df = df[df[columna] == valor]
        elif operador == "!=":
            filtered_df = df[df[columna] != valor]
        elif operador == ">":
            filtered_df = df[df[columna] > pd.to_numeric(valor)]
        elif operador == ">=":
            filtered_df = df[df[columna] >= pd.to_numeric(valor)]
        elif operador == "<":
            filtered_df = df[df[columna] < pd.to_numeric(valor)]
        elif operador == "<=":
            filtered_df = df[df[columna] <= pd.to_numeric(valor)]
        elif operador == "contains":
            filtered_df = df[df[columna].astype(str).str.contains(valor, na=False)]
        elif operador == "startswith":
            filtered_df = df[df[columna].astype(str).str.startswith(valor, na=False)]
        elif operador == "endswith":
            filtered_df = df[df[columna].astype(str).str.endswith(valor, na=False)]
        elif operador == "isnull":
            filtered_df = df[df[columna].isnull()]
        elif operador == "notnull":
            filtered_df = df[df[columna].notnull()]
        else:
            return {"success": False, "error": f"Operador '{operador}' no válido"}
        
        # Guardar resultado
        context.set_variable(resultado_var, filtered_df)
        
        return {
            "success": True,
            "message": f"DataFrame filtrado: {len(filtered_df)} filas de {len(df)} originales guardado en '{resultado_var}'",
            "filas_originales": len(df),
            "filas_filtradas": len(filtered_df)
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error filtrando DataFrame: {str(e)}"}


@action(
    category="procesamiento",
    name="Transformar Columnas", 
    description="Aplica transformaciones a columnas del DataFrame",
    schema=[
        {
            "key": "dataframe_var",
            "label": "Variable DataFrame",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable que contiene el DataFrame"
        },
        {
            "key": "columna", 
            "label": "Columna a transformar",
            "type": "text",
            "required": True,
            "description": "Nombre de la columna a transformar"
        },
        {
            "key": "transformacion",
            "label": "Tipo de transformación",
            "type": "select",
            "required": True,
            "options": [
                {"value": "upper", "label": "Mayúsculas"},
                {"value": "lower", "label": "Minúsculas"},
                {"value": "title", "label": "Título (Primera Mayúscula)"},
                {"value": "strip", "label": "Quitar espacios"},
                {"value": "replace", "label": "Reemplazar texto"},
                {"value": "numeric", "label": "Convertir a numérico"},
                {"value": "datetime", "label": "Convertir a fecha"},
                {"value": "multiply", "label": "Multiplicar por valor"},
                {"value": "add", "label": "Sumar valor"}
            ],
            "description": "Tipo de transformación a aplicar"
        },
        {
            "key": "parametro1",
            "label": "Parámetro 1",
            "type": "text", 
            "required": False,
            "description": "Primer parámetro (para replace: texto a buscar, para math: valor)"
        },
        {
            "key": "parametro2", 
            "label": "Parámetro 2",
            "type": "text",
            "required": False,
            "description": "Segundo parámetro (para replace: texto de reemplazo)"
        },
        {
            "key": "nueva_columna",
            "label": "Nueva columna",
            "type": "text",
            "required": False, 
            "description": "Nombre para nueva columna (si está vacío, modifica la original)"
        }
    ]
)
def transformar_columnas(context: FlowContext, dataframe_var: str, columna: str, 
                        transformacion: str, parametro1: str = None, parametro2: str = None,
                        nueva_columna: str = None) -> Dict[str, Any]:
    """
    Aplica transformaciones a columnas de un DataFrame.
    """
    try:
        # Obtener el DataFrame
        df = context.get_variable(dataframe_var)
        if df is None:
            return {"success": False, "error": f"Variable '{dataframe_var}' no encontrada"}
            
        if not isinstance(df, pd.DataFrame):
            return {"success": False, "error": f"Variable '{dataframe_var}' no es un DataFrame"}
            
        # Verificar que la columna existe
        if columna not in df.columns:
            return {"success": False, "error": f"Columna '{columna}' no existe en el DataFrame"}
        
        # Crear copia del DataFrame
        df_result = df.copy()
        target_col = nueva_columna if nueva_columna else columna
        
        # Aplicar transformación
        if transformacion == "upper":
            df_result[target_col] = df_result[columna].astype(str).str.upper()
        elif transformacion == "lower":
            df_result[target_col] = df_result[columna].astype(str).str.lower()  
        elif transformacion == "title":
            df_result[target_col] = df_result[columna].astype(str).str.title()
        elif transformacion == "strip":
            df_result[target_col] = df_result[columna].astype(str).str.strip()
        elif transformacion == "replace":
            if not parametro1:
                return {"success": False, "error": "Parámetro 1 (texto a buscar) requerido para replace"}
            parametro2 = parametro2 or ""
            df_result[target_col] = df_result[columna].astype(str).str.replace(parametro1, parametro2)
        elif transformacion == "numeric":
            df_result[target_col] = pd.to_numeric(df_result[columna], errors='coerce')
        elif transformacion == "datetime":
            df_result[target_col] = pd.to_datetime(df_result[columna], errors='coerce')
        elif transformacion == "multiply":
            if not parametro1:
                return {"success": False, "error": "Parámetro 1 (valor) requerido para multiply"}
            df_result[target_col] = pd.to_numeric(df_result[columna], errors='coerce') * float(parametro1)
        elif transformacion == "add":
            if not parametro1:
                return {"success": False, "error": "Parámetro 1 (valor) requerido para add"}
            df_result[target_col] = pd.to_numeric(df_result[columna], errors='coerce') + float(parametro1)
        else:
            return {"success": False, "error": f"Transformación '{transformacion}' no válida"}
        
        # Guardar resultado
        context.set_variable(dataframe_var, df_result)
        
        action_desc = f"Transformación '{transformacion}' aplicada a columna '{columna}'"
        if nueva_columna:
            action_desc += f" -> nueva columna '{nueva_columna}'"
            
        return {
            "success": True,
            "message": action_desc,
            "columna_transformada": target_col,
            "filas_procesadas": len(df_result)
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error transformando columnas: {str(e)}"}


@action(
    category="procesamiento",
    name="Agrupar Datos",
    description="Agrupa datos por una o más columnas y calcula estadísticas",
    schema=[
        {
            "key": "dataframe_var",
            "label": "Variable DataFrame",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable que contiene el DataFrame"
        },
        {
            "key": "columnas_grupo",
            "label": "Columnas para agrupar",
            "type": "text",
            "required": True, 
            "description": "Columnas para agrupar (separadas por coma)"
        },
        {
            "key": "columna_agregacion",
            "label": "Columna para agregar",
            "type": "text",
            "required": True,
            "description": "Columna sobre la cual aplicar la función de agregación"
        },
        {
            "key": "funcion_agregacion",
            "label": "Función de agregación",
            "type": "select",
            "required": True,
            "options": [
                {"value": "count", "label": "Contar"},
                {"value": "sum", "label": "Sumar"},
                {"value": "mean", "label": "Promedio"},
                {"value": "median", "label": "Mediana"},
                {"value": "min", "label": "Mínimo"},
                {"value": "max", "label": "Máximo"},
                {"value": "std", "label": "Desviación estándar"},
                {"value": "var", "label": "Varianza"}
            ],
            "description": "Función estadística a aplicar"
        },
        {
            "key": "resultado_var",
            "label": "Variable resultado",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable donde guardar el resultado agrupado"
        }
    ]
)
def agrupar_datos(context: FlowContext, dataframe_var: str, columnas_grupo: str,
                 columna_agregacion: str, funcion_agregacion: str, 
                 resultado_var: str) -> Dict[str, Any]:
    """
    Agrupa datos y calcula estadísticas.
    """
    try:
        # Obtener el DataFrame
        df = context.get_variable(dataframe_var)
        if df is None:
            return {"success": False, "error": f"Variable '{dataframe_var}' no encontrada"}
            
        if not isinstance(df, pd.DataFrame):
            return {"success": False, "error": f"Variable '{dataframe_var}' no es un DataFrame"}
        
        # Procesar columnas de agrupamiento
        group_cols = [col.strip() for col in columnas_grupo.split(',')]
        
        # Verificar que las columnas existen
        missing_cols = [col for col in group_cols if col not in df.columns]
        if missing_cols:
            return {"success": False, "error": f"Columnas no encontradas: {missing_cols}"}
            
        if columna_agregacion not in df.columns:
            return {"success": False, "error": f"Columna de agregación '{columna_agregacion}' no encontrada"}
        
        # Realizar agrupamiento
        grouped = df.groupby(group_cols)[columna_agregacion]
        
        # Aplicar función de agregación
        if funcion_agregacion == "count":
            result = grouped.count().reset_index()
        elif funcion_agregacion == "sum":
            result = grouped.sum().reset_index()
        elif funcion_agregacion == "mean":
            result = grouped.mean().reset_index()
        elif funcion_agregacion == "median":
            result = grouped.median().reset_index()
        elif funcion_agregacion == "min":
            result = grouped.min().reset_index()
        elif funcion_agregacion == "max":
            result = grouped.max().reset_index()
        elif funcion_agregacion == "std":
            result = grouped.std().reset_index()
        elif funcion_agregacion == "var":
            result = grouped.var().reset_index()
        else:
            return {"success": False, "error": f"Función de agregación '{funcion_agregacion}' no válida"}
        
        # Renombrar columna resultado
        result = result.rename(columns={columna_agregacion: f"{columna_agregacion}_{funcion_agregacion}"})
        
        # Guardar resultado  
        context.set_variable(resultado_var, result)
        
        return {
            "success": True,
            "message": f"Datos agrupados por {group_cols} con {funcion_agregacion} en '{resultado_var}'",
            "grupos_creados": len(result),
            "columnas_grupo": group_cols,
            "funcion_aplicada": funcion_agregacion
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error agrupando datos: {str(e)}"}


@action(
    category="procesamiento",
    name="Eliminar Duplicados",
    description="Elimina filas duplicadas del DataFrame",
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
            "label": "Columnas para comparar", 
            "type": "text",
            "required": False,
            "description": "Columnas a considerar para duplicados (todas si está vacío, separadas por coma)"
        },
        {
            "key": "mantener",
            "label": "Registro a mantener",
            "type": "select",
            "required": True,
            "options": [
                {"value": "first", "label": "Primer registro"},
                {"value": "last", "label": "Último registro"},
                {"value": "false", "label": "Eliminar todos los duplicados"}
            ],
            "description": "Cuál registro mantener cuando hay duplicados"
        }
    ]
)
def eliminar_duplicados(context: FlowContext, dataframe_var: str, 
                       columnas: str = None, mantener: str = "first") -> Dict[str, Any]:
    """
    Elimina duplicados de un DataFrame.
    """
    try:
        # Obtener el DataFrame
        df = context.get_variable(dataframe_var)
        if df is None:
            return {"success": False, "error": f"Variable '{dataframe_var}' no encontrada"}
            
        if not isinstance(df, pd.DataFrame):
            return {"success": False, "error": f"Variable '{dataframe_var}' no es un DataFrame"}
        
        filas_originales = len(df)
        
        # Procesar columnas si se especifican
        subset_cols = None
        if columnas:
            subset_cols = [col.strip() for col in columnas.split(',')]
            missing_cols = [col for col in subset_cols if col not in df.columns]
            if missing_cols:
                return {"success": False, "error": f"Columnas no encontradas: {missing_cols}"}
        
        # Eliminar duplicados
        keep_option = mantener if mantener != "false" else False
        df_result = df.drop_duplicates(subset=subset_cols, keep=keep_option)
        
        # Guardar resultado
        context.set_variable(dataframe_var, df_result)
        
        filas_eliminadas = filas_originales - len(df_result)
        
        return {
            "success": True,
            "message": f"Eliminados {filas_eliminadas} duplicados. {len(df_result)} filas restantes",
            "filas_originales": filas_originales,
            "filas_eliminadas": filas_eliminadas,
            "filas_resultantes": len(df_result)
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error eliminando duplicados: {str(e)}"}


@action(
    category="procesamiento",
    name="Ordenar Avanzado",
    description="Ordena DataFrame por múltiples columnas con criterios específicos",
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
            "label": "Columnas para ordenar",
            "type": "text",
            "required": True,
            "description": "Columnas para ordenar (separadas por coma)"
        },
        {
            "key": "orden",
            "label": "Orden de clasificación",
            "type": "select",
            "required": True,
            "options": [
                {"value": "asc", "label": "Ascendente"},
                {"value": "desc", "label": "Descendente"}
            ],
            "description": "Orden para todas las columnas"
        },
        {
            "key": "nulos_al_final",
            "label": "Valores nulos al final",
            "type": "select",
            "required": True,
            "options": [
                {"value": "true", "label": "Sí"},
                {"value": "false", "label": "No"}
            ],
            "description": "Colocar valores nulos al final del ordenamiento"
        }
    ]
)
def ordenar_avanzado(context: FlowContext, dataframe_var: str, columnas: str,
                    orden: str = "asc", nulos_al_final: str = "true") -> Dict[str, Any]:
    """
    Ordena un DataFrame por múltiples columnas con opciones avanzadas.
    """
    try:
        # Obtener el DataFrame
        df = context.get_variable(dataframe_var)
        if df is None:
            return {"success": False, "error": f"Variable '{dataframe_var}' no encontrada"}
            
        if not isinstance(df, pd.DataFrame):
            return {"success": False, "error": f"Variable '{dataframe_var}' no es un DataFrame"}
        
        # Procesar columnas
        sort_cols = [col.strip() for col in columnas.split(',')]
        missing_cols = [col for col in sort_cols if col not in df.columns]
        if missing_cols:
            return {"success": False, "error": f"Columnas no encontradas: {missing_cols}"}
        
        # Configurar parámetros de ordenamiento
        ascending = orden == "asc"
        na_position = "last" if nulos_al_final == "true" else "first"
        
        # Ordenar DataFrame
        df_result = df.sort_values(
            by=sort_cols, 
            ascending=ascending, 
            na_position=na_position
        ).reset_index(drop=True)
        
        # Guardar resultado
        context.set_variable(dataframe_var, df_result)
        
        return {
            "success": True,
            "message": f"DataFrame ordenado por {sort_cols} en orden {'ascendente' if ascending else 'descendente'}",
            "columnas_ordenamiento": sort_cols,
            "orden": orden,
            "filas_ordenadas": len(df_result)
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error ordenando DataFrame: {str(e)}"}


@action(
    category="procesamiento",
    name="Crear Tabla Pivote",
    description="Crea una tabla pivote a partir del DataFrame",
    schema=[
        {
            "key": "dataframe_var",
            "label": "Variable DataFrame",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable que contiene el DataFrame"
        },
        {
            "key": "columna_indice",
            "label": "Columna índice",
            "type": "text", 
            "required": True,
            "description": "Columna que será el índice de la tabla pivote"
        },
        {
            "key": "columna_columnas",
            "label": "Columna para columnas",
            "type": "text",
            "required": True,
            "description": "Columna cuyos valores únicos serán las nuevas columnas"
        },
        {
            "key": "columna_valores",
            "label": "Columna de valores",
            "type": "text",
            "required": True,
            "description": "Columna que contiene los valores a agregar"
        },
        {
            "key": "funcion_agregacion",
            "label": "Función de agregación",
            "type": "select",
            "required": True,
            "options": [
                {"value": "sum", "label": "Sumar"},
                {"value": "mean", "label": "Promedio"},
                {"value": "count", "label": "Contar"},
                {"value": "min", "label": "Mínimo"},
                {"value": "max", "label": "Máximo"}
            ],
            "description": "Función para agregar valores duplicados"
        },
        {
            "key": "resultado_var",
            "label": "Variable resultado",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable donde guardar la tabla pivote"
        }
    ]
)
def pivotar_tabla(context: FlowContext, dataframe_var: str, columna_indice: str,
                 columna_columnas: str, columna_valores: str, funcion_agregacion: str,
                 resultado_var: str) -> Dict[str, Any]:
    """
    Crea una tabla pivote del DataFrame.
    """
    try:
        # Obtener el DataFrame
        df = context.get_variable(dataframe_var)
        if df is None:
            return {"success": False, "error": f"Variable '{dataframe_var}' no encontrada"}
            
        if not isinstance(df, pd.DataFrame):
            return {"success": False, "error": f"Variable '{dataframe_var}' no es un DataFrame"}
        
        # Verificar que las columnas existen
        required_cols = [columna_indice, columna_columnas, columna_valores]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return {"success": False, "error": f"Columnas no encontradas: {missing_cols}"}
        
        # Crear tabla pivote
        pivot_table = df.pivot_table(
            index=columna_indice,
            columns=columna_columnas, 
            values=columna_valores,
            aggfunc=funcion_agregacion,
            fill_value=0
        )
        
        # Resetear índice para convertir en DataFrame normal
        pivot_df = pivot_table.reset_index()
        
        # Limpiar nombres de columnas
        pivot_df.columns.name = None
        
        # Guardar resultado
        context.set_variable(resultado_var, pivot_df)
        
        return {
            "success": True,
            "message": f"Tabla pivote creada en '{resultado_var}' ({len(pivot_df)} filas, {len(pivot_df.columns)} columnas)",
            "filas": len(pivot_df),
            "columnas": len(pivot_df.columns),
            "funcion_aplicada": funcion_agregacion
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error creando tabla pivote: {str(e)}"}
