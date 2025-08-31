# modules/funciones/navegador/navegador.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

try:
    import pygetwindow as gw
except Exception:
    gw = None

# Apertura de navegador y URL
def abrir_pagina_web_selenium(url: str):
    options = Options()
    options.add_argument("--start-maximized")
    # Selenium 4.6+ usa Selenium Manager → no hace falta Service(executable_path=...)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(1.5)
    return driver

def cambiar_pagina_web_selenium(driver, nueva_url: str):
    if driver is None:
        raise RuntimeError("Driver no inicializado. Ejecutá 'abrir_pagina_web_selenium' primero.")
    driver.get(nueva_url)
    time.sleep(1.2)

def cerrar_navegador_selenium(driver):
    if driver is None:
        return
    try:
        driver.quit()
    except Exception:
        pass

def maximizar_navegador(driver):
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

def minimizar_navegador(driver):
    if driver is None:
        return
    if gw:
        try:
            window_title = driver.title
            for w in gw.getWindowsWithTitle(window_title):
                w.minimize()
        except Exception:
            pass