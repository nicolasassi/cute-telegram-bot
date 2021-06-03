import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CAT_API_TOKEN = os.getenv("CAT_API_TOKEN")
BASE_CAT_API_URL = os.getenv("BASE_CAT_API_URL")
BASE_WIKIPEDIA_API_URL = os.getenv("BASE_WIKIPEDIA_API_URL")
