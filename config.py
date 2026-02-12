import json
import os

# Path to the config folder
CONFIG_FOLDER = "config"

# Make sure the folder exists
os.makedirs(CONFIG_FOLDER, exist_ok=True)

# Full path to the config file
CONFIG_FILE = os.path.join(CONFIG_FOLDER, "config.json")

DEFAULT_CONFIG = {
    "thunderbird_folder": ""
}



def load_config():
    """
    Load configuration from a JSON file.
    If the configuration file does not exist, creates it with default settings
    and returns the default configuration. Otherwise, reads and parses the
    existing configuration file.
    Returns:
        dict: A dictionary containing the configuration settings loaded from
            the JSON file or the default configuration if the file didn't exist.
    """

    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f) # Reads the JSON content of the file and converts it into a Python dictionary



def save_config(cfg):
    """
    Save configuration dictionary to a JSON file.
    
    Writes the provided configuration dictionary to the CONFIG_FILE path
    as formatted JSON with 4-space indentation.
    
    Args:
        cfg (dict): Configuration dictionary to save.
    
    Returns:
        None
    
    Raises:
        IOError: If the file cannot be written.
        TypeError: If cfg contains non-JSON serializable objects.
    """

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)