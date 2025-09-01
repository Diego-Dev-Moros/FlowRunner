# FlowRunner — Información del proyecto

## 1. Propósito
**FlowRunner** permite **definir y ejecutar flujos** mediante nodos visuales. Su meta es que tareas frecuentes (archivos, Excel, esperas, etc.) se integren de forma **rápida y mantenible**.

---

## 2. Componentes y responsabilidades

### 2.1. Frontend (carpeta `vistas/`)
- **servicio.html**: estructura base (topbar, catálogo, canvas, consola, propiedades).
- **styles/estilos.css**: tema, nodos, puertos, edges, paneles y **scrollbars personalizados**.
- **services/main.js**:
  - Inicializa topbar, catálogo, consola y panel de propiedades.
  - Maneja **drag & drop** de nodos, **pan (Space + arrastrar)** y **zoom (Ctrl + rueda)**.
  - Construye/actualiza **edges** en tiempo real.
  - Serializa a JSON (steps/edges) y **ejecuta** el flujo contra Python.
  - Centra la vista en el nodo seleccionado/creado (**tecla F** o automático).
- **services/state.js**: estado fuente de verdad (lista de pasos, edges, seleccionado y resultados).
- **services/catalog.js**: define **nodos** (typeId, nombre, categoría y **schema** de props).
- **services/registry.js**: filtra el catálogo según `ENABLED_TYPES` enviado por Python.
- **services/edges.js**: calcula posiciones y dibuja curvas **Bézier** con flecha.
- **services/ui/**:
  - `topbar.js`: Limpiar/Importar/Exportar.
  - `toolbar.js`: catálogo lateral por categorías (drag & drop).
  - `properties.js`: genera inputs/selects/textarea a partir del `schema`.
  - `console.js`: consola (Ejecutar/Detener/Limpiar) y API de logs.
- **services/io/json.js**: utilidades para import/export de flujos.
- **services/runtime/**: *glue* para ejecutar/transformar (lado UI).

**Datos clave de la UI**
- Un **nodo** tiene: `id`, `typeId`, `nombre`, `position:{x,y}`, `props:{...}`.
- Un **edge** tiene: `{ from: stepId, to: stepId }`.
- Al borrar X, si existía A→X y X→B, la UI crea **A→B** para conservar la continuidad.

---

### 2.2. Backend (carpeta `modules/`)
- **index.py** (raíz): arranca Eel, sirve la UI y expone:
  - `run_flow(flow_json)` → recibe el grafo y lo ejecuta.
  - `cancel_flow()` → solicita cancelación.
  - `get_enabled_types()` → (opcional) lista blanca para el catálogo.
  - Emite `eel.notify_progress({...})` durante la ejecución.
- **modules/funciones/acciones/**:
  - `control.py` → **Pausa/esperas** y utilidades de control.
  - `fs.py` → **sistema de archivos**: listar, mover, copiar, borrar.
  - `io_read.py` → **lecturas** (por ejemplo, rangos de Excel).
  - `io_write.py` → **escrituras** (CSV/Excel).
  - `web.py` → acciones web/HTTP (si aplica).
  - `dialogos_wrappers.py` → accesos a diálogos nativos.
- **modules/funciones/archivos/** (`lectura.py`, `escritura.py`, `gestor.py`) → soporte de E/S.
- **modules/funciones/navegador/navegador.py** → utilidades de automatización web/local (si se usa).
- **modules/helpers.py** y **modules/config.py** → utilidades y configuración.

**Contrato de ejecución**
- **UI → Python**
  - `eel.run_flow(flow)` ⇒ `{ ok: bool, variables?: list[str], error?: str }`
  - `eel.cancel_flow()`
- **Python → UI**
  - `eel.notify_progress({ stepId, message?, level?, preview? })`

`preview` permite mostrar en el **panel derecho** un resultado del paso (por ejemplo, un listado de archivos).

---

## 3. Módulos creados y su función (resumen)

- `acciones/control.py`: `pausa(segundos)` y futuros controles (retry, branch, etc.).
- `acciones/fs.py`: `listar_carpeta`, `mover`, `copiar`, `borrar`, `crear_carpeta`.
- `acciones/io_read.py`: `excel_leer_rango`, etc.
- `acciones/io_write.py`: `escribir_csv`, `escribir_excel`, `excel_crear_hoja`.
- `acciones/web.py`: placeholders para operaciones web/HTTP.
- `archivos/lectura.py` y `archivos/escritura.py`: helpers de E/S.
- `navegador/navegador.py`: automatización de navegador (si procede).
- `dialogos.py`, `extras.py`, `other.py`: funciones auxiliares.

Cada **typeId** definido en `catalog.js` debe tener su handler en Python o estar mapeado a uno existente.

---

## 4. Flujo de datos

1. La UI arma `flow = { version, steps[], edges[] }`.
2. Se envía con `eel.run_flow(flow)`.
3. Python resuelve el orden y ejecuta cada `typeId`.
4. Python emite `notify_progress` con mensajes y/o `preview`.
5. La UI actualiza la consola y los resultados del paso seleccionado.

**Ejemplo de `notify_progress`:**
```python
eel.notify_progress({
  "stepId": "N1_listar",
  "message": "Se listaron 120 archivos",
  "level": "info",
  "preview": ["C:/carpeta/a.txt", "C:/carpeta/b.txt"]  # o dict/tabla/lo que corresponda
})
```

---

## 5. Convenciones y buenas prácticas

- Mantener coherencia de id/typeId entre UI y backend.

- Definir schema minimal para props (tipos: text, number, select, textarea).

- Emitir preview solo si es útil; la UI lo mostrará en el panel derecho.

- Usar ENABLED_TYPES para ocultar funciones no listas para producción.

- Manejar errores en Python y devolver { ok: false, error: "mensaje" } si corresponde.

---

## 6. Funciones disponibles 

- Pausa, Variable Set/Get

- Carpeta: Listar

- Excel: Leer rango

- Escribir CSV, Escribir Excel, Excel: Crear hoja

- Archivo: Mover, Copiar, Borrar

- Carpeta: Crear
