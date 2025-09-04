# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-09-03

### Agregado

- Pestaña de "Configuración" en la GUI para gestionar la clave API de Gemini.
- Creación de `config/settings.ini.template` como plantilla de configuración segura.
- Archivo de manual de usuario `WIKI.md` movido a la carpeta `docs/`.

### Cambiado

- La aplicación ya no almacena la clave API en el código fuente. La clave se guarda y se lee desde la GUI en el archivo `config/settings.ini`.

### Corregido

- **Falla de Seguridad Crítica:** Se ha eliminado la clave API del repositorio. El archivo `config/settings.ini` ahora es ignorado por Git para prevenir futuras filtraciones.
- Solucionado un error en la GUI que impedía guardar la clave API correctamente debido a un problema de renderizado de color en la barra de estado.

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
