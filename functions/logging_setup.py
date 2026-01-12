# functions/logging_setup.py

import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(debug: bool = False):
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
