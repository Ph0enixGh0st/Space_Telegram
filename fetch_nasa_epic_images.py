import argparse
import os
import requests

from dotenv import load_dotenv
from pathlib import Path


def get_nasa_epic(path, api_key, count=15):

    payload = {"api_key": api_key}
    nasa_epic_all_photo_dates_url = "https://api.nasa.gov/EPIC/api/natural/all"
    all_dates_response = requests.get(nasa_epic_all_photo_dates_url, params=payload)
    all_dates_response = all_dates_response.json()

    cycle_count = 0

    for date in all_dates_response:

        while cycle_count < count:

            single_date = all_dates_response[cycle_count]["date"]
            nasa_epic_url_blank = f"https://api.nasa.gov/EPIC/api/natural/date/{single_date}"

            image_name_pool = requests.get(nasa_epic_url_blank, params=payload)
            image_name_pool.raise_for_status()
            image_name_pool = image_name_pool.json()
            image_name = image_name_pool[0]["image"]

            single_date = single_date.replace("-", "/")

            nasa_epic_url = f"https://api.nasa.gov/EPIC/archive/natural/{single_date}/png/{image_name}.png"
            nasa_epic_photo = requests.get(nasa_epic_url, params=payload)
            nasa_epic_photo.raise_for_status()
            file_name = f"nasa_epic_{cycle_count}"

            with open(f"{os.path.join(path, file_name)}.png", "wb") as file:
                file.write(nasa_epic_photo.content)
            cycle_count += 1


def main():

    load_dotenv()

    api_key = os.environ["NASA_API_KEY"]
    parser = argparse.ArgumentParser(description="The script downloads photos from NASA EPIC API")
    parser.add_argument("-q", "--qty", default=15, help="How many photos you want to download? Q-ty is 10 by default", type=int)
    args = parser.parse_args()
    count = args.qty
    current_dir = os.getcwd()
    path = os.path.join(current_dir, "tg_upload_photos_pool")
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    get_nasa_epic(path, api_key, count)


if __name__ == '__main__':
    main()
