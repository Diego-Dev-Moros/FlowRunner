import pandas as pd
from modules.core.registry import ActionRegistry
from modules.core.context import FlowContext

# Limpiar e inicializar
ActionRegistry.clear_registry()
ActionRegistry.auto_discover_actions()

# Crear contexto y DataFrame de prueba
ctx = FlowContext()
df_test = pd.DataFrame({
    'A': [1, 2, 2, 3, 3, 4], 
    'B': ['a', 'b', 'b', 'c', 'c', 'd'],
    'C': [10.5, 20.1, 20.1, 30.3, 30.3, 40.8]
})

ctx.set_variable('test_df', df_test)

print("=== TEST DE PROCESAMIENTO DE DATOS ===")
print("\nDataFrame original:")
print(df_test)
print(f"Filas: {len(df_test)}, Duplicados: {df_test.duplicated().sum()}")

# Test 1: Eliminar duplicados
print("\n1️⃣ ELIMINANDO DUPLICADOS...")
action = ActionRegistry.get_action('eliminar_duplicados')
result = action.callable_func(ctx, 'test_df')
print(f"✅ {result['message']}")

df_after = ctx.get_variable('test_df')
print("DataFrame después:")
print(df_after)

# Test 2: Calcular estadísticas 
print("\n2️⃣ CALCULANDO ESTADÍSTICAS...")
ctx.set_variable('stats_df', df_after)  # Renombrar para stats
action = ActionRegistry.get_action('calcular_estadisticas')
result = action.callable_func(ctx, 'stats_df', 'estadisticas_resultado', formato_salida='dataframe')
print(f"✅ {result['message']}")

stats_result = ctx.get_variable('estadisticas_resultado')
print("Estadísticas calculadas:")
print(stats_result)

print("\n🚀 FASE 1 - PROCESAMIENTO DE DATOS: ¡COMPLETADA CON ÉXITO!")
