# modules/actions/navigation/browser.py
"""
Acciones de navegación web.
"""

from typing import Dict, Any
from modules.core import action, FlowContext
from modules.actions.base import success_result, error_result, validate_required_params
from modules.utils.web_automation import abrir_pagina_web, cambiar_pagina_web, maximizar_navegador


@action(
    category='navegacion',
    name='Abrir página web',
    description='Abre una página web en el navegador.',
    schema=[
        {'key': 'url', 'label': 'URL', 'type': 'text', 'required': True, 'placeholder': 'https://example.com'}
    ],
    provides='driver'
)
def abrir_pagina_action(context: FlowContext, url: str) -> Dict[str, Any]:
    """
    Abre una página web y almacena el driver.
    """
    try:
        error = validate_required_params({'url': url}, ['url'])
        if error:
            return error_result(error)
        
        # Usar la función consolidada de utilidades
        driver = abrir_pagina_web(url)
        
        if driver:
            # Guardar el driver en el contexto
            context.set_driver(driver)
            return success_result(f"Página abierta: {url}")
        else:
            return error_result("No se pudo abrir la página")
        
    except Exception as e:
        return error_result(f"Error abriendo página: {str(e)}")


@action(
    category='navegacion',
    name='Cambiar a otra página',
    description='Navega a una URL diferente en el navegador actual.',
    schema=[
        {'key': 'url', 'label': 'URL', 'type': 'text', 'required': True, 'placeholder': 'https://example.com'}
    ]
)
def cambiar_pagina_action(context: FlowContext, url: str) -> Dict[str, Any]:
    """
    Cambia la página en el navegador actual.
    """
    try:
        error = validate_required_params({'url': url}, ['url'])
        if error:
            return error_result(error)
        
        driver = context.get_driver()
        if not driver:
            return error_result("No hay navegador abierto. Usar 'Abrir página web' primero.")
        
        cambiar_pagina_web(driver, url)
        return success_result(f"Navegado a: {url}")
        
    except Exception as e:
        return error_result(f"Error cambiando página: {str(e)}")


@action(
    category='navegacion',
    name='Maximizar navegador',
    description='Maximiza la ventana del navegador.',
    schema=[]
)
def maximizar_navegador_action(context: FlowContext) -> Dict[str, Any]:
    """
    Maximiza el navegador actual.
    """
    try:
        driver = context.get_driver()
        if not driver:
            return error_result("No hay navegador abierto. Usar 'Abrir página web' primero.")
        
        maximizar_navegador(driver)
        return success_result("Navegador maximizado")
        
    except Exception as e:
        return error_result(f"Error maximizando navegador: {str(e)}")
