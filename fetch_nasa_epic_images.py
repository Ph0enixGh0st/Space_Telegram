import argparse
import os
import requests

from pathlib import Path
from urllib.parse import urlencode


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
      
      image_name_response = requests.get(nasa_epic_url_blank, params=payload)
      image_name_response.raise_for_status()
      image_name_response = image_name_response.json()
      image_name = image_name_response[0]["image"]
      
           
      single_date = single_date.replace("-", "/")
            
      nasa_epic_url = f"https://api.nasa.gov/EPIC/archive/natural/{single_date}/png/{image_name}.png"
      nasa_epic_photo = requests.get(nasa_epic_url, params=payload)
      nasa_epic_photo.raise_for_status()
      file_name = f"nasa_epic_{cycle_count}"
      

      with open(f"{path}/{file_name}.png", 'wb') as file:
        file.write(nasa_epic_photo.content)
      
      cycle_count += 1
      
      print(f"Here goes EPIC photo #{cycle_count}")



def main(api_key):
    
  parser = argparse.ArgumentParser(
  description='The script downloads photos from NASA EPIC API'
  )
  parser.add_argument("-q", "--qty", default=15, help='How many photos you want to download? Q-ty is 10 by default', type=int)
  args = parser.parse_args()
  count = int(args.qty)
    
  current_dir = os.getcwd()
  path = os.path.join(current_dir, "tg_upload_photos_pool")

  Path(f"{path}").mkdir(parents=True, exist_ok=True)

  get_nasa_epic(path, api_key, count)

  print("Task completed")


def run_script(api_key):
  main(api_key)


if __name__ == '__main__':
    main()