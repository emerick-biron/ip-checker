import logging
import re
from urllib.parse import urljoin

import requests

from ip_checker.config import IPCHECKER_GOTIFY_URL, IPCHECKER_GOTIFY_TOKEN, IPCHECKER_GOTIFY_PRIORITY
from ip_checker.notifications.notification import NotificationMessage
from ip_checker.notifications.notification_channel import NotificationChannel


class GotifyNotification(NotificationChannel):
    def __init__(self):
        super().__init__()
        self.gotify_url = urljoin(IPCHECKER_GOTIFY_URL, "/message")

    def send(self, notification_message: NotificationMessage, retry_count: int = 0):
        try:
            response = requests.post(
                url=f"{self.gotify_url}?token={IPCHECKER_GOTIFY_TOKEN}",
                json={
                    "message": notification_message.content,
                    "priority": IPCHECKER_GOTIFY_PRIORITY,
                    "title": notification_message.subject
                }
            )
            response.raise_for_status()
            logging.info("Gotify notification sent successfully")
        except Exception as e:
            sanitized_error = re.sub(r"token=[^&]+", "token=*******", str(e))
            logging.error(f"Error sending Gotify notification: {sanitized_error}")
            self.failed_notifications[notification_message] = retry_count
