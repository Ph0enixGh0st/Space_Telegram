import os
import random
import telegram
import time

from dotenv import load_dotenv
from pathlib import Path

import fetch_nasa_apod_images
import fetch_nasa_epic_images
import fetch_spacex_images


def start_spam(bot, tg_channel, timer_delay, photo_path):

    loop_on = True
    files_pool = []

    for root, dirs, files in os.walk(photo_path):
        files_pool = files

    while loop_on:

        for photo in files_pool:

            bot.send_message(chat_id=tg_channel, text=f"uploaded {photo}")
            with open(os.path.join(photo_path, photo), 'rb') as file:
                bot.send_document(chat_id=tg_channel, document=file)
            time.sleep(timer_delay)

        random.shuffle(files_pool)


def main():

    load_dotenv()

    tg_token = os.environ["TG_TOKEN"]
    bot = telegram.Bot(token=tg_token)
    tg_channel = os.environ["TG_CHANNEL"]
    api_key = os.environ["NASA_API_KEY"]
    current_dir = os.getcwd()
    photo_path = os.path.join(current_dir, "tg_upload_photos_pool")
    timer_delay = float(os.environ.get("LOG_INTERVAL"))

    fetch_nasa_apod_images.fetch_nasa_apod_images(photo_path, api_key)
    fetch_nasa_epic_images.get_nasa_epic(photo_path, api_key)
    fetch_spacex_images.fetch_spacex_images()

    start_spam(bot, tg_channel, timer_delay, photo_path)


if __name__ == '__main__':
    main()
