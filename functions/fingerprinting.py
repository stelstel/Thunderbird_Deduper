# functions/fingerprinting.py

import hashlib
from functions.normalizing import normalize


def get_one_msg_fingerprint_simple(message):
    msg_id = message.get("message-id", "")
    subject = message.get("subject", "")
    sender = message.get("from", "")

    fingerprint = f"{msg_id}|{subject}|{sender}"
    return normalize(fingerprint)


def get_one_msg_fingerprint_with_body(message, body_chars=80):
    """
    Header-based fingerprint + small body snippet
    (fixes the '1 remaining duplicate' issue)
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
    Byte-for-byte fingerprint.
    Absolutely no duplicates can survive this.
    """
    raw = message.as_bytes().replace(b"\r\n", b"\n")
    return hashlib.md5(raw).hexdigest()
