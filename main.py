#!/usr/bin/env python3
import requests
import dotenv
import os
import logging
import sys


# Get the absolute path of the script in the case that it is symlinked
actual_script_dir = os.path.dirname(os.path.realpath(__file__))

# Specify the path to the .env file
env_path = os.path.join(actual_script_dir, ".env")

# Load the .env file manually
dotenv.load_dotenv(env_path)
# log with timestamp and log to file and console
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/home/lrasmussen/log/notications.log"),
        logging.StreamHandler(),
    ],
)


MM_WEBHOOK_URL = os.getenv("MM_WEBHOOK_URL")


def send_mattermost_message(message):
    """function to send message to mattermost using webhook"""
    if (not MM_WEBHOOK_URL) or (MM_WEBHOOK_URL == ""):
        logging.error("MM_WEBHOOK_URL is not set in environment")
        return
    # if message is a list, join it to a string
    if isinstance(message, list):
        message = " ".join(message)
    response = requests.post(MM_WEBHOOK_URL, json={"text": message})
    return response.status_code


if __name__ == "__main__":
    # check if we have stdin input and use that as message
    if sys.stdin.isatty():
        # we are not piped any input
        # get message from arguments
        message = sys.argv[1:]
    else:
        message = sys.stdin.read()

    # send message to mattermost
    status_code = send_mattermost_message(message)
    if status_code == 200:
        logging.info(f"Message sent to mattermost: {message}")
    else:
        logging.error(f"Failed to send message to mattermost: {message}")
