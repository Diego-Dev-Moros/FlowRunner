# 🚀 ToolKit - Guía de instalación y ejecución

> Herramienta de automatización con **UI basada en Eel** y empaquetado con **PyInstaller**.

---

## 📑 Tabla de contenidos
- [🔹 Requisitos previos](#-requisitos-previos)
- [🔹 Crear y activar entorno virtual](#-crear-y-activar-entorno-virtual)
- [🔹 Ejecutar en desarrollo](#-ejecutar-en-desarrollo)
- [🔹 Empaquetar como ejecutable](#-empaquetar-como-ejecutable-eel--pyinstaller)
  - [📂 Carpeta de la UI](#-carpeta-de-la-ui)
  - [⚙️ Comando base](#️-comando-base)
  - [🔧 PyInstaller ≥ 6.0](#-pyinstaller--60)
  - [📦 Salida del build](#-salida-del-build)
  - [🧹 Limpieza](#-limpieza)
- [🔹 Configurar funciones visibles (catálogo)](#-configurar-funciones-visibles-catálogo)
- [🔹 Solución de problemas](#-solución-de-problemas)
- [🔹 Actualizar dependencias](#-actualizar-dependencias)
- [🔹 Notas de ejecución](#-notas-de-ejecución)
- [⚡ Resumen rápido](#-resumen-rápido)

---

## 🔹 Requisitos previos

- ✅ **Python 3.10+** (recomendado **3.11**)  
- ✅ **pip** actualizado  
- ✅ Sistemas soportados: **Windows / macOS / Linux**  
- *(Opcional)* **Google Chrome** si usarás el módulo navegador  
  *(Selenium Manager gestiona el driver automáticamente)*  

---

## 🔹 Crear y activar entorno virtual

### 💻 Windows (PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 💻 Windows (CMD)
```cmd
py -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 🐧 macOS / Linux (bash/zsh)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

➡️ **Salir del entorno:**  
```bash
deactivate
```

⚡ **Comando rápido (Windows):**
```bash
py -m venv .venv; .venv\scripts\activate; pip install -r requirements.txt
```

---

## 🔹 Ejecutar en desarrollo

```bash
python index.py
```

- Abre la UI → `vistas/servicio.html`  
- Logs visibles en la consola integrada  
- Cambios en **JS/CSS** se reflejan al recargar  

---

## 🔹 Empaquetar como ejecutable (Eel + PyInstaller)

### 📂 Carpeta de la UI
El segundo argumento de **Eel** debe apuntar a la carpeta raíz de la UI estática:  
```bash
vistas
```

### ⚙️ Comando base
```bash
python -m eel index.py vistas -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole
```

### 🔧 PyInstaller ≥ 6.0
Agregar:  
```bash
--contents-directory .
```

✅ Comando completo:
```bash
python -m eel index.py vistas -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole --contents-directory .
```

### 📦 Salida del build
- `dist/ToolKit/` → ejecutable final  
- `build/` y archivo `.spec` → generados en la compilación  

### 🧹 Limpieza
```bash
# macOS / Linux
rm -rf build dist *.spec

# Windows (PowerShell)
Remove-Item build, dist, *.spec -Recurse -Force
```

---

## 🔹 Configurar funciones visibles (catálogo)

Archivo: **`modules/config.py`**

```python
ENABLED_TYPES = {
    'leer_csv', 'leer_excel', 'leer_txt', 'excel_leer_rango',
    'escribir_csv', 'escribir_excel', 'excel_crear_hoja',
    'archivo_mover', 'archivo_copiar', 'archivo_borrar',
    'carpeta_crear', 'carpeta_listar',
    'pausa', 'variable_set', 'variable_get',
    # Si queda vacío → se asume “todas habilitadas”.
}
```

🔹 La UI llama `eel.get_enabled_types()` para filtrar el catálogo.

---

## 🔹 Solución de problemas

⚠️ **UI en blanco / `eel.js not found`**  
- Verifica que la carpeta sea `vistas`  
- Confirma que `servicio.html` y `assets` estén allí  

⚠️ **Selenium/Chrome falla**  
```bash
pip install -U selenium
```
- Instala Google Chrome  
- Si falla, instala driver manualmente  

⚠️ **macOS (Gatekeeper)**  
- Primera vez: **Control + clic → Abrir**  
- Para distribución: firma/notarización  

⚠️ **Windows (SmartScreen)**  
- Ejecutables no firmados → **firma digital recomendada**  

---

## 🔹 Actualizar dependencias
```bash
pip install -U -r requirements.txt
```

---

## 🔹 Notas de ejecución

El backend puede enviar progreso a la UI:

```python
eel.notify_progress({
    "stepId": "N1_listar",
    "message": "Se listaron 120 archivos",
    "level": "info",
    "preview": ["C:/carpeta/a.txt", "C:/carpeta/b.txt"]
})
```

🔹 La UI mostrará el mensaje en consola y, si coincide el `stepId`, el **preview** en el panel derecho.  

### Atajos de la UI
- ⌨️ **F** → centra el nodo seleccionado  
- 🖱️ **Space + arrastrar** → pan  
- 🖱️ **Ctrl + rueda** → zoom  

---

## ⚡ Resumen rápido

```bash
# Crear entorno virtual
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Desarrollo
python index.py

# Empaquetar (PyInstaller < 6.0)
python -m eel index.py vistas -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole

# Empaquetar (PyInstaller ≥ 6.0)
python -m eel index.py vistas -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole --contents-directory .
```
# 🚀 ToolKit - Guía de instalación y ejecución

> Herramienta de automatización con **UI basada en Eel** y empaquetado con **PyInstaller**.

---

## 📑 Tabla de contenidos
- [🔹 Requisitos previos](#-requisitos-previos)
- [🔹 Crear y activar entorno virtual](#-crear-y-activar-entorno-virtual)
- [🔹 Ejecutar en desarrollo](#-ejecutar-en-desarrollo)
- [🔹 Empaquetar como ejecutable](#-empaquetar-como-ejecutable-eel--pyinstaller)
  - [📂 Carpeta de la UI](#-carpeta-de-la-ui)
  - [⚙️ Comando base](#️-comando-base)
  - [🔧 PyInstaller ≥ 6.0](#-pyinstaller--60)
  - [📦 Salida del build](#-salida-del-build)
  - [🧹 Limpieza](#-limpieza)
- [🔹 Configurar funciones visibles (catálogo)](#-configurar-funciones-visibles-catálogo)
- [🔹 Solución de problemas](#-solución-de-problemas)
- [🔹 Actualizar dependencias](#-actualizar-dependencias)
- [🔹 Notas de ejecución](#-notas-de-ejecución)
- [⚡ Resumen rápido](#-resumen-rápido)

---

## 🔹 Requisitos previos

- ✅ **Python 3.10+** (recomendado **3.11**)  
- ✅ **pip** actualizado  
- ✅ Sistemas soportados: **Windows / macOS / Linux**  
- *(Opcional)* **Google Chrome** si usarás el módulo navegador  
  *(Selenium Manager gestiona el driver automáticamente)*  

---

## 🔹 Crear y activar entorno virtual

### 💻 Windows (PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 💻 Windows (CMD)
```cmd
py -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 🐧 macOS / Linux (bash/zsh)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

➡️ **Salir del entorno:**  
```bash
deactivate
```

⚡ **Comando rápido (Windows):**
```bash
py -m venv .venv; .venv\scripts\activate; pip install -r requirements.txt
```

---

## 🔹 Ejecutar en desarrollo

```bash
python index.py
```

- Abre la UI → `vistas/servicio.html`  
- Logs visibles en la consola integrada  
- Cambios en **JS/CSS** se reflejan al recargar  

---

## 🔹 Empaquetar como ejecutable (Eel + PyInstaller)

### 📂 Carpeta de la UI
El segundo argumento de **Eel** debe apuntar a la carpeta raíz de la UI estática:  
```bash
vistas
```

### ⚙️ Comando base
```bash
python -m eel index.py vistas -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole
```

### 🔧 PyInstaller ≥ 6.0
Agregar:  
```bash
--contents-directory .
```

✅ Comando completo:
```bash
python -m eel index.py vistas -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole --contents-directory .
```

### 📦 Salida del build
- `dist/ToolKit/` → ejecutable final  
- `build/` y archivo `.spec` → generados en la compilación  

### 🧹 Limpieza
```bash
# macOS / Linux
rm -rf build dist *.spec

# Windows (PowerShell)
Remove-Item build, dist, *.spec -Recurse -Force
```

---

## 🔹 Configurar funciones visibles (catálogo)

Archivo: **`modules/config.py`**

```python
ENABLED_TYPES = {
    'leer_csv', 'leer_excel', 'leer_txt', 'excel_leer_rango',
    'escribir_csv', 'escribir_excel', 'excel_crear_hoja',
    'archivo_mover', 'archivo_copiar', 'archivo_borrar',
    'carpeta_crear', 'carpeta_listar',
    'pausa', 'variable_set', 'variable_get',
    # Si queda vacío → se asume “todas habilitadas”.
}
```

🔹 La UI llama `eel.get_enabled_types()` para filtrar el catálogo.

---

## 🔹 Solución de problemas

⚠️ **UI en blanco / `eel.js not found`**  
- Verifica que la carpeta sea `vistas`  
- Confirma que `servicio.html` y `assets` estén allí  

⚠️ **Selenium/Chrome falla**  
```bash
pip install -U selenium
```
- Instala Google Chrome  
- Si falla, instala driver manualmente  

⚠️ **macOS (Gatekeeper)**  
- Primera vez: **Control + clic → Abrir**  
- Para distribución: firma/notarización  

⚠️ **Windows (SmartScreen)**  
- Ejecutables no firmados → **firma digital recomendada**  

---

## 🔹 Actualizar dependencias
```bash
pip install -U -r requirements.txt
```

---

## 🔹 Notas de ejecución

El backend puede enviar progreso a la UI:

```python
eel.notify_progress({
    "stepId": "N1_listar",
    "message": "Se listaron 120 archivos",
    "level": "info",
    "preview": ["C:/carpeta/a.txt", "C:/carpeta/b.txt"]
})
```

🔹 La UI mostrará el mensaje en consola y, si coincide el `stepId`, el **preview** en el panel derecho.  

### Atajos de la UI
- ⌨️ **F** → centra el nodo seleccionado  
- 🖱️ **Space + arrastrar** → pan  
- 🖱️ **Ctrl + rueda** → zoom  

---

## ⚡ Resumen rápido

```bash
# Crear entorno virtual
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Desarrollo
python index.py

# Empaquetar (PyInstaller < 6.0)
python -m eel index.py vistas -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole

# Empaquetar (PyInstaller ≥ 6.0)
python -m eel index.py vistas -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole --contents-directory .
```
