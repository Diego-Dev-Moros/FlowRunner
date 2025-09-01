# ToolKit - Guía de instalación y ejecución

> Herramienta de automatización con UI basada en Eel y empaquetado con PyInstaller.

---

## 📌 Tabla de contenidos

- [Requisitos previos](#-requisitos-previos)
- [Crear y activar entorno virtual](#-crear-y-activar-entorno-virtual)
- [Ejecutar en desarrollo](#-ejecutar-en-desarrollo)
- [Empaquetar como ejecutable](#-empaquetar-como-ejecutable-eel--pyinstaller)
  - [Carpeta de la UI](#carpeta-de-la-ui)
  - [Comando base](#comando-base)
  - [PyInstaller ≥ 6.0](#pyinstaller--60)
  - [Salida del build](#salida-del-build)
  - [Limpieza](#limpieza)
- [Configurar funciones visibles (catálogo)](#-configurar-funciones-visibles-catálogo)
- [Solución de problemas](#-solución-de-problemas)
- [Actualizar dependencias](#-actualizar-dependencias)
- [Notas de ejecución](#-notas-de-ejecución)
- [Resumen rápido](#-resumen-rápido)

---

## 🔹 Requisitos previos

<details>
<summary>Ver requisitos</summary>

- **Python 3.10+** (recomendado 3.11)  
- **pip** actualizado  
- Sistemas soportados: Windows / macOS / Linux  
- *(Opcional)* Google Chrome si usarás el módulo de navegador; Selenium Manager gestiona el driver automáticamente

</details>

---

## 🔹 Crear y activar entorno virtual

<details>
<summary>Windows (PowerShell)</summary>

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
---
</details> 
<details> <summary>Windows (CMD)</summary>
    py -m venv .venv
    .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
</details> 
<details> <summary>macOS / Linux (bash/zsh)</summary>
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
</details>

Salir del entorno virtual: 
deactivate
Comando rápido:
py -m venv .venv; .venv/scripts/activate; pip install -r requirements.txt
Ejecutar en desarrollo
<details> <summary>Instrucciones</summary>

Con el entorno virtual activado:

python index.py


Levanta la UI (vistas/servicio.html) mediante Eel

La consola integrada permite ejecutar flujos y ver logs

Cambios en JS/CSS se reflejan automáticamente al recargar

</details>
🔹 Empaquetar como ejecutable (Eel + PyInstaller)
Carpeta de la UI
<details> <summary>Detalles</summary>

El segundo argumento de Eel debe apuntar a la carpeta raíz de la UI estática.
En este proyecto: vistas

</details>
Comando base
<details> <summary>Detalles</summary>
python -m eel index.py vistas -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole


index.py → script principal

vistas → carpeta con HTML/CSS/JS

-n ToolKit → nombre del ejecutable (personalizable)

--copy-metadata pikepdf → incluye metadatos de pikepdf

--collect-data docxcompose → incluye datos de docxcompose

--noconsole → oculta la consola (quítalo para depurar)

</details>
PyInstaller ≥ 6.0
<details> <summary>Detalles</summary>

Agrega:

--contents-directory .


Comando completo:

python -m eel index.py vistas -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole --contents-directory .

</details>
Salida del build
<details> <summary>Detalles</summary>

dist/ToolKit/ → ejecutable final

build/ y archivo .spec → generados durante la compilación

</details>
Limpieza
<details> <summary>Detalles</summary>
# macOS / Linux
rm -rf build dist *.spec

# Windows (PowerShell)
Remove-Item build, dist, *.spec -Recurse -Force

</details>
🔹 Configurar funciones visibles (catálogo)
<details> <summary>Detalles</summary>

Archivo: modules/config.py

ENABLED_TYPES = {
    'leer_csv', 'leer_excel', 'leer_txt', 'excel_leer_rango',
    'escribir_csv', 'escribir_excel', 'excel_crear_hoja',
    'archivo_mover', 'archivo_copiar', 'archivo_borrar',
    'carpeta_crear', 'carpeta_listar',
    'pausa', 'variable_set', 'variable_get',
    # Si queda vacío → se asume “todas habilitadas”.
}


La UI llama eel.get_enabled_types() para filtrar el catálogo

</details>
🔹 Solución de problemas
<details> <summary>Problemas comunes</summary>

UI en blanco / “eel.js not found”

Verifica que el argumento de carpeta sea vistas

Confirma que servicio.html y assets estén dentro de vistas

Selenium/Chrome falla

Asegura tener Google Chrome instalado

Actualiza Selenium: pip install -U selenium

Si persiste, instala el driver manualmente

macOS (Gatekeeper)

Primera vez: Control + clic → Abrir

Para distribución: firma/notarización

Windows (SmartScreen)

Puede advertir ejecutables no firmados; se recomienda firma digital

Ver logs en el build

Quita --noconsole para ver salida en terminal

</details>
🔹 Actualizar dependencias
pip install -U -r requirements.txt

🔹 Notas de ejecución
<details> <summary>Detalles</summary>

El backend puede emitir progreso a la UI:

eel.notify_progress({
    "stepId": "N1_listar",
    "message": "Se listaron 120 archivos",
    "level": "info",
    "preview": ["C:/carpeta/a.txt", "C:/carpeta/b.txt"]
})


La UI mostrará message en consola y, si stepId coincide con el nodo seleccionado, preview en el panel derecho

Atajos de la UI:

F → centra la vista en el nodo seleccionado

Space + arrastrar → pan

Ctrl + rueda → zoom

</details>
🔹 Resumen rápido
<details> <summary>Comandos esenciales</summary>
Crear entorno virtual e instalar dependencias
py -m venv .venv
.venv\Scripts\Activate.ps1   # (Windows PowerShell)
pip install -r requirements.txt

Desarrollo
python index.py

Empaquetar

PyInstaller < 6.0

python -m eel index.py vistas -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole


PyInstaller ≥ 6.0

python -m eel index.py vistas -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole --contents-directory .

</details> ```