# functions/process_1_mbox.py

import mailbox
import logging

from functions.fingerprinting import get_one_msg_fingerprint_strict, get_one_msg_fingerprint_with_body
from functions.replace_mbox_file import write_mbox_file


def process_one_mbox(mbox_path):
    """
    Process an mbox file to identify and remove duplicate messages.
    Reads all messages from the specified mbox file, compares them using a strict
    fingerprinting method to detect duplicates, and removes any duplicate entries.
    The mbox file is only rewritten if duplicates were found and removed.
    Args:
        mbox_path (str): Path to the mbox file to process.
    Returns:
        tuple: A tuple containing:
            - None: Reserved for potential future use.
            - str: A message describing the action taken. Empty string if no 
              duplicates were found, otherwise a message indicating the number 
              of duplicates deleted.
            - int: The count of duplicate messages that were deleted.
    Side Effects:
        - Logs an info-level message if duplicates were deleted.
        - Overwrites the mbox file if duplicates were removed.
    """
    logger = logging.getLogger(__name__)

    # --- Read all messages first (important!)
    mbox = mailbox.mbox(mbox_path)
    messages = list(mbox)
    mbox.close()

    seen = set()
    kept_messages = []
    deleted_count = 0

    for message in messages:
        # fingerprint = get_one_msg_fingerprint_with_body(message)
        fingerprint = get_one_msg_fingerprint_strict(message)

        if fingerprint not in seen:
            seen.add(fingerprint)
            kept_messages.append(message)
        else:
            deleted_count += 1

    # --- Only rewrite the mailbox if something was deleted
    if deleted_count > 0:
        write_mbox_file(mbox_path, kept_messages)

        logger.info(
            "Deleted %d duplicate messages from mbox %s",
            deleted_count,
            mbox_path
        )

        msg = f"Deleted {deleted_count} duplicate messages from mbox {mbox_path}\n"
    else:
        msg = ""

    return None, msg, deleted_count
