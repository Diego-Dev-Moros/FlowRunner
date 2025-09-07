#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico completo para encontrar TODOS los recursos faltantes
"""
import os
import re
import json
from pathlib import Path

def find_all_resources():
    """Encuentra todos los recursos referenciados en HTML, CSS y JS"""
    base_dir = Path('.')
    resources = {
        'html': [],
        'css': [],
        'js_modules': [],
        'js_resources': [],
        'missing': [],
        'existing': []
    }
    
    print("🔍 ANÁLISIS EXHAUSTIVO DE RECURSOS")
    print("=" * 60)
    
    # 1. Analizar HTML principal
    html_path = base_dir / 'vistas' / 'servicio.html'
    if html_path.exists():
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        # Enlaces CSS
        css_links = re.findall(r'href="([^"]+\.css)"', html_content)
        resources['css'].extend(css_links)
        
        # Enlaces JavaScript
        js_links = re.findall(r'src="([^"]+\.js)"', html_content)
        resources['js_modules'].extend(js_links)
        
        # Favicon
        favicon_links = re.findall(r'href="([^"]+favicon[^"]*)"', html_content)
        resources['js_resources'].extend(favicon_links)
        
        print(f"📄 HTML Principal: {html_path}")
        print(f"   CSS encontrados: {css_links}")
        print(f"   JS encontrados: {js_links}")
        print(f"   Favicon: {favicon_links}")
    
    # 2. Analizar main.js y sus imports
    main_js = base_dir / 'vistas' / 'services' / 'main.js'
    if main_js.exists():
        with open(main_js, 'r', encoding='utf-8') as f:
            main_content = f.read()
            
        # Imports ES6
        imports = re.findall(r'import.*from\s+[\'"]([^\'"]+)[\'"]', main_content)
        resources['js_modules'].extend(imports)
        
        print(f"📦 main.js imports: {imports}")
    
    # 3. Verificar existencia de todos los recursos
    all_resources = resources['css'] + resources['js_modules'] + resources['js_resources']
    
    for resource in all_resources:
        # Convertir rutas relativas
        if resource.startswith('./'):
            resource_path = base_dir / 'vistas' / 'services' / resource[2:]
        elif resource.startswith('../'):
            resource_path = base_dir / resource[3:]
        elif resource.startswith('/'):
            # eel.js es servido por el servidor, no como archivo estático
            if 'eel.js' in resource:
                resources['existing'].append(f"{resource} (servido por EEL)")
                continue
            resource_path = base_dir / resource[1:]
        else:
            resource_path = base_dir / 'vistas' / resource
            
        if resource_path.exists():
            size = resource_path.stat().st_size
            resources['existing'].append(f"{resource} → {resource_path} ({size} bytes)")
        else:
            resources['missing'].append(f"{resource} → {resource_path} (FALTANTE)")
    
    # 4. Verificar archivos CSS específicos
    css_files = [
        'vistas/styles/estilos.css'
    ]
    
    for css_file in css_files:
        css_path = base_dir / css_file
        if css_path.exists():
            # Analizar imports en CSS
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # Buscar @import, url(), etc.
            css_imports = re.findall(r'@import\s+[\'"]([^\'"]+)[\'"]', css_content)
            url_refs = re.findall(r'url\([\'"]?([^\'")\s]+)[\'"]?\)', css_content)
            
            if css_imports or url_refs:
                print(f"🎨 CSS {css_file}:")
                if css_imports:
                    print(f"   @imports: {css_imports}")
                if url_refs:
                    print(f"   URLs: {url_refs}")
                    
                for url_ref in url_refs:
                    if not url_ref.startswith('http') and not url_ref.startswith('data:'):
                        ref_path = css_path.parent / url_ref
                        if ref_path.exists():
                            resources['existing'].append(f"CSS: {url_ref} → {ref_path}")
                        else:
                            resources['missing'].append(f"CSS: {url_ref} → {ref_path} (FALTANTE)")
    
    # 5. Resultados
    print("\n" + "=" * 60)
    print("📊 RESULTADOS DEL DIAGNÓSTICO")
    print("=" * 60)
    
    print(f"\n✅ RECURSOS EXISTENTES ({len(resources['existing'])}):")
    for item in resources['existing']:
        print(f"   • {item}")
    
    if resources['missing']:
        print(f"\n❌ RECURSOS FALTANTES ({len(resources['missing'])}):")
        for item in resources['missing']:
            print(f"   • {item}")
    else:
        print(f"\n🎉 ¡NO HAY RECURSOS FALTANTES!")
    
    # 6. Verificar rutas de servidor
    print(f"\n🌐 VERIFICACIÓN DE RUTAS DE SERVIDOR:")
    print("   • /eel.js → Servido automáticamente por EEL")
    print("   • /vistas/servicio.html → Archivo principal")
    print("   • /vistas/services/*.js → Módulos ES6")
    print("   • /vistas/styles/*.css → Hojas de estilo")
    
    return resources

def check_network_dependencies():
    """Verifica dependencias de red y configuración del servidor"""
    print("\n" + "=" * 60)
    print("🌐 VERIFICACIÓN DE CONFIGURACIÓN DEL SERVIDOR")
    print("=" * 60)
    
    # Verificar index.py
    if os.path.exists('index.py'):
        with open('index.py', 'r', encoding='utf-8') as f:
            index_content = f.read()
            
        # Buscar configuración de EEL
        if 'eel.init' in index_content:
            print("✅ EEL inicializado correctamente")
        
        if 'eel.start' in index_content:
            print("✅ Servidor EEL configurado para iniciar")
            
        # Buscar puerto
        port_match = re.search(r'port=(\d+)', index_content)
        if port_match:
            print(f"🔌 Puerto configurado: {port_match.group(1)}")
        
        # Buscar directorio web
        if "'vistas'" in index_content or '"vistas"' in index_content:
            print("📁 Directorio web: vistas")

def main():
    print("🚀 DIAGNÓSTICO COMPLETO DE INTEGRACIÓN FLOWRUNNER")
    print("=" * 80)
    
    resources = find_all_resources()
    check_network_dependencies()
    
    # Resumen final
    print("\n" + "=" * 80)
    print("🎯 RESUMEN FINAL")
    print("=" * 80)
    
    total_resources = len(resources['existing']) + len(resources['missing'])
    success_rate = len(resources['existing']) / total_resources * 100 if total_resources > 0 else 100
    
    print(f"📈 Tasa de éxito: {success_rate:.1f}%")
    print(f"✅ Recursos existentes: {len(resources['existing'])}")
    print(f"❌ Recursos faltantes: {len(resources['missing'])}")
    
    if len(resources['missing']) == 0:
        print("\n🎉 ¡TODOS LOS RECURSOS ESTÁN PRESENTES!")
        print("✅ No debería haber errores 404")
        print("🚀 Sistema listo para funcionar")
    else:
        print(f"\n⚠️  Se encontraron {len(resources['missing'])} recursos faltantes")
        print("🔧 Revisa los recursos marcados como FALTANTES arriba")

if __name__ == "__main__":
    main()
