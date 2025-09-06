# Changelog
Todas las modificaciones relevantes de este proyecto se documentarán en este archivo.

Este archivo sigue el formato de **[Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)** y la estrategia de versionado **[SemVer](https://semver.org/lang/es/)**.

## [Unreleased]
### Added
- 🏗️ **ARQUITECTURA MODULAR COMPLETA**: Nueva estructura `modules/actions/` con auto-discovery
- 🔧 **ActionRegistry**: Sistema de registro automático de acciones con decoradores `@action`
- 🎯 **FlowExecutor**: Motor de ejecución mejorado con gestión de contexto
- 📁 **Organización por dominios**: control/, data/, dialogs/, navigation/, files/, finalization/
- 🛠️ **Utilidades consolidadas**: modules/utils/ con data_io, web_automation, dialogs
- 🚀 **12 NUEVAS ACCIONES**: Duplicamos funcionalidad (24 total en 8 categorías)
  - **Navegación Web**: abrir_pagina, cambiar_pagina, maximizar_navegador  
  - **Gestión de Archivos**: crear_carpeta, mover_archivo, copiar_archivo, eliminar_archivo
  - **Escritura de Datos**: escribir_csv, escribir_excel, escribir_txt
  - **Finalización**: cerrar_navegador, finalizar_todo
- 🎨 **Frontend reorganizado**: Catálogo con emojis y nuevas categorías
- 🧪 **Sistema de testing**: test_registry.py y test_integration.py

### Changed
- 🌐 **NAVEGADOR EN MODO APP**: Fija problema de apertura en pestañas
- 📊 **Detección de navegadores**: Chrome/Edge con fallback automático
- 🔄 **Mejora en context management**: Variables y driver state unificados
- 📋 **Catálogo UI**: Nuevas categorías con iconos emoji (🚀🌐📖📊💬📁🏁)

### Fixed
- 🐛 **Browser app mode**: Navegador ahora abre como aplicación independiente
- 🔧 **Import dependencies**: Eliminadas dependencias circulares
- ⚡ **Performance**: Auto-discovery optimizado para carga rápida

### Removed
- 🗑️ **Arquitectura legacy eliminada**:
  - modules/funciones/ (estructura monolítica antigua)
  - modules/config.py (mapeo manual de acciones)
  - modules/helpers.py (utilidades obsoletas)
  - modules/funciones/extras.py (8.5KB de código monolítico)
- 🧹 **Código duplicado**: Consolidación de funciones similares

### Security
- 🛡️ **Validación mejorada**: Parámetros requeridos y tipos de datos
- 🔒 **Path safety**: Validación de rutas en operaciones de archivos

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
