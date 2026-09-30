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

logger = logging.getLogger(__name__)

def extraction(amp_api_key: str, amp_secret_key: str, url: str, amp_dir: str, timestamp: str, extension: str, clean_extension: str):

    os.makedirs(amp_dir, exist_ok = True)

    filename = f'{amp_dir}/{timestamp}.json'

    yesterday = dt.now() - timedelta(days=1)

    start_time = yesterday.strftime('%Y%m%dT00')
    end_time = yesterday.strftime('%Y%m%dT23')

    params = {
        'start': start_time,
        'end': end_time
    }

    response = requests.get(url, params=params, auth=(amp_api_key, amp_secret_key))

    status = response.status_code

    zip_path = f'{amp_dir}/{timestamp}.zip'
    extract_dir = f'{amp_dir}/{timestamp}'

    clean_extract_dir = f'{amp_dir}/clean'
    os.makedirs(clean_extract_dir, exist_ok = True)

    if status == 200:
        try:
            with open(zip_path, 'wb') as file:     
                    file.write(response.content)        

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:  
                    zip_ref.extractall(extract_dir)  

            gz_folder = os.path.join(extract_dir, os.listdir(extract_dir)[0])

            # Unzip each .gz file (no printing here, these are temp files)
            for item in os.listdir(gz_folder):
                if item.endswith(extension):
                    file_path = os.path.join(gz_folder, item)
                    out_path = file_path[:-3]
                    with gzip.open(file_path, 'rb') as f_in:
                        with open(out_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)

            today = dt.now().strftime('%Y-%m-%d')

            for item in os.listdir(gz_folder):
                if item.endswith(clean_extension):
                    project_id, data_date, hour = item.split('_', 2)
                    new_name = f'{project_id}_{today}_{hour}'
                    source_path = os.path.join(gz_folder, item)
                    clean_path = os.path.join(clean_extract_dir, new_name)
                    shutil.move(source_path, clean_path)
                    print(f'{new_name} was successfully saved')
                    logger.info(f'{new_name} was successfully saved')

            print(f'{clean_extract_dir} was successfully saved')
            logger.info(f'{clean_extract_dir} was successfully saved')

            shutil.rmtree(extract_dir)
            os.remove(zip_path)
            print(f'{extract_dir} and {zip_path} was successfully deleted')
            logger.info(f'{extract_dir} and {zip_path} was successfully deleted')
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