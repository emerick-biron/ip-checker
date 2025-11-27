import logging
import os
import socket


class MissingEnvironmentVariable(Exception):
    pass


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

IPCHECKER_SMTP_PASSWORD = os.getenv("IPCHECKER_SMTP_PASSWORD")
IPCHECKER_SMTP_PASSWORD_FILE = os.getenv("IPCHECKER_SMTP_PASSWORD_FILE")
IPCHECKER_SMTP_PORT = os.getenv("IPCHECKER_SMTP_PORT")
IPCHECKER_SMTP_SERVER = os.getenv("IPCHECKER_SMTP_SERVER")
IPCHECKER_SMTP_SENDER_EMAIL = os.getenv("IPCHECKER_SMTP_SENDER_EMAIL")
IPCHECKER_SMTP_RECIPIENT_EMAIL = os.getenv("IPCHECKER_SMTP_RECIPIENT_EMAIL", IPCHECKER_SMTP_SENDER_EMAIL)

IPCHECKER_GOTIFY_URL = os.getenv("IPCHECKER_GOTIFY_URL")
IPCHECKER_GOTIFY_TOKEN = os.getenv("IPCHECKER_GOTIFY_TOKEN")
IPCHECKER_GOTIFY_TOKEN_FILE = os.getenv("IPCHECKER_GOTIFY_TOKEN_FILE")
IPCHECKER_GOTIFY_PRIORITY = int(os.getenv("IPCHECKER_GOTIFY_PRIORITY", 10))

IPCHECKER_WEBHOOK_URL = os.getenv("IPCHECKER_WEBHOOK_URL")
IPCHECKER_WEBHOOK_METHOD = os.getenv("IPCHECKER_WEBHOOK_METHOD", "POST")
IPCHECKER_WEBHOOK_AUTH_HEADER = os.getenv("IPCHECKER_WEBHOOK_AUTH_HEADER")
IPCHECKER_WEBHOOK_AUTH_HEADER_FILE = os.getenv("IPCHECKER_WEBHOOK_AUTH_HEADER_FILE")
if IPCHECKER_WEBHOOK_METHOD:
    IPCHECKER_WEBHOOK_METHOD = IPCHECKER_WEBHOOK_METHOD.upper()

IPCHECKER_TELEGRAM_CHAT_ID = os.getenv("IPCHECKER_TELEGRAM_CHAT_ID")
IPCHECKER_TELEGRAM_BOT_TOKEN = os.getenv("IPCHECKER_TELEGRAM_BOT_TOKEN")
IPCHECKER_TELEGRAM_BOT_TOKEN_FILE = os.getenv("IPCHECKER_TELEGRAM_BOT_TOKEN_FILE")

IPCHECKER_CHECK_INTERVAL = int(os.getenv("IPCHECKER_CHECK_INTERVAL", 30))

IPCHECKER_NOTIFICATION_CHANNELS = os.getenv("IPCHECKER_NOTIFICATION_CHANNELS", "").split(",")

IPCHECKER_NOTIFICATIONS_MAX_RETRIES = int(os.getenv("IPCHECKER_NOTIFICATIONS_MAX_RETRIES", 3))

IPCHECKER_HOSTNAME = os.getenv("IPCHECKER_HOSTNAME", socket.gethostname())

if IPCHECKER_SMTP_PASSWORD_FILE:
    try:
        with open(IPCHECKER_SMTP_PASSWORD_FILE) as f:
            IPCHECKER_SMTP_PASSWORD = f.read().strip()
    except (OSError, FileNotFoundError, ValueError) as e:
        logging.error(f"An error occurred while reading password file: {e}")

if IPCHECKER_GOTIFY_TOKEN_FILE:
    try:
        with open(IPCHECKER_GOTIFY_TOKEN_FILE) as f:
            IPCHECKER_GOTIFY_TOKEN = f.read().strip()
    except (OSError, FileNotFoundError, ValueError) as e:
        logging.error(f"An error occurred while reading Gotify token file: {e}")

if IPCHECKER_WEBHOOK_AUTH_HEADER_FILE:
    try:
        with open(IPCHECKER_WEBHOOK_AUTH_HEADER_FILE) as f:
            IPCHECKER_WEBHOOK_AUTH_HEADER = f.read().strip()
    except (OSError, FileNotFoundError, ValueError) as e:
        logging.error(f"An error occurred while reading webhook auth header file: {e}")

if IPCHECKER_TELEGRAM_BOT_TOKEN_FILE:
    try:
        with open(IPCHECKER_TELEGRAM_BOT_TOKEN_FILE) as f:
            IPCHECKER_TELEGRAM_BOT_TOKEN = f.read().strip()
    except (OSError, FileNotFoundError, ValueError) as e:
        logging.error(f"An error occurred while reading Telegram bot token file: {e}")

enabled_channels = []

if "smtp" in IPCHECKER_NOTIFICATION_CHANNELS:
    if IPCHECKER_SMTP_PASSWORD and IPCHECKER_SMTP_SERVER and IPCHECKER_SMTP_PORT and IPCHECKER_SMTP_SENDER_EMAIL:
        enabled_channels.append("smtp")
    else:
        logging.error("SMTP configuration is incomplete. Disabling SMTP notifications.")

if "gotify" in IPCHECKER_NOTIFICATION_CHANNELS:
    if IPCHECKER_GOTIFY_URL and IPCHECKER_GOTIFY_TOKEN:
        enabled_channels.append("gotify")
    else:
        logging.error("Gotify configuration is incomplete. Disabling Gotify notifications.")

if "webhook" in IPCHECKER_NOTIFICATION_CHANNELS:
    if IPCHECKER_WEBHOOK_URL:
        enabled_channels.append("webhook")
    else:
        logging.error("Webhook URL is not set. Disabling Webhook notifications.")

if "telegram" in IPCHECKER_NOTIFICATION_CHANNELS:
    if IPCHECKER_TELEGRAM_CHAT_ID and IPCHECKER_TELEGRAM_BOT_TOKEN:
        enabled_channels.append("telegram")
    else:
        logging.error("Telegram configuration is incomplete. Disabling Telegram notifications.")

IPCHECKER_NOTIFICATION_CHANNELS = enabled_channels

logging.info(f"Active notification channels: {IPCHECKER_NOTIFICATION_CHANNELS}")
