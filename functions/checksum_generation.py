# functions/checksum_generation.py

import hashlib
import mailbox

from functions.fingerprinting import get_one_msg_fingerprint_simple

def get_one_msg_fingerprint_hashed(message):
    """
    Generate an MD5 hash fingerprint for a single email message.
    This function takes a message object, extracts a simple fingerprint representation
    of it, and returns the hexadecimal digest of its MD5 hash.
    Args:
        message: An email message object to be hashed.
    Returns:
        str: The hexadecimal representation of the MD5 hash of the message fingerprint.
    """
    msg = get_one_msg_fingerprint_simple(message)

    hash_object = hashlib.md5(msg.encode())
    hash_object = hash_object.hexdigest()

    return hash_object



def get_messages_fingerprint_hashed_list(mbox_path):
    """
    Generate a list of hashed fingerprints for all messages in a mailbox file.
    This function opens an mbox file, iterates through all messages, and computes
    a hashed fingerprint for each message to be used for deduplication purposes.
    Args:
        mbox_path (str): The file path to the mbox mailbox file.
    Returns:
        list: A list of hashed fingerprints, one for each message in the mailbox.
    Example:
        >>> fingerprints = get_messages_fingerprint_hashed_list("/path/to/mailbox.mbox")
        >>> print(len(fingerprints))
    """
    
    mbox = mailbox.mbox(mbox_path)
    msgs_hashed_list = []

    for message in mbox:
        msgs_hashed_list.append( get_one_msg_fingerprint_hashed(message) )
    
    return msgs_hashed_list



def get_messages_fingerprint_hashed_str(mbox_path):
    """
    Generate a newline-separated string of hashed message fingerprints from an mbox file.
    This function retrieves a list of hashed message fingerprints from the specified mbox file
    and concatenates them into a single string with each fingerprint on a new line.
    Args:
        mbox_path (str): The file path to the mbox file to process.
    Returns:
        str: A string containing hashed message fingerprints, with each fingerprint
             separated by a newline character. Returns an empty string if no messages
             are found.
    """
    msgs_hashed_str = ""
    msg_list = get_messages_fingerprint_hashed_list(mbox_path)

    for msg in msg_list:
        msgs_hashed_str += msg + "\n"
    
    return msgs_hashed_str