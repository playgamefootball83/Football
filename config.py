import os
from dotenv import load_dotenv

load_dotenv()  # ये जरूरी है .env से वैल्यू लोड करने के लिए

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
