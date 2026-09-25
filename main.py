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


# Create logging folder and then file path

log_dir = 'log'
os.makedirs(log_dir, exist_ok = True)
log_filename = f'{amp_dir}/{timestamp}.json'


# Configure the logging
log_filename = f"logs/logging_amplitude_data_{dt.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

# Create the logger
logger = logging.getLogger()
logger.info('Logger successfully initialised')

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

clean_extract_dir = f'{amp_dir}/{timestamp}/clean'
os.makedirs(clean_extract_dir, exist_ok = True)

extension = ".json.gz"
clean_extension = ".json"

#6. While loop and check against status code
max_retry = 5
attempt = 0
delay = 10

while attempt < max_retry:

    if status == 200:
    #Creating and open the file on disk at zip_path in write-binary mode
        with open(zip_path, 'wb') as file:     
            file.write(response.content)        
        #Write the downloaded raw bytes into that file, this is saving the zip

    #Need to open the zip file and unzip everything inside it into the extract_dir
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:  
            zip_ref.extractall(extract_dir)   
        #Sub-folder created and then we
        #grab that subfolder's full path so we can look inside it
        gz_folder = os.path.join(extract_dir, os.listdir(extract_dir)[0])

        for item in os.listdir(gz_folder):     #Loop through every filename inside that subfolder
            if item.endswith(extension):        #Only process files ending in ".json.gz", skip everything else
                file_path = os.path.join(gz_folder, item)  #Build the full path to this .json.gz file
                out_path = file_path[:-3]                   #Same path, minus the last 3 chars (".gz"), which then becomes the output filename

                with gzip.open(file_path, 'rb') as f_in:    #Open the .gz file for reading, with gzip decompressing it as we read
                    with open(out_path, 'wb') as f_out:      #Create the new decompressed output file
                        shutil.copyfileobj(f_in, f_out)       #Stream the decompressed bytes from f_in into f_out


        for item in os.listdir(gz_folder):
            if item.endswith(clean_extension):
                source_path = os.path.join(gz_folder, item)
                clean_path = os.path.join(clean_extract_dir, item)
                shutil.move(source_path, clean_path)
                         
    else:
        print(status, response.text)  #Rquest failed, so print the status code and error message for debugging

shutil.rmtree(gz_folder)
os.remove(zip_path)
#add logging in
#add true except