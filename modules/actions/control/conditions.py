# modules/actions/control/conditions.py
"""
Acciones de condiciones avanzadas para FlowRunner.
Incluye switch/case, condiciones múltiples, etc.
"""

from typing import Dict, List, Any, Optional, Union
from modules.core.decorators import action
from modules.core.context import FlowContext
import re


@action(
    category="control",
    name="Condición Múltiple",
    description="Evalúa múltiples condiciones con operadores lógicos (switch/case)",
    schema=[
        {
            "key": "variable_evaluacion",
            "label": "Variable a evaluar",
            "type": "text",
            "required": True,
            "description": "Variable que se evaluará contra múltiples casos"
        },
        {
            "key": "casos",
            "label": "Casos (JSON)",
            "type": "text",
            "required": True,
            "description": "JSON con casos: {\"caso1\": \"accion1\", \"caso2\": \"accion2\", \"default\": \"accion_default\"}"
        },
        {
            "key": "comparacion_estricta",
            "label": "Comparación estricta",
            "type": "select",
            "required": True,
            "options": [
                {"value": "true", "label": "Sí - tipos y valores deben coincidir"},
                {"value": "false", "label": "No - solo valores deben coincidir"}
            ],
            "description": "Si usar comparación estricta (===) o relajada (==)"
        },
        {
            "key": "resultado_variable",
            "label": "Variable resultado",
            "type": "text",
            "required": True,
            "description": "Variable donde guardar el resultado del caso ejecutado"
        }
    ]
)
def condicional_multiple(context: FlowContext, variable_evaluacion: str, casos: str,
                        comparacion_estricta: str, resultado_variable: str) -> Dict[str, Any]:
    """
    Evalúa múltiples condiciones tipo switch/case.
    """
    try:
        # Obtener valor a evaluar
        valor = context.get_variable(variable_evaluacion)
        if valor is None:
            return {"success": False, "error": f"Variable '{variable_evaluacion}' no encontrada"}
        
        # Parsear casos JSON
        try:
            import json
            casos_dict = json.loads(casos)
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"JSON de casos inválido: {str(e)}"}
        
        if not isinstance(casos_dict, dict):
            return {"success": False, "error": "Los casos deben ser un objeto JSON"}
        
        # Evaluar casos
        caso_encontrado = None
        resultado_caso = None
        es_estricta = comparacion_estricta == "true"
        
        for caso, accion in casos_dict.items():
            if caso == "default":
                continue  # El default se evalúa al final
            
            # Convertir caso al tipo apropiado si no es comparación estricta
            caso_valor = caso
            if not es_estricta:
                try:
                    # Intentar convertir a número
                    if '.' in caso:
                        caso_valor = float(caso)
                    else:
                        caso_valor = int(caso)
                except ValueError:
                    # Mantener como string
                    caso_valor = caso
            
            # Comparar
            if es_estricta:
                coincide = valor == caso and type(valor) == type(caso_valor)
            else:
                coincide = str(valor) == str(caso_valor)
            
            if coincide:
                caso_encontrado = caso
                resultado_caso = accion
                break
        
        # Si no se encontró ningún caso, usar default
        if caso_encontrado is None:
            if "default" in casos_dict:
                caso_encontrado = "default"
                resultado_caso = casos_dict["default"]
            else:
                return {
                    "success": False,
                    "error": f"No se encontró caso para '{valor}' y no hay caso 'default'"
                }
        
        # Guardar resultado
        context.set_variable(resultado_variable, resultado_caso)
        
        return {
            "success": True,
            "message": f"Caso '{caso_encontrado}' ejecutado para valor '{valor}'",
            "valor_evaluado": valor,
            "caso_ejecutado": caso_encontrado,
            "resultado": resultado_caso,
            "total_casos": len(casos_dict),
            "comparacion_estricta": es_estricta
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error en condición múltiple: {str(e)}"}


@action(
    category="control",
    name="Condición AND/OR",
    description="Evalúa múltiples condiciones con operadores lógicos AND/OR",
    schema=[
        {
            "key": "condiciones",
            "label": "Condiciones (JSON)",
            "type": "text",
            "required": True,
            "description": "JSON array: [{\"variable\":\"var1\",\"operador\":\">\",\"valor\":\"10\"},{\"variable\":\"var2\",\"operador\":\"==\",\"valor\":\"activo\"}]"
        },
        {
            "key": "operador_logico",
            "label": "Operador lógico",
            "type": "select",
            "required": True,
            "options": [
                {"value": "AND", "label": "AND - Todas las condiciones deben ser verdaderas"},
                {"value": "OR", "label": "OR - Al menos una condición debe ser verdadera"}
            ],
            "description": "Cómo combinar las condiciones"
        },
        {
            "key": "resultado_variable",
            "label": "Variable resultado",
            "type": "text",
            "required": True,
            "description": "Variable donde guardar el resultado booleano"
        },
        {
            "key": "detalle_variable",
            "label": "Variable detalle",
            "type": "text",
            "required": False,
            "description": "Variable donde guardar detalles de evaluación (opcional)"
        }
    ]
)
def condicional_and_or(context: FlowContext, condiciones: str, operador_logico: str,
                      resultado_variable: str, detalle_variable: str = None) -> Dict[str, Any]:
    """
    Evalúa múltiples condiciones con AND/OR.
    """
    try:
        # Parsear condiciones JSON
        try:
            import json
            condiciones_list = json.loads(condiciones)
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"JSON de condiciones inválido: {str(e)}"}
        
        if not isinstance(condiciones_list, list):
            return {"success": False, "error": "Las condiciones deben ser un array JSON"}
        
        resultados_individuales = []
        resultado_final = None
        
        for i, condicion in enumerate(condiciones_list):
            if not isinstance(condicion, dict):
                return {"success": False, "error": f"Condición {i+1} debe ser un objeto"}
            
            if not all(key in condicion for key in ["variable", "operador", "valor"]):
                return {"success": False, "error": f"Condición {i+1} debe tener 'variable', 'operador' y 'valor'"}
            
            # Obtener valor de variable
            valor_actual = context.get_variable(condicion["variable"])
            if valor_actual is None:
                resultados_individuales.append({
                    "condicion": condicion,
                    "resultado": False,
                    "error": f"Variable '{condicion['variable']}' no encontrada"
                })
                continue
            
            # Convertir valor objetivo
            valor_objetivo = condicion["valor"]
            try:
                if '.' in str(valor_objetivo):
                    valor_objetivo = float(valor_objetivo)
                else:
                    valor_objetivo = int(valor_objetivo)
            except (ValueError, TypeError):
                pass  # Mantener como string
            
            # Evaluar condición
            try:
                operador = condicion["operador"]
                if operador == "==":
                    resultado_cond = valor_actual == valor_objetivo
                elif operador == "!=":
                    resultado_cond = valor_actual != valor_objetivo
                elif operador == ">":
                    resultado_cond = float(valor_actual) > float(valor_objetivo)
                elif operador == ">=":
                    resultado_cond = float(valor_actual) >= float(valor_objetivo)
                elif operador == "<":
                    resultado_cond = float(valor_actual) < float(valor_objetivo)
                elif operador == "<=":
                    resultado_cond = float(valor_actual) <= float(valor_objetivo)
                elif operador == "contains":
                    resultado_cond = str(valor_objetivo) in str(valor_actual)
                elif operador == "startswith":
                    resultado_cond = str(valor_actual).startswith(str(valor_objetivo))
                elif operador == "endswith":
                    resultado_cond = str(valor_actual).endswith(str(valor_objetivo))
                elif operador == "regex":
                    resultado_cond = bool(re.search(str(valor_objetivo), str(valor_actual)))
                else:
                    resultados_individuales.append({
                        "condicion": condicion,
                        "resultado": False,
                        "error": f"Operador '{operador}' no válido"
                    })
                    continue
                
                resultados_individuales.append({
                    "condicion": condicion,
                    "resultado": resultado_cond,
                    "valor_actual": valor_actual,
                    "valor_objetivo": valor_objetivo,
                    "operador": operador
                })
                
            except (ValueError, TypeError) as e:
                resultados_individuales.append({
                    "condicion": condicion,
                    "resultado": False,
                    "error": f"Error evaluando condición: {str(e)}"
                })
        
        # Calcular resultado final
        resultados_bool = [r["resultado"] for r in resultados_individuales if "error" not in r]
        
        if not resultados_bool:
            return {"success": False, "error": "No se pudieron evaluar las condiciones"}
        
        if operador_logico == "AND":
            resultado_final = all(resultados_bool)
        elif operador_logico == "OR":
            resultado_final = any(resultados_bool)
        else:
            return {"success": False, "error": f"Operador lógico '{operador_logico}' no válido"}
        
        # Guardar resultados
        context.set_variable(resultado_variable, resultado_final)
        
        if detalle_variable:
            detalle = {
                "resultado_final": resultado_final,
                "operador_logico": operador_logico,
                "total_condiciones": len(condiciones_list),
                "condiciones_verdaderas": sum(resultados_bool),
                "condiciones_evaluadas": resultados_individuales
            }
            context.set_variable(detalle_variable, detalle)
        
        return {
            "success": True,
            "message": f"Evaluación {operador_logico}: {resultado_final} ({sum(resultados_bool)}/{len(resultados_bool)} condiciones verdaderas)",
            "resultado_final": resultado_final,
            "condiciones_evaluadas": len(resultados_bool),
            "condiciones_verdaderas": sum(resultados_bool),
            "operador_logico": operador_logico
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error en condición AND/OR: {str(e)}"}


@action(
    category="control",
    name="Esperar Condición",
    description="Espera hasta que se cumpla una condición específica",
    schema=[
        {
            "key": "variable_condicion",
            "label": "Variable a evaluar",
            "type": "text",
            "required": True,
            "description": "Variable que se evaluará continuamente"
        },
        {
            "key": "operador",
            "label": "Operador de comparación",
            "type": "select",
            "required": True,
            "options": [
                {"value": "==", "label": "Igual a"},
                {"value": "!=", "label": "Diferente de"},
                {"value": ">", "label": "Mayor que"},
                {"value": ">=", "label": "Mayor o igual que"},
                {"value": "<", "label": "Menor que"},
                {"value": "<=", "label": "Menor o igual que"},
                {"value": "exists", "label": "Variable existe"},
                {"value": "not_exists", "label": "Variable no existe"}
            ],
            "description": "Operador para evaluar la condición"
        },
        {
            "key": "valor_esperado",
            "label": "Valor esperado",
            "type": "text",
            "required": False,
            "description": "Valor que debe tener la variable (no necesario para exists/not_exists)"
        },
        {
            "key": "timeout_segundos",
            "label": "Timeout (segundos)",
            "type": "number",
            "required": False,
            "description": "Tiempo máximo de espera en segundos (por defecto: 60)"
        },
        {
            "key": "intervalo_chequeo",
            "label": "Intervalo de chequeo (ms)",
            "type": "number",
            "required": False,
            "description": "Cada cuántos ms verificar la condición (por defecto: 1000)"
        }
    ]
)
def esperar_condicion(context: FlowContext, variable_condicion: str, operador: str,
                     valor_esperado: str = None, timeout_segundos: int = 60,
                     intervalo_chequeo: int = 1000) -> Dict[str, Any]:
    """
    Espera hasta que se cumpla una condición.
    """
    try:
        import time
        
        tiempo_inicio = time.time()
        intervalo_segundos = intervalo_chequeo / 1000.0
        chequeos_realizados = 0
        
        # Convertir valor esperado si es necesario
        valor_esperado_typed = valor_esperado
        if valor_esperado and operador in [">", ">=", "<", "<="]:
            try:
                valor_esperado_typed = float(valor_esperado) if '.' in valor_esperado else int(valor_esperado)
            except ValueError:
                return {"success": False, "error": f"Valor esperado '{valor_esperado}' no es numérico para operador '{operador}'"}
        
        while True:
            chequeos_realizados += 1
            tiempo_transcurrido = time.time() - tiempo_inicio
            
            # Verificar timeout
            if tiempo_transcurrido > timeout_segundos:
                return {
                    "success": False,
                    "error": f"Timeout alcanzado ({timeout_segundos}s) esperando condición",
                    "chequeos_realizados": chequeos_realizados,
                    "tiempo_transcurrido": round(tiempo_transcurrido, 2)
                }
            
            # Obtener valor actual
            if operador in ["exists", "not_exists"]:
                valor_actual = context.get_variable(variable_condicion)
                condicion_cumplida = (valor_actual is not None) if operador == "exists" else (valor_actual is None)
                valor_actual_display = valor_actual if valor_actual is not None else "None"
            else:
                valor_actual = context.get_variable(variable_condicion)
                if valor_actual is None:
                    condicion_cumplida = False
                    valor_actual_display = "None"
                else:
                    valor_actual_display = valor_actual
                    
                    try:
                        # Evaluar condición
                        if operador == "==":
                            condicion_cumplida = str(valor_actual) == str(valor_esperado_typed)
                        elif operador == "!=":
                            condicion_cumplida = str(valor_actual) != str(valor_esperado_typed)
                        elif operador in [">", ">=", "<", "<="]:
                            valor_actual_num = float(valor_actual)
                            if operador == ">":
                                condicion_cumplida = valor_actual_num > valor_esperado_typed
                            elif operador == ">=":
                                condicion_cumplida = valor_actual_num >= valor_esperado_typed
                            elif operador == "<":
                                condicion_cumplida = valor_actual_num < valor_esperado_typed
                            elif operador == "<=":
                                condicion_cumplida = valor_actual_num <= valor_esperado_typed
                        else:
                            return {"success": False, "error": f"Operador '{operador}' no soportado"}
                    except (ValueError, TypeError):
                        condicion_cumplida = False
            
            # Si la condición se cumple, salir
            if condicion_cumplida:
                return {
                    "success": True,
                    "message": f"Condición cumplida: '{variable_condicion}' {operador} '{valor_esperado}' después de {chequeos_realizados} chequeos",
                    "tiempo_espera": round(tiempo_transcurrido, 2),
                    "chequeos_realizados": chequeos_realizados,
                    "valor_final": valor_actual_display,
                    "condicion": f"{variable_condicion} {operador} {valor_esperado}"
                }
            
            # Esperar antes del siguiente chequeo
            time.sleep(intervalo_segundos)
        
    except Exception as e:
        return {"success": False, "error": f"Error esperando condición: {str(e)}"}
