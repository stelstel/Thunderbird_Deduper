# functions/process_1_mbox.py

import mailbox
import logging
from collections import Counter
from functions.checksum_generation import get_messages_fingerprint_hashed_list
from functions.replace_mbox_file import write_mbox_file


def process_one_mbox(mbox_path):
    mbox = mailbox.mbox(mbox_path)
    checksums = get_messages_fingerprint_hashed_list(mbox_path)

    seen = set()
    kept_messages = []
    deleted_count = 0

    for message, checksum in zip(mbox, checksums):
        if checksum not in seen:
            seen.add(checksum)
            kept_messages.append(message)
        else:
            deleted_count += 1

    mbox.close()

    if deleted_count > 0:
        write_mbox_file(mbox_path, kept_messages)
        logging.info(
            f"Deleted {deleted_count} duplicate messages from mbox {mbox_path}"
        )

    msg = ""
    
    if deleted_count > 0:
        msg = f"Deleted {deleted_count} duplicate messages from mbox {mbox_path}\n"

    return None, msg, deleted_count
