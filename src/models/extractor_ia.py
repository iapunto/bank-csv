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
estructurados de vuelta, utilizando los modelos Pydantic definidos en data_models.py
"""

import google.generativeai as genai
import configparser
import logging
from typing import List, Optional

# Importamos nuestros modelos de datos definidos en el archivo anterior.
from src.model.data_models import Transaccion, ExtractoBancario

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExtractorIA:
    """
    Clase que encapsula la lógica para extraer transacciones de un PDF
    utilizando la API de Google Gemini.
    """

    def __init__(self, config_path: str = 'config/settings.ini'):
        """
        Inicializa el extractor. Lee la clave de API desde el archivo de
        configuración y configura el modelo de Gemini.
        """
        try:
            config = configparser.ConfigParser()
            config.read(config_path)
            api_key = config['API']['GEMINI_API_KEY']

            if not api_key or api_key == 'TU_API_KEY_AQUI':
                raise ValueError(
                    "La clave de API de Gemini no ha sido configurada en config/settings.ini")

            genai.configure(api_key=api_key)

            # Seleccionamos el modelo. 'gemini-1.5-flash' es una opción rápida y económica.
            # 'gemini-1.5-pro' es más potente para documentos complejos.
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash-latest")

        except (KeyError, FileNotFoundError) as e:
            logger.error(f"Error de configuración: {e}")
            raise ConnectionError(
                f"Error: No se pudo encontrar o leer el archivo de configuración en '{config_path}'. "
                f"Asegúrate de que existe y tiene el formato correcto.")
        except Exception as e:
            # Captura cualquier otro error durante la inicialización
            logger.error(f"Error inesperado durante la inicialización: {e}")
            raise ConnectionError(
                f"Ocurrió un error al configurar la API de Gemini: {e}")

    def extraer_transacciones_de_pdf(self, pdf_path: str) -> Optional[List[Transaccion]]:
        """
        Procesa un archivo PDF, extrae las transacciones y las devuelve como una
        lista de objetos Transaccion.

        Args:
            pdf_path: La ruta al archivo PDF que se va a procesar.

        Returns:
            Una lista de objetos Transaccion si la extracción es exitosa,
            o None si ocurre un error.
        """
        logger.info(f"Iniciando procesamiento del archivo: {pdf_path}")

        try:
            # 1. Subir el archivo a la API de Gemini.
            # La API procesa archivos subidos temporalmente (duran 48h).
            pdf_file = genai.upload_file(
                path=pdf_path, mime_type="application/pdf")
            logger.info("Archivo PDF subido exitosamente a la API.")

            # 2. Crear el prompt (instrucción) para la IA.
            # Este es un paso crucial. Un prompt claro y detallado mejora la precisión.
            prompt = """
            Analiza el siguiente documento PDF, que es un extracto bancario.
            Tu tarea es extraer única y exclusivamente las líneas de transacción de la tabla de movimientos.

            Ignora por completo cualquier otra información como:
            - Cabeceras de página (nombre del banco, número de página, etc.).
            - Pies de página.
            - Saldos resumidos, saldos iniciales o finales.
            - Publicidad o información de contacto.

            Para cada transacción, extrae la fecha, la descripción y los importes de débito o crédito.
            Es muy importante que estandarices todas las fechas al formato final 'dd-mm-aaaa'.
            """

            # 3. Realizar la llamada a la API con el prompt y el esquema de respuesta.
            logger.info(
                "Enviando solicitud a Gemini para extracción de datos...")
            response = self.model.generate_content(
                [prompt, pdf_file],
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                    # ¡Aquí le decimos a la IA el formato exacto que queremos!
                    response_schema=ExtractoBancario
                )
            )
            logger.info("Respuesta recibida de Gemini.")

            # 4. La biblioteca de Google parsea automáticamente la respuesta JSON
            # en nuestro objeto Pydantic 'ExtractoBancario'.
            extracto_bancario_obj: ExtractoBancario = response.candidates[0].content.parts[0].text

            return extracto_bancario_obj.transacciones

        except Exception as e:
            logger.error(f"Error durante la extracción de datos: {e}")
            return None
