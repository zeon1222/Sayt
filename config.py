import os
from dotenv import load_dotenv

# .env faylını yüklə
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "112201")  # Default şifrə

# Sayt məlumatları
SITE_TITLE = "HəcZiyarətiAz"
PRICE = 6100

# Yoxlama
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("⚠️ XƏBƏRDARLIQ: .env faylında TELEGRAM_BOT_TOKEN və ya TELEGRAM_CHAT_ID tapılmadı!")
