#1. Initialy import all libraries/packages necessary for the script to run

import requests
import os
import json
import time
import logging
import shutil
import math
import zipfile
import gzip
from datetime import datetime as dt, timedelta
from dotenv import load_dotenv

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

yesterday = dt.now() - timedelta(days=1)

start_time = yesterday.strftime('%Y%m%dT00')
end_time = yesterday.strftime('%Y%m%dT23')


#5. Create the logging folder and configure

log_dir = 'log'
os.makedirs(log_dir, exist_ok = True)
log_filename = f"{log_dir}/logging_amplitude_data_{dt.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

logger = logging.getLogger()

#6. Create time parameters and then also create response variable using URL variable created earlier

params = {
    'start': start_time,
    'end': end_time
}

response = requests.get(url, params=params, auth=(amp_api_key, amp_secret_key))

#7. If statement to ensure status code is working, then from that include 

status = response.status_code

zip_path = f'{amp_dir}/{timestamp}.zip'
extract_dir = f'{amp_dir}/{timestamp}'

clean_extract_dir = f'{amp_dir}/{timestamp}/clean'
os.makedirs(clean_extract_dir, exist_ok = True)

extension = ".json.gz"
clean_extension = ".json"

if status == 200:
    try:
        with open(zip_path, 'wb') as file:     
                file.write(response.content)        

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:  
                zip_ref.extractall(extract_dir)  

        gz_folder = os.path.join(extract_dir, os.listdir(extract_dir)[0])

        for item in os.listdir(gz_folder):     
            if item.endswith(extension):        
                file_path = os.path.join(gz_folder, item) 
                out_path = file_path[:-3]                   
                with gzip.open(file_path, 'rb') as f_in:
                    with open(out_path, 'wb') as f_out:  
                        shutil.copyfileobj(f_in, f_out)      
                        print(f'{gz_folder} was successfully saved')
                        logger.info(f'{gz_folder} was successfully saved')
                        
        for item in os.listdir(gz_folder):
            if item.endswith(clean_extension):
                source_path = os.path.join(gz_folder, item)
                clean_path = os.path.join(clean_extract_dir, item)
                shutil.move(source_path, clean_path)
        print(f'{clean_extract_dir} was successfully saved')
        logger.info(f'{clean_extract_dir} was successfully saved')
    except Exception as e:
        print(f'An error has occured: {e}')
        logger.error(f'An error has occured: {e}')
elif status == 400:
     print(f'The size of the exported data is too large. Please shorten the time ranges and try again')
     logger.warning(f'The size of the exported data is too large. Please shorten the time ranges and try again')
elif status == 404:
     print(f'No data available for the time range requested.')
     logger.debug(f'No data available for the time range requested.')
elif status == 504:
     print(f'The amount of data is large causing a timeout. For large amounts of data, use the Amazon S3 destination.')
     logger.debug(f'The amount of data is large causing a timeout. For large amounts of data, use the Amazon S3 destination.')    
else:                     
    print(f'{status} status code. Error. Please fix')
    logger.critical(f'{status} status code. Error. Please fix')


shutil.rmtree(gz_folder)
os.remove(zip_path)
print(f'{gz_folder} and {zip_path} was successfully deleted')
logger.info(f'{gz_folder} and {zip_path} was successfully deleted')