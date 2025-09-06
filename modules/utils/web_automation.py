# modules/utils/web_automation.py
"""
Utilidades consolidadas para automatización web.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import time
from typing import Any, Optional

try:
    import pygetwindow as gw
except ImportError:
    gw = None


def crear_driver_chrome() -> webdriver.Chrome:
    """Crea un driver de Chrome con opciones optimizadas."""
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    # Selenium 4.6+ usa Selenium Manager automáticamente
    driver = webdriver.Chrome(options=options)
    return driver


def crear_driver_edge() -> webdriver.Edge:
    """Crea un driver de Edge con opciones optimizadas."""
    options = EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = webdriver.Edge(options=options)
    return driver


def abrir_pagina_web(url: str) -> webdriver.Chrome:
    """Abre una página web en Chrome."""
    try:
        driver = crear_driver_chrome()
        driver.get(url)
        time.sleep(1.5)
        return driver
    except Exception:
        # Fallback a Edge si Chrome falla
        driver = crear_driver_edge()
        driver.get(url)
        time.sleep(1.5)
        return driver


def cambiar_pagina_web(driver: Any, nueva_url: str) -> None:
    """Cambia la URL en el navegador actual."""
    if driver is None:
        raise RuntimeError("Driver no inicializado. Usar 'abrir_pagina_web' primero.")
    
    driver.get(nueva_url)
    time.sleep(1.2)


def cerrar_navegador(driver: Any) -> None:
    """Cierra el navegador."""
    if driver is None:
        return
    
    try:
        driver.quit()
    except Exception:
        pass


def maximizar_navegador(driver: Any) -> None:
    """Maximiza la ventana del navegador."""
    if driver is None:
        return
    
    # Intento con API del navegador
    try:
        driver.maximize_window()
        return
    except Exception:
        pass
    
    # Fallback con pygetwindow por título
    if gw:
        try:
            window_title = driver.title
            for w in gw.getWindowsWithTitle(window_title):
                w.maximize()
        except Exception:
            pass


def minimizar_navegador(driver: Any) -> None:
    """Minimiza la ventana del navegador."""
    if driver is None:
        return
    
    if gw:
        try:
            window_title = driver.title
            for w in gw.getWindowsWithTitle(window_title):
                w.minimize()
        except Exception:
            pass
