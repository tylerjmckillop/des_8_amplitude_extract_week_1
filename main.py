from modules.loginitialise import setup_logging
from modules.amplitude_extract_module import extraction
from modules.amplitude_load_module import load
from datetime import datetime as dt
from dotenv import load_dotenv
import os

load_dotenv()

logger = setup_logging('logs', dt.now().strftime('%Y-%m-%d %H-%M-%S'))

extraction = extraction(os.getenv("AMP_API_KEY"), os.getenv("AMP_SECRET_KEY"), 'https://analytics.eu.amplitude.com/api/2/export', 'amplitude_data', dt.now().strftime('%Y-%m-%d %H-%M-%S'), '.json.gz', '.json')

load = load(os.getenv('AWS_ACCESS_KEY'), os.getenv('AWS_SECRET_ACCESS_KEY'), os.getenv('AWS_BUCKET_NAME'), dt.now().strftime('%Y-%m-%d %H-%M-%S'), 'load_log', 'amplitude_data')