# Changelog
Todas las modificaciones relevantes de este proyecto se documentarán en este archivo.

Este archivo sigue el formato de **[Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)** y la estrategia de versionado **[SemVer](https://semver.org/lang/es/)**.

## [Unreleased] - 2025-09-06

### ⚡ MAJOR UPDATES - Phase 2 Control Flow & Logging System

### Added
- 🏗️ **ARQUITECTURA MODULAR COMPLETA**: Nueva estructura `modules/actions/` con auto-discovery
- 🔧 **ActionRegistry**: Sistema de registro automático de acciones con decoradores `@action`
- 🎯 **FlowExecutor**: Motor de ejecución mejorado con gestión de contexto y logging integrado
- 📁 **Organización por dominios**: control/, data/, dialogs/, navigation/, files/, finalization/
- 🛠️ **Utilidades consolidadas**: modules/utils/ con data_io, web_automation, dialogs, **logging**

#### 🧮 PHASE 1: PROCESAMIENTO DE DATOS AVANZADO (11 nuevas acciones)
- **transforms.py**: filtrar_dataframe, transformar_columnas, agrupar_datos, eliminar_duplicados, ordenar_avanzado, pivotar_tabla
- **statistics.py**: calcular_estadisticas, normalizar_datos  
- **joins.py**: unir_datasets, concatenar_datasets
- **validators.py**: validar_datos
- **🎯 ETL Capabilities**: Convierte FlowRunner en herramienta completa de procesamiento de datos

#### 🎮 PHASE 2: CONTROL DE FLUJO AVANZADO (12 nuevas acciones)
- **loops.py**: bucle_for_rango, bucle_for_lista, repetir_hasta, interrumpir_flujo
- **conditions.py**: condicional_multiple (switch/case), condicional_and_or, esperar_condicion
- **exceptions.py**: try_catch_finally, validar_variable
- **timing.py**: delay_dinamico, esperar_hasta_hora, programar_ejecucion
- **🚀 Advanced Flow Control**: Loops, conditionals, exception handling, dynamic scheduling

#### 🔍 SISTEMA DE LOGGING CENTRALIZADO
- **📁 /var Directory**: user.log, error.log, temp.log
- **FlowLogger**: Logging centralizado con niveles y contexto estructurado
- **Integración completa**: Executor con logging automático de acciones y flujos
- **🎯 Trazabilidad**: Registro completo de actividad del usuario y errores

#### 🧪 TESTING & INTEGRATION
- **test_control_fase2.py**: Tests completos Phase 2 control flow
- **test_flows_integration.py**: Tests de flujos completos con logging
- **Flujos de prueba**: flujo_simple_phase2.json, flujo_complejo_phase2.json
- **85.7% success rate** en testing de Phase 2

### Changed
- 🌐 **NAVEGADOR EN MODO APP**: Fija problema de apertura en pestañas
- 📊 **Detección de navegadores**: Chrome/Edge con fallback automático
- 🔄 **Mejora en context management**: Variables y driver state unificados
- 📋 **Catálogo UI actualizado**: Nuevas categorías 🎮 Control de Flujo Avanzado, 🧮 Procesamiento Avanzado
- ⚡ **Executor mejorado**: Logging automático de inicio/fin de acciones y flujos
- 📈 **47 acciones totales**: Sistema completo con capacidades empresariales

### Fixed
- 🐛 **Browser app mode**: Navegador ahora abre como aplicación independiente
- 🔧 **Import dependencies**: Eliminadas dependencias circulares
- ⚡ **Performance**: Auto-discovery optimizado para carga rápida
- 🎯 **Parameter mapping**: Corrección de mapeo de parámetros en executor
- 🔍 **Error handling**: Logging estructurado de errores con contexto completo

### Technical Details
- **Arquitectura**: Modular con auto-discovery pattern
- **Total Actions**: 47 acciones en 9 categorías
- **Backend**: Python con decoradores, typing, dataclasses
- **Frontend**: ES6 modules con dynamic catalog system
- **Logging**: Structured JSON logging con rotación automática
- **Testing**: Unit + integration tests con 85%+ success rate

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
