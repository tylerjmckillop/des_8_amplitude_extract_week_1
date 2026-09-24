#1. Initialy import all libraries/packages necessary for the script to run

import requests

import os

import json

from datetime import datetime as dt, timedelta
import time

import logging

import boto3

from dotenv import load_dotenv

import math


#2. Create secret key variables 

load_dotenv() 

amp_api_key = os.getenv("AMP_API_KEY")
amp_secret_key = os.getenv("AMP_SECRET_KEY")
print(amp_api_key)
print(amp_secret_key)

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
print(start_time)
print(end_time)




