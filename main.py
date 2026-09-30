from modules.loginitialise import setup_logging
# from modules.bikepoint_extract_modularised import extract 
# from modules.bikepoint_load_modularised import load_files_to_s3
from datetime import datetime as dt
from dotenv import load_dotenv
import os

load_dotenv()

logger = setup_logging('logs', dt.now().strftime('%Y-%m-%d %H-%M-%S'))