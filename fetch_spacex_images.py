import argparse
import requests

from importlib.resources import path
from pathlib import Path


def fetch_spacex_images(path = "tg_upload_photos_pool\\", id="latest"):

  launch_data_url = f"https://api.spacexdata.com/v5/launches/{id}"
  launch_data = requests.get(launch_data_url)
  launch_data = launch_data.json()
  launch_data.raise_for_status()
  
  n = 0
  for photo in launch_data['links']["flickr"]["original"]:
  
    file_name = "spacex_" + str(n)
    launch_data = requests.get(photo)
    launch_data.raise_for_status()
    with open(f"{path}/{file_name}.jpeg", 'wb') as file:
        file.write(launch_data.content)
    n += 1
    print(f"Here goes Space X photo #{n}")
    

def main():
  
  path = "tg_upload_photos_pool\\"
  Path(f"{path}").mkdir(parents=True, exist_ok=True)

  parser = argparse.ArgumentParser(
  description='The script downloads photos from SpaceX launches'
  )
  parser.add_argument("-l", "--launch_id", help='Enter Space_X launch id here')
  args = parser.parse_args()
  if args.launch_id is not None:
    launch_id = args.launch_id
  else:
    launch_id = "latest"
  
  fetch_spacex_images("tg_upload_photos_pool\\", launch_id)
  print("Task completed")
  

if __name__ == '__main__':
    main()
