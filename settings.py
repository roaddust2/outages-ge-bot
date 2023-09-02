import os
from dotenv import load_dotenv
from apscheduler.jobstores.memory import MemoryJobStore
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

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL_ASYNC = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# APScheduler settings
# https://apscheduler.readthedocs.io/en/3.x/userguide.html#configuring-the-scheduler

TIMEZONE = "Asia/Tbilisi"

jobstores = {
    'default': MemoryJobStore(),
}


# Translation configuration
# Google Translate is used as provider
# https://deep-translator.readthedocs.io/en/latest/README.html#id1

translator = GoogleTranslator(source='ka', target='en')
