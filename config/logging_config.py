# -*- coding: utf-8 -*-
"""
Fichero: logging_config.py
Proyecto: Extractor de Movimientos Bancarios con IA

Desarrollado por: IA Punto Soluciones Tecnológicas
Para: Industrias Pico
Responsable: MEng Sergio Rondón
Fecha de Creación: 03/09/2025

Descripción:
Configuración avanzada de logging para la aplicación.
"""

import logging
import logging.handlers
import os
import configparser
from datetime import datetime


def setup_logging(config_path: str = 'config/settings.ini') -> None:
    """
    Configura el sistema de logging de la aplicación.
    
    Args:
        config_path: Ruta al archivo de configuración
    """
    try:
        # Leer configuración
        config = configparser.ConfigParser()
        config.read(config_path)
        
        # Obtener configuración de logging
        log_level = config.get('LOGGING', 'LOG_LEVEL', fallback='INFO')
        log_file = config.get('LOGGING', 'LOG_FILE', fallback='app.log')
        log_encoding = config.get('LOGGING', 'LOG_ENCODING', fallback='utf-8')
        
        # Crear directorio de logs si no existe
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configurar nivel de logging
        level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Configurar formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Configurar handler para archivo con rotación
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=1024*1024,  # 1MB
            backupCount=5,
            encoding=log_encoding
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        
        # Configurar handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        
        # Configurar logger raíz
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        
        # Limpiar handlers existentes
        root_logger.handlers.clear()
        
        # Agregar handlers
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        # Log de inicio
        logger = logging.getLogger(__name__)
        logger.info("Sistema de logging configurado correctamente")
        logger.info(f"Nivel de logging: {log_level}")
        logger.info(f"Archivo de log: {log_file}")
        
    except Exception as e:
        # Fallback a configuración básica si falla la configuración avanzada
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logging.error(f"Error al configurar logging avanzado: {e}")
        logging.info("Usando configuración básica de logging")


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para el módulo especificado.
    
    Args:
        name: Nombre del módulo (generalmente __name__)
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)


def log_function_call(func_name: str, args: tuple = None, kwargs: dict = None):
    """
    Decorador para logging de llamadas a funciones.
    
    Args:
        func_name: Nombre de la función
        args: Argumentos posicionales
        kwargs: Argumentos de palabra clave
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            logger.debug(f"Llamando a {func_name} con args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Función {func_name} completada exitosamente")
                return result
            except Exception as e:
                logger.error(f"Error en función {func_name}: {e}")
                raise
        return wrapper
    return decorator
