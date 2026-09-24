#1. Initialy import all libraries/packages necessary for the script to run

import requests

import os

import json

from datetime import datetime as dt, timedelta
import time

import logging

import boto3

import glob
import shutil

from dotenv import load_dotenv

import math

import zipfile
import gzip


#2. Create secret key variables and URL variable

load_dotenv() 

amp_api_key = os.getenv("AMP_API_KEY")
amp_secret_key = os.getenv("AMP_SECRET_KEY")

url = 'https://analytics.eu.amplitude.com/api/2/export'

#3. Create local file where data will sit

#Create a folder for our extracted data if it doesn't already exist
#If it finds something called data_dir it is ok
amp_dir = 'amplitude_data'
os.makedirs(amp_dir, exist_ok = True)

#Create a timestamp so each extract gets a unique filename 
timestamp = dt.now().strftime('%Y-%m-%d %H-%M-%S')
filename = f'{amp_dir}/{timestamp}.json'


#4. Create timestamps to extract amount of data

# Get yesterday's date
yesterday = dt.now() - timedelta(days=1)

# Format the start and end time strings
start_time = yesterday.strftime('%Y%m%dT00')
end_time = yesterday.strftime('%Y%m%dT23')


#5. Create time parameters and then also create response variable using URL variable created earlier

params = {
    'start': start_time,
    'end': end_time
}

response = requests.get(url, params=params, auth=(amp_api_key, amp_secret_key))

#6. If statement to ensure status code is working, then from that include 

status = response.status_code

zip_path = f'{amp_dir}/{timestamp}.zip'
extract_dir = f'{amp_dir}/{timestamp}'
extension = ".json.gz"


#6. Check against status code

if status == 200: 
    with open(zip_path, 'wb') as file:
        file.write(response.content)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    # look inside the project-id folder that extractall created
    gz_folder = os.path.join(extract_dir, os.listdir(extract_dir)[0])

    for item in os.listdir(gz_folder):
        if item.endswith(extension):
            file_path = os.path.join(gz_folder, item)     # full path to the file
            out_path = file_path[:-3]                     # chop off ".gz"
            with gzip.open(file_path, 'rb') as f_in:
                with open(out_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(out_path)
else:
    print(status, response.text)

#new folder with unzipped files is where they save 
#add logging in
#add true except