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



def calc_duration(start_time, end_time):
    duration = end_time - start_time
    duration_minutes = duration.seconds / 60
    duration_seconds = duration.seconds % 60
    duration_millis = duration.microseconds // 1000
    
    if duration_minutes < 1:
        duration_mins_secs = f"{duration_seconds}.{duration_millis} seconds"
    elif duration_minutes == 1:
        duration_mins_secs = f"1 minute and {duration_seconds}.{duration_millis} seconds"
    else:
        duration_mins_secs = f"{int(duration_minutes)} minutes and {duration_seconds}.{duration_millis} seconds"
    
    return duration_mins_secs

