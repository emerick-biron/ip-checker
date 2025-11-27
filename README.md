# IP Checker

**IP Checker** is a Python application that periodically monitors the public IP address of the host machine and notifies
changes through multiple notification channels (SMTP, Gotify). The application is designed to be **lightweight**,
**configurable**, and **containerized** using Docker.

## Features

- Periodically checks the public IP address.
- Sends notifications when the IP changes.
- Supports multiple notification channels:
    - **SMTP (Email)**
    - **Gotify (Self-hosted push notifications)**
    - **Webhook (Custom endpoints, e.g., n8n, Discord, etc.)**
  - **Telegram (Bot API)**
- Retries failed notifications automatically.
- Can be deployed as a **Docker container**.

## Installation

### Prerequisites

- **Python 3.12+**
- **uv** (for dependency management)
- **Docker** (if running in a container)

## Configuration

The application is configured using **environment variables**. Below are the available options:

### **General Settings**

| Variable                              | Required | Default         | Description                                                                             |
|---------------------------------------|----------|-----------------|-----------------------------------------------------------------------------------------|
| `IPCHECKER_CHECK_INTERVAL`            | ❌        | `30`            | Interval in minutes between IP checks                                                   |
| `IPCHECKER_NOTIFICATION_CHANNELS`     | ❌        | `""`            | Comma-separated list of notification channels (`smtp`, `gotify`, `webhook`, `telegram`) |
| `IPCHECKER_NOTIFICATIONS_MAX_RETRIES` | ❌        | `5`             | Maximum number of retry attempts for failed notifications before giving up              |
| `IPCHECKER_HOSTNAME`                  | ❌        | System hostname | Custom hostname to display in notifications (defaults to system hostname)               |

### **SMTP (Email) Notification**

| Variable                         | Required                                       | Default      | Description                                                                |
|----------------------------------|------------------------------------------------|--------------|----------------------------------------------------------------------------|
| `IPCHECKER_SMTP_SERVER`          | ✅                                              | -            | SMTP server address                                                        |
| `IPCHECKER_SMTP_PORT`            | ✅                                              | -            | SMTP server port                                                           |
| `IPCHECKER_SMTP_SENDER_EMAIL`    | ✅                                              | -            | Sender email address                                                       |
| `IPCHECKER_SMTP_RECIPIENT_EMAIL` | ❌                                              | sender email | Recipient email address                                                    |
| `IPCHECKER_SMTP_PASSWORD`        | ⚠️ (if `IPCHECKER_SMTP_PASSWORD_FILE` not set) | -            | SMTP authentication password                                               |
| `IPCHECKER_SMTP_PASSWORD_FILE`   | ⚠️ (if `IPCHECKER_SMTP_PASSWORD` not set)      | -            | Path to a file containing the SMTP password (takes precedence if provided) |

### **Gotify Notification**

| Variable                      | Required                                      | Default | Description                                |
|-------------------------------|-----------------------------------------------|---------|--------------------------------------------|
| `IPCHECKER_GOTIFY_URL`        | ✅                                             | -       | Gotify server URL                          |
| `IPCHECKER_GOTIFY_TOKEN`      | ⚠️ (if `IPCHECKER_GOTIFY_TOKEN_FILE` not set) | -       | Gotify application token                   |
| `IPCHECKER_GOTIFY_TOKEN_FILE` | ⚠️ (if `IPCHECKER_GOTIFY_TOKEN` not set)      | -       | Path to a file containing the Gotify token |
| `IPCHECKER_GOTIFY_PRIORITY`   | ❌                                             | `10`    | Gotify message priority (1-10)             |

### **Webhook Notification**

