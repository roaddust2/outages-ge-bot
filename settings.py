import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator


# Environment variables settings
# To store vars secretly, create an '.env' file in root folder
# and add them. To load vars load_dotenv() is called
# https://pypi.org/project/python-dotenv/

load_dotenv()


API_TOKEN = os.getenv('API_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')


# Translation configuration
# Google Translate is used as provider
# https://deep-translator.readthedocs.io/en/latest/README.html#id1

translator = GoogleTranslator(source='ka', target='en')
