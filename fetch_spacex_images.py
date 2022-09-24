import argparse
import os
import requests

from importlib.resources import path
from pathlib import Path


def fetch_spacex_images(path="tg_upload_photos_pool", launch_id="latest"):

    spacex_launches_url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    spacex_launches = requests.get(spacex_launches_url)
    spacex_launches.raise_for_status()
    spacex_launches = spacex_launches.json()

    for photo_number, photo in enumerate(spacex_launches["links"]["flickr"]["original"]):

        file_name = f"spacex_{photo_number}"
        spacex_launches = requests.get(photo)
        spacex_launches.raise_for_status()
        with open(f"{os.path.join(path, file_name)}.jpeg", "wb") as file:
            file.write(spacex_launches.content)


def main():

    path = "tg_upload_photos_pool"
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(description="The script downloads photos from SpaceX launches")
    parser.add_argument("-l", "--launch_id", default="latest", help="Enter Space_X launch id here")
    args = parser.parse_args()
    launch_id = args.launch_id

    fetch_spacex_images(path, launch_id)
    print("Task completed")


if __name__ == "__main__":
    main()