| Variable                             | Required                                             | Default | Description                                                                    |
|--------------------------------------|------------------------------------------------------|---------|--------------------------------------------------------------------------------|
| `IPCHECKER_WEBHOOK_URL`              | ✅                                                    | -       | Webhook endpoint URL to send the notification to                               |
| `IPCHECKER_WEBHOOK_METHOD`           | ❌                                                    | `POST`  | HTTP method to use (`POST`, `PUT`, etc.)                                       |
| `IPCHECKER_WEBHOOK_AUTH_HEADER`      | ⚠️ (if `IPCHECKER_WEBHOOK_AUTH_HEADER_FILE` not set) | -       | Full value of the `Authorization` header (e.g. `Bearer abc123`, `Basic xyz==`) |
| `IPCHECKER_WEBHOOK_AUTH_HEADER_FILE` | ⚠️ (if `IPCHECKER_WEBHOOK_AUTH_HEADER` not set)      | -       | Path to a file containing the full `Authorization` header value                |

### **Telegram Notification**

| Variable                            | Required                                            | Default | Description                                                         |
|-------------------------------------|-----------------------------------------------------|---------|---------------------------------------------------------------------|
| `IPCHECKER_TELEGRAM_CHAT_ID`        | ✅                                                   | -       | Telegram chat ID (user, group, or channel) to send messages to      |
| `IPCHECKER_TELEGRAM_BOT_TOKEN`      | ⚠️ (if `IPCHECKER_TELEGRAM_BOT_TOKEN_FILE` not set) | -       | Telegram bot token                                                  |
| `IPCHECKER_TELEGRAM_BOT_TOKEN_FILE` | ⚠️ (if `IPCHECKER_TELEGRAM_BOT_TOKEN` not set)      | -       | Path to a file containing the Telegram bot token (takes precedence) |

> [!NOTE]
> If both a variable and its `_FILE` variant are set, the `_FILE` variant **always takes precedence**.

## Usage

### **Running Locally**

1. Install dependencies:
   ```bash
   uv sync
   ```
2. Set the necessary environment variables.
3. Run the application:
   ```bash
   uv run python -m ip_checker
   ```

### **Running with Docker**

1. Build the Docker image:
   ```bash
   docker build -t ip-checker .
   ```
2. Run the container:
   ```bash
   docker run -e IPCHECKER_CHECK_INTERVAL=30 \
              -e IPCHECKER_NOTIFICATION_CHANNELS="smtp,gotify,webhook,telegram" \
              -e IPCHECKER_SMTP_SERVER="smtp.example.com" \
              -e IPCHECKER_SMTP_PORT="587" \
              -e IPCHECKER_SMTP_SENDER_EMAIL="sender@example.com" \
              -e IPCHECKER_SMTP_PASSWORD="yourpassword" \
              -e IPCHECKER_GOTIFY_URL="https://gotify.example.com" \
              -e IPCHECKER_GOTIFY_TOKEN="your_token" \
              -e IPCHECKER_WEBHOOK_URL="https://hooks.example.com/ip-change" \
              -e IPCHECKER_TELEGRAM_CHAT_ID="123456789" \
              -e IPCHECKER_TELEGRAM_BOT_TOKEN="your_telegram_bot_token" \
              ip-checker
   ```

### **Running with Docker Compose**

Create a `docker-compose.yml` file:

```yaml
version: "3.8"

services:
  ip-checker:
    build: .
    environment:
      IPCHECKER_CHECK_INTERVAL: "30"
      IPCHECKER_NOTIFICATION_CHANNELS: "smtp,gotify,telegram"
      IPCHECKER_SMTP_SERVER: "smtp.example.com"
      IPCHECKER_SMTP_PORT: "587"
      IPCHECKER_SMTP_SENDER_EMAIL: "sender@example.com"
      IPCHECKER_SMTP_PASSWORD: "yourpassword"
      IPCHECKER_GOTIFY_URL: "https://gotify.example.com"
      IPCHECKER_GOTIFY_TOKEN: "your_token"
      IPCHECKER_TELEGRAM_CHAT_ID: "123456789"
      IPCHECKER_TELEGRAM_BOT_TOKEN: "your_telegram_bot_token"
```

Start the service:

```bash
docker compose up -d
```

## Development

### **Setting up the Development Environment**

1. Install dependencies:
   ```bash
   uv sync
   ```
2. Run the application in development mode:
   ```bash
   uv run python -m ip_checker
   ```
