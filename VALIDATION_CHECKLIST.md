# 📋 Checklist de Validación - FlowRunner Refactorizado

## 🚀 PRUEBAS DE FUNCIONALIDAD BÁSICA

### ✅ Inicialización y Carga
- [ ] La aplicación carga sin errores en consola
- [ ] Se cargan correctamente estilos-clean.css y nodes-complete.css
- [ ] Todos los módulos se importan sin errores
- [ ] Topbar, sidebar y props panel son visibles
- [ ] Canvas muestra hint inicial "Arrastra funciones desde la izquierda"

### ✅ Creación y Manipulación de Nodos
- [ ] **Crear nodo**: Arrastrear desde catálogo crea nodo en canvas
- [ ] **Seleccionar nodo**: Click en nodo lo selecciona (borde naranja)
- [ ] **Mover nodo**: Drag desde header mueve el nodo
- [ ] **Eliminar nodo**: Click en X elimina el nodo con confirmación
- [ ] **Propiedades**: Seleccionar nodo actualiza panel derecho

### ✅ Sistema de Formas de Nodos
- [ ] **Decisión**: Crear "condicional_si" → muestra forma de rombo
- [ ] **Loop**: Crear "bucle_mientras" → muestra hexágono con marca interior
- [ ] **Inicio**: Crear "inicio" → muestra píldora verde
- [ ] **Cierre**: Crear "fin" → muestra píldora roja
- [ ] **Hover**: Hover sobre nodos con formas las resalta

### ✅ Conexiones (Edges)
- [ ] **Crear conexión**: Click puerto salida → puertos entrada se resaltan → click entrada crea edge
- [ ] **Edge visual**: Conexiones aparecen como líneas curvas naranjas
- [ ] **No duplicados**: Intentar crear conexión duplicada la rechaza
- [ ] **No auto-conexión**: Intentar conectar nodo consigo mismo la rechaza
- [ ] **Eliminar**: Borrar nodo elimina sus conexiones

### ✅ Pan y Zoom
- [ ] **Zoom in**: Ctrl + Wheel Up aumenta zoom (máx 200%)
- [ ] **Zoom out**: Ctrl + Wheel Down reduce zoom (mín 50%)
- [ ] **Pan**: Space + drag mueve la vista
- [ ] **Grosor constante**: Edges mantienen grosor al hacer zoom
- [ ] **Transform origin**: Zoom se hace desde esquina superior izquierda

### ✅ Viewport y Centrado
- [ ] **Auto-centrar**: Crear nodo centra la vista automáticamente
- [ ] **Tecla F**: Con nodo seleccionado, F centra la vista
- [ ] **Animación suave**: Centrado usa animación suave
- [ ] **Canvas size**: Canvas se redimensiona según nodos
- [ ] **Scroll**: Canvas es scrolleable cuando nodos salen del viewport

## 🎯 PRUEBAS DE PERFORMANCE

### ✅ Drag Performance
- [ ] **Test 15 nodos**: Crear 15 nodos en canvas
- [ ] **Drag continuo**: Arrastrar nodo en círculos por 3 segundos
- [ ] **FPS target**: Mantener ~45+ FPS durante drag (sin stuttering notable)
- [ ] **Edge updates**: Edges se actualizan suavemente durante drag
- [ ] **Memory**: No aumentos significativos de memoria

### ✅ Zoom Performance
- [ ] **Zoom 75%**: Reducir a 75% → edges mantienen grosor
- [ ] **Zoom 200%**: Aumentar a 200% → edges mantienen grosor  
- [ ] **Vector effect**: Edges usan vector-effect: non-scaling-stroke
- [ ] **Shape rendering**: Edges usan shape-rendering: geometricPrecision
- [ ] **Transform smooth**: Transiciones de zoom son fluidas

## 📁 PRUEBAS DE I/O (Import/Export)

### ✅ Export JSON
- [ ] **Crear flujo**: Crear 3+ nodos conectados
- [ ] **Exportar**: Topbar → Exportar descarga archivo .json
- [ ] **JSON válido**: Archivo se abre y contiene estructura válida
- [ ] **Datos completos**: JSON incluye steps, edges, positions, props

