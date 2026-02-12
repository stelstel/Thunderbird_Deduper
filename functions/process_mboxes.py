# functions/process_mboxes.py

import logging

from functions.process_1_mbox import process_one_mbox
from PySide6.QtWidgets import QApplication

def process_mboxes(mboxes, progress_bar):
    """
    Process multiple mailboxes to remove duplicate messages.
    Args:
        mboxes (list): A list of mailbox objects to be processed for duplicate removal.
        progress_bar (QProgressBar): A GUI progress bar widget to display processing progress.
    Returns:
        tuple: A tuple containing:
            - mboxes (list): The updated list of mailbox objects after duplicate removal.
            - msg_out (str): Concatenated messages/output from processing each mailbox.
            - total_messages_deleted (int): The total count of duplicate messages deleted across all mailboxes.
    Notes:
        - Progress is incremented equally across all mailboxes.
        - GUI events are processed after each mailbox to ensure responsive UI updates.
        - Results are logged to the logging system.
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