# Wiki y Manual de Usuario - Extractor de Movimientos Bancarios con IA

Bienvenido a la guía del Extractor de Movimientos Bancarios. Esta wiki te ayudará a instalar, configurar y utilizar la aplicación de manera efectiva.

## 📜 Índice

1.  [**Guía para Usuarios Finales**](#1-guía-para-usuarios-finales)
    -   [Descarga e Instalación](#descarga-e-instalación)
    -   [Configuración Inicial (API Key)](#configuración-inicial-api-key)
    -   [Manual de Uso](#manual-de-uso)
2.  [**Guía para Desarrolladores**](#2-guía-para-desarrolladores)
    -   [Requisitos Previos](#requisitos-previos)
    -   [Instalación desde el Código Fuente](#instalación-desde-el-ódigo-fuente)
    -   [Ejecutar la Aplicación en Modo Desarrollo](#ejecutar-la-aplicación-en-modo-desarrollo)
3.  [**Detalles de Configuración Avanzada**](#3-detalles-de-configuración-avanzada)
4.  [**Solución de Problemas Comunes**](#4-solución-de-problemas-comunes)

---

## 1. Guía para Usuarios Finales

Esta sección es para ti si solo quieres usar la aplicación sin lidiar con el código.

### Descarga e Instalación

1.  Ve a la [**página de Releases en GitHub**](https://github.com/iapunto/bank-csv/releases).
2.  Busca la última versión (ej. `v1.2.23`).
3.  En la sección de **Assets**, descarga el archivo `BankCSVExtractor.exe`.
4.  Guarda el archivo `.exe` en una carpeta de tu elección. ¡Eso es todo! No necesita instalación.

### Configuración Inicial (API Key)

La primera vez que ejecutes la aplicación, necesitarás configurar tu clave de API de Google Gemini.

1.  Haz doble clic en `BankCSVExtractor.exe` para iniciar la aplicación.
2.  Ve a la pestaña **"Configuración"**.
3.  Pega tu clave de API de Gemini en el campo de texto.
4.  Haz clic en el botón **"Guardar Clave"**.

La aplicación guardará tu clave en un archivo `settings.ini` junto al `.exe` y estará lista para usarse.

### Manual de Uso

1.  Ve a la pestaña **"Extractor"**.
2.  Haz clic en **"Seleccionar Archivo PDF"** y elige el extracto bancario que deseas procesar.
3.  Haz clic en **"Generar CSV"**.
4.  La aplicación te pedirá que elijas dónde guardar el archivo CSV resultante.
5.  ¡Listo! El archivo CSV con tus transacciones será guardado en la ubicación que elegiste.

---

## 2. Guía para Desarrolladores

Esta sección es para ti si quieres modificar el código, compilar tu propia versión o contribuir al proyecto.

### Requisitos Previos

-   **Python 3.8** o superior.
-   **Git** instalado.
-   Una **Clave de API de Google Gemini**.

### Instalación desde el Código Fuente

1.  **Clona el Repositorio:**
    ```bash
    git clone https://github.com/iapunto/bank-csv.git
    cd bank-csv
    ```

2.  **Crea y Activa un Entorno Virtual:**
    ```bash
    # Para Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Instala las Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### Ejecutar la Aplicación en Modo Desarrollo

-   Para iniciar la aplicación, ejecuta:
    ```bash
    python main.py
    ```
-   La configuración de la API Key se gestiona de la misma forma que para el usuario final, a través de la pestaña "Configuración".

---

## 3. Detalles de Configuración Avanzada

La aplicación se controla a través del archivo `settings.ini`. Cuando usas el `.exe`, este archivo se crea junto a él. En modo desarrollo, se crea en la raíz del proyecto.

-   `[API]`
    -   `GEMINI_API_KEY`: Tu clave de API.
-   `[APP]`
    -   `APPEARANCE_MODE`: Tema visual (`Light`, `Dark`, `System`).
    -   `COLOR_THEME`: Color de acento (`blue`, `green`, `dark-blue`).
-   `[CSV]`
    -   `DATE_FORMAT`: Formato para las fechas en el CSV (`dd-mm-aaaa`).

---

## 4. Solución de Problemas Comunes

-   **Error: "API Key no configurada" o similar al iniciar:**
    -   Asegúrate de haber guardado una clave API válida en la pestaña "Configuración".

-   **Error: "Archivo PDF no válido"**
    -   Asegúrate de que el archivo es un PDF válido y no está corrupto.
    -   El sistema funciona mejor con PDFs que contienen texto seleccionable, no imágenes escaneadas.