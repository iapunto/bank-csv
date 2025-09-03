# -*- coding: utf-8 -*-
"""
Fichero: csv_writer.py
Proyecto: Extractor de Movimientos Bancarios con IA

Desarrollado por: IA Punto Soluciones Tecnológicas
Para: Industrias Pico
Responsable: MEng Sergio Rondón
Fecha de Creación: 03/09/2025

Descripción:
Este módulo proporciona la funcionalidad para escribir la lista de transacciones
extraídas en un archivo CSV con un formato estandarizado.
"""

import csv
import logging
from typing import List

# Importamos nuestro modelo de datos para tener una referencia de tipo estricta.
from .data_models import Transaccion

# Configurar logging
logger = logging.getLogger(__name__)


def escribir_transacciones_a_csv(transacciones: List[Transaccion], output_path: str) -> bool:
    """
    Escribe una lista de objetos Transaccion en un archivo CSV.

    Args:
        transacciones: Una lista que contiene los objetos Transaccion extraídos.
        output_path: La ruta completa del archivo donde se guardará el CSV
                     (ej. 'C:/Users/Usuario/Desktop/extracto_banco_salida.csv').

    Returns:
        True si el archivo se escribió correctamente, False si ocurrió un error.
    """
    if not transacciones:
        logger.warning(
            "No se encontraron transacciones para escribir en el CSV.")
        return False

    # Validar que todos los elementos sean instancias de Transaccion
    if not all(isinstance(t, Transaccion) for t in transacciones):
        logger.error(
            "La lista contiene elementos que no son instancias de Transaccion")
        return False

    # Definimos las cabeceras que tendrá nuestro archivo CSV.
    headers = ['Dia', 'Etiqueta', 'Debit', 'Credit']

    logger.info(
        f"Escribiendo {len(transacciones)} transacciones en el archivo: {output_path}")

    try:
        with open(output_path, mode='w', newline='', encoding='utf-8') as csv_file:
            # Usamos DictWriter para mapear directamente los atributos del objeto a las columnas.
            writer = csv.DictWriter(csv_file, fieldnames=headers)

            # Escribir la fila de cabeceras
            writer.writeheader()

            # Escribir cada transacción en una nueva fila
            for i, transaccion in enumerate(transacciones):
                try:
                    # Pydantic nos da un método .model_dump() que convierte el objeto a un diccionario.
                    row_data = transaccion.model_dump()

                    # Formatear y mapear los datos a las nuevas cabeceras
                    csv_row = {
                        'Dia': row_data['fecha'],
                        'Etiqueta': row_data['descripcion'],
                        'Debit': (f"{row_data['debito']:.2f}" if row_data.get('debito') is not None else None),
                        'Credit': (f"{row_data['credito']:.2f}" if row_data.get('credito') is not None else None)
                    }

                    writer.writerow(csv_row)
                except Exception as e:
                    logger.error(
                        f"Error al escribir la transacción {i+1}: {e}")
                    # Continuar con la siguiente transacción en lugar de fallar completamente
                    continue

        logger.info("Archivo CSV generado exitosamente.")
        return True

    except IOError as e:
        logger.error(f"Error de E/S al escribir el archivo CSV: {e}")
        return False
    except Exception as e:
        logger.error(f"Ocurrió un error inesperado al escribir el CSV: {e}")
        return False
