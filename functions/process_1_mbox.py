# functions/process_1_mbox.py

import mailbox
import logging

from collections import Counter
# from models.mailbox_xxx import Mailbox

from functions.checksum_generation import get_messages_fingerprint_hashed_list
from functions.replace_mbox_file import write_mbox_file



def process_one_mbox(mbox_path):
    msg = ""
    mbox = mailbox.mbox(mbox_path)
    msg_checksums = get_messages_fingerprint_hashed_list(mbox_path)
    counts = Counter(msg_checksums)
    
    delete_these = []

    for checksum, count in counts.items():
        if count > 1: # Duplicate found
            indices = []

            # Loop over the list msg_checksums, and for each item give me both its position (i) and its value (value).
            for i, value in enumerate(msg_checksums):
                if value == checksum:
                    indices.append(i)

            for i in range(count - 1):
                delete_these.append(indices[-1])
                indices.pop() # Keep one copy, remove the rest

    mail_messages_before = len(msg_checksums) 
    
    for index in sorted(delete_these, reverse=True):
        del msg_checksums[index] # Remove the checksum from the list
        del mbox[index]  # Remove the message from the mbox

    mail_messages_after = len(msg_checksums) 
    mail_messages_deleted = mail_messages_before - mail_messages_after
    all_messages = []

    for message in mbox:
        all_messages.append(message)

    mbox.close()
    write_mbox_file(mbox_path, all_messages)

    if mail_messages_deleted > 0:
        logging.info(f"Deleted {mail_messages_deleted} duplicate messages from mbox {mbox_path}")
        msg = f"Deleted {mail_messages_deleted} duplicate messages from mbox {mbox_path}\n"
    
    return mbox, msg, mail_messages_deleted 
