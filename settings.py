import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator


# Environment variables settings
# To store vars secretly, create an '.env' file in root folder
# and add them. To load vars load_dotenv() is called
# https://pypi.org/project/python-dotenv/

load_dotenv()


API_TOKEN = os.getenv('API_TOKEN')

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


# Translation configuration
# Google Translate is used as provider
# https://deep-translator.readthedocs.io/en/latest/README.html#id1

translator = GoogleTranslator(source='ka', target='en')
