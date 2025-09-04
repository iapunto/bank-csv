# 🏦 Extractor de Movimientos Bancarios con IA

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Un sistema inteligente diseñado para **convertir extractos bancarios en formato PDF a archivos CSV**, facilitando la **conciliación de movimientos en Odoo** y otros sistemas ERP o contables. Utiliza la API de Google Gemini para una extracción precisa y automatizada de transacciones.

## 🚀 Características

- **🤖 IA Avanzada**: Utiliza Google Gemini para extracción inteligente de datos
- **📊 CSV Estandarizado**: Genera archivos CSV con formato consistente
- **🖥️ Interfaz Moderna**: GUI intuitiva usando CustomTkinter
- **🔒 Validación Robusta**: Esquemas Pydantic para integridad de datos
- **📝 Logging Completo**: Sistema de logging con rotación automática
- **🧪 Tests Automatizados**: Suite completa de tests unitarios
- **⚙️ Configuración Flexible**: Archivos INI para personalización
- **🛠️ Herramientas de Desarrollo**: Black, Flake8, MyPy, Pytest

## 📋 Requisitos

- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows, macOS, Linux
- **API Key**: Clave de Google Gemini ([Obtener aquí](https://makersuite.google.com/app/apikey))

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/iapunto/bank-csv.git
cd bank-csv
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
# Instalación básica
pip install -r requirements.txt

# Instalación completa con herramientas de desarrollo
make install-dev
```

### 4. Configurar API Key

Edita el archivo `config/settings.ini`:

```ini
[API]
GEMINI_API_KEY = tu_api_key_aqui
```

## 🚀 Uso

### Ejecución básica

```bash
python main.py
```

### Comandos de desarrollo

```bash
# Ver todos los comandos disponibles
make help

# Ejecutar tests
make test

# Verificar calidad del código
make check

# Formatear código
make format

# Ejecutar con tests previos
make run-dev
```

## 🏗️ Arquitectura

El proyecto sigue el patrón **MVC (Modelo-Vista-Controlador)**:

```
src/
├── models/          # Lógica de negocio y datos
│   ├── data_models.py      # Esquemas Pydantic
│   ├── extractor_ia.py     # Integración con Gemini
│   └── csv_writer.py       # Generación de CSV
├── views/           # Interfaz de usuario
│   └── main_window.py      # Ventana principal
├── controllers/     # Lógica de control
│   └── app_controller.py   # Controlador principal
└── utils/           # Utilidades
    └── error_handler.py    # Manejo de errores

config/              # Configuración
├── settings.ini            # Configuración principal
└── logging_config.py       # Configuración de logging

tests/               # Tests unitarios
└── test_basic.py           # Tests básicos
```

## 🔧 Configuración

### Archivo de configuración principal (`config/settings.ini`)

```ini
[API]
GEMINI_API_KEY = tu_api_key_aqui
GEMINI_MODEL = gemini-1.5-flash-latest

[APP]
APPEARANCE_MODE = System
COLOR_THEME = blue
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 250

[LOGGING]
LOG_LEVEL = INFO
LOG_FILE = app.log
LOG_ENCODING = utf-8

[CSV]
CSV_ENCODING = utf-8
CSV_DELIMITER = ,
DATE_FORMAT = dd-mm-aaaa
```

## 🧪 Testing

### Ejecutar tests

```bash
# Tests básicos
python -m pytest tests/ -v

# Tests con cobertura
make test-cov

# Tests específicos
python -m pytest tests/test_basic.py::TestDataModels -v
```

### Cobertura de código

```bash
# Generar reporte HTML
python -m pytest --cov=src --cov-report=html

# Ver en navegador
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

## 📊 Calidad del Código

### Linting y formateo

```bash
# Verificar formato
make check

# Formatear automáticamente
make format

# Verificar tipos
python -m mypy src/
```

### Pre-commit hooks

```bash
# Instalar hooks
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

## 🐛 Solución de Problemas

### Error: "API Key no configurada"

1. Verifica que `config/settings.ini` existe
2. Asegúrate de que `GEMINI_API_KEY` tenga tu clave válida
3. Reinicia la aplicación

### Error: "Módulo no encontrado"

1. Verifica que estés en el directorio raíz del proyecto
2. Activa el entorno virtual si lo usas
3. Instala las dependencias: `pip install -r requirements.txt`

### Error: "Archivo PDF no válido"

1. Verifica que el archivo sea un PDF válido
2. Asegúrate de que el PDF contenga texto (no solo imágenes)
3. Verifica que el PDF no esté corrupto

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Convenciones de commits

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Cambios de formato
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests

## 📝 Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para un historial completo de cambios.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **IA Punto Soluciones Tecnológicas** - _Desarrollo inicial_ - [IA Punto](https://iapunto.com)
- **MEng Sergio Rondón** - _Responsable del proyecto_

## 🌟 Créditos

Este proyecto fue desarrollado por **IA Punto** para **Industrias Pico SAS**.

## 🙏 Agradecimientos

- [Google Gemini](https://ai.google.dev/) por la API de IA
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) por la interfaz moderna
- [Pydantic](https://pydantic.dev/) por la validación de datos
- [Pytest](https://pytest.org/) por el framework de testing

## 📞 Soporte

- **Email**: desarrollo@iapunto.com
- **Issues**: [GitHub Issues](https://github.com/iapunto/bank-csv/issues)
- **Documentación**: [Wiki del proyecto](https://github.com/iapunto/bank-csv/wiki)

---

⭐ **¡Si este proyecto te es útil, considera darle una estrella!**
