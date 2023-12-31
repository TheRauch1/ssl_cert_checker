# ssl_checker

A simple Python script to check SSL certificates for a list of domains and send notifications to Discord via a webhook if the certificate is about to expire.

## Installation

1. Clone the repository
2. Install the required packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Set the following environment variables:
- `DOMAINS`: Comma-separated list of domains to check SSL certificates for
- `WEBHOOK_URL`: Discord webhook URL to send notifications to
- `CHECK_DAILY_AT`: Time of day to check certificates at (in 24-hour format, e.g. `14:00`). Defaults to `12:00`
- `ENV`: Set to `dev` if running in development environment
- `LOG_LEVEL`: Set to `DEBUG` if running in development environment
2. Run the script:
    ```bash
    python main.py
    ```

## Docker Usage
```bash
   docker build -t ssl-checker .
```

```bash
   docker run -d \
    --name ssl-checker \
    -e DOMAINS=example.com,example2.com \
    -e WEBHOOK_URL=https://discord.com/api/webhooks/123/abc \
    ssl-checker
```
