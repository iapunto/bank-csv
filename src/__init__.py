# -*- coding: utf-8 -*-
"""
Extractor de Movimientos Bancarios con IA

Un sistema inteligente para extraer y procesar transacciones bancarias
de archivos PDF utilizando la API de Google Gemini.

Desarrollado por: IA Punto Soluciones Tecnológicas
Para: Industrias Pico
Responsable: MEng Sergio Rondón
Fecha de Creación: 03/09/2025
"""

__version__ = "1.0.0"
__author__ = "IA Punto Soluciones Tecnológicas"
__email__ = "sergio.rondon@puntosoluciones.com"

from .models import Transaccion, ExtractoBancario, ExtractorIA, escribir_transacciones_a_csv
from .controllers import AppController
from .views import MainWindow

__all__ = [
    'Transaccion',
    'ExtractoBancario',
    'ExtractorIA',
    'escribir_transacciones_a_csv',
    'AppController',
    'MainWindow'
]
