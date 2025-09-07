# Changelog
Todas las modificaciones relevantes de este proyecto se documentarán en este archivo.

Este archivo sigue el formato de **[Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)** y la estrategia de versionado **[SemVer](https://semver.org/lang/es/)**.

## [Unreleased] - 2025-09-06

### CRITICAL FIXES - Sistema Completamente Estable
*Commit: 81eb9cc - Corrección completa de errores de tipos y validaciones*

#### Fixed - Errores Críticos Resueltos
- **"Paso sin tipo definido"**: `buildFlowJSON()` ahora incluye tanto `typeId` como `type` para compatibilidad backend
- **Errores de conversión de tipos**: 
  - `pausa()`: Conversión automática string→float antes de validaciones numéricas
  - `delay_dinamico()`: Conversión de todos los parámetros numéricos al inicio
  - `bucle_for_rango()`: Conversión string→int para inicio, fin, paso, max_iteraciones
- **Variable scope issues**: Corregida lógica en `flujo_simple_phase2.json` para usar referencias correctas
- **"'<=' not supported between instances of 'str' and 'int'"**: Eliminado completamente con conversiones automáticas

#### Added - Nuevas Funcionalidades Estables
- **Sistema Toast Completo**:
  - Diseño moderno con animaciones suaves
  - 5 tipos: success, error, warning, info, loading
  - Auto-hide configurable y botón close manual
  - Soporte dark mode y responsive design
  - Integración completa frontend/backend
- **Error Handler Robusto**:
  - Captura global de errores JavaScript
  - Manejo de promesas rechazadas (unhandledrejection)
  - Intercepción de console.error/warn
  - Almacenamiento local como fallback de logging
- **Sistema de Logging Centralizado**:
  - `FlowLogger` con rotación automática de archivos
  - Logs estructurados en formato JSON
  - Integración completa entre frontend y backend
  - Categorías: user.log, error.log, temp.log

#### Enhanced - Acciones de Procesamiento Avanzado
- **calcular_estadisticas**: Análisis estadístico completo de DataFrames
- **normalizar_datos**: Normalización con métodos min-max, z-score, robust
- **filtrar_dataframe**: Filtrado avanzado con operadores lógicos
- **transformar_columnas**: Transformaciones matemáticas y de cadenas
- **agrupar_datos**: Agrupamiento con agregaciones personalizadas
- **eliminar_duplicados**: Limpieza inteligente de datos duplicados
- **ordenar_avanzado**: Ordenamiento multi-columna con direcciones
- **pivotar_tabla**: Creación de tablas pivote avanzadas
- **validar_datos**: Validación de calidad con reportes detallados

#### Testing - Suite Completa de Validación
- **test_complete_system.py**: Validación integral del sistema
- **test_control_final.py**: Tests de acciones de control avanzado
- **test_processing_fase1.py**: Validación de procesamiento de datos
- **test_integration_complete.py**: Tests de integración end-to-end
- **Flujos de prueba actualizados**: flujo_simple_phase2_fixed.json, flujo_complejo_phase2.json
- **Zero errores 404**: Todos los import conflicts resueltos

#### Technical Improvements
- **47+ acciones operativas**: Sistema completo sin errores de ejecución
- **Conversiones automáticas**: Todos los parámetros string convertidos apropiadamente
- **favicon.svg**: Icono SVG moderno integrado
- **43 archivos modificados**: 6,872 inserciones, 78 eliminaciones
- **Sistema listo para Phase 3**: Base completamente estable

### MAJOR UPDATES - Phase 2 Control Flow & Logging System

### Added
- **ARQUITECTURA MODULAR COMPLETA**: Nueva estructura `modules/actions/` con auto-discovery
- **ActionRegistry**: Sistema de registro automático de acciones con decoradores `@action`
- **FlowExecutor**: Motor de ejecución mejorado con gestión de contexto y logging integrado
- **Organización por dominios**: control/, data/, dialogs/, navigation/, files/, finalization/
- **Utilidades consolidadas**: modules/utils/ con data_io, web_automation, dialogs, **logging**

#### PHASE 1: PROCESAMIENTO DE DATOS AVANZADO (11 nuevas acciones)
- **transforms.py**: filtrar_dataframe, transformar_columnas, agrupar_datos, eliminar_duplicados, ordenar_avanzado, pivotar_tabla
- **statistics.py**: calcular_estadisticas, normalizar_datos  
- **joins.py**: unir_datasets, concatenar_datasets
- **validators.py**: validar_datos
- **ETL Capabilities**: Convierte FlowRunner en herramienta completa de procesamiento de datos

#### PHASE 2: CONTROL DE FLUJO AVANZADO (12 nuevas acciones)
- **loops.py**: bucle_for_rango, bucle_for_lista, repetir_hasta, interrumpir_flujo
- **conditions.py**: condicional_multiple (switch/case), condicional_and_or, esperar_condicion
- **exceptions.py**: try_catch_finally, validar_variable
- **timing.py**: delay_dinamico, esperar_hasta_hora, programar_ejecucion
- **Advanced Flow Control**: Loops, conditionals, exception handling, dynamic scheduling

#### SISTEMA DE LOGGING CENTRALIZADO
- **/var Directory**: user.log, error.log, temp.log
- **FlowLogger**: Logging centralizado con niveles y contexto estructurado
- **Integración completa**: Executor con logging automático de acciones y flujos
- **Trazabilidad**: Registro completo de actividad del usuario y errores

#### TESTING & INTEGRATION
- **test_control_fase2.py**: Tests completos Phase 2 control flow
- **test_flows_integration.py**: Tests de flujos completos con logging
- **Flujos de prueba**: flujo_simple_phase2.json, flujo_complejo_phase2.json
- **85.7% success rate** en testing de Phase 2

### Changed
- **NAVEGADOR EN MODO APP**: Fija problema de apertura en pestañas
- **Detección de navegadores**: Chrome/Edge con fallback automático
- **Mejora en context management**: Variables y driver state unificados
- **Catálogo UI actualizado**: Nuevas categorías Control de Flujo Avanzado, Procesamiento Avanzado
- **Executor mejorado**: Logging automático de inicio/fin de acciones y flujos
- **47 acciones totales**: Sistema completo con capacidades empresariales

### Fixed
- **Browser app mode**: Navegador ahora abre como aplicación independiente
- **Import dependencies**: Eliminadas dependencias circulares
- **Performance**: Auto-discovery optimizado para carga rápida
- **Parameter mapping**: Corrección de mapeo de parámetros en executor
- **Error handling**: Logging estructurado de errores con contexto completo

### Technical Details
- **Arquitectura**: Modular con auto-discovery pattern
- **Total Actions**: 47 acciones en 9 categorías
- **Backend**: Python con decoradores, typing, dataclasses
- **Frontend**: ES6 modules con dynamic catalog system
- **Logging**: Structured JSON logging con rotación automática
- **Testing**: Unit + integration tests con 85%+ success rate

### Removed
- **Arquitectura legacy eliminada**:
  - modules/funciones/ (estructura monolítica antigua)
  - modules/config.py (mapeo manual de acciones)
  - modules/helpers.py (utilidades obsoletas)
  - modules/funciones/extras.py (8.5KB de código monolítico)
- **Código duplicado**: Consolidación de funciones similares

### Security
- **Validación mejorada**: Parámetros requeridos y tipos de datos
- **Path safety**: Validación de rutas en operaciones de archivos

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
