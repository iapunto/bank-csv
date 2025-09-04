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
import webbrowser
import toml
import importlib.metadata # Importamos importlib.metadata

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
        self.geometry("500x320")  # Aumentamos un poco la altura
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

        # --- Pie de página (Footer) ---
        self._crear_footer()

        # --- Barra de estado en la parte inferior ---
        self.status_bar = ctk.CTkLabel(self, text="Listo", anchor="w")
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=(0,0))
        self.default_status_color = self.status_bar.cget("text_color")

        logger.info("Ventana principal inicializada correctamente")

    def _crear_widgets_extractor(self, tab):
        """Crea los widgets para la pestaña de extracción."""
        extractor_frame = ctk.CTkFrame(tab)
        extractor_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.select_pdf_button = ctk.CTkButton(
            extractor_frame,
            text="Seleccionar Archivo PDF",
            command=self._on_select_pdf_click
        )
        self.select_pdf_button.pack(pady=10, padx=10)

        self.file_path_label = ctk.CTkLabel(
            extractor_frame,
            text="Ningún archivo seleccionado",
            wraplength=450
        )
        self.file_path_label.pack(pady=5, padx=10)

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

        api_key_label = ctk.CTkLabel(config_frame, text="Clave API de Google Gemini:")
        api_key_label.pack(pady=(0, 5), padx=10, anchor="w")

        self.api_key_entry = ctk.CTkEntry(config_frame, width=400, show="*")
        self.api_key_entry.pack(pady=5, padx=10, fill="x")
        if self.controller:
            current_key = self.controller.get_api_key()
            if current_key not in ["No encontrada", "Error de lectura"]:
                self.api_key_entry.insert(0, current_key)

        self.save_api_key_button = ctk.CTkButton(
            config_frame,
            text="Guardar Clave",
            command=self._on_save_api_key_click
        )
        self.save_api_key_button.pack(pady=20, padx=10)

    def _crear_footer(self):
        """Crea el pie de página con la información de versión y desarrollador."""
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 5))

        # --- Obtener versión ---
        version = "1.2.25" # Versión manual

        version_label = ctk.CTkLabel(footer_frame, text=f"v{version}", font=("Segoe UI", 10))
        version_label.pack(side="left")

        # --- Info Desarrollador ---
        dev_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        dev_frame.pack(side="right")

        dev_label = ctk.CTkLabel(dev_frame, text="Desarrollado por ", font=("Segoe UI", 10))
        dev_label.pack(side="left")

        link_label = ctk.CTkLabel(dev_frame, text="IA Punto", font=("Segoe UI", 10, "underline"), text_color="#60a5fa", cursor="hand2")
        link_label.pack(side="left")
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://iapunto.com"))

        separator_label = ctk.CTkLabel(dev_frame, text=" | ", font=("Segoe UI", 10))
        separator_label.pack(side="left")

        email_label = ctk.CTkLabel(dev_frame, text="Soporte", font=("Segoe UI", 10, "underline"), text_color="#60a5fa", cursor="hand2")
        email_label.pack(side="left")
        email_label.bind("<Button-1>", lambda e: webbrowser.open_new("mailto:desarrollo@iapunto.com"))

    def _on_save_api_key_click(self):
        if self.controller:
            new_key = self.api_key_entry.get()
            self.controller.save_api_key(new_key)

    def _on_select_pdf_click(self):
        if self.controller:
            self.controller.seleccionar_archivo_pdf()

    def _on_generate_csv_click(self):
        if self.controller:
            self.controller.generar_csv()

    def actualizar_ruta_archivo(self, ruta: str):
        if ruta:
            nombre_archivo = os.path.basename(ruta)
            self.file_path_label.configure(text=f"Archivo: {nombre_archivo}")
            self.generate_csv_button.configure(state="normal")
        else:
            self.file_path_label.configure(text="Ningún archivo seleccionado")
            self.generate_csv_button.configure(state="disabled")

    def actualizar_barra_estado(self, mensaje: str, es_error: bool = False):
        self.status_bar.configure(text=mensaje)
        self.status_bar.configure(text_color="red" if es_error else self.default_status_color)

    def run(self):
        self.mainloop()
