# modules/actions/control/loops.py
"""
Acciones de bucles avanzados para FlowRunner.
Incluye for, do-while, repetir hasta, etc.
"""

import time
from typing import Dict, List, Any, Optional, Union
from modules.core.decorators import action
from modules.core.context import FlowContext


@action(
    category="control",
    name="Bucle For con Rango",
    description="Ejecuta un bucle for con un rango numérico específico",
    schema=[
        {
            "key": "variable_contador",
            "label": "Variable contador",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable que contendrá el valor actual del bucle"
        },
        {
            "key": "inicio",
            "label": "Valor inicial",
            "type": "number",
            "required": True,
            "description": "Valor inicial del contador"
        },
        {
            "key": "fin",
            "label": "Valor final",
            "type": "number",
            "required": True,
            "description": "Valor final del contador (inclusivo)"
        },
        {
            "key": "paso",
            "label": "Incremento",
            "type": "number",
            "required": False,
            "description": "Incremento en cada iteración (por defecto: 1)"
        },
        {
            "key": "max_iteraciones",
            "label": "Máximo iteraciones",
            "type": "number",
            "required": False,
            "description": "Límite máximo de iteraciones por seguridad (por defecto: 1000)"
        }
    ]
)
def bucle_for_rango(context: FlowContext, variable_contador: str, inicio: int, fin: int,
                   paso: int = 1, max_iteraciones: int = 1000) -> Dict[str, Any]:
    """
    Ejecuta un bucle for con rango numérico.
    """
    try:
        # Convertir parámetros numéricos si vienen como string
        if isinstance(inicio, str):
            inicio = int(inicio)
        if isinstance(fin, str):
            fin = int(fin)
        if isinstance(paso, str):
            paso = int(paso)
        if isinstance(max_iteraciones, str):
            max_iteraciones = int(max_iteraciones)
            
        if paso == 0:
            return {"success": False, "error": "El incremento no puede ser cero"}
        
        if paso > 0 and inicio > fin:
            return {"success": False, "error": "Con incremento positivo, inicio debe ser <= fin"}
        
        if paso < 0 and inicio < fin:
            return {"success": False, "error": "Con incremento negativo, inicio debe ser >= fin"}
        
        iteraciones = 0
        valores_procesados = []
        
        current = inicio
        while ((paso > 0 and current <= fin) or (paso < 0 and current >= fin)) and iteraciones < max_iteraciones:
            # Establecer variable del contador
            context.set_variable(variable_contador, current)
            valores_procesados.append(current)
            
            current += paso
            iteraciones += 1
            
            # Pequeña pausa para evitar bloqueos
            if iteraciones % 100 == 0:
                time.sleep(0.001)
        
        return {
            "success": True,
            "message": f"Bucle for completado: {iteraciones} iteraciones de {inicio} a {fin} (paso {paso})",
            "iteraciones_realizadas": iteraciones,
            "rango_procesado": f"{inicio} a {fin}",
            "paso_utilizado": paso,
            "valores_procesados": valores_procesados[:10] if len(valores_procesados) > 10 else valores_procesados,  # Solo primeros 10 para el reporte
            "total_valores": len(valores_procesados)
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error en bucle for: {str(e)}"}


@action(
    category="control",
    name="Bucle For sobre Lista",
    description="Itera sobre los elementos de una lista o array",
    schema=[
        {
            "key": "variable_elemento",
            "label": "Variable elemento actual",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable que contendrá el elemento actual"
        },
        {
            "key": "variable_indice",
            "label": "Variable índice",
            "type": "text",
            "required": False,
            "description": "Variable que contendrá el índice actual (opcional)"
        },
        {
            "key": "lista_variable",
            "label": "Variable lista",
            "type": "text",
            "required": True,
            "description": "Nombre de la variable que contiene la lista a iterar"
        },
        {
            "key": "max_iteraciones",
            "label": "Máximo iteraciones",
            "type": "number",
            "required": False,
            "description": "Límite máximo de iteraciones por seguridad (por defecto: 10000)"
        }
    ]
)
def bucle_for_lista(context: FlowContext, variable_elemento: str, lista_variable: str,
                   variable_indice: str = None, max_iteraciones: int = 10000) -> Dict[str, Any]:
    """
    Itera sobre los elementos de una lista.
    """
    try:
        # Obtener la lista
        lista = context.get_variable(lista_variable)
        if lista is None:
            return {"success": False, "error": f"Variable '{lista_variable}' no encontrada"}
        
        # Convertir a lista si es necesario
        if not isinstance(lista, (list, tuple)):
            # Intentar convertir desde pandas Series, numpy array, etc.
            try:
                if hasattr(lista, 'tolist'):
                    lista = lista.tolist()
                elif hasattr(lista, '__iter__') and not isinstance(lista, (str, dict)):
                    lista = list(lista)
                else:
                    return {"success": False, "error": f"Variable '{lista_variable}' no es iterable"}
            except:
                return {"success": False, "error": f"No se pudo convertir '{lista_variable}' a lista"}
        
        if len(lista) == 0:
            return {
                "success": True,
                "message": "Lista vacía, no se ejecutaron iteraciones",
                "iteraciones_realizadas": 0,
                "elementos_procesados": 0
            }
        
        elementos_procesados = []
        iteraciones_realizadas = min(len(lista), max_iteraciones)
        
        for i, elemento in enumerate(lista):
            if i >= max_iteraciones:
                break
                
            # Establecer variables
            context.set_variable(variable_elemento, elemento)
            if variable_indice:
                context.set_variable(variable_indice, i)
            
            elementos_procesados.append(elemento)
            
            # Pequeña pausa cada 100 iteraciones
            if i > 0 and i % 100 == 0:
                time.sleep(0.001)
        
        return {
            "success": True,
            "message": f"Bucle sobre lista completado: {iteraciones_realizadas} elementos procesados",
            "iteraciones_realizadas": iteraciones_realizadas,
            "total_elementos": len(lista),
            "elementos_muestra": elementos_procesados[:5] if len(elementos_procesados) > 5 else elementos_procesados,
            "truncado": len(lista) > max_iteraciones
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error en bucle for sobre lista: {str(e)}"}


@action(
    category="control", 
    name="Repetir Hasta",
    description="Repite acciones hasta que se cumpla una condición (do-while)",
    schema=[
        {
            "key": "variable_condicion",
            "label": "Variable de condición",
            "type": "text",
            "required": True,
            "description": "Variable que se evaluará como condición de parada"
        },
        {
            "key": "valor_objetivo",
            "label": "Valor objetivo",
            "type": "text",
            "required": True,
            "description": "Valor que debe tener la variable para detener el bucle"
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
                {"value": "<=", "label": "Menor o igual que"}
            ],
            "description": "Operador para comparar la variable con el valor objetivo"
        },
        {
            "key": "max_iteraciones",
            "label": "Máximo iteraciones",
            "type": "number",
            "required": False,
            "description": "Límite máximo de iteraciones por seguridad (por defecto: 1000)"
        },
        {
            "key": "delay_ms",
            "label": "Delay entre iteraciones (ms)",
            "type": "number",
            "required": False,
            "description": "Pausa en milisegundos entre cada iteración (por defecto: 100)"
        }
    ]
)
def repetir_hasta(context: FlowContext, variable_condicion: str, valor_objetivo: str,
                 operador: str, max_iteraciones: int = 1000, delay_ms: int = 100) -> Dict[str, Any]:
    """
    Repite hasta que se cumpla una condición (bucle do-while).
    """
    try:
        iteraciones = 0
        delay_segundos = delay_ms / 1000.0
        
        # Convertir valor objetivo al tipo apropiado
        try:
            # Intentar convertir a número
            if '.' in valor_objetivo:
                valor_objetivo_typed = float(valor_objetivo)
            else:
                valor_objetivo_typed = int(valor_objetivo)
        except ValueError:
            # Mantener como string
            valor_objetivo_typed = valor_objetivo
        
        condicion_cumplida = False
        ultimo_valor = None
        
        while not condicion_cumplida and iteraciones < max_iteraciones:
            iteraciones += 1
            
            # Obtener valor actual de la variable
            valor_actual = context.get_variable(variable_condicion)
            ultimo_valor = valor_actual
            
            if valor_actual is None:
                return {"success": False, "error": f"Variable '{variable_condicion}' no encontrada en iteración {iteraciones}"}
            
            # Evaluar condición
            try:
                # Intentar convertir valor actual al mismo tipo
                if isinstance(valor_objetivo_typed, (int, float)):
                    if isinstance(valor_actual, str):
                        valor_actual = float(valor_actual) if '.' in valor_actual else int(valor_actual)
                
                # Aplicar operador
                if operador == "==":
                    condicion_cumplida = valor_actual == valor_objetivo_typed
                elif operador == "!=":
                    condicion_cumplida = valor_actual != valor_objetivo_typed
                elif operador == ">":
                    condicion_cumplida = valor_actual > valor_objetivo_typed
                elif operador == ">=":
                    condicion_cumplida = valor_actual >= valor_objetivo_typed
                elif operador == "<":
                    condicion_cumplida = valor_actual < valor_objetivo_typed
                elif operador == "<=":
                    condicion_cumplida = valor_actual <= valor_objetivo_typed
                else:
                    return {"success": False, "error": f"Operador '{operador}' no válido"}
                    
            except (ValueError, TypeError):
                return {"success": False, "error": f"No se pudo comparar '{valor_actual}' {operador} '{valor_objetivo_typed}' en iteración {iteraciones}"}
            
            # Pausa si no se ha cumplido la condición
            if not condicion_cumplida and delay_segundos > 0:
                time.sleep(delay_segundos)
        
        if condicion_cumplida:
            return {
                "success": True,
                "message": f"Condición cumplida en {iteraciones} iteraciones: '{ultimo_valor}' {operador} '{valor_objetivo_typed}'",
                "iteraciones_realizadas": iteraciones,
                "condicion_cumplida": True,
                "valor_final": ultimo_valor,
                "valor_objetivo": valor_objetivo_typed,
                "operador_usado": operador
            }
        else:
            return {
                "success": False,
                "error": f"Alcanzado límite máximo de {max_iteraciones} iteraciones sin cumplir condición",
                "iteraciones_realizadas": iteraciones,
                "ultimo_valor": ultimo_valor,
                "valor_objetivo": valor_objetivo_typed
            }
        
    except Exception as e:
        return {"success": False, "error": f"Error en repetir hasta: {str(e)}"}


@action(
    category="control",
    name="Interrumpir Flujo",
    description="Interrumpe la ejecución del flujo (break/continue)",
    schema=[
        {
            "key": "tipo_interrupcion",
            "label": "Tipo de interrupción",
            "type": "select",
            "required": True,
            "options": [
                {"value": "break", "label": "Break - Salir del bucle actual"},
                {"value": "continue", "label": "Continue - Ir a la siguiente iteración"},
                {"value": "exit", "label": "Exit - Terminar todo el flujo"}
            ],
            "description": "Tipo de interrupción a ejecutar"
        },
        {
            "key": "condicion_variable",
            "label": "Variable de condición",
            "type": "text",
            "required": False,
            "description": "Variable a evaluar para decidir si interrumpir (opcional)"
        },
        {
            "key": "condicion_valor",
            "label": "Valor de condición",
            "type": "text",
            "required": False,
            "description": "Valor para comparar con la variable (opcional)"
        },
        {
            "key": "mensaje_salida",
            "label": "Mensaje de salida",
            "type": "text",
            "required": False,
            "description": "Mensaje personalizado al interrumpir"
        }
    ]
)
def interrumpir_flujo(context: FlowContext, tipo_interrupcion: str, 
                     condicion_variable: str = None, condicion_valor: str = None,
                     mensaje_salida: str = None) -> Dict[str, Any]:
    """
    Interrumpe la ejecución del flujo con diferentes tipos de interrupción.
    """
    try:
        # Evaluar condición si se proporciona
        debe_interrumpir = True
        
        if condicion_variable and condicion_valor:
            valor_actual = context.get_variable(condicion_variable)
            if valor_actual is None:
                return {"success": False, "error": f"Variable de condición '{condicion_variable}' no encontrada"}
            
            # Comparación simple (==)
            debe_interrumpir = str(valor_actual) == str(condicion_valor)
        
        if not debe_interrumpir:
            return {
                "success": True,
                "message": "Condición no cumplida, continúa la ejecución normal",
                "interrumpido": False
            }
        
        # Preparar mensaje de salida
        if not mensaje_salida:
            if tipo_interrupcion == "break":
                mensaje_salida = "Saliendo del bucle actual"
            elif tipo_interrupcion == "continue":
                mensaje_salida = "Continuando a la siguiente iteración"
            elif tipo_interrupcion == "exit":
                mensaje_salida = "Terminando la ejecución del flujo"
            else:
                mensaje_salida = f"Interrupción tipo: {tipo_interrupcion}"
        
        # Establecer flag de interrupción en el contexto
        context.set_variable('__flow_interrupt_type', tipo_interrupcion)
        context.set_variable('__flow_interrupt_message', mensaje_salida)
        context.set_variable('__flow_interrupt_active', True)
        
        return {
            "success": True,
            "message": mensaje_salida,
            "interrumpido": True,
            "tipo_interrupcion": tipo_interrupcion,
            "condicion_evaluada": condicion_variable is not None
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error interrumpiendo flujo: {str(e)}"}
