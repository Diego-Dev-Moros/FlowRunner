// Config
export const AUTOCONNECT_NEW_NODES = true;

// Colores (coinciden con estilos PwC)
export const COLOR_EDGE = '#FF6600';              // naranja PwC
export const COLOR_EDGE_HALO = 'rgba(255,102,0,0.12)';

// Títulos por categoría mejorados (más amigables para usuarios finales)
export const CAT_TITLES = {
  // Flujo principal
  inicio: '🚀 Inicio & Configuración',
  navegacion: '🌐 Navegación Web',
  logica: '🔄 Control y Decisiones',
  finalizacion: '🏁 Finalización',
  
  // Operaciones de datos
  lectura: '📖 Leer Información',
  escritura: '💾 Guardar Información', 
  archivos: '📁 Gestión de Archivos',
  datos: '📊 Procesar Datos',
  
  // Interacción y sistema
  dialogos: '💬 Preguntar al Usuario',
  sistema: '⚙️ Herramientas del Sistema',
  utilidades: '🔧 Funciones Útiles'
};

// Orden de visualización optimizado para flujo de trabajo lógico
export const CATEGORY_ORDER = [
  'inicio', 'navegacion', 'lectura', 'datos', 
  'logica', 'escritura', 'archivos', 
  'dialogos', 'sistema', 'utilidades', 'finalizacion'
];
