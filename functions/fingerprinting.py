# functions/fingerprinting.py

import hashlib
from functions.normalizing import normalize


def get_one_msg_fingerprint_simple(message):
    """
    Generate a simple fingerprint for an email message.
    This function creates a unique identifier by combining the message ID, subject,
    and sender information. The resulting fingerprint is normalized to ensure
    consistency.
    Args:
        message (dict): A dictionary containing email message headers with keys
            such as "message-id", "subject", and "from".
    Returns:
        str: A normalized fingerprint string composed of message-id, subject, and
            sender separated by pipe characters (|).
    Example:
        >>> msg = {"message-id": "123@example.com", "subject": "Hello", "from": "user@example.com"}
        >>> fingerprint = get_one_msg_fingerprint_simple(msg)
    """
    msg_id = message.get("message-id", "")
    subject = message.get("subject", "")
    sender = message.get("from", "")

    fingerprint = f"{msg_id}|{subject}|{sender}"
    return normalize(fingerprint)


def get_one_msg_fingerprint_with_body(message, body_chars=80):
    """
    Generate a fingerprint for an email message by combining header and body information.
    This function creates a unique identifier for a message by concatenating a header-based
    fingerprint with a normalized excerpt from the message body. It extracts plain text content
    from both simple and multipart messages.
    Args:
        message: An email message object (typically from the email module).
        body_chars (int, optional): The maximum number of characters to extract from the 
                                     message body for the fingerprint. Defaults to 80.
    Returns:
        str: A combined fingerprint string in the format "{header_fingerprint}|{normalized_body}".
             If body extraction fails, returns only the header fingerprint with an empty body section.
    Raises:
        None: Exceptions during body extraction are caught and the body is set to an empty string.
    Note:
        - Extracts the first text/plain part from multipart messages.
        - Normalizes the body content before inclusion in the fingerprint.
        - Decoding errors in the body are ignored, defaulting to replacement characters.
    """
    header_fp = get_one_msg_fingerprint_simple(message)

    body = ""

    try:
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = message.get_payload(decode=True).decode(errors="ignore")
    except Exception:
        body = ""

    body = normalize(body[:body_chars])

    return f"{header_fp}|{body}"


def get_one_msg_fingerprint_strict(message):
    """
    Generate a strict MD5 fingerprint of an email message.
    
    Normalizes the message by converting CRLF line endings to LF,
    then computes and returns the MD5 hash digest as a hexadecimal string.
    This provides a consistent fingerprint for exact message comparison.
    
    Args:
        message: An email message object with an as_bytes() method.
    
    Returns:
        str: The hexadecimal representation of the MD5 hash of the normalized message.
    """
    raw = message.as_bytes().replace(b"\r\n", b"\n")
    return hashlib.md5(raw).hexdigest()
