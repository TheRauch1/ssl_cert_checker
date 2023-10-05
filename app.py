import ssl
import socket
import os
import schedule
import time
import requests
import logging
import sys
from datetime import datetime

log_level = os.environ.get("DEBUG_LEVEL") if os.environ.get("DEBUG_LEVEL") else "INFO"
match log_level.lower():
    case "debug":
        log_level = logging.DEBUG
    case "info":
        log_level = logging.INFO


logging.basicConfig(stream=sys.stdout, level=log_level, format='%(asctime)s %(levelname)s %(message)s')
logging.info('Started')

def check_ssl_expiry(domain):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
    conn.connect((domain, 443))
    ssl_info = conn.getpeercert()
    conn.close()

    expiry_date = datetime.strptime(ssl_info["notAfter"], r"%b %d %H:%M:%S %Y %Z")
    days_to_expiry = (expiry_date - datetime.utcnow()).days

    logging.debug("------")
    logging.debug(f"domain: {domain}")
    logging.debug(f"expiry date: {expiry_date}")
    logging.debug(f"days to expire: {days_to_expiry}")
    logging.debug("------")


    return days_to_expiry, expiry_date


def send_discord_message(webhook_url, message):
    payload = {"content": message}
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()


def job():
    for domain in domains:
        days_left, expiry_date = check_ssl_expiry(domain)
        if os.environ.get("ENV") == "dev":
            message = f'DEV ENV: SSL certificate for {domain} expires on {expiry_date.strftime("%Y-%m-%d %H:%M:%S")}.'
            send_discord_message(webhook_url, message)
        elif days_left < 7:
            message = f"SSL certificate for {domain} expires in {days_left} days!"
            send_discord_message(webhook_url, message)


if __name__ == "__main__":
    domains = os.environ["DOMAINS"].split(",")
    webhook_url = os.environ["WEBHOOK_URL"]

    logging.info(f"Log level: {log_level}")
    logging.info(f"Domains: {domains}")

    if os.environ.get("ENV") == "dev":
        job()  # Call the job function directly if in dev environment
    else:
        schedule.every().day.at("12:00").do(
            job
        )  # Schedule the job function if not in dev environment
        schedule.every().day.at("16:05").do(
            job
        )  # Schedule the job function if not in dev environment

        while True:
            schedule.run_pending()
            time.sleep(1)
