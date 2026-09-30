#Import the packages required

import os
import boto3
from dotenv import load_dotenv
import logging
from datetime import datetime as dt

logger = logging.getLogger(__name__)

def load(AWS_ACCESS_KEY: str, AWS_SECRET_ACCESS_KEY: str, AWS_BUCKET_NAME: str, timestamp: str, log_dir: str, amp_dir: str):

    s3_client = boto3.client(
        's3',
        aws_access_key_id = AWS_ACCESS_KEY,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )

    os.makedirs(log_dir, exist_ok = True)
    log_filename = f'{log_dir}/{timestamp}.log'

    logging.basicConfig(
        filename = log_filename,
        format = '%(asctime)s - %(levelname)s -%(message)s',
        level = logging.INFO
    )

    clean_extract_dir = f'{amp_dir}/clean' 
    clean = os.listdir(clean_extract_dir)

    for file in clean:
            file_to_upload = f'amplitude_data/clean/{file}'
            try: 
                s3_client.upload_file(file_to_upload, AWS_BUCKET_NAME, file)
                print(f'{file} Uploaded successfully')
                logger.info(f'{file} successfully uploaded')
                os.remove(file_to_upload)
            except Exception as e:
                print(f'An error has occurred: {e}')
                logger.error(f'An error has occured: {e}')