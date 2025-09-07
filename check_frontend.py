import os
import sys

def check_frontend_files():
    print("🔍 VERIFICACIÓN DE ARCHIVOS FRONTEND")
    print("=" * 50)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Archivos críticos del frontend
    critical_files = [
        'vistas/servicio.html',
        'vistas/services/main.js',
        'vistas/services/state.js',
        'vistas/services/registry.js',
        'vistas/services/edges.js',
        'vistas/services/canvas.js',
        'vistas/services/ui/properties.js',  # Corregido de props.js
        'vistas/services/ui/topbar.js',
        'vistas/services/ui/toolbar.js',
        'vistas/services/ui/console.js',
        'vistas/services/ui/toast.js',
        'vistas/services/ui/error-handler.js',
        'vistas/services/runtime/handlers.js',
        'favicon.svg'
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in critical_files:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            existing_files.append((file_path, size))
        else:
            missing_files.append(file_path)
    
    # Mostrar resultados
    print(f"✅ Archivos existentes: {len(existing_files)}")
    for file_path, size in existing_files:
        print(f"   • {file_path}: {size} bytes")
    
    if missing_files:
        print(f"\n❌ Archivos faltantes: {len(missing_files)}")
        for file_path in missing_files:
            print(f"   • {file_path}")
    
    # Verificar imports en main.js
    main_js_path = os.path.join(base_dir, 'vistas', 'services', 'main.js')
    if os.path.exists(main_js_path):
        with open(main_js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar imports problemáticos
        imports_to_check = [
            './ui/props.js',      # Debería ser properties.js
            './ui/properties.js', # Correcto
            './state.js',
            './registry.js',
            './edges.js',
            './canvas.js'
        ]
        
        print(f"\n🔍 Verificación de imports en main.js:")
        for import_path in imports_to_check:
            if import_path in content:
                status = "✅" if import_path != './ui/props.js' else "❌"
                print(f"   {status} {import_path}")
    
    # Resumen
    total_files = len(critical_files)
    success_rate = (len(existing_files) / total_files) * 100
    
    print(f"\n📊 RESUMEN:")
    print(f"   • Total archivos: {total_files}")
    print(f"   • Existentes: {len(existing_files)}")
    print(f"   • Faltantes: {len(missing_files)}")
    print(f"   • Tasa de éxito: {success_rate:.1f}%")
    
    if len(missing_files) == 0:
        print("\n🎉 ¡TODOS LOS ARCHIVOS FRONTEND ESTÁN PRESENTES!")
        print("✅ No debería haber más errores 404")
    else:
        print("\n⚠️  Algunos archivos faltan, podrían causar errores 404")
    
    return len(missing_files) == 0

if __name__ == "__main__":
    success = check_frontend_files()
    sys.exit(0 if success else 1)
