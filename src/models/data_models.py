# src/model/data_models.py

"""
Fichero: data_models.py
Proyecto: Extractor de Movimientos Bancarios con IA

Desarrollado por: IA Punto Soluciones Tecnológicas
Para: Industrias Pico
Responsable: MEng Sergio Rondón
Fecha de Creación: 03/09/2025

Descripción:
Este módulo define los modelos de datos Pydantic que estructuran la información
extraída de los extractos bancarios.

Estos modelos sirven como un "contrato" para la API de Gemini, asegurando que
la salida de la IA sea consistente y fácil de manejar.
"""

from pydantic import BaseModel, Field, BeforeValidator
from typing import List, Optional, Annotated

def clean_number_string(value: str) -> str:
    """
    Limpia una cadena de texto numérica para que pueda ser convertida a float.
    Elimina los separadores de miles (puntos) y estandariza el separador
    decimal a un punto.
    Ej: "1.234,56" -> "1234.56"
    """
    if isinstance(value, str):
        # Eliminar los puntos que actúan como separadores de miles.
        # Reemplazar la coma decimal por un punto.
        return value.replace(".", "").replace(",", ".")
    return value


class Transaccion(BaseModel):
    """
    Representa una única línea de transacción en un extracto bancario.
    Las descripciones en los campos (Field) ayudan a la IA a comprender mejor
    qué información debe extraer para cada atributo.
    """
    fecha: str = Field(
        description="La fecha completa de la transacción. Debe ser estandarizada al formato 'dd-mm-aaaa'."
    )

    descripcion: str = Field(
        description="La descripción completa o etiqueta de la transacción, tal como aparece en el extracto."
    )

    debito: Annotated[Optional[float], BeforeValidator(clean_number_string)] = Field(
        description="El importe del débito (gasto o salida de dinero). Si la transacción no es un débito, este campo debe ser nulo."
    )

    credito: Annotated[Optional[float], BeforeValidator(clean_number_string)] = Field(
        description="El importe del crédito (ingreso o entrada de dinero). Si la transacción no es un crédito, este campo debe ser nulo."
    )


class ExtractoBancario(BaseModel):
    """
    Representa el contenido completo de un extracto bancario, que consiste
    en una lista de transacciones individuales.
    """
    transacciones: List[Transaccion] = Field(
        description="Una lista que contiene todas las líneas de transacción individuales extraídas del documento."
    )