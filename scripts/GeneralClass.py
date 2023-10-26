from abc import ABC, abstractmethod
from config.settings import get_config
import requests
from bs4 import BeautifulSoup
import logging
import os


class GeneralClass(ABC):
    def __init__(self):
        self.config = get_config()
        self.driver = None
        self.page_content = None

    @abstractmethod
    def process(self):
        page_content = self.get_site(self.site)
        self.page_content = page_content

    def get_site(self, site):
        session = requests.Session()
        try:
            response = session.get(site)
            if response.status_code == 200:
                page_content = response.text
                soup = BeautifulSoup(page_content, 'lxml')
                return soup
            else:
                print(f"Error {response.status_code}: {response.reason}")
                print(response.headers['Location'])
        except Exception as e:
            print("Error de conexión: ", e)
            print(f"El sitio es {site}")
        return False

    def get_site_phone(self):
        return self.config['site_1']

    def get_site_quick(self):
        return self.config['site_2']

    def setup_logger(self, logger_name, log_file):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            # Asegurarse de que el directorio de logs existe
            os.makedirs(os.path.dirname(log_file), exist_ok=True)

            # Configurar el handler de archivo
            file_handler = logging.FileHandler(log_file)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
            file_handler.setFormatter(formatter)

            # Añadir el handler al logger
            logger.addHandler(file_handler)

        return logger
