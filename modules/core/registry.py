# modules/core/registry.py
"""
Registro automático de acciones para FlowRunner.
Maneja el descubrimiento y mapeo automático de funciones.
"""

from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass, field
import importlib
import inspect
import os


@dataclass
class ActionSpec:
    """
    Especificación de una acción registrada.
    """
    id: str
    category: str
    name: str
    description: str
    schema: List[Dict[str, Any]]
    callable_func: Callable
    provides: Optional[str] = None
    clear_driver: bool = False
    module_path: str = ""


class ActionRegistry:
    """
    Registro centralizado de todas las acciones disponibles.
    """
    
    _actions: Dict[str, ActionSpec] = {}
    _categories: Dict[str, List[ActionSpec]] = {}
    _initialized = False
    
    @classmethod
    def register_action(cls, id: str, category: str, name: str, 
                       description: str, schema: List[Dict], 
                       callable_func: Callable, provides: Optional[str] = None,
                       clear_driver: bool = False) -> None:
        """
        Registra una nueva acción.
        """
        spec = ActionSpec(
            id=id,
            category=category,
            name=name,
            description=description,
            schema=schema,
            callable_func=callable_func,
            provides=provides,
            clear_driver=clear_driver,
            module_path=callable_func.__module__ if callable_func else ""
        )
        
        cls._actions[id] = spec
        
        # Organizar por categorías
        if category not in cls._categories:
            cls._categories[category] = []
        cls._categories[category].append(spec)
        
        print(f"[REGISTRY] Registrada acción: {id} ({category})")
    
    @classmethod
    def get_action(cls, action_id: str) -> Optional[ActionSpec]:
        """
        Obtiene una acción por su ID.
        """
        return cls._actions.get(action_id)
    
    @classmethod
    def list_by_category(cls) -> Dict[str, List[ActionSpec]]:
        """
        Lista todas las acciones organizadas por categoría.
        """
        return cls._categories.copy()
    
    @classmethod
    def list_all_actions(cls) -> Dict[str, ActionSpec]:
        """
        Lista todas las acciones registradas.
        """
        return cls._actions.copy()
    
    @classmethod
    def get_enabled_types(cls, enabled_set: set = None) -> List[str]:
        """
        Obtiene la lista de tipos habilitados para el frontend.
        """
        if enabled_set is None:
            # Si no hay filtro, devolver todos
            return list(cls._actions.keys())
        
        return [action_id for action_id in cls._actions.keys() 
                if action_id in enabled_set]
    
    @classmethod
    def auto_discover_actions(cls, base_path: str = "modules.actions") -> None:
        """
        Auto-descubre y carga todas las acciones desde el directorio actions.
        """
        if cls._initialized:
            return
            
        print(f"[REGISTRY] Iniciando auto-descubrimiento desde {base_path}")
        
        try:
            # Importar todos los módulos de actions
            cls._import_actions_recursively(base_path)
            cls._initialized = True
            print(f"[REGISTRY] Auto-descubrimiento completado: {len(cls._actions)} acciones")
            
        except Exception as e:
            print(f"[REGISTRY] Error en auto-descubrimiento: {e}")
    
    @classmethod
    def _import_actions_recursively(cls, module_path: str) -> None:
        """
        Importa recursivamente todos los módulos de acciones.
        """
        try:
            # Convertir path de módulo a path de archivo
            path_parts = module_path.split('.')
            current_path = os.path.join(*path_parts)
            
            if not os.path.exists(current_path):
                return
            
            # Si es un archivo .py, importarlo
            if current_path.endswith('.py'):
                importlib.import_module(module_path)
                return
            
            # Si es un directorio, explorar recursivamente
            if os.path.isdir(current_path):
                for item in os.listdir(current_path):
                    if item == '__pycache__':
                        continue
                        
                    item_path = os.path.join(current_path, item)
                    
                    if item.endswith('.py') and item != '__init__.py':
                        # Importar módulo python
                        module_name = item[:-3]  # remover .py
                        full_module_path = f"{module_path}.{module_name}"
                        try:
                            importlib.import_module(full_module_path)
                        except ImportError as e:
                            print(f"[REGISTRY] No se pudo importar {full_module_path}: {e}")
                    
                    elif os.path.isdir(item_path) and not item.startswith('.'):
                        # Explorar subdirectorio
                        cls._import_actions_recursively(f"{module_path}.{item}")
                        
        except Exception as e:
            print(f"[REGISTRY] Error importando {module_path}: {e}")
    
    @classmethod
    def clear_registry(cls) -> None:
        """
        Limpia el registro (útil para testing).
        """
        cls._actions.clear()
        cls._categories.clear() 
        cls._initialized = False
