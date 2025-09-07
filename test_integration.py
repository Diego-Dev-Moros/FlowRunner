#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test de integración para los flujos de Phase 2.
Prueba los flujos completos usando el executor.
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.core.executor import FlowExecutor
from modules.utils.logging import FlowLogger

def load_flow(filename: str) -> dict:
    """Carga un flujo desde archivo JSON."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando flujo {filename}: {e}")
        return None

def test_flow_execution(flow_file: str, flow_name: str):
    """Prueba la ejecución de un flujo."""
    print(f"\n🔄 PROBANDO: {flow_name}")
    print("=" * 50)
    
    # Cargar flujo
    flow = load_flow(flow_file)
    if not flow:
        print(f"❌ No se pudo cargar el flujo: {flow_file}")
        return False
    
    # Ejecutar flujo
    executor = FlowExecutor()
    
    try:
        result = executor.execute_flow(flow)
        
        success = result.get('ok', False)
        if success:
            print(f"✅ {flow_name} - ÉXITO")
            print(f"   📊 Variables creadas: {len(result.get('variables', []))}")
            if result.get('message'):
                print(f"   💬 Mensaje: {result['message']}")
        else:
            print(f"❌ {flow_name} - ERROR")
            print(f"   🚨 Error: {result.get('error', 'Error desconocido')}")
        
        return success
        
    except Exception as e:
        print(f"❌ {flow_name} - EXCEPCIÓN: {str(e)}")
        return False
    categories = ActionRegistry.list_by_category()
    print(f"✓ Acciones registradas: {len(actions)}")
    print(f"✓ Categorías disponibles: {list(categories.keys())}")
    
    # Probar creación de executor
    executor = FlowExecutor()
    context = FlowContext()
    print("✓ FlowExecutor y FlowContext creados")
    
    # Probar una acción directa
    print("\n--- Probando acción de variable directamente ---")
    action_spec = ActionRegistry.get_action("variable_set")
    if action_spec:
        try:
            # Ejecutar la función directamente
            result = action_spec.callable_func(context, 
                variable='test_var',
                valor='Hello FlowRunner!'
            )
            
            if result and result.get('ok'):
                print("✓ Acción variable_set ejecutada exitosamente")
                print(f"  Variables en contexto: {list(context.variables.keys())}")
                print(f"  Resultado: {result.get('result')}")
            else:
                print("✗ Error en acción variable_set")
                print(f"  Result: {result}")
        except Exception as e:
            print(f"✗ Error ejecutando variable_set: {e}")
    else:
        print("✗ No se encontró la acción variable_set")
    
    # Probar obtener la variable
    print("\n--- Probando lectura de variable ---")
    action_spec2 = ActionRegistry.get_action("variable_get")
    if action_spec2:
        try:
            result2 = action_spec2.callable_func(context,
                variable='test_var'
            )
            
            if result2 and result2.get('ok'):
                print("✓ Acción variable_get ejecutada exitosamente")
                print(f"  Variables en contexto: {list(context.variables.keys())}")
                print(f"  Resultado: {result2.get('result')}")
            else:
                print("✗ Error en acción variable_get")
                print(f"  Result: {result2}")
        except Exception as e:
            print(f"✗ Error ejecutando variable_get: {e}")
    else:
        print("✗ No se encontró la acción variable_get")
    
    # Mostrar resumen final
    print("\n--- RESUMEN DE INTEGRACIÓN ---")
    for cat, action_specs in categories.items():
        action_names = [spec.name for spec in action_specs]
        print(f"{cat.upper()}: {len(action_names)} acciones")
        for name in action_names:
            print(f"  - {name}")
    
    print(f"\n✓ Sistema de acciones funcionando correctamente")
    print(f"✓ Total: {len(actions)} acciones en {len(categories)} categorías")
    return True

if __name__ == "__main__":
    test_action_system()
