/**
 * 🍞 Sistema de Notificaciones Toast
 * Sistema moderno de notificaciones con diseño elegante y animaciones
 */

class ToastManager {
  constructor() {
    this.container = null;
    this.toasts = new Map();
    this.init();
  }

  init() {
    // Crear contenedor principal
    this.container = document.createElement('div');
    this.container.id = 'toast-container';
    this.container.className = 'toast-container';
    document.body.appendChild(this.container);

    // Agregar estilos
    if (!document.getElementById('toast-styles')) {
      const style = document.createElement('style');
      style.id = 'toast-styles';
      style.textContent = `
        .toast-container {
          position: fixed;
          top: 20px;
          right: 20px;
          z-index: 10000;
          pointer-events: none;
          display: flex;
          flex-direction: column;
          gap: 8px;
          max-width: 400px;
        }

        .toast {
          background: white;
          border: 1px solid #e0e0e0;
          border-radius: 12px;
          padding: 16px 20px;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
          backdrop-filter: blur(10px);
          pointer-events: auto;
          transform: translateX(400px);
          opacity: 0;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          display: flex;
          align-items: center;
          gap: 12px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          font-size: 14px;
          line-height: 1.4;
          min-height: 48px;
          position: relative;
          overflow: hidden;
        }

        .toast.show {
          transform: translateX(0);
          opacity: 1;
        }

        .toast.hide {
          transform: translateX(400px);
          opacity: 0;
        }

        .toast::before {
          content: '';
          position: absolute;
          left: 0;
          top: 0;
          width: 4px;
          height: 100%;
          background: var(--toast-color);
        }

        .toast-icon {
          font-size: 20px;
          flex-shrink: 0;
          width: 24px;
          height: 24px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .toast-content {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .toast-title {
          font-weight: 600;
          color: #1a1a1a;
          margin: 0;
        }

        .toast-message {
          color: #666;
          margin: 0;
        }

        .toast-close {
          background: none;
          border: none;
          font-size: 18px;
          color: #999;
          cursor: pointer;
          padding: 4px;
          border-radius: 6px;
          transition: all 0.2s;
          flex-shrink: 0;
        }

        .toast-close:hover {
          background: #f0f0f0;
          color: #666;
        }

        /* Tipos de toast */
        .toast.success {
          --toast-color: #10b981;
          border-left-color: #10b981;
        }

        .toast.error {
          --toast-color: #ef4444;
          border-left-color: #ef4444;
        }

        .toast.warning {
          --toast-color: #f59e0b;
          border-left-color: #f59e0b;
        }

        .toast.info {
          --toast-color: #3b82f6;
          border-left-color: #3b82f6;
        }

        .toast.loading {
          --toast-color: #8b5cf6;
          border-left-color: #8b5cf6;
        }

        /* Barra de progreso */
        .toast-progress {
          position: absolute;
          bottom: 0;
          left: 0;
          height: 3px;
          background: var(--toast-color);
          opacity: 0.3;
          transform-origin: left;
          transition: transform linear;
        }

        /* Animación de carga */
        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        .toast.loading .toast-icon {
          animation: spin 1s linear infinite;
        }

        /* Dark theme */
        @media (prefers-color-scheme: dark) {
          .toast {
            background: #2a2a2a;
            border-color: #404040;
            color: #e0e0e0;
          }
          
          .toast-title {
            color: #f0f0f0;
          }
          
          .toast-message {
            color: #b0b0b0;
          }
          
          .toast-close {
            color: #b0b0b0;
          }
          
          .toast-close:hover {
            background: #404040;
            color: #e0e0e0;
          }
        }
      `;
      document.head.appendChild(style);
    }
  }

  show(options = {}) {
    const {
      type = 'info',
      title = '',
      message = '',
      duration = 5000,
      closable = true,
      action = null
    } = options;

    const id = 'toast_' + Date.now() + Math.random().toString(36).substr(2, 9);
    
    // Crear elemento toast
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.setAttribute('data-id', id);

    // Icono basado en tipo
    const icons = {
      success: '✅',
      error: '❌',
      warning: '⚠️',
      info: 'ℹ️',
      loading: '⌛'
    };

    // Construir contenido
    toast.innerHTML = `
      <div class="toast-icon">${icons[type] || icons.info}</div>
      <div class="toast-content">
        ${title ? `<div class="toast-title">${title}</div>` : ''}
        ${message ? `<div class="toast-message">${message}</div>` : ''}
      </div>
      ${closable ? '<button class="toast-close" aria-label="Cerrar">×</button>' : ''}
      ${duration > 0 ? '<div class="toast-progress"></div>' : ''}
    `;

    // Agregar al contenedor
    this.container.appendChild(toast);
    this.toasts.set(id, toast);

    // Event listeners
    if (closable) {
      const closeBtn = toast.querySelector('.toast-close');
      closeBtn.addEventListener('click', () => this.hide(id));
    }

    if (action) {
      toast.style.cursor = 'pointer';
      toast.addEventListener('click', (e) => {
        if (!e.target.closest('.toast-close')) {
          action();
        }
      });
    }

    // Mostrar con animación
    requestAnimationFrame(() => {
      toast.classList.add('show');
    });

    // Barra de progreso y auto-hide
    if (duration > 0) {
      const progress = toast.querySelector('.toast-progress');
      if (progress) {
        progress.style.transform = 'scaleX(1)';
        progress.style.transition = `transform ${duration}ms linear`;
        
        setTimeout(() => {
          progress.style.transform = 'scaleX(0)';
        }, 10);
      }

      setTimeout(() => {
        this.hide(id);
      }, duration);
    }

    return id;
  }

  hide(id) {
    const toast = this.toasts.get(id);
    if (!toast) return;

    toast.classList.add('hide');
    
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
      this.toasts.delete(id);
    }, 300);
  }

  hideAll() {
    this.toasts.forEach((toast, id) => {
      this.hide(id);
    });
  }

  // Métodos de conveniencia
  success(title, message, options = {}) {
    return this.show({ ...options, type: 'success', title, message });
  }

  error(title, message, options = {}) {
    return this.show({ ...options, type: 'error', title, message, duration: 8000 });
  }

  warning(title, message, options = {}) {
    return this.show({ ...options, type: 'warning', title, message, duration: 6000 });
  }

  info(title, message, options = {}) {
    return this.show({ ...options, type: 'info', title, message });
  }

  loading(title, message, options = {}) {
    return this.show({ ...options, type: 'loading', title, message, duration: 0 });
  }

  // Actualizar toast existente
  update(id, options = {}) {
    const toast = this.toasts.get(id);
    if (!toast) return;

    const { title, message, type } = options;
    
    if (type) {
      toast.className = `toast ${type} show`;
    }
    
    if (title || message) {
      const titleEl = toast.querySelector('.toast-title');
      const messageEl = toast.querySelector('.toast-message');
      
      if (title && titleEl) titleEl.textContent = title;
      if (message && messageEl) messageEl.textContent = message;
    }
  }
}

// Crear instancia global
window.toast = new ToastManager();

// Exportar para uso en módulos
export default window.toast;
