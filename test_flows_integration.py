# test_flows_integration.py
"""
Test de integración completo para Phase 2.
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

def test_logging_system():
    """Prueba el sistema de logging."""
    print(f"\n🔍 PROBANDO SISTEMA DE LOGGING")
    print("=" * 50)
    
    # Limpiar log temporal
    FlowLogger.clear_temp_log()
    
    # Hacer algunos logs de prueba
    FlowLogger.log_user("Test del sistema de logging iniciado")
    FlowLogger.log_temp("Datos de debug", {"test": True, "timestamp": "2025-09-06"})
    FlowLogger.log_error("Error de prueba", context={"test_mode": True})
    
    # Verificar archivos de log
    log_files_found = 0
    for log_type in ['user', 'error', 'temp']:
        log_file = os.path.join('var', f'{log_type}.log')
        if os.path.exists(log_file):
            log_files_found += 1
            print(f"✅ Log {log_type}.log creado correctamente")
            
            # Mostrar últimas líneas
            recent_logs = FlowLogger.get_recent_logs(log_type, 2)
            if recent_logs:
                print(f"   📝 Últimas entradas ({len(recent_logs)}):")
                for line in recent_logs[-1:]:  # Solo la última
                    print(f"      {line.strip()}")
        else:
            print(f"❌ Log {log_type}.log no encontrado")
    
    print(f"\n📊 Sistema de logging: {log_files_found}/3 archivos creados")
    return log_files_found >= 3

def main():
    """Función principal del test de integración."""
    
    print("🚀 TEST DE INTEGRACIÓN COMPLETO - PHASE 2")
    print("=" * 60)
    
    # Probar sistema de logging
    logging_ok = test_logging_system()
    
    # Probar flujos
    flows_to_test = [
        ("test/flujo_simple_phase2.json", "Flujo Simple Phase 2"),
        ("test/flujo_complejo_phase2.json", "Flujo Complejo Phase 2")
    ]
    
    results = []
    
    for flow_file, flow_name in flows_to_test:
        if os.path.exists(flow_file):
            success = test_flow_execution(flow_file, flow_name)
            results.append((flow_name, success))
        else:
            print(f"\n❌ ARCHIVO NO ENCONTRADO: {flow_file}")
            results.append((flow_name, False))
    
    # Resumen final
    print(f"\n📊 RESUMEN FINAL")
    print("=" * 60)
    
    print(f"🔍 Sistema de Logging: {'✅ OK' if logging_ok else '❌ ERROR'}")
    
    successful_flows = 0
    for flow_name, success in results:
        status = "✅ ÉXITO" if success else "❌ ERROR"
        print(f"🔄 {flow_name}: {status}")
        if success:
            successful_flows += 1
    
    total_flows = len(results)
    success_rate = (successful_flows / total_flows) * 100 if total_flows > 0 else 0
    
    print(f"\n🎯 ESTADÍSTICAS:")
    print(f"   📈 Tasa de éxito: {success_rate:.1f}% ({successful_flows}/{total_flows})")
    print(f"   🔍 Logging: {'Funcionando' if logging_ok else 'Con problemas'}")
    
    # Mostrar logs recientes del usuario
    print(f"\n📋 ÚLTIMAS ACTIVIDADES (user.log):")
    recent_user_logs = FlowLogger.get_recent_logs('user', 5)
    for line in recent_user_logs[-3:]:  # Últimas 3 líneas
        print(f"   {line.strip()}")
    
    # Resultado final
    overall_success = logging_ok and successful_flows == total_flows
    final_status = "✅ TODO OK" if overall_success else "⚠️ CON PROBLEMAS"
    
    print(f"\n🏁 RESULTADO FINAL: {final_status}")
    
    if overall_success:
        print("   🎉 Todos los sistemas funcionando correctamente!")
        print("   🚀 Listo para Phase 3!")
    else:
        print("   🔧 Algunos sistemas necesitan atención")

if __name__ == "__main__":
    main()
