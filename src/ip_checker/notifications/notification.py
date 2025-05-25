from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationMessage:
    subject: str
    content: str
