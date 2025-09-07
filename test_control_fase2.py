# test_control_fase2.py
"""
Test completo de todas las acciones de control de flujo (Phase 2).
Incluye loops, conditions, exceptions y timing.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.core.context import FlowContext
from modules.core.registry import ActionRegistry

def execute_action_test(action_id: str, context: FlowContext, params: dict):
    """Helper para ejecutar acciones en tests."""
    action_spec = ActionRegistry.get_action(action_id)
    if not action_spec:
        return {"success": False, "error": f"Acción {action_id} no encontrada"}
    
    try:
        # Preparar parámetros incluyendo context
        final_params = {"context": context}
        final_params.update(params)
        
        # Ejecutar función
        result = action_spec.callable_func(**final_params)
        return result
    except Exception as e:
        return {"success": False, "error": f"Error ejecutando {action_id}: {str(e)}"}

def test_phase2_control_actions():
    """Test de todas las acciones de Phase 2."""
    
    # Inicializar contexto
    context = FlowContext()
    
    # Auto-descubrir acciones
    ActionRegistry.auto_discover_actions()
    
    print("🧪 TESTING PHASE 2 - CONTROL FLOW ACTIONS")
    print("=" * 60)
    
    # Preparar datos de prueba
    context.set_variable('lista_numeros', [1, 2, 3, 4, 5])
    context.set_variable('contador_test', 0)
    context.set_variable('valor_test', 10)
    
    # 1. TEST LOOPS (loops.py)
    print("\n🔄 TESTING LOOPS:")
    print("-" * 30)
    
    # Test bucle_for_rango
    result = execute_action_test('bucle_for_rango', context, {
        'variable_contador': 'i',
        'inicio': 1,
        'fin': 4,
        'paso': 1
    })
    print(f"✅ bucle_for_rango: {result.get('success', False)} - {result.get('message', result.get('error'))}")
    
    # Test bucle_for_lista
    result = execute_action_test('bucle_for_lista', context, {
        'lista_o_variable': 'lista_numeros',
        'variable_elemento': 'elemento',
        'variable_contador': 'idx',
        'max_iteraciones': 10
    })
    print(f"✅ bucle_for_lista: {result.get('success', False)} - {result.get('message', result.get('error'))}")
    
    # Test repetir_hasta
    context.set_variable('contador_hasta', 0)
    result = execute_action_test('repetir_hasta', context, {
        'condicion_parada': 'contador_hasta >= 3',
        'max_iteraciones': 5,
        'variable_iteracion': 'iter_count'
    })
    print(f"✅ repetir_hasta: {result.get('success', False)} - {result.get('message', result.get('error'))}")
    
    # Test interrumpir_flujo
    result = execute_action_test('interrumpir_flujo', context, {
        'tipo_interrupcion': 'break',
        'mensaje_log': 'Interrupción de prueba',
        'variable_estado': 'estado_interrupcion'
    })
    print(f"✅ interrumpir_flujo: {result.get('success', False)} - {result.get('message', result.get('error'))}")
    
    # 2. TEST CONDITIONS (conditions.py)
    print("\n🎯 TESTING CONDITIONS:")
    print("-" * 30)
    
    # Test condicional_multiple (switch-case)
    context.set_variable('estado', 'activo')
    result = execute_action_test('condicional_multiple', context, {
        'variable_evaluacion': 'estado',
        'casos': '{"activo": "estado_activo", "inactivo": "estado_inactivo", "default": "estado_desconocido"}',
        'comparacion_estricta': 'false',
        'resultado_variable': 'resultado_switch'
    })
    print(f"✅ condicional_multiple: {result.get('success', False)} - {result.get('message', result.get('error'))}")
    
    # Test condicional_and_or
    context.set_variable('edad', 25)
    context.set_variable('activo', True)
    result = execute_action_test('condicional_and_or', context, {
        'condicion_1': 'edad >= 18',
        'condicion_2': 'activo == True', 
        'operador': 'and',
        'resultado_variable': 'usuario_valido'
    })
    print(f"✅ condicional_and_or: {result.get('success', False)} - {result.get('message', result.get('error'))}")
    
    # Test esperar_condicion
    context.set_variable('proceso_completado', False)
    # Simular que el proceso se completa inmediatamente para el test
    context.set_variable('proceso_completado', True)
    result = execute_action_test('esperar_condicion', context, {
        'condicion_espera': 'proceso_completado == True',
        'timeout_segundos': 1,  # Reducido para test rápido
        'intervalo_verificacion': 0.1,
        'accion_timeout': 'error'
    })
    print(f"✅ esperar_condicion: {result.get('success', False)} - {result.get('message', result.get('error'))}")
    
    # 3. TEST EXCEPTIONS (exceptions.py)
    print("\n⚠️ TESTING EXCEPTIONS:")
    print("-" * 30)
    
    # Test try_catch_finally - caso exitoso
    result = execute_action_test('try_catch_finally', context, {
        'accion_catch': 'continue',
        'variable_error': 'ultimo_error',
        'error_esperado': 'any'
    })
    print(f"✅ try_catch_finally (éxito): {result.get('success', False)} - {result.get('message', result.get('error'))}")
    
    # Test validar_variable
    context.set_variable('email_test', 'user@example.com')
    result = execute_action_test('validar_variable', context, {
        'nombre_variable': 'email_test',
        'tipo_validacion': 'email',
        'es_obligatoria': 'true',
        'resultado_variable': 'validacion_email'
    })
    print(f"✅ validar_variable: {result.get('success', False)} - {result.get('message', result.get('error'))}")
    
    # 4. TEST TIMING (timing.py)
    print("\n⏰ TESTING TIMING:")
    print("-" * 30)
    
    # Test delay_dinamico
    result = execute_action_test('delay_dinamico', context, {
        'tipo_delay': 'fijo',
        'valor_base': 0.01,  # 10ms para que el test sea muy rápido
        'min_delay': 0.005,
        'max_delay': 1.0
    })
    print(f"✅ delay_dinamico: {result.get('success', False)} - {result.get('message', result.get('error'))}")
    
    # Test esperar_hasta_hora (continuará inmediatamente porque ya pasó)
    result = execute_action_test('esperar_hasta_hora', context, {
        'hora_objetivo': '00:00:01',  # Hora que ya pasó hoy
        'accion_si_pasado': 'continuar'
    })
    print(f"✅ esperar_hasta_hora: {result.get('success', False)} - {result.get('message', result.get('error'))}")
    
    # Test programar_ejecucion
    result = execute_action_test('programar_ejecucion', context, {
        'tipo_programacion': 'una_vez',
        'momento_inicial': '+1s',
        'variable_contador': 'ejecuciones_programadas'
    })
    print(f"✅ programar_ejecucion: {result.get('success', False)} - {result.get('message', result.get('error'))}")
    
    # RESUMEN FINAL
    print("\n📊 RESUMEN DE PHASE 2:")
    print("=" * 60)
    all_actions = ActionRegistry.list_all_actions()
    print(f"📦 Total acciones registradas: {len(all_actions)}")
    
    control_actions = [spec for spec in all_actions.values() if spec.category == 'control']
    print(f"🎮 Acciones de control: {len(control_actions)}")
    
    for action in control_actions:
        print(f"   • {action.name} ({action.id})")
    
    # Mostrar algunas variables del contexto
    print(f"\n🔢 Variables de contexto creadas durante tests:")
    # Variables que sabemos que se crearon durante los tests
    test_vars = ['lista_numeros', 'contador_test', 'valor_test', 'estado', 'edad', 'activo', 'email_test', 'i']
    for var_name in test_vars:
        value = context.get_variable(var_name)
        if value is not None:
            print(f"   • {var_name}: {value}")
    
    print(f"\n✅ Phase 2 Control Flow testing completado!")

if __name__ == "__main__":
    test_phase2_control_actions()
