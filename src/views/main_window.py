# -*- coding: utf-8 -*-
"""
Fichero: main_window.py
Proyecto: Extractor de Movimientos Bancarios con IA

Desarrollado por: IA Punto Soluciones Tecnológicas
Para: Industrias Pico
Responsable: MEng Sergio Rondón
Fecha de Creación: 03/09/2025

Descripción:
Este módulo define la clase MainWindow, que construye y gestiona la interfaz
gráfica de usuario (GUI) de la aplicación utilizando la biblioteca customtkinter.
La vista es responsable de mostrar los elementos visuales y de delegar las
acciones del usuario al controlador.
"""

import customtkinter as ctk
import os
import logging

# Configurar logging
logger = logging.getLogger(__name__)


class MainWindow(ctk.CTk):
    """
    Clase que representa la ventana principal de la aplicación.
    """

    def __init__(self, controller):
        """
        Inicializa la ventana principal y sus componentes.

        Args:
            controller: Una instancia del AppController que manejará la lógica.
        """
        super().__init__()

        self.controller = controller

        # --- Configuración de la Ventana Principal ---
        self.title("Extractor de Movimientos Bancarios")
        self.geometry("500x250")
        self.resizable(False, False)

        # Configurar el tema (Light, Dark, System)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # --- Creación de Widgets (Componentes de la UI) ---

        # Frame principal para organizar los widgets
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # 1. Botón para seleccionar el archivo PDF
        self.select_pdf_button = ctk.CTkButton(
            main_frame,
            text="Seleccionar Archivo PDF",
            command=self._on_select_pdf_click
        )
        self.select_pdf_button.pack(pady=10, padx=10)

        # 2. Etiqueta para mostrar el nombre del archivo seleccionado
        self.file_path_label = ctk.CTkLabel(
            main_frame,
            text="Ningún archivo seleccionado",
            wraplength=450  # Para que el texto largo no se salga de la ventana
        )
        self.file_path_label.pack(pady=5, padx=10)

        # 3. Botón para iniciar el proceso de generación del CSV
        self.generate_csv_button = ctk.CTkButton(
            main_frame,
            text="Generar CSV",
            command=self._on_generate_csv_click,
            state="disabled"  # Deshabilitado hasta que se seleccione un archivo
        )
        self.generate_csv_button.pack(pady=10, padx=10)

        # 4. Barra de estado en la parte inferior
        self.status_bar = ctk.CTkLabel(
            self,
            text="Listo",
            anchor="w"  # Alinear texto a la izquierda (west)
        )
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=5)

        logger.info("Ventana principal inicializada correctamente")

    def _on_select_pdf_click(self):
        """Maneja el clic en el botón de seleccionar PDF."""
        try:
            if self.controller:
                self.controller.seleccionar_archivo_pdf()
            else:
                logger.warning(
                    "Controlador no disponible para seleccionar archivo PDF")
                self.actualizar_barra_estado(
                    "Error: Controlador no disponible", es_error=True)
        except Exception as e:
            logger.error(f"Error al seleccionar archivo PDF: {e}")
            self.actualizar_barra_estado(f"Error: {str(e)}", es_error=True)

    def _on_generate_csv_click(self):
        """Maneja el clic en el botón de generar CSV."""
        try:
            if self.controller:
                self.controller.generar_csv()
            else:
                logger.warning("Controlador no disponible para generar CSV")
                self.actualizar_barra_estado(
                    "Error: Controlador no disponible", es_error=True)
        except Exception as e:
            logger.error(f"Error al generar CSV: {e}")
            self.actualizar_barra_estado(f"Error: {str(e)}", es_error=True)

    def actualizar_ruta_archivo(self, ruta: str):
        """
        Actualiza la etiqueta que muestra la ruta del archivo y habilita/deshabilita
        el botón de generar CSV.
        """
        try:
            if ruta:
                # Mostramos solo el nombre del archivo, no la ruta completa, para que sea más limpio
                nombre_archivo = os.path.basename(ruta)
                self.file_path_label.configure(
                    text=f"Archivo: {nombre_archivo}")
                self.generate_csv_button.configure(state="normal")
                logger.info(f"Ruta de archivo actualizada: {nombre_archivo}")
            else:
                self.file_path_label.configure(
                    text="Ningún archivo seleccionado")
                self.generate_csv_button.configure(state="disabled")
                logger.info("Ruta de archivo limpiada")
        except Exception as e:
            logger.error(f"Error al actualizar ruta de archivo: {e}")

    def actualizar_barra_estado(self, mensaje: str, es_error: bool = False):
        """
        Actualiza el texto y el color de la barra de estado.
        """
        try:
            self.status_bar.configure(text=mensaje)
            if es_error:
                self.status_bar.configure(text_color="red")
                logger.warning(f"Estado de error: {mensaje}")
            else:
                # Usar el color de texto por defecto del tema
                self.status_bar.configure(
                    text_color=ctk.ThemeManager.theme["text_color"])
                logger.info(f"Estado actualizado: {mensaje}")
        except Exception as e:
            logger.error(f"Error al actualizar barra de estado: {e}")

    def run(self):
        """Inicia el bucle principal de la aplicación para mostrar la ventana."""
        try:
            logger.info("Iniciando bucle principal de la aplicación")
            self.mainloop()
        except Exception as e:
            logger.error(f"Error en el bucle principal: {e}")
            raise
