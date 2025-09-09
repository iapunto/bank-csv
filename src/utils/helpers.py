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

def get_icon_path() -> str:
    """
    Obtiene la ruta al archivo de icono, manejando el empaquetado de PyInstaller.
    Busca un archivo .ico y, si no lo encuentra, un .png.

    Returns:
        La ruta absoluta al archivo de icono, o una cadena vacía si no se encuentra.
    """
    # Lista de posibles nombres de icono en orden de preferencia
    possible_icons = ["images/icono.ico", "images/icono.png"]

    for icon in possible_icons:
        try:
            # Usamos resource_path para obtener la ruta correcta
            path = resource_path(os.path.join("assets", icon))
            if os.path.exists(path):
                return path
        except Exception:
            # Si hay algún error, simplemente probamos el siguiente
            continue
            
    return ""  # Retorna una cadena vacía si no se encuentra ningún icono