### ✅ Import JSON
- [ ] **Archivo válido**: Importar JSON válido carga nodos correctamente
- [ ] **Positions**: Nodos aparecen en posiciones correctas
- [ ] **Connections**: Edges se recrean correctamente
- [ ] **Auto-center**: Se centra automáticamente en primer nodo
- [ ] **Error handling**: JSON inválido muestra error claro

### ✅ Clear Canvas
- [ ] **Confirmación**: Clear canvas pide confirmación si hay nodos
- [ ] **Limpieza completa**: Elimina todos nodos y edges
- [ ] **Reset state**: Limpia selección y resultados
- [ ] **Hint visible**: Muestra hint "Arrastra funciones..."

## 🔧 PRUEBAS DE INTEGRACIÓN

### ✅ Runtime Bridge
- [ ] **Mock execution**: Sin backend, run_flow ejecuta modo demo
- [ ] **Progress simulation**: Modo demo simula progreso de nodos
- [ ] **Status visual**: Nodos muestran estados (running → completed)
- [ ] **Console logs**: Progreso aparece en consola
- [ ] **Stop function**: Stop cancela ejecución demo

### ✅ Eel Integration (si disponible)
- [ ] **notify_progress**: Python puede enviar notificaciones
- [ ] **run_flow**: Ejecutar flujo real llama Python
- [ ] **get_enabled_types**: Catálogo se filtra según backend
- [ ] **Error handling**: Errores de Python se muestran correctamente

## 🧪 PRUEBAS TÉCNICAS

### ✅ CSS Architecture
- [ ] **estilos-clean.css**: Solo contiene layout, UI global, no reglas .node
- [ ] **nodes-complete.css**: Contiene todas las reglas específicas de nodos
- [ ] **No conflicts**: Estilos no se pisaan entre archivos
- [ ] **Responsive**: Layout funciona en diferentes tamaños de ventana

### ✅ Module Loading
- [ ] **ES6 imports**: Todos los imports funcionan correctamente
- [ ] **No circular deps**: Sin dependencias circulares
- [ ] **Error boundaries**: Errores en módulos no rompen toda la app
- [ ] **Tree shaking**: Solo se cargan módulos utilizados

### ✅ Memory Management
- [ ] **Event cleanup**: Listeners se limpian al eliminar nodos
- [ ] **No memory leaks**: Uso de memoria estable durante uso prolongado
- [ ] **DOM cleanup**: Elementos DOM se eliminan correctamente
- [ ] **State consistency**: Estado permanece consistente

## 📊 CRITERIOS DE ÉXITO

### 🟢 PASA (95-100%)
- Todas las pruebas críticas pasan
- Performance target cumplido (45+ FPS)
- Sin errores en consola
- **Estado**: ✅ Listo para producción

### 🟡 PASA CON OBSERVACIONES (85-94%)
- Funcionalidad principal funciona
- Performance aceptable
- Errores menores o warnings
- **Estado**: ⚠️ Aprobar con plan de mejoras

### 🔴 NO PASA (<85%)
- Funcionalidad crítica falla
- Performance insuficiente
- Errores que impiden uso normal
- **Estado**: ❌ Requiere correcciones antes de aprobar

## 🔄 ROLLBACK PROCEDURES

Si alguna prueba crítica falla:

1. **Revertir HTML**:
   ```html
   <link rel="stylesheet" href="/vistas/styles/estilos.css" />
   <script type="module" src="/vistas/services/main.js"></script>
   ```

2. **Documentar issue**:
   - Qué prueba falló
   - Error específico
   - Steps to reproduce
   - Contexto del navegador/OS

3. **Notificar equipo**:
   - Issue crítico identificado
   - Rollback ejecutado
   - Plan de corrección requerido

---

## 📝 NOTAS DE VALIDACIÓN

**Fecha**: _______________  
**Validador**: _______________  
**Navegador**: _______________  
**OS**: _______________  

**Resultado general**: 🟢 PASA / 🟡 PASA CON OBSERVACIONES / 🔴 NO PASA

**Comentarios**:
_________________________________
_________________________________
_________________________________

**Próximos pasos**:
_________________________________
_________________________________
_________________________________
