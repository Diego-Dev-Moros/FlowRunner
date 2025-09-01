# Contribuir a FlowRunner

¡Gracias por tu interés en contribuir! Este documento explica el flujo de trabajo y las pautas para proponer cambios.

## 1. Antes de empezar
- Lee `documentation/Information.md` para entender la arquitectura (UI + Python/Eel).
- Para instalación/ejecución local usa **`Comments.md`** (ahí están los comandos).
- Usa **SemVer** y registra cambios en **`CHANGELOG.md`** (sección *Unreleased*).

## 2. Reportar issues / proponer mejoras
- Abre un *issue* con:
  - Contexto y motivación.
  - Pasos para reproducir (si es bug).
  - Comportamiento esperado.
  - Capturas o logs si aplica.

## 3. Flujo de trabajo (PRs)
1. **Fork** del repositorio.
2. Crea una rama desde `main`:
   - `feature/<breve-descripcion>`
   - `fix/<breve-descripcion>`
   - `docs/<breve-descripcion>`
3. Sigue **Conventional Commits** en los mensajes:
   - `feat: agrega acción carpeta_listar`
   - `fix: corrige redibujado de edges en resize`
   - `docs: actualiza Information.md`
   - `refactor: separa extras.py en módulos`
4. Asegúrate de que el código **compila/ejecuta** y la UI funciona:
   - Frontend: abrir `vistas/servicio.html` a través de `index.py` (Eel).
   - Backend: ejecutar flujos básicos desde la consola integrada.
5. Actualiza `CHANGELOG.md` y documentación si aplica.
6. Crea el **Pull Request**:
   - Explica *qué cambia* y *por qué*.
   - Incluye pasos de prueba manuales y capturas si corresponde.

## 4. Estilo de código

### 4.1. JavaScript (frontend)
- Módulos ES (`type="module"`), funciones puras cuando sea posible.
- Evitar dependencias globales; usar selectores específicos por id/clase.
- Mantener responsabilidades separadas:
  - `main.js`: orquestación de UI.
  - `edges.js`: dibujo de conexiones.
  - `toolbar.js` / `topbar.js` / `console.js`: UI específicas.
  - `properties.js`: render dinámico de formularios desde `schema`.
- No mezclar lógica de ejecución con renderizado (para eso está `runtime/`).

### 4.2. Python (backend)
- PEP8 como guía general.
- Módulos organizados por responsabilidad:
  - `funciones/acciones`: orquestadores de dominio (fs, control, io_read, io_write, web).
  - `funciones/archivos`: helpers de I/O.
  - `navegador/`: automatización local/web si aplica.
- Validar inputs del flujo (rutas, tipos, formatos).
- Emitir `eel.notify_progress({ stepId, message?, level?, preview? })` cuando ayude al usuario.
- Responder a la UI con `{ "ok": true/false, "error"?: str, "variables"?: [] }`.

## 5. Catálogo y compatibilidad UI ↔ Backend
- Cada `typeId` en `vistas/services/catalog.js` debe tener un **handler** en Python.
- Usa `modules/config.py` → `ENABLED_TYPES` para *whitelists* de funciones visibles.
- Diseña `schema` minimal por nodo (tipos: `text`, `number`, `select`, `textarea`).
- Si tu acción produce datos interesantes, envía `preview` para mostrarlos en el panel derecho.

## 6. Pruebas manuales recomendadas
- Crear 3–4 nodos (p. ej., *Carpeta: Listar* → *Pausa* → *Escribir CSV*).
- Mover nodos y verificar que los edges se redibujan correctamente.
- Eliminar el nodo intermedio y confirmar la **reconexión A→B**.
- Importar/Exportar el JSON y volver a ejecutar.
- Probar `notify_progress` con `preview` (ver panel derecho).

## 7. Lanzamientos
- Actualiza `CHANGELOG.md` (*Unreleased* → versión nueva).
- Etiqueta el release (`vX.Y.Z`).
- Verifica que `ENABLED_TYPES` refleje lo que quieres mostrar en producción.

## 8. Código de conducta
Sé cordial y profesional. No se toleran faltas de respeto ni conductas discriminatorias.

## 9. Licencia
Al contribuir, aceptas que tus cambios se publiquen bajo la licencia del proyecto (ver `LICENSE`).
