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
    Maneja de forma robusta los separadores de miles ('.' o ',') y decimales ('.' o ',').
    Ejemplos:
    - "1.234,56" -> "1234.56"
    - "1,234.56" -> "1234.56"
    - "741.00"   -> "741.00"
    - "1.234"    -> "1234"
    """
    if not isinstance(value, str):
        return value
    
    value = value.strip()
    
    has_dot = '.' in value
    has_comma = ',' in value

    if has_dot and has_comma:
        if value.rfind('.') > value.rfind(','):
            # Format: 1,234.56
            return value.replace(',', '')
        else:
            # Format: 1.234,56
            return value.replace('.', '').replace(',', '.')
    
    if has_comma:
        # If there are multiple commas, they are thousands separators
        if value.count(',') > 1:
            return value.replace(',', '')
        # If there is one comma, it's a decimal separator
        else:
            # Ambiguous case: "1,234" vs "1,23".
            # If the part after the comma has 3 digits, it's likely a thousand separator.
            if len(value.split(',')[1]) == 3:
                return value.replace(',', '')
            else:
                return value.replace(',', '.')
        
    if has_dot:
        # If there are multiple dots, they are thousands separators
        if value.count('.') > 1:
            return value.replace('.', '')
        # If there is one dot, it could be decimal or thousands
        else:
            parts = value.split('.')
            # If the part after the dot is not 3 digits long, it's probably a decimal.
            # Or if it is 3 digits but there are no thousands (e.g. ".500").
            if len(parts[1]) != 3 or len(parts[0]) == 0:
                return value # Treat as decimal
            else: # e.g. "1.234"
                return value.replace('.', '') # Treat as thousands
    
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