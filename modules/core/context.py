# modules/core/context.py
"""
Contexto de ejecución para FlowRunner.
Maneja variables, estado y recursos compartidos durante la ejecución.
"""

from typing import Dict, Any, Optional
import threading


class FlowContext:
    """
    Contexto de ejecución que mantiene el estado durante un flujo.
    """
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.drivers: Dict[str, Any] = {}
        self.resources: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self.execution_id: Optional[str] = None
        self.current_step: Optional[str] = None
    
    def set_variable(self, name: str, value: Any) -> None:
        """
        Establece una variable en el contexto.
        """
        with self._lock:
            self.variables[name] = value
            print(f"[CONTEXT] Variable '{name}' = {repr(value)}")
    
    def get_variable(self, name: str, default: Any = None) -> Any:
        """
        Obtiene una variable del contexto.
        """
        with self._lock:
            value = self.variables.get(name, default)
            print(f"[CONTEXT] Leyendo variable '{name}' = {repr(value)}")
            return value
    
    def has_variable(self, name: str) -> bool:
        """
        Verifica si existe una variable.
        """
        with self._lock:
            return name in self.variables
    
    def list_variables(self) -> Dict[str, Any]:
        """
        Lista todas las variables actuales.
        """
        with self._lock:
            return self.variables.copy()
    
    def set_driver(self, driver_type: str, driver: Any) -> None:
        """
        Establece un driver (navegador, etc.) en el contexto.
        """
        with self._lock:
            self.drivers[driver_type] = driver
            print(f"[CONTEXT] Driver '{driver_type}' establecido")
    
    def get_driver(self, driver_type: str) -> Any:
        """
        Obtiene un driver del contexto.
        """
        with self._lock:
            return self.drivers.get(driver_type)
    
    def clear_driver(self, driver_type: str) -> None:
        """
        Limpia un driver del contexto.
        """
        with self._lock:
            if driver_type in self.drivers:
                driver = self.drivers.pop(driver_type)
                # Intentar cerrar el driver si tiene método close/quit
                if hasattr(driver, 'quit'):
                    try:
                        driver.quit()
                    except:
                        pass
                elif hasattr(driver, 'close'):
                    try:
                        driver.close()
                    except:
                        pass
                print(f"[CONTEXT] Driver '{driver_type}' limpiado")
    
    def clear_all_drivers(self) -> None:
        """
        Limpia todos los drivers.
        """
        with self._lock:
            for driver_type in list(self.drivers.keys()):
                self.clear_driver(driver_type)
    
    def set_resource(self, name: str, resource: Any) -> None:
        """
        Establece un recurso compartido.
        """
        with self._lock:
            self.resources[name] = resource
    
    def get_resource(self, name: str, default: Any = None) -> Any:
        """
        Obtiene un recurso compartido.
        """
        with self._lock:
            return self.resources.get(name, default)
    
    def cleanup(self) -> None:
        """
        Limpia todos los recursos del contexto.
        """
        print("[CONTEXT] Iniciando limpieza del contexto")
        self.clear_all_drivers()
        with self._lock:
            self.variables.clear()
            self.resources.clear()
        print("[CONTEXT] Contexto limpiado")
