# Changelog
Todas las modificaciones relevantes de este proyecto se documentarán en este archivo.

Este archivo sigue el formato de **[Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)** y la estrategia de versionado **[SemVer](https://semver.org/lang/es/)**.

## [Unreleased]
### Added
- (Ejemplo) Nueva acción: `carpeta_listar` con patrón de búsqueda.

### Changed
- (Ejemplo) UI: Zoom con Ctrl + rueda y pan con Space + arrastrar.

### Fixed
- (Ejemplo) Reconexión de edges al eliminar nodos intermedios.

### Deprecated
- (Ejemplo) Acción `excel_exportar_legacy` (usar `escribir_excel`).

### Removed
- (Ejemplo) Eliminado código muerto en `extras.py`.

### Security
- (Ejemplo) Validación de rutas para evitar path traversal.

---

## [1.0.0] - 2025-09-01
### Added
- Primera versión estable con:
  - Canvas con nodos, puertos y edges (Bézier).
  - Import/Export de flujos (JSON).
  - Catálogo filtrado por `ENABLED_TYPES` desde backend.
  - Acciones disponibles: Pausa, Variable Set/Get, Carpeta: Listar/Crear, Archivo: Mover/Copiar/Borrar, Excel: Leer rango, Escribir CSV/Excel, Excel: Crear hoja.
  - Consola integrada (Run/Stop/Clear) y `notify_progress` para preview.

### Fixed
- Redibujado robusto de edges en scroll/resize.

---
