import logging

import requests

from ip_checker.config import IPCHECKER_TELEGRAM_BOT_TOKEN, IPCHECKER_TELEGRAM_CHAT_ID
from ip_checker.notifications.notification import NotificationMessage
from ip_checker.notifications.notification_channel import NotificationChannel


class TelegramNotification(NotificationChannel):
    def __init__(self):
        super().__init__()
        self.telegram_url = f"https://api.telegram.org/bot{IPCHECKER_TELEGRAM_BOT_TOKEN}/sendMessage"

    def send(self, notification_message: NotificationMessage, retry_count: int = 0):
        try:

            message = f"*{notification_message.subject}:*\n\n{notification_message.content}"

            response = requests.post(
                url=self.telegram_url,
                json={
                    "chat_id": IPCHECKER_TELEGRAM_CHAT_ID,
                    "parse_mode": "Markdown",
                    "text": message
                }
            )
            response.raise_for_status()
            logging.info("Telegram notification sent successfully")
        except Exception as e:
            sanitized_error = str(e).replace(IPCHECKER_TELEGRAM_BOT_TOKEN, "*******")
            logging.error(f"Error sending Telegram notification: {sanitized_error}")
            self.failed_notifications[notification_message] = retry_count
