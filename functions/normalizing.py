# functions/normalizing.py

import re

def normalize(string):
    """
    Normalize a string by converting to lowercase, stripping whitespace, and collapsing multiple spaces.
    Args:
        string (str): The input string to normalize.
    Returns:
        str: The normalized string with lowercase letters, leading/trailing whitespace removed,
             and consecutive whitespace characters replaced with a single space.
    """
    string = string.lower().strip()
    string = re.sub(r"\s+", " ", string)
    
    return string