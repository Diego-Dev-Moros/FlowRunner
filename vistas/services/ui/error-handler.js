/**
 * 🚨 Frontend Error Handler
 * Maneja errores del frontend y los envía al sistema de logging
 */

import toast from './toast.js';

class FrontendErrorHandler {
  constructor() {
    this.setupGlobalErrorHandlers();
    this.setupConsoleInterception();
  }

  setupGlobalErrorHandlers() {
    // Errores JavaScript globales
    window.addEventListener('error', (event) => {
      const error = {
        type: 'javascript_error',
        message: event.message,
        filename: event.filename,
        line: event.lineno,
        column: event.colno,
        stack: event.error?.stack,
        timestamp: new Date().toISOString(),
        url: window.location.href
      };
      
      this.logError(error);
      this.showUserNotification('Error JavaScript', event.message);
    });

    // Errores de promesas no manejadas
    window.addEventListener('unhandledrejection', (event) => {
      const error = {
        type: 'unhandled_promise_rejection',
        message: event.reason?.message || event.reason,
        stack: event.reason?.stack,
        timestamp: new Date().toISOString(),
        url: window.location.href
      };
      
      this.logError(error);
      this.showUserNotification('Error de Promesa', 'Error no manejado en operación asíncrona');
      
      // Prevenir que aparezca en la consola del navegador
      event.preventDefault();
    });

    // Errores de recursos (imágenes, scripts, etc.)
    window.addEventListener('error', (event) => {
      if (event.target !== window) {
        const error = {
          type: 'resource_error',
          resource: event.target.tagName,
          source: event.target.src || event.target.href,
          message: `Failed to load ${event.target.tagName.toLowerCase()}`,
          timestamp: new Date().toISOString(),
          url: window.location.href
        };
        
        this.logError(error);
        
        // Solo notificar si no es el favicon
        if (!error.source.includes('favicon')) {
          this.showUserNotification('Recurso no encontrado', `No se pudo cargar: ${error.source}`);
        }
      }
    }, true);
  }

  setupConsoleInterception() {
    // Interceptar console.error para logging
    const originalError = console.error;
    console.error = (...args) => {
      const error = {
        type: 'console_error',
        message: args.join(' '),
        timestamp: new Date().toISOString(),
        url: window.location.href,
        stack: (new Error()).stack
      };
      
      this.logError(error);
      originalError.apply(console, args);
    };

    // Interceptar console.warn para logging
    const originalWarn = console.warn;
    console.warn = (...args) => {
      const warning = {
        type: 'console_warning',
        message: args.join(' '),
        timestamp: new Date().toISOString(),
        url: window.location.href
      };
      
      this.logWarning(warning);
      originalWarn.apply(console, args);
    };
  }

  async logError(error) {
    try {
      // Intentar enviar al backend
      if (window.eel && typeof window.eel.log_frontend_error === 'function') {
        await window.eel.log_frontend_error(error)();
      } else {
        // Fallback: almacenar localmente
        this.storeLocalError(error);
      }
    } catch (e) {
      console.warn('No se pudo enviar error al backend:', e);
      this.storeLocalError(error);
    }
  }

  async logWarning(warning) {
    try {
      if (window.eel && typeof window.eel.log_frontend_warning === 'function') {
        await window.eel.log_frontend_warning(warning)();
      } else {
        this.storeLocalWarning(warning);
      }
    } catch (e) {
      console.warn('No se pudo enviar warning al backend:', e);
      this.storeLocalWarning(warning);
    }
  }

  storeLocalError(error) {
    const errors = JSON.parse(localStorage.getItem('flowrunner_errors') || '[]');
    errors.push(error);
    
    // Mantener solo los últimos 50 errores
    if (errors.length > 50) {
      errors.splice(0, errors.length - 50);
    }
    
    localStorage.setItem('flowrunner_errors', JSON.stringify(errors));
  }

  storeLocalWarning(warning) {
    const warnings = JSON.parse(localStorage.getItem('flowrunner_warnings') || '[]');
    warnings.push(warning);
    
    // Mantener solo los últimos 50 warnings
    if (warnings.length > 50) {
      warnings.splice(0, warnings.length - 50);
    }
    
    localStorage.setItem('flowrunner_warnings', JSON.stringify(warnings));
  }

  showUserNotification(title, message) {
    // Solo mostrar notificación si no es un error de favicon
    if (message.includes('favicon') || message.includes('404')) {
      return; // Ignorar errores de favicon
    }
    
    toast.error(title, message, {
      duration: 8000,
      closable: true
    });
  }

  // Método para reportar errores manualmente
  reportError(error, context = {}) {
    const errorData = {
      type: 'manual_error',
      message: error.message || error,
      stack: error.stack,
      context: context,
      timestamp: new Date().toISOString(),
      url: window.location.href
    };
    
    this.logError(errorData);
    this.showUserNotification('Error de aplicación', error.message || error);
  }

  // Método para reportar warnings manualmente
  reportWarning(message, context = {}) {
    const warningData = {
      type: 'manual_warning',
      message: message,
      context: context,
      timestamp: new Date().toISOString(),
      url: window.location.href
    };
    
    this.logWarning(warningData);
    toast.warning('Advertencia', message);
  }

  // Obtener errores almacenados localmente
  getLocalErrors() {
    return JSON.parse(localStorage.getItem('flowrunner_errors') || '[]');
  }

  // Limpiar errores locales
  clearLocalErrors() {
    localStorage.removeItem('flowrunner_errors');
    localStorage.removeItem('flowrunner_warnings');
  }
}

// Crear instancia global
window.errorHandler = new FrontendErrorHandler();

// Exportar para uso en módulos
export default window.errorHandler;
