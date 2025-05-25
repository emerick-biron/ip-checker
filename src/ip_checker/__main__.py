import time

import schedule

from ip_checker.config import IPCHECKER_CHECK_INTERVAL
from ip_checker.ip_checker import IPChecker


def main():
    checker = IPChecker()
    retry_notifications_every = max(1, IPCHECKER_CHECK_INTERVAL // 3)
    schedule.every(IPCHECKER_CHECK_INTERVAL).minutes.do(checker.check_ip)
    schedule.every(retry_notifications_every).minutes.do(checker.retry_failed_notifications)

    while True:
        schedule.run_pending()
        # Sleep until the next scheduled task, but:
        # - Ensure at least 1 second to prevent rapid looping.
        # - Avoid sleeping too long (max 60s) to stay responsive.
        # - Handle None (no tasks) by defaulting to 1 second.
        time.sleep(min(60, max(1, schedule.idle_seconds() or 1)))


if __name__ == '__main__':
    main()
