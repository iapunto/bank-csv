# -*- coding: utf-8 -*-
"""
Fichero: main.py
Proyecto: Extractor de Movimientos Bancarios con IA

Desarrollado por: IA Punto Soluciones Tecnológicas
Para: Industrias Pico
Responsable: MEng Sergio Rondón
Fecha de Creación: 03/09/2025

Descripción:
Este es el punto de entrada principal para la aplicación. Su función es
instanciar la Vista (MainWindow) y el Controlador (AppController),
conectarlos y iniciar el bucle principal de la interfaz gráfica.
"""

import sys
import os

# --- INICIO: Parche para PyInstaller ---
# Determinar la ruta base, ya sea en desarrollo o empaquetado
if getattr(sys, 'frozen', False):
    # Si está empaquetado, la base es el directorio del .exe
    base_path = os.path.dirname(sys.executable)
else:
    # Si está en desarrollo, la base es el directorio del script main.py
    base_path = os.path.dirname(os.path.abspath(__file__))

# Añadir la ruta base al sys.path para que encuentre el paquete 'src'
sys.path.insert(0, base_path)
# --- FIN: Parche para PyInstaller ---

import logging
import traceback

# Cambiamos las importaciones para que sean más robustas con PyInstaller
from src import MainWindow, AppController

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


def main():
    """
    Función principal que construye y ejecuta la aplicación.
    """
    try:
        logger.info("Iniciando aplicación Extractor de Movimientos Bancarios")

        # 1. Crear una instancia de la Vista (la ventana principal).
        logger.info("Creando ventana principal...")
        view = MainWindow(controller=None)

        # 2. Crear una instancia del Controlador y pasarle la Vista.
        logger.info("Creando controlador principal...")
        controller = AppController(view)

        # 3. Asignar el controlador a la Vista.
        logger.info("Conectando vista y controlador...")
        view.controller = controller

        # 4. Iniciar la aplicación.
        logger.info("Iniciando bucle principal de la aplicación...")
        view.run()

    except ImportError as e:
        # Error de importación (módulos faltantes)
        error_msg = f"Error de importación: {e}"
        logger.error(error_msg)
        print(f"Error fatal: {error_msg}", file=sys.stderr)
        print("Asegúrate de que todas las dependencias estén instaladas:",
              file=sys.stderr)
        print("pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    except FileNotFoundError as e:
        # Error de archivo de configuración
        error_msg = f"Archivo de configuración no encontrado: {e}"
        logger.error(error_msg)
        print(f"Error fatal: {error_msg}", file=sys.stderr)
        print("Verifica que el archivo config/settings.ini existe y contiene tu API key", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        # Captura de errores inesperados al iniciar la aplicación.
        error_msg = f"Error fatal al iniciar la aplicación: {e}"
        logger.error(error_msg)
        logger.error(f"Traceback completo: {traceback.format_exc()}")
        print(f"Error fatal: {error_msg}", file=sys.stderr)
        print("Revisa el archivo app.log para más detalles", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


# --- FIN DEL ARCHIVO ---
