# functions/process_mboxes.py

import logging

from functions.process_1_mbox import process_one_mbox
from PySide6.QtWidgets import QApplication

def process_mboxes(mboxes, progress_bar):
    """
    Process a list of mailbox objects by applying transformations to each.
    Args:
        mboxes (list): A list of mailbox objects to be processed.
    Returns:
        tuple: A tuple containing:
            - mboxes (list): The list of processed mailbox objects.
            - msg_out (str): A concatenated string of messages from processing each mailbox.
    """

    i = 0
    msg_out = ""
    total_messages_deleted = 0
    progress_per_mbox = int((100 - progress_bar.value()) / len(mboxes))

    for mbox in mboxes:
        mbox, msg, messages_deleted = process_one_mbox(mbox)
        mboxes[i] = mbox
        msg_out += msg
        total_messages_deleted += messages_deleted
        progress_bar.setValue(progress_bar.value() + progress_per_mbox)
        QApplication.processEvents()  # Forces GUI update immediately
        i += 1

    logging.info(f"Total duplicate messages deleted across all mailboxes: {total_messages_deleted}")

    return mboxes, msg_out, total_messages_deleted