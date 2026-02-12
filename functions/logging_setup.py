# functions/logging_setup.py

import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(debug: bool = False):
    """
    Configure the root logger with a rotating file handler.
    Sets up logging to write to a file with automatic rotation when it reaches 2 MB.
    Creates a logs directory if it doesn't exist and configures the logging format
    to include timestamp, log level, and message.
    Args:
        debug (bool, optional): If True, sets logging level to DEBUG. 
                               If False, sets logging level to INFO. Defaults to False.
    Returns:
        None
    Side Effects:
        - Creates a 'logs' directory in the current working directory if it doesn't exist
        - Configures the root logger with a RotatingFileHandler
        - Adds a handler to the root logger if one doesn't already exist
        - Log file is created at 'logs/thunderbird_deduper.log'
        - Rotated backup logs are kept up to a maximum of 5 files
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "thunderbird_deduper.log")

    handler = RotatingFileHandler(
        log_file,
        maxBytes = 2 * 1024 * 1024,  # 2 MB
        backupCount = 5,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler.setFormatter(formatter)

    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        logger.addHandler(handler)
