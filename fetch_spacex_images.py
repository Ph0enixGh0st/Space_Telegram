import argparse
import requests

from importlib.resources import path
from pathlib import Path


def fetch_spacex_images(path="tg_upload_photos_pool", launch_id="latest"):

  launch_data_url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
  launch_data = requests.get(launch_data_url)
  launch_data.raise_for_status()
  launch_data = launch_data.json()
    
  n = 0
  for photo in launch_data['links']["flickr"]["original"]:
  
    file_name = "spacex_" + str(n)
    launch_data = requests.get(photo)
    launch_data.raise_for_status()
    with open(f"{os.path.join(path, file_name)}.jpeg", 'wb') as file:
        file.write(launch_data.content)
    n += 1
    print(f"Here goes Space X photo #{n}")
    

def main():
  
  path = "tg_upload_photos_pool"
  Path(f"{path}").mkdir(parents=True, exist_ok=True)

  parser = argparse.ArgumentParser(
  description='The script downloads photos from SpaceX launches'
  )
  parser.add_argument("-l", "--launch_id", default="latest", help='Enter Space_X launch id here, if none is provided - the latest launch images will be downloaded')
  args = parser.parse_args()
  launch_id = args.launch_id
  
  fetch_spacex_images(path, launch_id)
  print("Task completed")
  

def run_script():
  main()


if __name__ == '__main__':
    main()