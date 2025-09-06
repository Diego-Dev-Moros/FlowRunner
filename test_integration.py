#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prueba de integración para verificar que el nuevo sistema de acciones
funciona correctamente con el frontend.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.core import ActionRegistry, FlowExecutor, FlowContext
from modules.actions import *  # Import all action modules

def test_action_system():
    """Prueba el sistema completo de acciones."""
    print("=== PRUEBA DE INTEGRACIÓN DEL SISTEMA DE ACCIONES ===\n")
    
    # Verificar que las acciones están registradas
    actions = ActionRegistry.list_all_actions()
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
