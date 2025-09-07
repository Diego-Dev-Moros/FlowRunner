# modules/actions/control/exceptions.py
"""
Acciones para manejo de excepciones y errores en FlowRunner.
Incluye try/catch/finally, validaciones, etc.
"""

from typing import Dict, List, Any, Optional, Union
from modules.core.decorators import action
from modules.core.context import FlowContext


@action(
    category="control",
    name="Try-Catch-Finally",
    description="Manejo de errores con bloques try/catch/finally",
    schema=[
        {
            "key": "variable_error",
            "label": "Variable para error",
            "type": "text",
            "required": False,
            "description": "Variable donde guardar información del error si ocurre"
        },
        {
            "key": "error_esperado",
            "label": "Tipo de error esperado",
            "type": "select",
            "required": False,
            "options": [
                {"value": "any", "label": "Cualquier error"},
                {"value": "variable_not_found", "label": "Variable no encontrada"},
                {"value": "type_error", "label": "Error de tipo"},
                {"value": "value_error", "label": "Error de valor"},
                {"value": "file_not_found", "label": "Archivo no encontrado"},
                {"value": "permission_error", "label": "Error de permisos"},
                {"value": "timeout", "label": "Timeout"},
                {"value": "custom", "label": "Error personalizado"}
            ],
            "description": "Tipo específico de error a capturar (opcional)"
        },
        {
            "key": "patron_error",
            "label": "Patrón de error",
            "type": "text",
            "required": False,
            "description": "Texto que debe contener el mensaje de error (opcional)"
        },
        {
            "key": "accion_catch",
            "label": "Acción en catch",
            "type": "select",
            "required": True,
            "options": [
                {"value": "continue", "label": "Continuar ejecución"},
                {"value": "stop", "label": "Detener flujo"},
                {"value": "retry", "label": "Reintentar acción"},
                {"value": "log_only", "label": "Solo registrar error"}
            ],
            "description": "Qué hacer cuando se captura un error"
        },
        {
            "key": "max_reintentos",
            "label": "Máximo reintentos",
            "type": "number",
            "required": False,
            "description": "Número máximo de reintentos si accion_catch es 'retry' (por defecto: 3)"
        },
        {
            "key": "delay_reintento",
            "label": "Delay entre reintentos (ms)",
            "type": "number",
            "required": False,
            "description": "Pausa entre reintentos en milisegundos (por defecto: 1000)"
        }
    ]
)
def try_catch_finally(context: FlowContext, accion_catch: str, variable_error: str = None,
                     error_esperado: str = None, patron_error: str = None,
                     max_reintentos: int = 3, delay_reintento: int = 1000) -> Dict[str, Any]:
    """
    Configura manejo de errores para las siguientes acciones.
    """
    try:
        import time
        
        # Configurar el contexto de manejo de errores
        error_config = {
            "activo": True,
            "variable_error": variable_error,
            "error_esperado": error_esperado,
            "patron_error": patron_error,
            "accion_catch": accion_catch,
            "max_reintentos": max_reintentos,
            "delay_reintento": delay_reintento / 1000.0,
            "reintentos_actuales": 0,
            "errores_capturados": []
        }
        
        context.set_variable('__error_handler_config', error_config)
        
        return {
            "success": True,
            "message": f"Manejo de errores configurado: {accion_catch} con {max_reintentos} reintentos máximo",
            "config": {
                "accion_catch": accion_catch,
                "error_esperado": error_esperado,
                "max_reintentos": max_reintentos,
                "delay_reintento_ms": delay_reintento
            }
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error configurando try-catch: {str(e)}"}


@action(
    category="control",
    name="Validar Variable",
    description="Valida que una variable cumpla condiciones específicas",
    schema=[
        {
            "key": "variable_nombre",
            "label": "Variable a validar",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable a validar"
        },
        {
            "key": "validaciones",
            "label": "Tipos de validación",
            "type": "text",
            "required": True,
            "description": "Tipos de validación separados por comas: exists,not_null,type,range,length,pattern"
        },
        {
            "key": "tipo_esperado",
            "label": "Tipo de dato esperado",
            "type": "select",
            "required": False,
            "options": [
                {"value": "str", "label": "Texto (string)"},
                {"value": "int", "label": "Entero"},
                {"value": "float", "label": "Decimal"},
                {"value": "bool", "label": "Booleano"},
                {"value": "list", "label": "Lista"},
                {"value": "dict", "label": "Diccionario"},
                {"value": "dataframe", "label": "DataFrame de pandas"}
            ],
            "description": "Tipo de dato que debe tener la variable"
        },
        {
            "key": "rango_min",
            "label": "Valor mínimo",
            "type": "number",
            "required": False,
            "description": "Valor mínimo permitido (para números)"
        },
        {
            "key": "rango_max",
            "label": "Valor máximo",
            "type": "number",
            "required": False,
            "description": "Valor máximo permitido (para números)"
        },
        {
            "key": "longitud_min",
            "label": "Longitud mínima",
            "type": "number",
            "required": False,
            "description": "Longitud mínima (para strings, listas, etc.)"
        },
        {
            "key": "longitud_max",
            "label": "Longitud máxima",
            "type": "number",
            "required": False,
            "description": "Longitud máxima (para strings, listas, etc.)"
        },
        {
            "key": "patron_regex",
            "label": "Patrón regex",
            "type": "text",
            "required": False,
            "description": "Expresión regular que debe cumplir (para strings)"
        },
        {
            "key": "accion_error",
            "label": "Acción si no es válido",
            "type": "select",
            "required": True,
            "options": [
                {"value": "error", "label": "Generar error"},
                {"value": "warning", "label": "Solo advertencia"},
                {"value": "fix", "label": "Intentar corregir"},
                {"value": "default", "label": "Asignar valor por defecto"}
            ],
            "description": "Qué hacer si la validación falla"
        },
        {
            "key": "valor_defecto",
            "label": "Valor por defecto",
            "type": "text",
            "required": False,
            "description": "Valor a asignar si la validación falla y accion_error es 'default'"
        }
    ]
)
def validar_variable(context: FlowContext, variable_nombre: str, validaciones: str,
                    accion_error: str, tipo_esperado: str = None, rango_min: float = None,
                    rango_max: float = None, longitud_min: int = None, longitud_max: int = None,
                    patron_regex: str = None, valor_defecto: str = None) -> Dict[str, Any]:
    """
    Valida una variable según múltiples criterios.
    """
    try:
        import re
        import pandas as pd
        
        # Parsear validaciones
        tipos_validacion = [v.strip() for v in validaciones.split(',')]
        resultados_validacion = []
        valor_actual = context.get_variable(variable_nombre)
        valor_original = valor_actual
        errores_encontrados = []
        warnings_encontrados = []
        
        # 1. VALIDACIÓN: exists
        if "exists" in tipos_validacion:
            if valor_actual is None:
                errores_encontrados.append(f"Variable '{variable_nombre}' no existe")
            else:
                resultados_validacion.append({"validacion": "exists", "resultado": "OK"})
        
        # Si la variable no existe y hay error, detener validaciones
        if valor_actual is None and errores_encontrados:
            if accion_error == "default" and valor_defecto:
                context.set_variable(variable_nombre, valor_defecto)
                return {
                    "success": True,
                    "message": f"Variable '{variable_nombre}' no existía, asignado valor por defecto: '{valor_defecto}'",
                    "accion_tomada": "valor_defecto_asignado",
                    "errores": errores_encontrados
                }
            elif accion_error == "error":
                return {"success": False, "error": errores_encontrados[0]}
            
        # Continuar validaciones si la variable existe
        if valor_actual is not None:
            
            # 2. VALIDACIÓN: not_null
            if "not_null" in tipos_validacion:
                if valor_actual == "" or valor_actual == [] or valor_actual == {}:
                    errores_encontrados.append(f"Variable '{variable_nombre}' está vacía")
                else:
                    resultados_validacion.append({"validacion": "not_null", "resultado": "OK"})
            
            # 3. VALIDACIÓN: type
            if "type" in tipos_validacion and tipo_esperado:
                tipo_actual = type(valor_actual).__name__
                
                # Mapear tipos especiales
                if tipo_esperado == "dataframe" and hasattr(valor_actual, 'iloc'):  # pandas DataFrame
                    tipo_valido = True
                elif tipo_esperado == "str" and isinstance(valor_actual, str):
                    tipo_valido = True
                elif tipo_esperado == "int" and isinstance(valor_actual, int):
                    tipo_valido = True
                elif tipo_esperado == "float" and isinstance(valor_actual, (int, float)):
                    tipo_valido = True
                elif tipo_esperado == "bool" and isinstance(valor_actual, bool):
                    tipo_valido = True
                elif tipo_esperado == "list" and isinstance(valor_actual, (list, tuple)):
                    tipo_valido = True
                elif tipo_esperado == "dict" and isinstance(valor_actual, dict):
                    tipo_valido = True
                else:
                    tipo_valido = False
                
                if not tipo_valido:
                    errores_encontrados.append(f"Variable '{variable_nombre}' es {tipo_actual}, esperado {tipo_esperado}")
                else:
                    resultados_validacion.append({"validacion": "type", "resultado": "OK", "tipo": tipo_actual})
            
            # 4. VALIDACIÓN: range (para números)
            if "range" in tipos_validacion and isinstance(valor_actual, (int, float)):
                if rango_min is not None and valor_actual < rango_min:
                    errores_encontrados.append(f"Variable '{variable_nombre}' ({valor_actual}) menor que mínimo ({rango_min})")
                elif rango_max is not None and valor_actual > rango_max:
                    errores_encontrados.append(f"Variable '{variable_nombre}' ({valor_actual}) mayor que máximo ({rango_max})")
                else:
                    resultados_validacion.append({"validacion": "range", "resultado": "OK", "valor": valor_actual})
            
            # 5. VALIDACIÓN: length
            if "length" in tipos_validacion:
                try:
                    longitud_actual = len(valor_actual)
                    if longitud_min is not None and longitud_actual < longitud_min:
                        errores_encontrados.append(f"Variable '{variable_nombre}' longitud {longitud_actual} menor que mínimo {longitud_min}")
                    elif longitud_max is not None and longitud_actual > longitud_max:
                        errores_encontrados.append(f"Variable '{variable_nombre}' longitud {longitud_actual} mayor que máximo {longitud_max}")
                    else:
                        resultados_validacion.append({"validacion": "length", "resultado": "OK", "longitud": longitud_actual})
                except TypeError:
                    warnings_encontrados.append(f"No se pudo validar longitud de '{variable_nombre}' (tipo {type(valor_actual).__name__})")
            
            # 6. VALIDACIÓN: pattern (regex para strings)
            if "pattern" in tipos_validacion and patron_regex:
                if isinstance(valor_actual, str):
                    if re.search(patron_regex, valor_actual):
                        resultados_validacion.append({"validacion": "pattern", "resultado": "OK"})
                    else:
                        errores_encontrados.append(f"Variable '{variable_nombre}' no coincide con patrón: {patron_regex}")
                else:
                    warnings_encontrados.append(f"Validación de patrón solo aplicable a strings, '{variable_nombre}' es {type(valor_actual).__name__}")
        
        # Procesar resultado de validaciones
        total_validaciones = len(tipos_validacion)
        validaciones_exitosas = len(resultados_validacion)
        
        if errores_encontrados:
            if accion_error == "error":
                return {
                    "success": False,
                    "error": f"Validación fallida: {'; '.join(errores_encontrados)}",
                    "errores": errores_encontrados,
                    "warnings": warnings_encontrados,
                    "validaciones_exitosas": validaciones_exitosas,
                    "total_validaciones": total_validaciones
                }
            elif accion_error == "warning":
                return {
                    "success": True,
                    "message": f"Validación completada con advertencias: {validaciones_exitosas}/{total_validaciones} exitosas",
                    "errores": errores_encontrados,
                    "warnings": warnings_encontrados,
                    "validaciones_exitosas": validaciones_exitosas,
                    "total_validaciones": total_validaciones
                }
            elif accion_error == "default" and valor_defecto:
                context.set_variable(variable_nombre, valor_defecto)
                return {
                    "success": True,
                    "message": f"Validación fallida, asignado valor por defecto: '{valor_defecto}'",
                    "errores": errores_encontrados,
                    "accion_tomada": "valor_defecto_asignado",
                    "valor_anterior": valor_original,
                    "valor_nuevo": valor_defecto
                }
            elif accion_error == "fix":
                # Intentar corregir automáticamente
                valor_corregido = valor_actual
                correcciones = []
                
                # Correcciones básicas
                if tipo_esperado == "str" and not isinstance(valor_actual, str):
                    valor_corregido = str(valor_actual)
                    correcciones.append("convertido a string")
                
                if tipo_esperado == "int" and isinstance(valor_actual, str):
                    try:
                        valor_corregido = int(float(valor_actual))
                        correcciones.append("convertido a entero")
                    except ValueError:
                        pass
                
                if tipo_esperado == "float" and isinstance(valor_actual, (str, int)):
                    try:
                        valor_corregido = float(valor_actual)
                        correcciones.append("convertido a decimal")
                    except ValueError:
                        pass
                
                if correcciones:
                    context.set_variable(variable_nombre, valor_corregido)
                    return {
                        "success": True,
                        "message": f"Variable corregida automáticamente: {'; '.join(correcciones)}",
                        "accion_tomada": "correccion_automatica",
                        "correcciones": correcciones,
                        "valor_anterior": valor_original,
                        "valor_nuevo": valor_corregido
                    }
        
        # Validación exitosa
        return {
            "success": True,
            "message": f"Validación exitosa: {validaciones_exitosas}/{total_validaciones} criterios cumplidos",
            "validaciones_exitosas": validaciones_exitosas,
            "total_validaciones": total_validaciones,
            "resultados": resultados_validacion,
            "warnings": warnings_encontrados if warnings_encontrados else None
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error validando variable: {str(e)}"}
