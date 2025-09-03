# -*- coding: utf-8 -*-
"""
Paquete de configuración para el Extractor de Movimientos Bancarios con IA.
"""

from .logging_config import setup_logging, get_logger, log_function_call

__all__ = [
    'setup_logging',
    'get_logger',
    'log_function_call'
]
