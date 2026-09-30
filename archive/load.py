#Import the packages required

import os
import boto3
from dotenv import load_dotenv
import logging
from datetime import datetime as dt

# Obtain .env variables
load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Set up S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

# Make a folder for log files if it doesn't already exist

timestamp = dt.now().strftime('%Y-%m-%d %H-%M-%S')

log_dir = 'load_log'
os.makedirs(log_dir, exist_ok = True)
log_filename = f'{log_dir}/{timestamp}.log'


# Configure logging so messages are written to the log file
logging.basicConfig(
    filename = log_filename,
    format = '%(asctime)s - %(levelname)s -%(message)s',
    level = logging.INFO
)

# Create the logger and confirm that is has been successfully set up 
logger = logging.getLogger()
logger.info('Logger successfully initialised')

# Run a dummy upload
# dummy_upload = 'amplitude_data/2026-09-25 16-03-26/clean/100011471_2026-09-24_0#0.json'
# file_name = '100011471_2026-09-24_0#0.json'

# try:
#     s3_client.upload_file(dummy_upload, AWS_BUCKET_NAME, file_name)
#     print("File uploaded")
# except Exception as e:
#     print(f'Error occurred: {e}')

amp_dir = 'amplitude_data'
timestamp = dt.now().strftime('%Y-%m-%d %H-%M-%S')
clean_extract_dir = f'{amp_dir}/clean' 

clean = os.listdir(clean_extract_dir)

for file in clean:
        file_to_upload = f'amplitude_data/clean/{file}'
        try: 
            s3_client.upload_file(file_to_upload, AWS_BUCKET_NAME, file)
            print(f'{file} Uploaded successfully')
            logger.info(f'{file} successfully uploaded')
            os.remove(file_to_upload) # Remove the file
        except Exception as e:
            print(f'An error has occurred: {e}')
            logger.error(f'An error has occured: {e}')