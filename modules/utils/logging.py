# modules/utils/logging.py
"""
Sistema de logging centralizado para FlowRunner.
Maneja logs de usuario, errores y temporales.
"""

import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any
import json


class FlowLogger:
    """
    Logger centralizado para FlowRunner.
    """
    
    _loggers: Dict[str, logging.Logger] = {}
    _handlers_initialized = False
    
    LOG_DIR = "var"
    LOG_FILES = {
        'user': 'user.log',
        'error': 'error.log', 
        'temp': 'temp.log'
    }
    
    @classmethod
    def setup_logging(cls):
        """
        Configura los loggers y handlers.
        """
        if cls._handlers_initialized:
            return
        
        # Crear directorio var si no existe
        os.makedirs(cls.LOG_DIR, exist_ok=True)
        
        # Configurar formato
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Configurar loggers
        for log_type, filename in cls.LOG_FILES.items():
            logger = logging.getLogger(f'flowrunner.{log_type}')
            logger.setLevel(logging.DEBUG)
            
            # Handler para archivo
            file_path = os.path.join(cls.LOG_DIR, filename)
            file_handler = logging.FileHandler(file_path, encoding='utf-8')
            file_handler.setFormatter(formatter)
            
            # Configurar niveles específicos
            if log_type == 'error':
                file_handler.setLevel(logging.ERROR)
            elif log_type == 'temp':
                file_handler.setLevel(logging.DEBUG)
            else:  # user
                file_handler.setLevel(logging.INFO)
            
            logger.addHandler(file_handler)
            cls._loggers[log_type] = logger
        
        cls._handlers_initialized = True
        cls.log_user("Sistema de logging inicializado")
    
    @classmethod
    def log_user(cls, message: str, level: str = "INFO", context: Optional[Dict] = None):
        """
        Log de actividad de usuario.
        """
        cls.setup_logging()
        logger = cls._loggers['user']
        
        # Preparar mensaje con contexto
        if context:
            full_message = f"{message} | Context: {json.dumps(context, ensure_ascii=False)}"
        else:
            full_message = message
        
        if level.upper() == "INFO":
            logger.info(full_message)
        elif level.upper() == "WARNING":
            logger.warning(full_message)
        elif level.upper() == "ERROR":
            logger.error(full_message)
        else:
            logger.debug(full_message)
    
    @classmethod
    def log_error(cls, error: str, exception: Optional[Exception] = None, 
                  action_id: Optional[str] = None, context: Optional[Dict] = None):
        """
        Log de errores.
        """
        cls.setup_logging()
        logger = cls._loggers['error']
        
        # Preparar información del error
        error_info = {
            "error": error,
            "action_id": action_id,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
        
        if exception:
            error_info["exception_type"] = type(exception).__name__
            error_info["exception_message"] = str(exception)
        
        # Log estructurado
        logger.error(json.dumps(error_info, ensure_ascii=False, indent=2))
    
    @classmethod
    def log_temp(cls, message: str, data: Optional[Dict] = None):
        """
        Log temporal para debugging y desarrollo.
        """
        cls.setup_logging()
        logger = cls._loggers['temp']
        
        if data:
            temp_entry = {
                "message": message,
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
            logger.debug(json.dumps(temp_entry, ensure_ascii=False, indent=2))
        else:
            logger.debug(message)
    
    @classmethod
    def log_action_start(cls, action_id: str, params: Dict[str, Any]):
        """
        Log de inicio de acción.
        """
        cls.log_user(f"Iniciando acción: {action_id}", context={"params": params})
    
    @classmethod
    def log_action_end(cls, action_id: str, success: bool, result: Optional[Dict] = None):
        """
        Log de finalización de acción.
        """
        status = "ÉXITO" if success else "ERROR"
        context = {"success": success}
        
        if result:
            context["result"] = result
        
        cls.log_user(f"Acción {action_id} - {status}", context=context)
    
    @classmethod
    def log_flow_start(cls, flow_name: str):
        """
        Log de inicio de flujo.
        """
        cls.log_user(f"=== INICIO DE FLUJO: {flow_name} ===", level="INFO")
    
    @classmethod
    def log_flow_end(cls, flow_name: str, success: bool, duration: Optional[float] = None):
        """
        Log de finalización de flujo.
        """
        status = "COMPLETADO" if success else "FALLIDO"
        context = {"success": success}
        
        if duration is not None:
            context["duration_seconds"] = duration
        
        cls.log_user(f"=== FIN DE FLUJO: {flow_name} - {status} ===", 
                    level="INFO", context=context)
    
    @classmethod
    def clear_temp_log(cls):
        """
        Limpia el log temporal.
        """
        temp_file = os.path.join(cls.LOG_DIR, cls.LOG_FILES['temp'])
        if os.path.exists(temp_file):
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(f"# Temp log limpiado - {datetime.now().isoformat()}\n")
            cls.log_user("Log temporal limpiado")
    
    @classmethod
    def get_recent_logs(cls, log_type: str = 'user', lines: int = 50) -> list:
        """
        Obtiene las últimas líneas de un log.
        """
        if log_type not in cls.LOG_FILES:
            return []
        
        file_path = os.path.join(cls.LOG_DIR, cls.LOG_FILES[log_type])
        
        if not os.path.exists(file_path):
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.readlines()[-lines:]
        except Exception:
            return []


# Alias para uso fácil
logger = FlowLogger
