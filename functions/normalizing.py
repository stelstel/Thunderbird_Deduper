# functions/normalizing.py

import re

def normalize(string):
    string = string.lower().strip()
    
    # Replace multiple spaces with a single space
    # Replace all occurrences of pattern in string with replacement
    """
    \s+
    means:
    One or more whitespace characters in a row
    Examples it matches:
    " "
    "\t"
    "\n\n"
    " \t \n "
    """

    string = re.sub(r"\s+", " ", string)
    
    return string