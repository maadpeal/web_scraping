# Proyecto de Web Scraping

## Descripción
Este proyecto está diseñado para realizar web scraping en dos sitios web diferentes, extrayendo información sobre dispositivos y sus precios. Utiliza Python, Selenium para la interacción con el navegador, y BeautifulSoup para el análisis de HTML.

## Requisitos
- Python 3.7 o superior
- Pip (gestor de paquetes de Python)
- Navegador Chrome y [ChromeDriver](https://sites.google.com/chromium.org/driver/)

## Instalación
1. Clona el repositorio en tu máquina local.
2. Navega al directorio del proyecto mediante la terminal o línea de comandos.
3. Ejecuta `pip install -r requirements.txt` para instalar las dependencias necesarias.

## Estructura del Proyecto
- `main.py`: Script principal que ejecuta los scripts de web scraping en paralelo.
- `GeneralClass.py`: Clase base que proporciona métodos comunes y configuración para los scripts de web scraping.
- `PhoneSiteScript.py`: Script para realizar web scraping en un sitio web de dispositivos.
- `QuickSiteScript.py`: Script para realizar web scraping en otro sitio web utilizando Selenium.
- `settings.py`: Archivo de configuración para almacenar variables y configuraciones generales.
- `requirements.txt`: Lista de dependencias y bibliotecas necesarias para ejecutar los scripts.

## Uso
Para ejecutar el proyecto, asegúrate de estar en el directorio correcto y ejecuta `python main.py`. Este script creará las carpetas necesarias si no existen, y luego ejecutará ambos scripts de web scraping en paralelo.

## Logging
El proyecto está configurado para registrar mensajes de debug e información en archivos de log separados para cada script:
- `./logs/phone_site.log`: Log para `PhoneSiteScript`.
- `./logs/quick_site.log`: Log para `QuickSiteScript`.

Puedes revisar estos archivos para obtener información detallada sobre la ejecución de los scripts y para depurar en caso de errores.

## Contribución
Si deseas contribuir al proyecto, por favor haz un fork del repositorio, crea una rama con tus cambios y envía un pull request. Todas las contribuciones son bienvenidas.
