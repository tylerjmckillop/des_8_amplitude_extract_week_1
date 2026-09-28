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

# Run a dummy upload
dummy_upload = '\2026-09-25 16-03-26\clean\100011471_2026-09-24_0#0.json'
file_name = '100011471_2026-09-24_0#0.json'

try:
    s3_client.upload_file(dummy_upload, AWS_BUCKET_NAME, file_name)
    print("File uploaded")
except Exception as e:
    print(f'Error occurred: {e}')