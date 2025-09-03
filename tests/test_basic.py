# -*- coding: utf-8 -*-
"""
Fichero: test_basic.py
Proyecto: Extractor de Movimientos Bancarios con IA

Desarrollado por: IA Punto Soluciones Tecnológicas
Para: Industrias Pico
Responsable: MEng Sergio Rondón
Fecha de Creación: 03/09/2025

Descripción:
Tests básicos para validar la funcionalidad del sistema.
"""

import unittest
import os
import sys
import tempfile
import shutil

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.data_models import Transaccion, ExtractoBancario
from src.models.csv_writer import escribir_transacciones_a_csv
from src.utils.error_handler import validate_file_path, format_error_message


class TestDataModels(unittest.TestCase):
    """Tests para los modelos de datos."""
    
    def test_transaccion_creation(self):
        """Test de creación de una transacción."""
        transaccion = Transaccion(
            dia="15-12-2025",
            descripcion="Compra en supermercado",
            debito=25.50,
            credito=None
        )
        
        self.assertEqual(transaccion.dia, "15-12-2025")
        self.assertEqual(transaccion.descripcion, "Compra en supermercado")
        self.assertEqual(transaccion.debito, 25.50)
        self.assertIsNone(transaccion.credito)
    
    def test_extracto_bancario_creation(self):
        """Test de creación de un extracto bancario."""
        transacciones = [
            Transaccion(dia="15-12-2025", descripcion="Compra", debito=25.50, credito=None),
            Transaccion(dia="16-12-2025", descripcion="Depósito", debito=None, credito=100.00)
        ]
        
        extracto = ExtractoBancario(transacciones=transacciones)
        
        self.assertEqual(len(extracto.transacciones), 2)
        self.assertIsInstance(extracto.transacciones[0], Transaccion)


class TestCSVWriter(unittest.TestCase):
    """Tests para el escritor de CSV."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.csv")
        
        self.test_transacciones = [
            Transaccion(dia="15-12-2025", descripcion="Compra", debito=25.50, credito=None),
            Transaccion(dia="16-12-2025", descripcion="Depósito", debito=None, credito=100.00)
        ]
    
    def tearDown(self):
        """Limpieza después de los tests."""
        shutil.rmtree(self.test_dir)
    
    def test_csv_writing(self):
        """Test de escritura de CSV."""
        success = escribir_transacciones_a_csv(self.test_transacciones, self.test_file)
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.test_file))
        
        # Verificar contenido del archivo
        with open(self.test_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        self.assertIn("dia,descripcion,debito,credito", content)
        self.assertIn("15-12-2025,Compra,25.5,", content)
        self.assertIn("16-12-2025,Depósito,,100.0", content)
    
    def test_csv_writing_empty_list(self):
        """Test de escritura de CSV con lista vacía."""
        success = escribir_transacciones_a_csv([], self.test_file)
        self.assertFalse(success)
    
    def test_csv_writing_invalid_data(self):
        """Test de escritura de CSV con datos inválidos."""
        invalid_data = [{"dia": "15-12-2025", "descripcion": "Test"}]
        success = escribir_transacciones_a_csv(invalid_data, self.test_file)
        self.assertFalse(success)


class TestErrorHandler(unittest.TestCase):
    """Tests para el manejador de errores."""
    
    def test_validate_file_path_existing(self):
        """Test de validación de archivo existente."""
        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_file = f.name
        
        try:
            # Validar archivo existente
            self.assertTrue(validate_file_path(temp_file))
            self.assertTrue(validate_file_path(temp_file, '.txt'))
            self.assertFalse(validate_file_path(temp_file, '.pdf'))
        finally:
            os.unlink(temp_file)
    
    def test_validate_file_path_nonexistent(self):
        """Test de validación de archivo inexistente."""
        self.assertFalse(validate_file_path("/ruta/inexistente/archivo.txt"))
    
    def test_format_error_message(self):
        """Test de formateo de mensajes de error."""
        error = ValueError("Error de prueba")
        
        message = format_error_message(error)
        self.assertEqual(message, "Error de prueba")
        
        message_with_context = format_error_message(error, "Contexto")
        self.assertEqual(message_with_context, "Contexto: Error de prueba")


class TestConfiguration(unittest.TestCase):
    """Tests para la configuración."""
    
    def test_config_file_exists(self):
        """Test de que el archivo de configuración existe."""
        config_path = "config/settings.ini"
        self.assertTrue(os.path.exists(config_path))
    
    def test_config_file_readable(self):
        """Test de que el archivo de configuración es legible."""
        config_path = "config/settings.ini"
        
        import configparser
        config = configparser.ConfigParser()
        
        try:
            config.read(config_path)
            self.assertIn('API', config.sections())
            self.assertIn('GEMINI_API_KEY', config['API'])
        except Exception as e:
            self.fail(f"No se pudo leer el archivo de configuración: {e}")


if __name__ == '__main__':
    # Configurar logging para los tests
    import logging
    logging.basicConfig(level=logging.WARNING)
    
    # Ejecutar tests
    unittest.main(verbosity=2)
