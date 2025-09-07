# modules/actions/control/timing.py
"""
Acciones de temporización y delays para FlowRunner.
Incluye pausas dinámicas, scheduling, etc.
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from modules.core.decorators import action
from modules.core.context import FlowContext


@action(
    category="control",
    name="Delay Dinámico",
    description="Pausa con duración calculada dinámicamente",
    schema=[
        {
            "key": "tipo_delay",
            "label": "Tipo de delay",
            "type": "select",
            "required": True,
            "options": [
                {"value": "fijo", "label": "Tiempo fijo en segundos"},
                {"value": "variable", "label": "Basado en variable"},
                {"value": "aleatorio", "label": "Tiempo aleatorio"},
                {"value": "progresivo", "label": "Incremento progresivo"},
                {"value": "exponencial", "label": "Backoff exponencial"}
            ],
            "description": "Cómo calcular el tiempo de pausa"
        },
        {
            "key": "valor_base",
            "label": "Valor base",
            "type": "number",
            "required": True,
            "description": "Tiempo base en segundos o nombre de variable"
        },
        {
            "key": "variable_multiplicador",
            "label": "Variable multiplicador",
            "type": "text",
            "required": False,
            "description": "Variable que contendrá el multiplicador (opcional)"
        },
        {
            "key": "min_delay",
            "label": "Delay mínimo",
            "type": "number",
            "required": False,
            "description": "Tiempo mínimo de pausa en segundos (por defecto: 0.1)"
        },
        {
            "key": "max_delay",
            "label": "Delay máximo",
            "type": "number",
            "required": False,
            "description": "Tiempo máximo de pausa en segundos (por defecto: 300)"
        },
        {
            "key": "contador_variable",
            "label": "Variable contador",
            "type": "text",
            "required": False,
            "description": "Variable para contar iteraciones (para progresivo/exponencial)"
        }
    ]
)
def delay_dinamico(context: FlowContext, tipo_delay: str, valor_base: float,
                  variable_multiplicador: str = None, min_delay: float = 0.1,
                  max_delay: float = 300.0, contador_variable: str = None) -> Dict[str, Any]:
    """
    Realiza una pausa con duración calculada dinámicamente.
    """
    try:
        import random
        
        # Convertir parámetros numéricos si vienen como string
        if isinstance(valor_base, str):
            valor_base = float(valor_base)
        if isinstance(min_delay, str):
            min_delay = float(min_delay)
        if isinstance(max_delay, str):
            max_delay = float(max_delay)
        
        tiempo_pausa = 0
        calculo_detalle = ""
        
        if tipo_delay == "fijo":
            tiempo_pausa = valor_base
            calculo_detalle = f"Tiempo fijo: {valor_base}s"
            
        elif tipo_delay == "variable":
            # Usar valor_base como nombre de variable
            variable_tiempo = context.get_variable(str(int(valor_base)) if valor_base == int(valor_base) else str(valor_base))
            if variable_tiempo is None:
                return {"success": False, "error": f"Variable '{valor_base}' no encontrada"}
            
            try:
                tiempo_pausa = float(variable_tiempo)
                calculo_detalle = f"Desde variable: {variable_tiempo}s"
            except (ValueError, TypeError):
                return {"success": False, "error": f"Variable '{valor_base}' no contiene un valor numérico válido"}
                
            # Aplicar multiplicador si existe
            if variable_multiplicador:
                multiplicador = context.get_variable(variable_multiplicador)
                if multiplicador is not None:
                    try:
                        tiempo_pausa *= float(multiplicador)
                        calculo_detalle += f" × {multiplicador} = {tiempo_pausa}s"
                    except (ValueError, TypeError):
                        pass
                        
        elif tipo_delay == "aleatorio":
            tiempo_pausa = random.uniform(min_delay, valor_base)
            calculo_detalle = f"Aleatorio entre {min_delay}s y {valor_base}s = {tiempo_pausa:.2f}s"
            
        elif tipo_delay == "progresivo":
            # Incremento lineal basado en contador
            contador = 1
            if contador_variable:
                contador_val = context.get_variable(contador_variable)
                if contador_val is not None:
                    try:
                        contador = int(contador_val)
                    except (ValueError, TypeError):
                        contador = 1
            
            tiempo_pausa = valor_base * contador
            calculo_detalle = f"Progresivo: {valor_base}s × {contador} = {tiempo_pausa}s"
            
            # Incrementar contador para próxima vez
            if contador_variable:
                context.set_variable(contador_variable, contador + 1)
                
        elif tipo_delay == "exponencial":
            # Backoff exponencial
            contador = 0
            if contador_variable:
                contador_val = context.get_variable(contador_variable)
                if contador_val is not None:
                    try:
                        contador = int(contador_val)
                    except (ValueError, TypeError):
                        contador = 0
            
            tiempo_pausa = valor_base * (2 ** contador)
            calculo_detalle = f"Exponencial: {valor_base}s × 2^{contador} = {tiempo_pausa}s"
            
            # Incrementar contador para próxima vez
            if contador_variable:
                context.set_variable(contador_variable, contador + 1)
        else:
            return {"success": False, "error": f"Tipo de delay '{tipo_delay}' no válido"}
        
        # Aplicar límites mín/máx
        tiempo_pausa = max(min_delay, min(tiempo_pausa, max_delay))
        
        # Ejecutar pausa
        tiempo_inicio = time.time()
        time.sleep(tiempo_pausa)
        tiempo_real = time.time() - tiempo_inicio
        
        return {
            "success": True,
            "message": f"Pausa completada: {tiempo_real:.2f}s ({calculo_detalle})",
            "tipo_delay": tipo_delay,
            "tiempo_calculado": tiempo_pausa,
            "tiempo_real": tiempo_real,
            "calculo": calculo_detalle
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error en delay dinámico: {str(e)}"}


@action(
    category="control",
    name="Esperar Hasta Hora",
    description="Espera hasta una hora específica del día",
    schema=[
        {
            "key": "hora_objetivo",
            "label": "Hora objetivo",
            "type": "text",
            "required": True,
            "description": "Hora objetivo en formato HH:MM:SS o HH:MM"
        },
        {
            "key": "fecha_objetivo",
            "label": "Fecha objetivo",
            "type": "text",
            "required": False,
            "description": "Fecha objetivo en formato YYYY-MM-DD (hoy si está vacío)"
        },
        {
            "key": "zona_horaria",
            "label": "Zona horaria",
            "type": "text",
            "required": False,
            "description": "Zona horaria (por defecto: local)"
        },
        {
            "key": "accion_si_pasado",
            "label": "Acción si ya pasó",
            "type": "select",
            "required": True,
            "options": [
                {"value": "siguiente_dia", "label": "Esperar hasta mañana"},
                {"value": "error", "label": "Generar error"},
                {"value": "continuar", "label": "Continuar inmediatamente"}
            ],
            "description": "Qué hacer si la hora objetivo ya pasó hoy"
        }
    ]
)
def esperar_hasta_hora(context: FlowContext, hora_objetivo: str, 
                      fecha_objetivo: str = None, zona_horaria: str = None,
                      accion_si_pasado: str = "siguiente_dia") -> Dict[str, Any]:
    """
    Espera hasta una hora específica.
    """
    try:
        from datetime import datetime, timedelta
        
        # Parsear hora objetivo
        try:
            if len(hora_objetivo.split(':')) == 2:
                hora_objetivo += ":00"  # Agregar segundos si no se especifican
            
            hora_parts = hora_objetivo.split(':')
            hora = int(hora_parts[0])
            minuto = int(hora_parts[1])
            segundo = int(hora_parts[2])
            
            if not (0 <= hora <= 23 and 0 <= minuto <= 59 and 0 <= segundo <= 59):
                return {"success": False, "error": f"Hora inválida: {hora_objetivo}"}
                
        except (ValueError, IndexError):
            return {"success": False, "error": f"Formato de hora inválido: {hora_objetivo}. Use HH:MM o HH:MM:SS"}
        
        # Determinar fecha objetivo
        ahora = datetime.now()
        if fecha_objetivo:
            try:
                fecha_parts = fecha_objetivo.split('-')
                ano = int(fecha_parts[0])
                mes = int(fecha_parts[1])
                dia = int(fecha_parts[2])
                fecha_base = datetime(ano, mes, dia)
            except (ValueError, IndexError):
                return {"success": False, "error": f"Formato de fecha inválido: {fecha_objetivo}. Use YYYY-MM-DD"}
        else:
            fecha_base = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Crear datetime objetivo
        momento_objetivo = fecha_base.replace(hour=hora, minute=minuto, second=segundo)
        
        # Verificar si ya pasó
        if momento_objetivo <= ahora:
            if accion_si_pasado == "error":
                return {
                    "success": False,
                    "error": f"La hora objetivo {hora_objetivo} ya pasó ({momento_objetivo})"
                }
            elif accion_si_pasado == "continuar":
                return {
                    "success": True,
                    "message": f"Hora objetivo {hora_objetivo} ya pasó, continuando inmediatamente",
                    "tiempo_espera": 0,
                    "momento_objetivo": momento_objetivo.isoformat(),
                    "accion_tomada": "continuar_inmediatamente"
                }
            elif accion_si_pasado == "siguiente_dia":
                momento_objetivo += timedelta(days=1)
        
        # Calcular tiempo de espera
        tiempo_espera = (momento_objetivo - ahora).total_seconds()
        
        if tiempo_espera > 86400:  # Más de 24 horas
            return {
                "success": False,
                "error": f"Tiempo de espera muy largo: {tiempo_espera/3600:.1f} horas. Máximo permitido: 24 horas"
            }
        
        # Realizar espera
        if tiempo_espera > 0:
            tiempo_inicio = time.time()
            
            # Para esperas largas, mostrar progreso cada minuto
            if tiempo_espera > 60:
                tiempo_transcurrido = 0
                while tiempo_transcurrido < tiempo_espera:
                    time.sleep(min(60, tiempo_espera - tiempo_transcurrido))
                    tiempo_transcurrido = time.time() - tiempo_inicio
                    
                    # Actualizar variable de progreso si se desea
                    progreso_pct = (tiempo_transcurrido / tiempo_espera) * 100
                    context.set_variable('__espera_progreso', {
                        "porcentaje": min(100, progreso_pct),
                        "tiempo_transcurrido": tiempo_transcurrido,
                        "tiempo_total": tiempo_espera,
                        "momento_objetivo": momento_objetivo.isoformat()
                    })
            else:
                time.sleep(tiempo_espera)
            
            tiempo_real = time.time() - tiempo_inicio
        else:
            tiempo_real = 0
        
        return {
            "success": True,
            "message": f"Espera completada hasta {momento_objetivo.strftime('%Y-%m-%d %H:%M:%S')}",
            "momento_objetivo": momento_objetivo.isoformat(),
            "tiempo_espera_calculado": tiempo_espera,
            "tiempo_espera_real": tiempo_real,
            "accion_tomada": accion_si_pasado if momento_objetivo <= ahora else "espera_normal"
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error esperando hasta hora: {str(e)}"}


@action(
    category="control",
    name="Programar Ejecución",
    description="Programa la ejecución para un momento específico o intervalo regular",
    schema=[
        {
            "key": "tipo_programacion",
            "label": "Tipo de programación",
            "type": "select",
            "required": True,
            "options": [
                {"value": "una_vez", "label": "Una sola vez"},
                {"value": "intervalo", "label": "Cada cierto tiempo"},
                {"value": "diario", "label": "Diario a la misma hora"},
                {"value": "semanal", "label": "Semanal"},
                {"value": "condicional", "label": "Cuando se cumpla condición"}
            ],
            "description": "Cómo programar la ejecución"
        },
        {
            "key": "momento_inicial",
            "label": "Momento inicial",
            "type": "text",
            "required": False,
            "description": "Cuándo empezar (formato: YYYY-MM-DD HH:MM:SS o +30s, +5m, +2h)"
        },
        {
            "key": "intervalo",
            "label": "Intervalo",
            "type": "text",
            "required": False,
            "description": "Intervalo de repetición (30s, 5m, 2h, 1d)"
        },
        {
            "key": "max_ejecuciones",
            "label": "Máximo ejecuciones",
            "type": "number",
            "required": False,
            "description": "Número máximo de ejecuciones (por defecto: sin límite)"
        },
        {
            "key": "variable_contador",
            "label": "Variable contador",
            "type": "text",
            "required": False,
            "description": "Variable para contar ejecuciones realizadas"
        },
        {
            "key": "condicion_parada",
            "label": "Condición de parada",
            "type": "text",
            "required": False,
            "description": "Variable que cuando sea 'true' o 'stop' terminará la programación"
        }
    ]
)
def programar_ejecucion(context: FlowContext, tipo_programacion: str, 
                       momento_inicial: str = None, intervalo: str = None,
                       max_ejecuciones: int = None, variable_contador: str = None,
                       condicion_parada: str = None) -> Dict[str, Any]:
    """
    Programa ejecución futura o repetitiva.
    """
    try:
        import re
        from datetime import datetime, timedelta
        
        # Parsear momento inicial
        momento_inicio = None
        if momento_inicial:
            # Formato relativo (+30s, +5m, +2h, +1d)
            if momento_inicial.startswith('+'):
                match = re.match(r'\+(\d+)([smhd])', momento_inicial)
                if match:
                    valor = int(match.group(1))
                    unidad = match.group(2)
                    
                    if unidad == 's':
                        delta = timedelta(seconds=valor)
                    elif unidad == 'm':
                        delta = timedelta(minutes=valor)
                    elif unidad == 'h':
                        delta = timedelta(hours=valor)
                    elif unidad == 'd':
                        delta = timedelta(days=valor)
                    
                    momento_inicio = datetime.now() + delta
                else:
                    return {"success": False, "error": f"Formato de momento inicial inválido: {momento_inicial}"}
            else:
                # Formato absoluto
                try:
                    momento_inicio = datetime.strptime(momento_inicial, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    try:
                        momento_inicio = datetime.strptime(momento_inicial, "%Y-%m-%d %H:%M")
                    except ValueError:
                        return {"success": False, "error": f"Formato de momento inicial inválido: {momento_inicial}"}
        else:
            momento_inicio = datetime.now()
        
        # Parsear intervalo si es necesario
        intervalo_segundos = None
        if intervalo and tipo_programacion in ["intervalo", "diario", "semanal"]:
            match = re.match(r'(\d+)([smhd])', intervalo)
            if match:
                valor = int(match.group(1))
                unidad = match.group(2)
                
                if unidad == 's':
                    intervalo_segundos = valor
                elif unidad == 'm':
                    intervalo_segundos = valor * 60
                elif unidad == 'h':
                    intervalo_segundos = valor * 3600
                elif unidad == 'd':
                    intervalo_segundos = valor * 86400
            else:
                return {"success": False, "error": f"Formato de intervalo inválido: {intervalo}"}
        
        # Configurar programación en el contexto
        config_programacion = {
            "activo": True,
            "tipo": tipo_programacion,
            "momento_inicio": momento_inicio.isoformat() if momento_inicio else None,
            "intervalo_segundos": intervalo_segundos,
            "max_ejecuciones": max_ejecuciones,
            "ejecuciones_realizadas": 0,
            "variable_contador": variable_contador,
            "condicion_parada": condicion_parada,
            "proxima_ejecucion": momento_inicio.isoformat() if momento_inicio else None
        }
        
        context.set_variable('__programacion_config', config_programacion)
        
        # Inicializar contador si se especifica
        if variable_contador:
            context.set_variable(variable_contador, 0)
        
        return {
            "success": True,
            "message": f"Programación configurada: {tipo_programacion} desde {momento_inicio}",
            "config": {
                "tipo": tipo_programacion,
                "momento_inicio": momento_inicio.isoformat() if momento_inicio else None,
                "intervalo": intervalo,
                "max_ejecuciones": max_ejecuciones
            },
            "proxima_ejecucion": momento_inicio.isoformat() if momento_inicio else "inmediata"
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error programando ejecución: {str(e)}"}
