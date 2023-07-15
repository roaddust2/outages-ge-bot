import os
from dotenv import load_dotenv


load_dotenv()


API_TOKEN = os.getenv('API_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
