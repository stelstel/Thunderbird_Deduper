# functions/functions.py

import logging
import psutil



# Global “catch-all”
def log_uncaught_exceptions(exctype, value, tb):
    logging.critical(
        "Uncaught exception",
        exc_info=(exctype, value, tb)
    )



def is_thunderbird_running() -> bool:
    for proc in psutil.process_iter(attrs=["name"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() == "thunderbird.exe":
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

