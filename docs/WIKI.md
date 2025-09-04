# Wiki y Manual de Usuario - Extractor de Movimientos Bancarios con IA

Bienvenido a la wiki del Extractor de Movimientos Bancarios. Esta guía te ayudará a instalar, configurar y utilizar la aplicación de manera efectiva.

## 📜 Índice

1.  [**Introducción**](#1-introducción)
2.  [**Instalación y Configuración Inicial**](#2-instalación-y-configuración-inicial)
    -   [Requisitos Previos](#requisitos-previos)
    -   [Pasos de Instalación](#pasos-de-instalación)
    -   [Configuración de la API Key](#configuración-de-la-api-key)
3.  [**Manual de Uso de la Aplicación**](#3-manual-de-uso-de-la-aplicación)
    -   [Iniciar la Aplicación](#iniciar-la-aplicación)
    -   [Interfaz Principal](#interfaz-principal)
    -   [Proceso de Extracción (Paso a Paso)](#proceso-de-extracción-paso-a-paso)
4.  [**Configuración Avanzada**](#4-configuración-avanzada)
    -   [Archivo `settings.ini`](#archivo-settingsini)
5.  [**Solución de Problemas Comunes**](#5-solución-de-problemas-comunes)

---

## 1. Introducción

El **Extractor de Movimientos Bancarios con IA** es una herramienta de escritorio diseñada para simplificar la contabilidad y el análisis financiero. La aplicación utiliza la inteligencia artificial de Google (a través de la API de Gemini) para leer archivos PDF de extractos bancarios, entender su contenido y exportar todas las transacciones a un archivo CSV estandarizado y fácil de manejar.

**Características Principales:**
- Extracción de datos de transacciones desde archivos PDF.
- Uso de IA para interpretar formatos de extractos diversos.
- Generación de un archivo `output.csv` con los datos limpios.
- Interfaz gráfica simple e intuitiva.

## 2. Instalación y Configuración Inicial

Sigue estos pasos para tener la aplicación funcionando en tu sistema.

### Requisitos Previos
- **Python 3.8** o una versión superior.
- Una **Clave de API de Google Gemini**. Puedes obtenerla gratuitamente [aquí](https://makersuite.google.com/app/apikey).

### Pasos de Instalación

1.  **Clona el Repositorio:**
    Abre una terminal o consola y ejecuta el siguiente comando:
    ```bash
    git clone https://github.com/iapunto/bank-csv.git
    cd bank-csv
    ```

2.  **Crea un Entorno Virtual (Recomendado):**
    Esto aísla las dependencias del proyecto.
    ```bash
    # Para Windows
    python -m venv venv
    venv\Scripts\activate

    # Para macOS/Linux
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Instala las Dependencias:**
    Con el entorno virtual activado, instala todo lo necesario con un solo comando:
    ```bash
    pip install -r requirements.txt
    ```

### Configuración de la API Key

Este es el paso más importante para que la IA funcione.

1.  Navega a la carpeta `config/`.
2.  Abre el archivo `settings.ini` con un editor de texto.
3.  Busca la línea `GEMINI_API_KEY` y pega tu clave de API después del signo `=`.

    ```ini
    [API]
    GEMINI_API_KEY = tu_api_key_aqui
    ```
4.  Guarda y cierra el archivo.

¡Listo! La aplicación ya está configurada para funcionar.

## 3. Manual de Uso de la Aplicación

### Iniciar la Aplicación

Asegúrate de tener el entorno virtual activado y estar en la carpeta raíz del proyecto. Luego, ejecuta:
```bash
python main.py
```
Se abrirá la ventana principal de la aplicación.

### Interfaz Principal

La interfaz es minimalista y fácil de usar. Contiene los siguientes elementos:
- **Un título:** "Extractor de Movimientos Bancarios".
- **Un botón "Seleccionar PDF":** Para abrir el explorador de archivos y elegir el extracto bancario que deseas procesar.
- **Un botón "Iniciar Extracción":** Para comenzar el proceso una vez seleccionado el archivo.
- **Una etiqueta de estado:** Muestra el progreso actual (ej. "Listo", "Procesando...", "Extracción completada").

### Proceso de Extracción (Paso a Paso)

1.  **Haz clic en "Seleccionar PDF"**.
2.  **Elige el archivo PDF** de tu extracto bancario y haz clic en "Abrir". La etiqueta de estado mostrará "Archivo seleccionado".
3.  **Haz clic en "Iniciar Extracción"**.
4.  **Espera**. La aplicación enviará el contenido del PDF a la IA de Gemini para su análisis. La etiqueta de estado mostrará "Procesando...". Este proceso puede tardar unos segundos.
5.  **¡Finalizado!** Cuando la extracción termine, la etiqueta de estado cambiará a "Extracción completada". En la carpeta raíz del proyecto, encontrarás un nuevo archivo llamado `output.csv` con todas las transacciones.

El archivo `output.csv` contendrá columnas como `fecha`, `descripcion`, `monto`, y `tipo_transaccion`.

## 4. Configuración Avanzada

Puedes personalizar el comportamiento de la aplicación editando el archivo `config/settings.ini`.

### Archivo `settings.ini`

-   `[API]`
    -   `GEMINI_API_KEY`: Tu clave de API.
    -   `GEMINI_MODEL`: El modelo de IA a usar. `gemini-1.5-flash-latest` es rápido y eficiente, mientras que `gemini-1.5-pro-latest` es más potente pero lento.

-   `[APP]`
    -   `APPEARANCE_MODE`: Tema visual (`Light`, `Dark`, `System`).
    -   `COLOR_THEME`: Color de acento de la interfaz (`blue`, `green`, `dark-blue`).

-   `[LOGGING]`
    -   `LOG_LEVEL`: Nivel de detalle de los registros (`INFO`, `DEBUG`).
    -   `LOG_FILE`: Nombre del archivo donde se guardan los registros (`app.log`).

-   `[CSV]`
    -   `CSV_ENCODING`: Codificación del archivo de salida (`utf-8`).
    -   `CSV_DELIMITER`: Separador de columnas (`,` por defecto).
    -   `DATE_FORMAT`: Formato para las fechas en el CSV (`dd-mm-aaaa`).

## 5. Solución de Problemas Comunes

-   **Error: "API Key no configurada"**
    1.  Verifica que `config/settings.ini` existe.
    2.  Asegúrate de que `GEMINI_API_KEY` tiene una clave válida.
    3.  Reinicia la aplicación.

-   **Error: "Módulo no encontrado"**
    1.  Asegúrate de estar en la carpeta raíz del proyecto.
    2.  Verifica que tu entorno virtual esté activado.
    3.  Prueba a reinstalar las dependencias: `pip install -r requirements.txt`.

-   **Error: "Archivo PDF no válido"**
    1.  Asegúrate de que el archivo es un PDF válido y no está corrupto.
    2.  El sistema funciona mejor con PDFs que contienen texto seleccionable, no imágenes escaneadas.
