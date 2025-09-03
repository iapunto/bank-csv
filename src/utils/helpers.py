# -*- coding: utf-8 -*-
"""
Fichero: helpers.py
Proyecto: Extractor de Movimientos Bancarios con IA

Desarrollado por: IA Punto Soluciones Tecnológicas
Para: Industrias Pico
Responsable: MEng Sergio Rondón
Fecha de Creación: 03/09/2025

Descripción:
Este módulo proporciona funciones de ayuda para la aplicación, como la resolución
de rutas de recursos para que funcione tanto en desarrollo como en el ejecutable
empaquetado con PyInstaller.
"""

import sys
import os


def resource_path(relative_path: str) -> str:
    """
    Obtiene la ruta absoluta a un recurso, manejando el caso de ejecución
    en un bundle de PyInstaller.

    Args:
        relative_path: La ruta relativa del archivo desde la raíz del proyecto.

    Returns:
        La ruta absoluta y correcta para acceder al recurso.
    """
    try:
        # PyInstaller crea una carpeta temporal y almacena su ruta en _MEIPASS.
        base_path = sys._MEIPASS
    except Exception:
        # Si no se está ejecutando en un bundle, la base es el directorio actual.
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
