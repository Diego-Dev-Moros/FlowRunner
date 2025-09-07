#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación de integridad COMPLETA de módulos JavaScript
"""
import os
import re
from pathlib import Path

def find_all_imports_exports():
    """Encuentra todas las importaciones y exportaciones"""
    services_dir = Path('vistas/services')
    modules = {}
    problems = []
    
    print("🔍 ANÁLISIS COMPLETO DE IMPORTS/EXPORTS")
    print("=" * 60)
    
    # Recopilar módulos
    for js_file in services_dir.rglob('*.js'):
        rel_path = js_file.relative_to(services_dir)
        
        try:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            modules[str(rel_path)] = {
                'path': js_file,
                'imports': [],
                'exports': [],
                'content': content,
                'size': js_file.stat().st_size
            }
            
            # Imports detallados
            import_patterns = [
                r'import\s+\{\s*([^}]+)\s*\}\s+from\s+[\'"]([^\'"]+)[\'"]',  # import { x, y } from './module'
                r'import\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',               # import x from './module'
                r'import\s+\*\s+as\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]'     # import * as x from './module'
            ]
            
            for pattern in import_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if len(match) == 2:
                        imported, module = match
                        modules[str(rel_path)]['imports'].append({
                            'names': imported.split(',') if '{' in imported else [imported.strip()],
                            'module': module,
                            'type': 'named' if '{' in str(imported) else ('namespace' if '*' in str(imported) else 'default')
                        })
            
            # Exports detallados
            export_patterns = [
                r'export\s+function\s+(\w+)',                  # export function name()
                r'export\s+const\s+(\w+)',                     # export const name
                r'export\s+\{\s*([^}]+)\s*\}',                 # export { x, y }
                r'export\s+default\s+(\w+)',                   # export default name
            ]
            
            for pattern in export_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0] if match[0] else match[1]
                    if '{' in match:
                        names = [n.strip() for n in match.split(',')]
                    else:
                        names = [match]
                    modules[str(rel_path)]['exports'].extend(names)
            
            # Export default especial
            if 'export default' in content:
                default_match = re.search(r'export\s+default\s+(\w+|\{[^}]*\})', content)
                if default_match:
                    modules[str(rel_path)]['exports'].append('default')
                    
        except Exception as e:
            problems.append(f"❌ Error leyendo {rel_path}: {e}")
    
    # Verificar importaciones
    print(f"\n📦 VERIFICANDO IMPORTACIONES")
    print("-" * 50)
    
    for module_path, info in modules.items():
        print(f"\n📄 {module_path}")
        
        for import_info in info['imports']:
            module_import = import_info['module']
            imported_names = import_info['names']
            
            # Resolver ruta del módulo importado
            if module_import.startswith('./'):
                resolved_path = str((Path(module_path).parent / module_import[2:]).with_suffix('.js')).replace('\\', '/')
            elif module_import.startswith('../'):
                resolved_path = str((Path(module_path).parent / module_import).with_suffix('.js')).replace('\\', '/')
            else:
                resolved_path = str(Path(module_import).with_suffix('.js')).replace('\\', '/')
            
            # Verificar si el módulo existe
            if resolved_path in modules:
                target_module = modules[resolved_path]
                
                # Verificar cada nombre importado
                for name in imported_names:
                    name = name.strip()
                    if name in target_module['exports'] or 'default' in target_module['exports']:
                        print(f"   ✅ {name} from {module_import}")
                    else:
                        print(f"   ❌ {name} from {module_import} (NO EXPORTADO)")
                        problems.append(f"{module_path}: import {name} from {module_import} - NO EXISTE")
            else:
                print(f"   ⚠️  {module_import} (módulo no encontrado)")
    
    # Resumen de problemas
    print(f"\n" + "=" * 60)
    print("🎯 RESUMEN DE PROBLEMAS")
    print("=" * 60)
    
    if problems:
        print(f"❌ PROBLEMAS ENCONTRADOS ({len(problems)}):")
        for problem in problems:
            print(f"   • {problem}")
    else:
        print("🎉 ¡NO HAY PROBLEMAS DE IMPORTACIÓN!")
    
    # Mostrar exportaciones disponibles para módulos problemáticos
    problem_modules = set()
    for problem in problems:
        if ':' in problem:
            module_name = problem.split(':')[0]
            problem_modules.add(module_name)
    
    if problem_modules:
        print(f"\n📋 EXPORTACIONES DISPONIBLES EN MÓDULOS PROBLEMÁTICOS:")
        for module_name in problem_modules:
            if module_name in modules:
                exports = modules[module_name]['exports']
                print(f"   • {module_name}: {exports}")
    
    return len(problems) == 0

if __name__ == "__main__":
    find_all_imports_exports()
