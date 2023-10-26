from dotenv import load_dotenv
import os


def get_config():
    load_dotenv()
    config = {
        'site_1': os.getenv('SITE_1'),
        'site_2': os.getenv('SITE_2'),
    }
    return config
