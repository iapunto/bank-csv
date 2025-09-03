# -*- coding: utf-8 -*-
"""
Paquete de utilidades para el Extractor de Movimientos Bancarios con IA.
"""

from .error_handler import (
    AppError,
    ConfigurationError,
    APIError,
    FileProcessingError,
    handle_errors,
    safe_execute,
    validate_file_path,
    format_error_message,
    log_error_summary
)

__all__ = [
    'AppError',
    'ConfigurationError',
    'APIError',
    'FileProcessingError',
    'handle_errors',
    'safe_execute',
    'validate_file_path',
    'format_error_message',
    'log_error_summary'
]
