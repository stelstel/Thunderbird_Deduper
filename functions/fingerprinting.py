# functions/fingerprinting.py

import mailbox

from functions.normalizing import normalize



def get_one_msg_fingerprint_simple(message):
    """
    Generate a unique fingerprint for an email message.
    Creates a concatenated string fingerprint from key message attributes
    (message ID, subject, sender, and date) to identify and distinguish
    individual messages.
    Args:
        message (dict): A dictionary containing email message headers with
            at minimum the following optional keys:
            - "message-id" (str): The unique message identifier
            - "subject" (str): The email subject line
            - "from" (str): The sender's email address
            - "date" (str): The message date
    Returns:
        str: A pipe-delimited fingerprint string in the format:
            "{message-id}|{subject}|{sender}|{date}"
    Example:
        >>> msg = {"message-id": "123", "subject": "Test", "from": "user@example.com", "date": "2024-01-01"}
        >>> get_one_msg_fingerprint(msg)
        '123|Test|user@example.com|2024-01-01'
    """
    msg_id = message.get("message-id", "")
    subject = message.get("subject", "")
    sender = message.get("from", "")
    date = message.get("date", "")
    fingerprint = f"{msg_id}|{subject}|{sender}|{date}"
    fingerprint = normalize(fingerprint)

    return fingerprint