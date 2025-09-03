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
import logging
import traceback
from src.views.main_window import MainWindow
from src.controllers.app_controller import AppController

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
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
        # Le pasamos 'None' inicialmente porque el controlador aún no existe.
        logger.info("Creando ventana principal...")
        view = MainWindow(controller=None)

        # 2. Crear una instancia del Controlador y pasarle la Vista.
        # Ahora el controlador puede comunicarse con la vista.
        logger.info("Creando controlador principal...")
        controller = AppController(view)

        # 3. Asignar el controlador a la Vista.
        # Ahora la vista puede enviar acciones al controlador (ej. clics de botón).
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
