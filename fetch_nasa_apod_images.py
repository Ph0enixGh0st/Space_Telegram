import argparse
import os
import requests

from dotenv import load_dotenv
from pathlib import Path


def fetch_nasa_apod_images(path, api_key, count=5):

    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    payload = {"api_key": api_key, "count": count}
    nasa_apod_url = "https://api.nasa.gov/planetary/apod"
    nasa_apod_images_pool = requests.get(nasa_apod_url, params=payload)
    nasa_apod_images_pool.raise_for_status()
    nasa_apod_images_pool = nasa_apod_images_pool.json()

    for photo_number, photo in enumerate(nasa_apod_images_pool):

        file_name = f"nasa_{photo_number}"
        url = nasa_apod_images_pool[photo_number]["url"]
        nasa_photo = requests.get(url)
        nasa_photo.raise_for_status()
        with open(f"{os.path.join(path, file_name)}.jpeg", "wb") as file:
            file.write(nasa_photo.content)


def main():

    load_dotenv()

    path = "tg_upload_photos_pool"
    api_key = os.environ["NASA_API_KEY"]
    parser = argparse.ArgumentParser(description="The script downloads photos from NASA APOD API")
    parser.add_argument("-q", "--qty", default=5, help="Enter the photos quantity you want (5 pcs by default).", type=int)
    args = parser.parse_args()
    count = args.qty

    fetch_nasa_apod_images(path, api_key, count)
    print("Task completed")


if __name__ == "__main__":
    main()
