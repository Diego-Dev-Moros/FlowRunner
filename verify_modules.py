#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación de integridad de módulos JavaScript ES6
"""
import os
import re
from pathlib import Path

def analyze_js_modules():
    """Analiza la integridad de todos los módulos JavaScript"""
    services_dir = Path('vistas/services')
    modules = {}
    issues = []
    
    print("🔍 ANÁLISIS DE INTEGRIDAD DE MÓDULOS JAVASCRIPT")
    print("=" * 70)
    
    # Recopilar todos los archivos .js
    for js_file in services_dir.rglob('*.js'):
        rel_path = js_file.relative_to(services_dir)
        
        try:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            modules[str(rel_path)] = {
                'path': js_file,
                'imports': [],
                'exports': [],
                'size': js_file.stat().st_size,
                'content': content
            }
            
            # Encontrar imports
            import_matches = re.findall(r'import\s+(?:\{[^}]*\}|\w+|\*\s+as\s+\w+)\s+from\s+[\'"]([^\'"]+)[\'"]', content)
            modules[str(rel_path)]['imports'] = import_matches
            
            # Encontrar exports
            export_matches = re.findall(r'export\s+(?:default\s+|const\s+|function\s+|class\s+)?(\w+)', content)
            if 'export default' in content:
                export_matches.append('default')
            modules[str(rel_path)]['exports'] = list(set(export_matches))  # Eliminar duplicados
            
        except Exception as e:
            issues.append(f"❌ Error leyendo {rel_path}: {e}")
    
    print(f"📦 Módulos encontrados: {len(modules)}")
    
    # Mostrar cada módulo
    for module_path, info in modules.items():
        print(f"\n📄 {module_path} ({info['size']} bytes)")
        if info['imports']:
            print(f"   📥 Imports: {info['imports']}")
        if info['exports']:
            print(f"   📤 Exports: {info['exports']}")
    
    # Verificar integridad de imports
    print(f"\n🔍 VERIFICACIÓN DE IMPORTS")
    print("=" * 50)
    
    for module_path, info in modules.items():
        for import_path in info['imports']:
            # Resolver ruta relativa
            module_dir = Path('vistas/services') / Path(module_path).parent
            
            if import_path.startswith('./'):
                resolved_path = (module_dir / import_path[2:]).with_suffix('.js')
            elif import_path.startswith('../'):
                resolved_path = (module_dir / import_path).with_suffix('.js')
            else:
                # Import absoluto desde services
                resolved_path = (Path('vistas/services') / import_path).with_suffix('.js')
            
            # Verificar si existe
            rel_resolved = resolved_path.relative_to(Path('vistas/services'))
            
            if str(rel_resolved) in modules:
                print(f"✅ {module_path}: {import_path} → {rel_resolved}")
            else:
                if resolved_path.exists():
                    print(f"⚠️  {module_path}: {import_path} → {rel_resolved} (archivo existe pero no analizado)")
                else:
                    print(f"❌ {module_path}: {import_path} → {rel_resolved} (NO EXISTE)")
                    issues.append(f"Import roto en {module_path}: {import_path}")
    
    # Buscar dependencias circulares
    print(f"\n🔄 VERIFICACIÓN DE DEPENDENCIAS CIRCULARES")
    print("=" * 50)
    
    def find_circular_deps(module, visited, path):
        if module in path:
            cycle = path[path.index(module):] + [module]
            return [cycle]
        if module in visited or module not in modules:
            return []
        
        visited.add(module)
        path.append(module)
        
        cycles = []
        for import_path in modules[module]['imports']:
            # Resolver import
            module_dir = Path(module).parent if Path(module).parent != Path('.') else Path('')
            
            if import_path.startswith('./'):
                resolved = str((module_dir / import_path[2:]).with_suffix('.js')).replace('\\', '/')
            elif import_path.startswith('../'):
                resolved = str((module_dir / import_path).with_suffix('.js')).replace('\\', '/')
            else:
                resolved = str(Path(import_path).with_suffix('.js')).replace('\\', '/')
            
            cycles.extend(find_circular_deps(resolved, visited, path[:]))
        
        path.pop()
        return cycles
    
    all_cycles = []
    for module in modules:
        cycles = find_circular_deps(module, set(), [])
        all_cycles.extend(cycles)
    
    # Eliminar duplicados de ciclos
    unique_cycles = []
    for cycle in all_cycles:
        normalized = min(cycle[:-1])  # Normalizar ciclo
        if not any(normalized in str(existing) for existing in unique_cycles):
            unique_cycles.append(cycle)
    
    if unique_cycles:
        print("⚠️  Dependencias circulares encontradas:")
        for cycle in unique_cycles:
            print(f"   🔄 {' → '.join(cycle)}")
    else:
        print("✅ No se encontraron dependencias circulares")
    
    # Verificar funciones críticas
    print(f"\n🎯 VERIFICACIÓN DE FUNCIONES CRÍTICAS")
    print("=" * 50)
    
    critical_functions = {
        'main.js': ['init', 'initApp'],
        'state.js': ['getState', 'setState'],
        'registry.js': ['registerAction', 'getAction'],
        'canvas.js': ['createNode', 'drawNode'],
        'edges.js': ['createEdge', 'drawEdge'],
        'ui/toast.js': ['showToast', 'showError'],
        'ui/topbar.js': ['initTopbar'],
        'ui/console.js': ['initConsole'],
        'ui/toolbar.js': ['initToolbar'],
        'ui/properties.js': ['renderPropsPanel'],
        'ui/error-handler.js': ['handleError'],
        'runtime/handlers.js': ['initHandlers']
    }
    
    missing_functions = []
    for module_path, functions in critical_functions.items():
        if module_path in modules:
            content = modules[module_path]['content']
            for func in functions:
                if f'function {func}' in content or f'{func} =' in content or f'const {func}' in content or f'export {func}' in content:
                    print(f"✅ {module_path}: {func}")
                else:
                    print(f"❌ {module_path}: {func} (NO ENCONTRADA)")
                    missing_functions.append(f"{module_path}:{func}")
        else:
            print(f"❌ {module_path}: MÓDULO NO ENCONTRADO")
    
    # Resumen final
    print(f"\n" + "=" * 70)
    print("🎯 RESUMEN DE INTEGRIDAD")
    print("=" * 70)
    
    total_issues = len(issues) + len(missing_functions) + len(unique_cycles)
    
    print(f"📊 Estadísticas:")
    print(f"   • Módulos analizados: {len(modules)}")
    print(f"   • Total de imports: {sum(len(m['imports']) for m in modules.values())}")
    print(f"   • Total de exports: {sum(len(m['exports']) for m in modules.values())}")
    print(f"   • Dependencias circulares: {len(unique_cycles)}")
    print(f"   • Funciones críticas faltantes: {len(missing_functions)}")
    print(f"   • Total de problemas: {total_issues}")
    
    if total_issues == 0:
        print(f"\n🎉 ¡INTEGRIDAD PERFECTA!")
        print("✅ Todos los módulos están correctamente integrados")
        print("🚀 Sistema listo para funcionar sin errores")
    else:
        print(f"\n⚠️  Se encontraron {total_issues} problemas de integridad")
        if issues:
            print("🔧 Problemas de imports:")
            for issue in issues:
                print(f"   • {issue}")
        if missing_functions:
            print("🔧 Funciones críticas faltantes:")
            for func in missing_functions:
                print(f"   • {func}")

if __name__ == "__main__":
    analyze_js_modules()
