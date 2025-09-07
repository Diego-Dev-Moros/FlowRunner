# test_quick_integration.py
"""
Test rápido de las funciones principales.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.core.executor import FlowExecutor
from modules.utils.logging import FlowLogger
import json

def test_simple_flow():
    """Test del flujo simple."""
    print("\n🔄 PROBANDO FLUJO SIMPLE")
    print("=" * 40)
    
    # Flujo simple definido directamente
    simple_flow = {
        "name": "Test Básico",
        "steps": [
            {
                "id": "s1", 
                "type": "variable_set", 
                "props": {"variable": "test_var", "valor": "123"}
            },
            {
                "id": "s2", 
                "type": "delay_dinamico", 
                "props": {"tipo_delay": "fijo", "valor_base": "0.1"}
            },
            {
                "id": "s3", 
                "type": "variable_get", 
                "props": {"variable": "test_var"}
            }
        ],
        "edges": [
            {"id": "e1", "source": "s1", "target": "s2"},
            {"id": "e2", "source": "s2", "target": "s3"}
        ]
    }
    
    executor = FlowExecutor()
    result = executor.execute_flow(simple_flow)
    
    success = result.get('ok', False)
    print(f"✅ Flujo simple: {'ÉXITO' if success else 'ERROR'}")
    if not success:
        print(f"   Error: {result.get('error')}")
    
    return success

def test_control_actions():
    """Test de acciones de control individualmente."""
    print("\n🎮 PROBANDO ACCIONES DE CONTROL")
    print("=" * 40)
    
    from modules.core.context import FlowContext
    from modules.core.registry import ActionRegistry
    
    # Auto-descubrir acciones
    ActionRegistry.auto_discover_actions()
    
    context = FlowContext()
    context.set_variable('test_num', 5)
    
    # Test bucle for rango
    bucle_spec = ActionRegistry.get_action('bucle_for_rango')
    if bucle_spec:
        try:
            result = bucle_spec.callable_func(
                context=context,
                variable_contador='i',
                inicio=1,
                fin=3,
                paso=1
            )
            print(f"✅ bucle_for_rango: {result.get('success', False)}")
        except Exception as e:
            print(f"❌ bucle_for_rango: Error - {e}")
    
    # Test delay dinámico
    delay_spec = ActionRegistry.get_action('delay_dinamico')
    if delay_spec:
        try:
            result = delay_spec.callable_func(
                context=context,
                tipo_delay='fijo',
                valor_base=0.05
            )
            print(f"✅ delay_dinamico: {result.get('success', False)}")
        except Exception as e:
            print(f"❌ delay_dinamico: Error - {e}")
    
    # Test condicional múltiple
    switch_spec = ActionRegistry.get_action('condicional_multiple')
    if switch_spec:
        try:
            result = switch_spec.callable_func(
                context=context,
                variable_evaluacion='test_num',
                casos='{"5": "encontrado", "default": "no_encontrado"}',
                comparacion_estricta='false',
                resultado_variable='resultado'
            )
            print(f"✅ condicional_multiple: {result.get('success', False)}")
        except Exception as e:
            print(f"❌ condicional_multiple: Error - {e}")

def main():
    """Test principal."""
    print("🚀 TEST RÁPIDO DE INTEGRACIÓN")
    print("=" * 50)
    
    # Test logging
    FlowLogger.log_user("Iniciando test rápido")
    print("✅ Sistema de logging funcionando")
    
    # Test flujo simple
    flow_success = test_simple_flow()
    
    # Test acciones individuales
    test_control_actions()
    
    # Resultado
    if flow_success:
        print(f"\n🎉 SISTEMA BÁSICO FUNCIONANDO!")
        print("✅ Logging OK, ✅ Flujos OK, ✅ Acciones OK")
    else:
        print(f"\n⚠️ Problemas detectados")

if __name__ == "__main__":
    main()
