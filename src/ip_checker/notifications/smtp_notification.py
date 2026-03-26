import logging
import smtplib
import ssl

from ip_checker.config import IPCHECKER_SMTP_SERVER, IPCHECKER_SMTP_PORT, IPCHECKER_SMTP_PASSWORD, \
    IPCHECKER_SMTP_SENDER_EMAIL, IPCHECKER_SMTP_RECIPIENT_EMAIL, IPCHECKER_SMTP_SENDER_NAME
from ip_checker.notifications.notification import NotificationMessage
from ip_checker.notifications.notification_channel import NotificationChannel


class SMTPNotification(NotificationChannel):

    def send(self, notification_message: NotificationMessage, retry_count: int = 0):
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(IPCHECKER_SMTP_SERVER, IPCHECKER_SMTP_PORT) as server:
                server.starttls(context=context)
                server.login(IPCHECKER_SMTP_SENDER_EMAIL, IPCHECKER_SMTP_PASSWORD)
                sender = f"{IPCHECKER_SMTP_SENDER_NAME} <{IPCHECKER_SMTP_SENDER_EMAIL}>" if IPCHECKER_SMTP_SENDER_NAME else IPCHECKER_SMTP_SENDER_EMAIL
                msg = f"From: {sender}\nSubject: {notification_message.subject}\n\n{notification_message.content}"
                server.sendmail(IPCHECKER_SMTP_SENDER_EMAIL, IPCHECKER_SMTP_RECIPIENT_EMAIL, msg)
                logging.info("E-mail sent successfully")
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            self.failed_notifications[notification_message] = retry_count
