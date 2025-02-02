import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
API_URL = os.environ.get('API_URL')
