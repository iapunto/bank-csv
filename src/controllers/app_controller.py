# -*- coding: utf-8 -*-
"""
Fichero: app_controller.py
Proyecto: Extractor de Movimientos Bancarios con IA

Desarrollado por: IA Punto Soluciones Tecnológicas
Para: Industrias Pico
Responsable: MEng Sergio Rondón
Fecha de Creación: 03/09/2025

Descripción:
Este módulo contiene la clase AppController, que actúa como el intermediario
entre la Vista (MainWindow) y el Modelo (ExtractorIA, csv_writer).
Maneja la lógica de la aplicación y responde a las interacciones del usuario.
"""

import os
import logging
import configparser
from tkinter import filedialog

# Importamos las clases y funciones necesarias de nuestros otros módulos
from src.models.extractor_ia import ExtractorIA
from src.models.csv_writer import escribir_transacciones_a_csv
from src.views.main_window import MainWindow
from src.utils.helpers import resource_path

# Configurar logging
logger = logging.getLogger(__name__)


class AppController:
    """
    Controlador principal de la aplicación.
    """

    def __init__(self, view: MainWindow):
        """
        Inicializa el controlador.

        Args:
            view: La instancia de la ventana principal (la Vista).
        """
        self.view = view
        self.selected_pdf_path = None
        self.config_path = resource_path("config/settings.ini")
        self.config = configparser.ConfigParser()

        try:
            # Inicializamos el Modelo (el extractor de IA) con la ruta correcta
            self.extractor = ExtractorIA(config_path=self.config_path)
            logger.info("Extractor de IA inicializado correctamente")
        except (ConnectionError, FileNotFoundError) as e:
            # Si hay un error al iniciar (ej. no hay API key), lo mostramos en la vista
            logger.error(f"Error al inicializar el extractor: {e}")
            self.view.actualizar_barra_estado(str(e), es_error=True)
            self.extractor = None

    def get_api_key(self) -> str:
        """Lee la clave de API desde el archivo de configuración."""
        try:
            self.config.read(self.config_path)
            return self.config.get('API', 'GEMINI_API_KEY', fallback='No encontrada')
        except Exception as e:
            logger.error(f"Error al leer la API Key: {e}")
            return "Error de lectura"

    def save_api_key(self, api_key: str):
        """Guarda la nueva clave de API en el archivo de configuración."""
        try:
            self.config.read(self.config_path)
            if not self.config.has_section('API'):
                self.config.add_section('API')
            self.config.set('API', 'GEMINI_API_KEY', api_key)
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
            
            logger.info("API Key guardada correctamente.")
            self.view.actualizar_barra_estado("API Key guardada correctamente.", es_error=False)
            
            # Re-inicializar el extractor con la nueva clave
            self.extractor = ExtractorIA(config_path=self.config_path)
            logger.info("Extractor de IA reinicializado con la nueva clave.")

        except Exception as e:
            logger.error(f"Error al guardar la API Key: {e}")
            self.view.actualizar_barra_estado(f"Error al guardar la API Key: {e}", es_error=True)

    def seleccionar_archivo_pdf(self):
        """
        Abre un diálogo para que el usuario seleccione un archivo PDF.
        Actualiza la vista con la ruta del archivo seleccionado.
        """
        # Abrir el explorador de archivos para seleccionar un PDF
        filepath = filedialog.askopenfilename(
            title="Seleccionar extracto bancario",
            filetypes=(("Archivos PDF", "*.pdf"),
                       ("Todos los archivos", "*.*"))
        )

        if filepath:
            self.selected_pdf_path = filepath
            self.view.actualizar_ruta_archivo(self.selected_pdf_path)
            self.view.actualizar_barra_estado(
                "Archivo cargado. Listo para generar CSV.")
            logger.info(f"Archivo PDF seleccionado: {filepath}")
        else:
            # Si el usuario cancela la selección
            self.selected_pdf_path = None
            self.view.actualizar_ruta_archivo(None)
            logger.info("Selección de archivo cancelada por el usuario")

    def generar_csv(self):
        """
        Orquesta el proceso completo de extracción y generación de CSV.
        """
        if not self.selected_pdf_path:
            self.view.actualizar_barra_estado(
                "Error: Por favor, selecciona un archivo PDF primero.", es_error=True)
            return

        if not self.extractor:
            self.view.actualizar_barra_estado(
                "Error: El extractor de IA no está configurado. Revisa la API Key.", es_error=True)
            return

        # 1. Actualizar la vista para informar al usuario
        self.view.actualizar_barra_estado(
            "Procesando... Contactando a la IA. Esto puede tardar un momento.")
        self.view.update_idletasks()  # Forzar actualización de la GUI

        # 2. Llamar al Modelo para extraer los datos
        logger.info("Iniciando extracción de transacciones del PDF")
        transacciones = self.extractor.extraer_transacciones_de_pdf(
            self.selected_pdf_path)

        # 3. Verificar el resultado de la extracción
        if not transacciones:
            self.view.actualizar_barra_estado(
                "Error: No se pudieron extraer transacciones del PDF.", es_error=True)
            logger.error("No se pudieron extraer transacciones del PDF")
            return

        # 4. Pedir al usuario dónde guardar el archivo CSV
        # Sugerir un nombre de archivo de salida basado en el de entrada
        input_filename = os.path.basename(self.selected_pdf_path)
        output_suggestion = os.path.splitext(
            input_filename)[0] + "_movimientos.csv"

        output_path = filedialog.asksaveasfilename(
            title="Guardar archivo CSV",
            initialfile=output_suggestion,
            defaultextension=".csv",
            filetypes=(("Archivos CSV", "*.csv"),)
        )

        if not output_path:
            self.view.actualizar_barra_estado(
                "Proceso cancelado por el usuario.")
            logger.info("Guardado de archivo CSV cancelado por el usuario")
            return

        # 5. Llamar al Modelo para escribir el archivo CSV
        logger.info(f"Escribiendo archivo CSV en: {output_path}")
        exito = escribir_transacciones_a_csv(transacciones, output_path)

        # 6. Informar al usuario del resultado final
        if exito:
            self.view.actualizar_barra_estado(
                f"¡Éxito! Archivo CSV guardado en: {os.path.basename(output_path)}")
            logger.info(f"Archivo CSV generado exitosamente en: {output_path}")
        else:
            self.view.actualizar_barra_estado(
                "Error: No se pudo escribir el archivo CSV.", es_error=True)
            logger.error(f"Error al escribir el archivo CSV en: {output_path}")
