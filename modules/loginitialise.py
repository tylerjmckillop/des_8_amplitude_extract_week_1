import os
import logging

def setup_logging(dir_name: str, timestamp: str):
    """This will initialise the logger

    Args:
        dir_name (str): Where you want your logs saved
        timestamp (str): The timestamp will be the name of the log file
    """
    os.makedirs(dir_name, exist_ok = True)
    log_filename = f'{dir_name}/{timestamp}.log'

    logging.basicConfig(
        filename = log_filename,
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level = logging.INFO
    )
    return logging.getLogger()
