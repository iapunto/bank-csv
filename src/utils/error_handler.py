# -*- coding: utf-8 -*-
"""
Fichero: error_handler.py
Proyecto: Extractor de Movimientos Bancarios con IA

Desarrollado por: IA Punto Soluciones Tecnológicas
Para: Industrias Pico
Responsable: MEng Sergio Rondón
Fecha de Creación: 03/09/2025

Descripción:
Módulo de utilidades para manejo centralizado de errores y excepciones.
"""

import logging
import traceback
from typing import Optional, Callable, Any
from functools import wraps


class AppError(Exception):
    """Clase base para errores personalizados de la aplicación."""
    
    def __init__(self, message: str, error_code: Optional[str] = None, 
                 original_error: Optional[Exception] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.original_error = original_error


class ConfigurationError(AppError):
    """Error relacionado con la configuración de la aplicación."""
    pass


class APIError(AppError):
    """Error relacionado con la API de Gemini."""
    pass


class FileProcessingError(AppError):
    """Error relacionado con el procesamiento de archivos."""
    pass


def handle_errors(error_handler: Optional[Callable] = None, 
                  log_error: bool = True, 
                  reraise: bool = True):
    """
    Decorador para manejo centralizado de errores.
    
    Args:
        error_handler: Función personalizada para manejar errores
        log_error: Si se debe registrar el error
        reraise: Si se debe relanzar la excepción
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger = logging.getLogger(func.__module__)
                
                if log_error:
                    logger.error(f"Error en {func.__name__}: {e}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                
                if error_handler:
                    try:
                        error_handler(e, func.__name__, args, kwargs)
                    except Exception as handler_error:
                        logger.error(f"Error en el manejador de errores: {handler_error}")
                
                if reraise:
                    raise
                
                return None
        return wrapper
    return decorator


def safe_execute(func: Callable, *args, default_return: Any = None, 
                error_message: str = "Error durante la ejecución", **kwargs) -> Any:
    """
    Ejecuta una función de forma segura, capturando cualquier error.
    
    Args:
        func: Función a ejecutar
        *args: Argumentos posicionales
        default_return: Valor a retornar en caso de error
        error_message: Mensaje de error personalizado
        **kwargs: Argumentos de palabra clave
        
    Returns:
        Resultado de la función o default_return en caso de error
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"{error_message}: {e}")
        return default_return


def validate_file_path(file_path: str, required_extension: Optional[str] = None) -> bool:
    """
    Valida que un archivo existe y tiene la extensión correcta.
    
    Args:
        file_path: Ruta del archivo a validar
        required_extension: Extensión requerida (opcional)
        
    Returns:
        True si el archivo es válido, False en caso contrario
    """
    import os
    
    try:
        if not os.path.exists(file_path):
            return False
        
        if not os.path.isfile(file_path):
            return False
        
        if required_extension:
            _, ext = os.path.splitext(file_path)
            if ext.lower() != required_extension.lower():
                return False
        
        return True
        
    except Exception as e:
        logging.getLogger(__name__).error(f"Error validando archivo {file_path}: {e}")
        return False


def format_error_message(error: Exception, context: str = "") -> str:
    """
    Formatea un mensaje de error legible para el usuario.
    
    Args:
        error: Excepción que ocurrió
        context: Contexto adicional del error
        
    Returns:
        Mensaje de error formateado
    """
    if isinstance(error, AppError):
        base_message = error.message
    else:
        base_message = str(error)
    
    if context:
        return f"{context}: {base_message}"
    
    return base_message


def log_error_summary(error: Exception, function_name: str, 
                     additional_info: Optional[dict] = None) -> None:
    """
    Registra un resumen del error para análisis posterior.
    
    Args:
        error: Excepción que ocurrió
        function_name: Nombre de la función donde ocurrió el error
        additional_info: Información adicional del contexto
    """
    logger = logging.getLogger(__name__)
    
    error_summary = {
        'error_type': type(error).__name__,
        'error_message': str(error),
        'function_name': function_name,
        'timestamp': logging.Formatter().formatTime(logging.LogRecord(
            name='', level=0, pathname='', lineno=0, msg='', args=(), exc_info=None
        )),
        'additional_info': additional_info or {}
    }
    
    logger.error(f"Resumen de error: {error_summary}")
