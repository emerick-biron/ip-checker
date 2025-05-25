import datetime
import logging
from typing import List

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from ip_checker.config import IPCHECKER_NOTIFICATION_CHANNELS
from ip_checker.notifications.gotify_notification import GotifyNotification
from ip_checker.notifications.notification import NotificationMessage
from ip_checker.notifications.notification_channel import NotificationChannel
from ip_checker.notifications.smtp_notification import SMTPNotification
from ip_checker.notifications.webhook_notification import WebhookNotification


class IPChecker:
    def __init__(self):
        self.old_ip = self.get_current_ip()
        self.notification_channels: List[NotificationChannel] = []
        self.setup_notification_channels()

        if self.old_ip is not None:
            current_dt = datetime.datetime.now()
            self.send_notifications(
                NotificationMessage(
                    subject="IP Checker",
                    content=f"IP Checker started at {current_dt.strftime('%Y-%m-%d %H:%M:%S')}.\nCurrent IP : {self.old_ip}"
                )
            )

    def setup_notification_channels(self):
        if "smtp" in IPCHECKER_NOTIFICATION_CHANNELS:
            self.notification_channels.append(SMTPNotification())
        if "gotify" in IPCHECKER_NOTIFICATION_CHANNELS:
            self.notification_channels.append(GotifyNotification())
        if "webhook" in IPCHECKER_NOTIFICATION_CHANNELS:
            self.notification_channels.append(WebhookNotification())

    def send_notifications(self, notification_message: NotificationMessage) -> None:
        for channel in self.notification_channels:
            logging.info(f"Sending notification via {type(channel).__name__}")
            channel.send(notification_message)

    @staticmethod
    def get_current_ip() -> str | None:
        session = requests.Session()
        retries = Retry(total=4, backoff_factor=3, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('https://', adapter)

        try:
            logging.info("Requesting current public IP")
            response = session.get('https://api.ipify.org')
            response.raise_for_status()
            current_ip = response.text.strip()
            logging.info(f"Current ip {current_ip}")
            return current_ip
        except requests.RequestException as e:
            logging.error(f"Error while retrieving IP: {e}")
            return None

    def check_ip(self) -> None:
        new_ip = self.get_current_ip()
        if new_ip and new_ip != self.old_ip:
            logging.warning("IP changed send notifications")
            current_dt = datetime.datetime.now()
            self.send_notifications(
                NotificationMessage(
                    subject="IP Checker",
                    content=f"IP address changed at {current_dt.strftime('%Y-%m-%d %H:%M:%S')}.\n\tOld IP : {self.old_ip}\n\tNew IP : {new_ip}"
                )
            )
            self.old_ip = new_ip

    def retry_failed_notifications(self):
        for channel in self.notification_channels:
            channel.retry_failed_notifications()
