import argparse
import os
import requests

from pathlib import Path
from urllib.parse import urlencode


def fetch_nasa_apod_images(path, api_key, count):
  
  Path(f"{path}").mkdir(parents=True, exist_ok=True)

  payload = {"api_key": api_key, "count": count}
  nasa_apod_url = "https://api.nasa.gov/planetary/apod"
  response = requests.get(nasa_apod_url, params=payload)
  response.raise_for_status()
  response = response.json()

  n = 0
  
  for photo in response:
    
    file_name = "nasa_" + str(n)
    url = response[n]["url"]
    nasa_photo = requests.get(url)
    nasa_photo.raise_for_status()
    with open(f"{os.path.join(path, file_name)}.jpeg", 'wb') as file:
        file.write(nasa_photo.content)
    n += 1
    print(f"Here goes APOD photo #{n}")


def main(api_key):
  
  parser = argparse.ArgumentParser(
  description='The script downloads photos from NASA APOD API'
  )
  parser.add_argument("-q", "--qty", default=5, help='Enter the photos quantity you want (5 pcs by default).', type=int)
  args = parser.parse_args()
  count = int(args.qty)

  
  fetch_nasa_apod_images("tg_upload_photos_pool\\", api_key, count)
  print("Task completed")


def run_script(api_key):
  main(api_key)


if __name__ == '__main__':
    main()
