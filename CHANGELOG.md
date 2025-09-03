# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-09-03

### Agregado

- Empaquetado de la aplicación como un archivo `.exe` único para Windows usando PyInstaller.
- Función de ayuda `resource_path` para resolver rutas de archivos en el ejecutable empaquetado.

### Cambiado

- **Formato de Salida CSV:**
  - Los montos numéricos ahora usan `.` como separador decimal y no tienen separadores de miles.
  - Las cabeceras del CSV se han cambiado a `Dia`, `Etiqueta`, `Debit`, `Credit`.
- **Manejo de Números:**
  - Mejorada la función `clean_number_string` para interpretar correctamente números con `.` como separador de miles y `,` como separador decimal.

### Corregido

- Solucionado un error crítico donde la aplicación empaquetada no podía encontrar el archivo de configuración `settings.ini`.

## [1.0.0] - 2025-09-03

### Agregado

- Sistema completo de extracción de movimientos bancarios con IA
- Interfaz gráfica moderna usando CustomTkinter
- Integración con API de Google Gemini
- Modelos de datos robustos usando Pydantic
- Sistema de logging avanzado con rotación de archivos
- Manejo centralizado de errores y excepciones
- Tests unitarios completos
- Configuración flexible y extensible
- Herramientas de desarrollo (black, flake8, mypy, pytest)
- Pre-commit hooks para calidad de código
- Makefile para automatización de tareas
- Documentación completa del código

### Características

- Extracción automática de transacciones de PDFs bancarios
- Generación de archivos CSV estandarizados
- Validación de datos usando esquemas Pydantic
- Interfaz de usuario intuitiva y responsive
- Manejo robusto de errores y logging detallado
- Configuración centralizada en archivo INI
- Soporte para múltiples modelos de Gemini

### Arquitectura

- Patrón MVC (Modelo-Vista-Controlador)
- Separación clara de responsabilidades
- Módulos bien estructurados y reutilizables
- Sistema de logging configurable
- Manejo de errores personalizado
- Tests automatizados con cobertura

### Dependencias

- google-generativeai >= 0.3.0
- pydantic >= 2.0.0
- customtkinter >= 5.2.0
- python-dateutil >= 2.8.0

### Compatibilidad

- Python 3.8+
- Windows, macOS, Linux
- Interfaz gráfica nativa en cada plataforma

## [0.1.0] - 2025-09-03

### Agregado

- Estructura inicial del proyecto
- Configuración básica de la aplicación
- Modelos de datos iniciales
- Interfaz gráfica básica

---

## Notas de Versión

### Versionado Semántico

- **MAJOR**: Cambios incompatibles con versiones anteriores
- **MINOR**: Nuevas funcionalidades compatibles hacia atrás
- **PATCH**: Correcciones de bugs compatibles hacia atrás

### Convenciones de Commits

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Cambios de formato (no afectan funcionalidad)
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests
- `chore:` Cambios en build, herramientas, etc.

### Proceso de Release

1. Desarrollar en rama `develop`
2. Crear rama `release/vX.Y.Z` para preparar release
3. Merge a `main` cuando esté listo
4. Tag de versión en `main`
5. Merge de `main` de vuelta a `develop`
