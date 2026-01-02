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
    Load configuration from file.
    Checks if the configuration file exists. If not, saves the default 
    configuration and returns it. If the file exists, reads and parses the JSON 
    configuration file and returns it as a dictionary.
    Returns:
        dict: A dictionary containing the configuration settings.
              If the file doesn't exist, returns the default configuration.
    """
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f) # Reads the JSON content of the file and converts it into a Python dictionary

def save_config(cfg):
    """
    Save configuration dictionary to a JSON file.

    Args:
        cfg (dict): Configuration dictionary to save.

    Returns:
        None

    Raises:
        IOError: If the file cannot be written.
        TypeError: If cfg is not JSON serializable.
    """
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)