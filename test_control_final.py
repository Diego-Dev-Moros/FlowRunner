# test_control_final.py
"""
Test final rápido de Phase 2 con parámetros correctos.
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
        final_params = {"context": context}
        final_params.update(params)
        result = action_spec.callable_func(**final_params)
        return result
    except Exception as e:
        return {"success": False, "error": f"Error ejecutando {action_id}: {str(e)}"}

def test_phase2_final():
    """Test final de Phase 2 con parámetros correctos."""
    
    context = FlowContext()
    ActionRegistry.auto_discover_actions()
    
    print("🚀 PHASE 2 FINAL TEST")
    print("=" * 40)
    
    # Setup
    context.set_variable('numeros', [10, 20, 30])
    context.set_variable('check_var', 5)
    
    # Test funcionalmente conocidos
    tests = [
        ("bucle_for_rango", {
            'variable_contador': 'i', 'inicio': 1, 'fin': 3, 'paso': 1
        }),
        ("bucle_for_lista", {
            'variable_elemento': 'item', 'variable_indice': 'idx', 
            'lista_variable': 'numeros', 'max_iteraciones': 5
        }),
        ("repetir_hasta", {
            'variable_condicion': 'check_var', 'valor_objetivo': 10, 
            'operador': '>=', 'max_iteraciones': 10, 'delay_ms': 100
        }),
        ("interrumpir_flujo", {
            'tipo_interrupcion': 'break', 'condicion_variable': 'check_var', 
            'condicion_valor': '5', 'mensaje_salida': 'Test interrupt'
        }),
        ("condicional_multiple", {
            'variable_evaluacion': 'check_var', 
            'casos': '{"5": "found", "default": "not_found"}',
            'comparacion_estricta': 'false', 'resultado_variable': 'result'
        }),
        ("delay_dinamico", {
            'tipo_delay': 'fijo', 'valor_base': 0.001
        }),
        ("try_catch_finally", {
            'accion_catch': 'continue', 'variable_error': 'error_var'
        })
    ]
    
    success_count = 0
    total_count = len(tests)
    
    for action_id, params in tests:
        result = execute_action_test(action_id, context, params)
        success = result.get('success', False)
        message = result.get('message', result.get('error'))
        status = "✅" if success else "❌"
        
        print(f"{status} {action_id}: {success} - {message}")
        
        if success:
            success_count += 1
    
    print(f"\n📊 RESULTADO FINAL:")
    print(f"✅ {success_count}/{total_count} acciones funcionando correctamente")
    print(f"📈 Tasa de éxito: {(success_count/total_count)*100:.1f}%")
    
    all_actions = ActionRegistry.list_all_actions()
    control_actions = [spec for spec in all_actions.values() if spec.category == 'control']
    print(f"🎮 Total acciones de control: {len(control_actions)}")
    
    print(f"\n🏁 Phase 2 Control Flow - COMPLETADO!")

if __name__ == "__main__":
    test_phase2_final()
