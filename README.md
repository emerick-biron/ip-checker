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
- Retries failed notifications automatically.
- Can be deployed as a **Docker container**.

## Installation

### Prerequisites

- **Python 3.12+**
- **Poetry** (for dependency management)
- **Docker** (if running in a container)

## Configuration

The application is configured using **environment variables**. Below are the available options:

### **General Settings**

| Variable                              | Required | Default | Description                                                                 |
|---------------------------------------|----------|---------|-----------------------------------------------------------------------------|
| `IPCHECKER_CHECK_INTERVAL`            | ❌        | `30`    | Interval in minutes between IP checks                                       |
| `IPCHECKER_NOTIFICATION_CHANNELS`     | ❌        | `""`    | Comma-separated list of notification channels (`smtp`, `gotify`, `webhook`) |
| `IPCHECKER_NOTIFICATIONS_MAX_RETRIES` | ❌        | `5`     | Maximum number of retry attempts for failed notifications before giving up  |

### **SMTP (Email) Notification**

| Variable                         | Required                                       | Default      | Description                                                                |
|----------------------------------|------------------------------------------------|--------------|----------------------------------------------------------------------------|
| `IPCHECKER_SMTP_SERVER`          | ✅                                              |              | SMTP server address                                                        |
| `IPCHECKER_SMTP_PORT`            | ✅                                              |              | SMTP server port                                                           |
| `IPCHECKER_SMTP_SENDER_EMAIL`    | ✅                                              |              | Sender email address                                                       |
| `IPCHECKER_SMTP_RECIPIENT_EMAIL` | ❌                                              | sender email | Recipient email address                                                    |
| `IPCHECKER_SMTP_PASSWORD`        | ⚠️ (if `IPCHECKER_SMTP_PASSWORD` not set)      |              | SMTP authentication password                                               |
| `IPCHECKER_SMTP_PASSWORD_FILE`   | ⚠️ (if `IPCHECKER_SMTP_PASSWORD_FILE` not set) |              | Path to a file containing the SMTP password (takes precedence if provided) |

### **Gotify Notification**

| Variable                      | Required                                 | Default | Description                                |
|-------------------------------|------------------------------------------|---------|--------------------------------------------|
| `IPCHECKER_GOTIFY_URL`        | ✅                                        |         | Gotify server URL                          |
| `IPCHECKER_GOTIFY_TOKEN`      | ❌  ⚠️ (if `IPCHECKER_GOTIFY_TOKEN`)      |         | Gotify application token                   |
| `IPCHECKER_GOTIFY_TOKEN_FILE` | ❌  ⚠️ (if `IPCHECKER_GOTIFY_TOKEN_FILE`) |         | Path to a file containing the Gotify token |
| `IPCHECKER_GOTIFY_PRIORITY`   | ❌                                        | `10`    | Gotify message priority (1-10)             |

### **Webhook Notification**

| Variable                             | Required | Default | Description                                                                    |
|--------------------------------------|----------|---------|--------------------------------------------------------------------------------|
| `IPCHECKER_WEBHOOK_URL`              | ✅        |         | Webhook endpoint URL to send the notification to                               |
| `IPCHECKER_WEBHOOK_METHOD`           | ❌        | `POST`  | HTTP method to use (`POST`, `PUT`, etc.)                                       |
| `IPCHECKER_WEBHOOK_AUTH_HEADER`      | ❌        |         | Full value of the `Authorization` header (e.g. `Bearer abc123`, `Basic xyz==`) |
| `IPCHECKER_WEBHOOK_AUTH_HEADER_FILE` | ❌        |         | Path to a file containing the full `Authorization` header value                |

> **Note**  
> Variables ending with `_FILE` always take precedence over their non-`_FILE` counterparts. If both are set, the `_FILE`
> variant will be used.

## Usage

### **Running Locally**

1. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
2. Set the necessary environment variables.
3. Run the application:
   ```bash
   poetry run python -m ip_checker
   ```

### **Running with Docker**

1. Build the Docker image:
   ```bash
   docker build -t ip-checker .
   ```
2. Run the container:
   ```bash
   docker run -e IPCHECKER_CHECK_INTERVAL=30 \
              -e NOTIFICATION_CHANNELS="smtp,gotify,webhook" \
              -e SMTP_SERVER="smtp.example.com" \
              -e SMTP_PORT="587" \
              -e SMTP_SENDER_EMAIL="sender@example.com" \
              -e SMTP_PASSWORD="yourpassword" \
              -e GOTIFY_URL="https://gotify.example.com" \
              -e GOTIFY_TOKEN="your_token" \
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
      NOTIFICATION_CHANNELS: "smtp,gotify"
      SMTP_SERVER: "smtp.example.com"
      SMTP_PORT: "587"
      SMTP_SENDER_EMAIL: "sender@example.com"
      SMTP_PASSWORD: "yourpassword"
      GOTIFY_URL: "https://gotify.example.com"
      GOTIFY_TOKEN: "your_token"
```

Start the service:

```bash
docker compose up -d
```

## Development

### **Setting up the Development Environment**

1. Install Poetry if not already installed:
   ```bash
   pip install poetry
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run the application in development mode:
   ```bash
   poetry run python -m ip_checker
   ```
