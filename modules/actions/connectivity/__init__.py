# modules/actions/connectivity/__init__.py
"""
Módulo de conectividad para FlowRunner Phase 3.
Incluye HTTP requests, webhooks, y authentication.
"""

from .http_requests import *
from .auth import *

__all__ = [
    # HTTP Actions
    'http_get',
    'http_post', 
    'http_put',
    'http_delete',
    'http_request_avanzado',
    
    # Auth Actions
    'configurar_auth_api',
    'generar_token_temporal',
]
