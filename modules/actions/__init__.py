# modules/actions/__init__.py
"""
Sistema de acciones modular para FlowRunner.
Auto-registra todas las acciones disponibles.
"""

from modules.core import ActionRegistry

# Importar explícitamente todos los módulos de acciones para activar los decoradores
from . import control
from . import data
from . import dialogs
from . import navigation
from . import files
from . import finalization

# También importar los módulos específicos
from .control import flow
from .data import processors, readers, writers
from .dialogs import pickers
from .navigation import browser
from .files import operations
from .finalization import cleanup

print("[ACTIONS] Módulo de acciones inicializado")
print(f"[ACTIONS] Auto-descubrimiento iniciado...")
