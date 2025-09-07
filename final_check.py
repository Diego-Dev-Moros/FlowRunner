#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación final - NO MÁS ERRORES 404
"""
import os
import re
from pathlib import Path

def final_verification():
    """Verificación final de que no hay errores 404"""
    print("🎯 VERIFICACIÓN FINAL - NO MÁS ERRORES 404")
    print("=" * 60)
    
    base_dir = Path('.')
    errors = []
    success = []
    
    # 1. HTML Principal
    html_path = base_dir / 'vistas' / 'servicio.html'
    if html_path.exists():
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        # Verificar CSS
        css_match = re.search(r'href="([^"]+\.css)"', html_content)
        if css_match:
            css_path = css_match.group(1)
            if css_path.startswith('/vistas/'):
                actual_path = base_dir / css_path[1:]  # Quitar '/'
            else:
                actual_path = base_dir / 'vistas' / css_path[2:]  # Quitar './'
                
            if actual_path.exists():
                success.append(f"✅ CSS: {css_path} → {actual_path} ({actual_path.stat().st_size} bytes)")
            else:
                errors.append(f"❌ CSS: {css_path} → {actual_path} (NO EXISTE)")
        
        # Verificar Favicon
        favicon_match = re.search(r'href="([^"]+favicon[^"]*)"', html_content)
        if favicon_match:
            favicon_path = favicon_match.group(1)
            if favicon_path.startswith('/'):
                actual_path = base_dir / favicon_path[1:]
            else:
                actual_path = base_dir / favicon_path[3:]  # Quitar '../'
                
            if actual_path.exists():
                success.append(f"✅ Favicon: {favicon_path} → {actual_path} ({actual_path.stat().st_size} bytes)")
            else:
                errors.append(f"❌ Favicon: {favicon_path} → {actual_path} (NO EXISTE)")
        
        # Verificar JS principal
        js_match = re.search(r'src="(/vistas/services/main\.js)"', html_content)
        if js_match:
            js_path = js_match.group(1)
            actual_path = base_dir / js_path[1:]  # Quitar '/'
            
            if actual_path.exists():
                success.append(f"✅ Main JS: {js_path} → {actual_path} ({actual_path.stat().st_size} bytes)")
            else:
                errors.append(f"❌ Main JS: {js_path} → {actual_path} (NO EXISTE)")
    
    # 2. Verificar todos los imports de main.js
    main_js = base_dir / 'vistas' / 'services' / 'main.js'
    if main_js.exists():
        with open(main_js, 'r', encoding='utf-8') as f:
            main_content = f.read()
            
        imports = re.findall(r'import.*from\s+[\'"]([^\'"]+)[\'"]', main_content)
        
        for import_path in imports:
            if import_path.startswith('./'):
                actual_path = main_js.parent / import_path[2:]
            else:
                actual_path = base_dir / 'vistas' / 'services' / import_path
            
            # Agregar extensión .js si no la tiene
            if not actual_path.suffix:
                actual_path = actual_path.with_suffix('.js')
                
            if actual_path.exists():
                success.append(f"✅ Import: {import_path} → {actual_path.relative_to(base_dir)} ({actual_path.stat().st_size} bytes)")
            else:
                errors.append(f"❌ Import: {import_path} → {actual_path.relative_to(base_dir)} (NO EXISTE)")
    
    # 3. Verificar error-handler.js específicamente
    error_handler_js = base_dir / 'vistas' / 'services' / 'ui' / 'error-handler.js'
    if error_handler_js.exists():
        with open(error_handler_js, 'r', encoding='utf-8') as f:
            error_handler_content = f.read()
            
        # Verificar import de toast
        toast_match = re.search(r'import\s+toast\s+from\s+[\'"]([^\'"]+)[\'"]', error_handler_content)
        if toast_match:
            toast_import = toast_match.group(1)
            if toast_import.startswith('./'):
                toast_path = error_handler_js.parent / toast_import[2:]
            else:
                toast_path = error_handler_js.parent / toast_import
                
            # Agregar .js si no lo tiene
            if not toast_path.suffix:
                toast_path = toast_path.with_suffix('.js')
                
            if toast_path.exists():
                success.append(f"✅ Toast Import: {toast_import} → {toast_path.relative_to(base_dir)} ({toast_path.stat().st_size} bytes)")
            else:
                errors.append(f"❌ Toast Import: {toast_import} → {toast_path.relative_to(base_dir)} (NO EXISTE)")
    
    # 4. Resultados
    print(f"\n📊 RESULTADOS:")
    print(f"✅ Recursos válidos: {len(success)}")
    print(f"❌ Recursos con error: {len(errors)}")
    
    if success:
        print(f"\n✅ RECURSOS CORRECTOS ({len(success)}):")
        for item in success:
            print(f"   {item}")
    
    if errors:
        print(f"\n❌ RECURSOS CON ERROR ({len(errors)}):")
        for item in errors:
            print(f"   {item}")
    
    print("\n" + "=" * 60)
    
    if len(errors) == 0:
        print("🎉 ¡PERFECTO! NO HAY ERRORES 404")
        print("✅ Todos los recursos están correctamente referenciados")
        print("🚀 El sistema debería funcionar sin errores")
        print("🎯 INTEGRACIÓN COMPLETA Y EXITOSA")
    else:
        print(f"⚠️  ATENCIÓN: {len(errors)} recursos con problemas")
        print("🔧 Revisa los recursos marcados como NO EXISTE")
    
    return len(errors) == 0

if __name__ == "__main__":
    final_verification()
