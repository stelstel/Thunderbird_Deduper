# functions/replace_mbox_file.py

import os
import mailbox
import logging
import tempfile
# import time
import shutil



def write_mbox_file(mbox_path, messages):
    directory = os.path.dirname(mbox_path)
    filename = os.path.basename(mbox_path)
    
    # # Remove old file
    # if os.path.exists(mbox_path):
    #     try:
    #         os.remove(mbox_path)
    #     except Exception as e:
    #         logging.exception(f"Error deleting old MBOX file {mbox_path}: {str(e)}")

    with tempfile.NamedTemporaryFile(
        dir=directory,
        delete=False
    ) as tmp:
        tmp_path = tmp.name

    # Wait until the lock file is gone
    # lock_file = mbox_path + ".lock"
    # wait_seconds = 1

    # while os.path.exists(lock_file) and wait_seconds < 10:  # max 10 seconds
    #     time.sleep(0.5)
    #     wait_seconds += 0.5

    # Create new mailbox
    try:
        mbox = mailbox.mbox(tmp_path)
        mbox.lock()
        
        for msg in messages:
            mbox.add(msg)
        
        """
        What flush() does:
            Forces all buffered writes to be written to disk
            Ensures data is physically stored
            Prevents partial mailboxes if program exits early
        """
        mbox.flush()

        mbox.unlock()
        mbox.close()

        # Atomic replace (Windows-safe)
        shutil.move(tmp_path, mbox_path)
    except Exception as e:
        logging.exception(f"Error writing MBOX file {mbox_path}: {str(e)}")

        if os.path.exists(tmp_path):
            os.remove(tmp_path)

        # What raise (with no arguments) does
        # It means:
        # “Re-raise the same exception that brought us here.”
        raise
        


