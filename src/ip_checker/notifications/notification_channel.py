import logging
from abc import ABC, abstractmethod
from typing import Dict

from ip_checker.config import IPCHECKER_NOTIFICATIONS_MAX_RETRIES
from ip_checker.notifications.notification import NotificationMessage


class NotificationChannel(ABC):

    def __init__(self):
        self.failed_notifications: Dict[NotificationMessage, int] = dict()

    @abstractmethod
    def send(self, notification_message: NotificationMessage, retry_count: int = 0):
        pass

    def retry_failed_notifications(self):
        if not self.failed_notifications:
            return

        logging.info(f"Retrying {len(self.failed_notifications)} failed notifications for {type(self).__name__}")

        failed = self.failed_notifications.copy()
        self.failed_notifications.clear()
        for notification_message in failed:
            try:
                retry_count = failed[notification_message]
                if retry_count < IPCHECKER_NOTIFICATIONS_MAX_RETRIES:
                    self.send(notification_message, retry_count + 1)
            except Exception as e:
                logging.error(f"Retry failed for {type(self).__name__}: {e}")
