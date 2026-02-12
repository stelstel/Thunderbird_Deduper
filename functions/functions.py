# functions/functions.py

import logging
import psutil
import os



# Global “catch-all”
def log_uncaught_exceptions(exctype, value, tb):
    """
    Log uncaught exceptions at the critical level.

    This function is designed to be used as a custom exception hook with
    sys.excepthook to ensure all uncaught exceptions are properly logged
    before the program terminates.

    Args:
        exctype (type): The exception type/class.
        value (Exception): The exception instance.
        tb (traceback): The traceback object associated with the exception.

    Returns:
        None
    """
    logging.critical(
        "Uncaught exception",
        exc_info=(exctype, value, tb)
    )



def is_thunderbird_running() -> bool:
    """
    Check if Thunderbird is currently running on the system.

    This function iterates through all active processes and checks if any of them
    is the Thunderbird email client (thunderbird.exe). It handles cases where processes
    may terminate or become inaccessible during iteration.

    Returns:
        bool: True if Thunderbird is running, False otherwise.

    Raises:
        None: Exceptions from process iteration are caught and suppressed.

    Example:
        >>> if is_thunderbird_running():
        ...     print("Thunderbird is currently running")
        ... else:
        ...     print("Thunderbird is not running")
    """
    for proc in psutil.process_iter(attrs=["name"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() == "thunderbird.exe":
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False



def calc_duration(start_time, end_time):
    """
    Calculate the duration between two datetime objects and format it as a human-readable string.
    Args:
        start_time (datetime): The start time as a datetime object.
        end_time (datetime): The end time as a datetime object.
    Returns:
        str: A formatted string representing the duration in the format:
            - "X.Y seconds" if duration is less than 1 minute
            - "1 minute and X.Y seconds" if duration is exactly 1 minute
            - "X minutes and Y.Z seconds" if duration is more than 1 minute
            where X is minutes/seconds, Y is seconds, and Z is milliseconds.
    """
    duration = end_time - start_time
    duration_minutes = duration.seconds // 60
    duration_seconds = duration.seconds % 60
    duration_millis = duration.microseconds // 1000
    
    if duration_minutes < 1:
        duration_mins_secs = f"{duration_seconds}.{duration_millis} seconds"
    elif duration_minutes == 1:
        duration_mins_secs = f"1 minute and {duration_seconds}.{duration_millis} seconds"
    else:
        duration_mins_secs = f"{int(duration_minutes)} minutes and {duration_seconds}.{duration_millis} seconds"
    
    return duration_mins_secs



def format_size(bytes_size):
    """
    Convert a byte size into a human-readable format.
    
    Converts a numeric byte value into a formatted string with appropriate
    units (B, KB, MB, GB, TB, or PB). The conversion divides by 1024 at each
    step until the size is less than 1024 or the largest unit is reached.
    
    Args:
        bytes_size (int or float): The size in bytes to format.
    
    Returns:
        str: A formatted string with the size and unit (e.g., "1.50 MB").
    
    Examples:
        >>> format_size(512)
        '512.00 B'
        >>> format_size(1048576)
        '1.00 MB'
        >>> format_size(1099511627776)
        '1.00 TB'
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} PB"  # unlikely to reach here

