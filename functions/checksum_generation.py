# functions/checksum_generation.py

import hashlib
import mailbox

from functions.fingerprinting import get_one_msg_fingerprint_simple

def get_one_msg_fingerprint_hashed(message):
    """
    Generate an MD5 hash fingerprint for a single email message.
    This function creates a simple fingerprint of a message and then
    converts it to an MD5 hash digest for comparison and deduplication purposes.
    Args:
        message: The message object to generate a fingerprint hash for.
    Returns:
        str: The hexadecimal representation of the MD5 hash of the message fingerprint.
    Example:
        >>> hash = get_one_msg_fingerprint_hashed(email_message)
        >>> print(hash)
        '5d41402abc4b2a76b9719d911017c592'
    """
   
    msg = get_one_msg_fingerprint_simple(message)

    hash_object = hashlib.md5(msg.encode())
    hash_object = hash_object.hexdigest()

    return hash_object



def get_messages_fingerprint_hashed_list(mbox_path):
    """
    Generate a list of hashed fingerprints for all messages in an mbox file.
    Args:
        mbox_path (str): The file path to the mbox file to process.
    Returns:
        list: A list of hashed fingerprints, one for each message in the mbox file.
    Raises:
        FileNotFoundError: If the mbox file does not exist at the specified path.
        mailbox.Error: If the mbox file is corrupted or cannot be read.
    """
    
    
    mbox = mailbox.mbox(mbox_path)
    msgs_hashed_list = []

    for message in mbox:
        msgs_hashed_list.append( get_one_msg_fingerprint_hashed(message) )
    
    return msgs_hashed_list



def get_messages_fingerprint_hashed_str(mbox_path):
    """
    Generate a concatenated string of hashed message fingerprints from an mbox file.
    Args:
        mbox_path (str): The file path to the mbox file to process.
    Returns:
        str: A newline-separated string of hashed message fingerprints from the mbox file.
    """
    msgs_hashed_str = ""
    msg_list = get_messages_fingerprint_hashed_list(mbox_path)

    for msg in msg_list:
        msgs_hashed_str += msg + "\n"
    
    return msgs_hashed_str