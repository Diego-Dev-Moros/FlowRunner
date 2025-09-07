# modules/browser_config.py
"""
Configuración y gestión de navegadores para modo aplicación de escritorio.
Soporta Chrome y Edge con fallback controlado.
"""

import os
import shutil
import subprocess
from eel import browsers
from typing import Dict, Optional, List, Tuple


class BrowserConfig:
    """Maneja la detección y configuración de navegadores para modo app."""
    
    def __init__(self):
        self.detected_browsers = {}
        self.app_modes = []
        self._detect_browsers()
        self._setup_app_modes()
    
    def _detect_browsers(self) -> None:
        """Detecta navegadores disponibles en el sistema."""
        # Rutas comunes de instalación
        pf = os.environ.get('ProgramFiles', r"C:\Program Files")
        pf86 = os.environ.get('ProgramFiles(x86)', r"C:\Program Files (x86)")
        lad = os.environ.get('LOCALAPPDATA', os.path.expanduser(r"~\AppData\Local"))
        
        # Chrome
        chrome_paths = [
            os.path.join(pf, r"Google\Chrome\Application\chrome.exe"),
            os.path.join(pf86, r"Google\Chrome\Application\chrome.exe"),
            os.path.join(lad, r"Google\Chrome\Application\chrome.exe"),
            shutil.which("chrome"),
            shutil.which("chrome.exe"),
        ]
        
        chrome = next((p for p in chrome_paths if p and os.path.exists(p)), None)
        if chrome:
            self.detected_browsers["chrome"] = chrome
            print(f"[BROWSER] Chrome detectado: {chrome}")
        
        # Edge
        edge_paths = [
            os.path.join(pf, r"Microsoft\Edge\Application\msedge.exe"),
            os.path.join(pf86, r"Microsoft\Edge\Application\msedge.exe"),
            shutil.which("msedge"),
            shutil.which("msedge.exe"),
        ]
        
        edge = next((p for p in edge_paths if p and os.path.exists(p)), None)
        if edge:
            self.detected_browsers["edge"] = edge
            print(f"[BROWSER] Edge detectado: {edge}")
        
        if not self.detected_browsers:
            print("[BROWSER] No se detectaron navegadores compatibles")
    
    def _setup_app_modes(self) -> None:
        """Configura los modos de aplicación disponibles."""
        # Orden de preferencia: Chrome primero, luego Edge
        if "chrome" in self.detected_browsers:
            self.app_modes.append("chrome-app")
        if "edge" in self.detected_browsers:
            self.app_modes.append("edge-app")
    
    def register_browsers(self) -> None:
        """Registra los navegadores con Eel."""
        for browser, path in self.detected_browsers.items():
            browsers.set_path(browser, path)
            browsers.set_path(f'{browser}-app', path)
            print(f"[BROWSER] Registrado {browser} en modo app")
    
    def get_app_options(self, host: str, port: int, page: str, size: Tuple[int, int]) -> Dict:
        """Genera las opciones optimizadas para modo aplicación."""
        url = f"http://{host}:{port}/{page}"
        
        return {
            'size': size,
            'host': host,
            'port': port,
            'block': True,
            # HOTFIX #4: Flags optimizados para mejor modo app
            'cmdline_args': [
                f'--app={url}',
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-default-apps',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-translate',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-features=VizDisplayCompositor',
                '--disable-web-security',  # Para desarrollo
                '--app-auto-launched',      # Comportamiento nativo app
                '--no-sandbox'              # Para compatibilidad
            ]
        }
    
    def test_browser_app_mode(self, browser_mode: str, url: str) -> bool:
        """Prueba si un navegador puede abrir en modo app."""
        try:
            if browser_mode not in self.detected_browsers.keys():
                browser_name = browser_mode.replace('-app', '')
                if browser_name not in self.detected_browsers:
                    return False
            
            browser_name = browser_mode.replace('-app', '')
            browser_path = self.detected_browsers[browser_name]
            
            # Comando de prueba sin bloqueo
            cmd = [
                browser_path,
                f'--app={url}',
                '--disable-web-security',
                '--no-first-run'
            ]
            
            # Ejecutar sin esperar (non-blocking)
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
            
        except Exception as e:
            print(f"[BROWSER] Error probando {browser_mode}: {e}")
            return False
    
    def get_fallback_modes(self) -> List[str]:
        """Devuelve modos de fallback (pestañas normales) si el modo app falla."""
        fallback = []
        if "chrome" in self.detected_browsers:
            fallback.append("chrome")
        if "edge" in self.detected_browsers:
            fallback.append("edge")
        return fallback
    
    def launch_app(self, page: str, host: str = 'localhost', port: int = 8000, 
                   size: Tuple[int, int] = (1280, 800)) -> Tuple[bool, str]:
        """
        Intenta lanzar la aplicación en modo app.
        
        Returns:
            Tuple[bool, str]: (éxito, modo_usado)
        """
        import eel
        
        self.register_browsers()
        app_options = self.get_app_options(host, port, page, size)
        
        # Intentar modos app primero
        for mode in self.app_modes:
            try:
                print(f"[BROWSER] Intentando modo aplicación: {mode}")
                eel.start(page, mode=mode, **app_options)
                return True, mode
                
            except Exception as e:
                print(f"[BROWSER] Falló {mode}: {e}")
                continue
        
        # Fallback a pestañas normales si el usuario lo permite
        print("[BROWSER] Modo aplicación falló. Intentando modos de pestaña...")
        fallback_modes = self.get_fallback_modes()
        
        for mode in fallback_modes:
            try:
                print(f"[BROWSER] Intentando modo pestaña: {mode}")
                # Opciones más simples para modo pestaña
                simple_options = {
                    'host': host,
                    'port': port,
                    'block': True
                }
                eel.start(page, mode=mode, **simple_options)
                return True, mode
                
            except Exception as e:
                print(f"[BROWSER] Falló {mode}: {e}")
                continue
        
        # Último recurso: servidor sin navegador
        try:
            print(f"[BROWSER] Iniciando servidor sin navegador: http://{host}:{port}/{page}")
            eel.start(page, mode=None, host=host, port=port, block=True)
            return True, "server-only"
            
        except Exception as e:
            print(f"[BROWSER] Error crítico: {e}")
            return False, "failed"


def create_browser_config() -> BrowserConfig:
    """Factory function para crear configuración de navegador."""
    return BrowserConfig()
