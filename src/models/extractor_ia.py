# -*- coding: utf-8 -*-
"""
Fichero: extractor_ia.py
Proyecto: Extractor de Movimientos Bancarios con IA

Desarrollado por: IA Punto Soluciones Tecnológicas
Para: Industrias Pico
Responsable: MEng Sergio Rondón
Fecha de Creación: 03/09/2025

Descripción:
Este módulo contiene la clase principal que interactúa con la API de Google Gemini.
Es responsable de enviar el archivo PDF y el prompt, y de recibir los datos
estructurados de vuelta, utilizando los modelos Pydantic definidos en data_models.py.
"""

import configparser
import logging
import os
import tempfile
from typing import List, Optional

import google.generativeai as genai
from PyPDF2 import PdfReader, PdfWriter

# CORRECCIÓN 2: Usar una ruta de importación absoluta para evitar problemas al ejecutar desde main.py.
from src.models.data_models import ExtractoBancario, Transaccion

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ExtractorIA:
    """
    Clase que encapsula la lógica para extraer transacciones de un PDF
    utilizando la API de Google Gemini.
    """

    def __init__(self, config_path: str = "config/settings.ini"):
        """
        Inicializa el extractor. Lee la clave de API desde el archivo de
        configuración y configura el modelo de Gemini.
        """
        try:
            config = configparser.ConfigParser()
            config.read(config_path)
            api_key = config["API"]["gemini_api_key"]
            model_name = config["API"]["gemini_model"]

            if not api_key or api_key == "TU_API_KEY_AQUI":
                raise ValueError(
                    "La clave de API de Gemini no ha sido configurada en config/settings.ini"
                )

            genai.configure(api_key=api_key)

            logger.info(f"Usando el modelo de Gemini: {model_name}")
            self.model = genai.GenerativeModel(model_name=model_name)

        except (KeyError, FileNotFoundError) as e:
            logger.error(f"Error de configuración: {e}")
            raise ConnectionError(
                f"Error: No se pudo encontrar o leer el archivo de configuración en \'{config_path}\'. "
                f"Asegúrate de que existe y tiene el formato correcto."
            )
        except Exception as e:
            # Captura cualquier otro error durante la inicialización
            logger.error(f"Error inesperado durante la inicialización: {e}")
            raise ConnectionError(
                f"Ocurrió un error al configurar la API de Gemini: {e}"
            )

    def _split_pdf_into_pages(self, pdf_path: str, temp_dir: str) -> List[str]:
        """
        Divide un archivo PDF en páginas individuales y las guarda como archivos temporales.
        """
        output_paths = []
        try:
            reader = PdfReader(pdf_path)
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                temp_page_path = os.path.join(temp_dir, f"page_{i + 1}.pdf")
                with open(temp_page_path, "wb") as output_pdf:
                    writer.write(output_pdf)
                output_paths.append(temp_page_path)
            logger.info(f"PDF dividido en {len(output_paths)} páginas temporales.")
        except Exception as e:
            logger.error(f"Error al dividir el PDF: {e}", exc_info=True)
            raise
        return output_paths

    def extraer_transacciones_de_pdf(
        self, pdf_path: str
    ) -> Optional[List[Transaccion]]:
        """
        Procesa un archivo PDF, extrayendo transacciones página por página
        utilizando la API de Google Gemini.

        Args:
            pdf_path: La ruta al archivo PDF que se va a procesar.

        Returns:
            Una lista de objetos Transaccion si la extracción es exitosa,
            o None si ocurre un error.
        """
        logger.info(f"Iniciando procesamiento del archivo: {pdf_path}")
        all_transactions: List[Transaccion] = []
        temp_dir = None

        try:
            # Crear un directorio temporal para las páginas del PDF
            temp_dir = tempfile.mkdtemp()
            logger.info(f"Directorio temporal creado: {temp_dir}")

            # Dividir el PDF en páginas individuales
            page_paths = self._split_pdf_into_pages(pdf_path, temp_dir)

            if not page_paths:
                logger.warning("No se pudieron dividir páginas del PDF.")
                return None

            for i, page_path in enumerate(page_paths):
                logger.info(f"Procesando página {i + 1}/{len(page_paths)}: {page_path}")

                # 1. Subir la página a la API de Gemini.
                pdf_file = genai.upload_file(path=page_path, mime_type="application/pdf")
                logger.info(f"Página {i + 1} subida. ID: {pdf_file.name}")

                # 2. Crear el prompt (instrucción) para la IA.
                prompt = f"""
                Analiza el siguiente documento PDF, que es la página {i + 1} de un extracto bancario.
                Tu tarea es extraer única y exclusivamente las líneas de transacción de la tabla de movimientos
                presentes en ESTA PÁGINA.

                Ignora por completo cualquier otra información como:
                - Cabeceras de página (nombre del banco, número de página, etc.).
                - Pies de página.
                - Saldos resumidos, saldos iniciales o finales.
                - Publicidad o información de contacto.

                Para cada transacción, extrae la fecha, la descripción y los importes de débito o crédito.
                Es muy importante que estandarices todas las fechas al formato final 'dd-mm-aaaa'.
                Si una fecha solo tiene día y mes, infiere el año del contexto del documento.

                Devuelve el resultado como un único objeto JSON que contenga una clave "transacciones",
                cuyo valor sea una lista de objetos JSON, donde cada objeto represente una transacción.
                Asegúrate de que el JSON esté bien formado.
                """

                logger.info(f"Enviando solicitud a Gemini para página {i + 1}...")
                response = self.model.generate_content(
                    [prompt, pdf_file],
                    generation_config={
                        "response_mime_type": "application/json",
                    },
                )
                logger.info(f"Respuesta recibida de Gemini para página {i + 1}.")

                # Parsear la respuesta JSON manualmente con Pydantic.
                try:
                    extracto_bancario_obj = ExtractoBancario.model_validate_json(response.text)
                except Exception as parse_error:
                    logger.error(f"Página {i + 1}: Error al parsear la respuesta JSON: {parse_error}", exc_info=True)
                    logger.warning(f"Página {i + 1}: Respuesta de texto de la IA que causó el error: {response.text}")
                    continue # Skip to the next page if parsing fails
                
                if extracto_bancario_obj and extracto_bancario_obj.transacciones:
                    logger.info(f"Página {i + 1}: Se extrajeron {len(extracto_bancario_obj.transacciones)} transacciones.")
                    all_transactions.extend(extracto_bancario_obj.transacciones)
                else:
                    logger.warning(f"Página {i + 1}: La IA no devolvió transacciones o la lista estaba vacía.")
                    try:
                        logger.warning(f"Página {i + 1}: Respuesta de texto de la IA: {response.text}")
                    except Exception:
                        pass # Ignore if text is not available

            logger.info(f"Extracción completada. Total de transacciones: {len(all_transactions)}")
            return all_transactions

        except Exception as e:
            logger.error(f"Error crítico durante la extracción de datos: {e}", exc_info=True)
            return None
        finally:
            # Limpiar archivos temporales
            if temp_dir and os.path.exists(temp_dir):
                for f in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, f))
                os.rmdir(temp_dir)
                logger.info(f"Directorio temporal {temp_dir} eliminado.")
