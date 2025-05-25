import datetime
import logging

import requests

from ip_checker.config import IPCHECKER_WEBHOOK_URL, IPCHECKER_WEBHOOK_AUTH_HEADER, IPCHECKER_WEBHOOK_METHOD
from ip_checker.notifications.notification import NotificationMessage
from ip_checker.notifications.notification_channel import NotificationChannel


class WebhookNotification(NotificationChannel):

    def send(self, notification_message: NotificationMessage, retry_count: int = 0):
        try:
            headers = {}
            if IPCHECKER_WEBHOOK_AUTH_HEADER:
                headers['Authorization'] = IPCHECKER_WEBHOOK_AUTH_HEADER

            payload = {
                "message": notification_message.content,
                "title": notification_message.subject,
                "sent_at": datetime.datetime.now().isoformat()
            }

            response = requests.request(
                method=IPCHECKER_WEBHOOK_METHOD,
                url=IPCHECKER_WEBHOOK_URL,
                headers=headers,
                json=payload if IPCHECKER_WEBHOOK_METHOD != "GET" else None,
                params=payload if IPCHECKER_WEBHOOK_METHOD == "GET" else None
            )
            response.raise_for_status()
            logging.info("Webhook notification sent successfully")
        except Exception as e:
            logging.error(f"Error sending Webhook notification: {e}")
            self.failed_notifications[notification_message] = retry_count
