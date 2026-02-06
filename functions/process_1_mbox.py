# functions/process_1_mbox.py

import mailbox
import logging

from functions.fingerprinting import get_one_msg_fingerprint_strict, get_one_msg_fingerprint_with_body
from functions.replace_mbox_file import write_mbox_file


def process_one_mbox(mbox_path):
    """
    Removes duplicate messages from a single mbox file.
    Duplicates are detected using a fingerprint consisting of
    headers + a small body snippet.
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
