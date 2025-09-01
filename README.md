# FlowRunner

**FlowRunner** es un **orquestador low-code** para construir flujos de trabajo a partir de **nodos arrastrables** y **conexiones SVG**. Está pensado para automatizar tareas de escritorio y de archivos de forma visual, mientras un backend en Python ejecuta los pasos y reporta progreso a la interfaz.

## Objetivo

- Reducir la fricción para **automatizar procesos** combinando operaciones de archivos, Excel, variables y esperas, sin escribir código en la mayoría de casos.
- Ofrecer una **UI clara**: catálogo de funciones, canvas con nodos, propiedades contextuales y consola de ejecución con logs.

## Tecnologías

- **Frontend:** HTML + CSS + JavaScript (sin framework), SVG para edges.
- **Integración:** [Eel](https://github.com/python-eel) para comunicar la UI con Python.
- **Backend:** Python 3 (módulos por dominio funcional).

## ¿Cómo funciona (alto nivel)?

1. Arrastras funciones desde el **catálogo** y creas **nodos** en el lienzo.
2. Conectas nodos con **edges** dirigidos para definir el flujo.
3. Configuras parámetros en el **panel de propiedades**.
4. Al ejecutar, la UI envía un **JSON del flujo** al backend.  
   El backend procesa y notifica progreso/resultados; la UI actualiza la **consola** y, cuando corresponde, muestra **previews** en el panel derecho.

## Funciones disponibles hoy

- **Funciones Básicas**
  - Pausa (esperar)
  - Variable: Set
  - Variable: Get
- **Acciones de Lectura**
  - Excel: Leer rango
  - Carpeta: Listar
- **Acciones de Escritura**
  - Escribir CSV
  - Escribir Excel
  - Excel: Crear hoja
  - Archivo: Mover
  - Archivo: Copiar
  - Archivo: Borrar
  - Carpeta: Crear

> La visibilidad real depende de los *feature flags* devueltos por el backend (`ENABLED_TYPES`).

## En carpeta (próximas)

- HTTP GET/POST y descargas
- Envío de email
- Condiciones / bifurcaciones y bucles
- Expresiones y variables avanzadas
- Lectura/escritura de más formatos

## Arquitectura resumida

UI (HTML/CSS/JS) ←→ Eel (bridge) ←→ Backend Python
│ │
├─ Construye y exporta JSON ├─ Ejecuta pasos (por typeId)
├─ Consola / propiedades ├─ Emite notify_progress(...)
└─ SVG edges / drag └─ Control de variables y archivos