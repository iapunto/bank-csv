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
        self.geometry("500x300")  # Aumentamos un poco la altura
        self.resizable(False, False)

        # Configurar el tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # --- Creación del sistema de pestañas ---
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(pady=10, padx=10, fill="both", expand=True)

        self.tab_view.add("Extractor")
        self.tab_view.add("Configuración")

        # --- Pestaña de Extracción ---
        self._crear_widgets_extractor(self.tab_view.tab("Extractor"))

        # --- Pestaña de Configuración ---
        self._crear_widgets_configuracion(self.tab_view.tab("Configuración"))

        # --- Barra de estado en la parte inferior ---
        self.status_bar = ctk.CTkLabel(self, text="Listo", anchor="w")
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=5)
        self.default_status_color = self.status_bar.cget("text_color")

        logger.info("Ventana principal inicializada correctamente")

    def _crear_widgets_extractor(self, tab):
        """Crea los widgets para la pestaña de extracción."""
        # Frame principal para organizar los widgets
        extractor_frame = ctk.CTkFrame(tab)
        extractor_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # 1. Botón para seleccionar el archivo PDF
        self.select_pdf_button = ctk.CTkButton(
            extractor_frame,
            text="Seleccionar Archivo PDF",
            command=self._on_select_pdf_click
        )
        self.select_pdf_button.pack(pady=10, padx=10)

        # 2. Etiqueta para mostrar el nombre del archivo seleccionado
        self.file_path_label = ctk.CTkLabel(
            extractor_frame,
            text="Ningún archivo seleccionado",
            wraplength=450
        )
        self.file_path_label.pack(pady=5, padx=10)

        # 3. Botón para iniciar el proceso de generación del CSV
        self.generate_csv_button = ctk.CTkButton(
            extractor_frame,
            text="Generar CSV",
            command=self._on_generate_csv_click,
            state="disabled"
        )
        self.generate_csv_button.pack(pady=10, padx=10)

    def _crear_widgets_configuracion(self, tab):
        """Crea los widgets para la pestaña de configuración."""
        config_frame = ctk.CTkFrame(tab)
        config_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # 1. Etiqueta para el campo de la API Key
        api_key_label = ctk.CTkLabel(config_frame, text="Clave API de Google Gemini:")
        api_key_label.pack(pady=(0, 5), padx=10, anchor="w")

        # 2. Campo de texto para la API Key
        self.api_key_entry = ctk.CTkEntry(config_frame, width=400, show="*")
        self.api_key_entry.pack(pady=5, padx=10, fill="x")
        if self.controller:
            current_key = self.controller.get_api_key()
            if current_key not in ["No encontrada", "Error de lectura"]:
                self.api_key_entry.insert(0, current_key)

        # 3. Botón para guardar la API Key
        self.save_api_key_button = ctk.CTkButton(
            config_frame,
            text="Guardar Clave",
            command=self._on_save_api_key_click
        )
        self.save_api_key_button.pack(pady=20, padx=10)

    def _on_save_api_key_click(self):
        """Maneja el clic en el botón de guardar API Key."""
        if self.controller:
            new_key = self.api_key_entry.get()
            self.controller.save_api_key(new_key)

    def _on_select_pdf_click(self):
        """Maneja el clic en el botón de seleccionar PDF."""
        if self.controller:
            self.controller.seleccionar_archivo_pdf()

    def _on_generate_csv_click(self):
        """Maneja el clic en el botón de generar CSV."""
        if self.controller:
            self.controller.generar_csv()

    def actualizar_ruta_archivo(self, ruta: str):
        """Actualiza la etiqueta de la ruta del archivo."""
        if ruta:
            nombre_archivo = os.path.basename(ruta)
            self.file_path_label.configure(text=f"Archivo: {nombre_archivo}")
            self.generate_csv_button.configure(state="normal")
        else:
            self.file_path_label.configure(text="Ningún archivo seleccionado")
            self.generate_csv_button.configure(state="disabled")

    def actualizar_barra_estado(self, mensaje: str, es_error: bool = False):
        """Actualiza el texto y color de la barra de estado."""
        self.status_bar.configure(text=mensaje)
        self.status_bar.configure(text_color="red" if es_error else self.default_status_color)

    def run(self):
        """Inicia el bucle principal de la aplicación."""
        self.mainloop()
