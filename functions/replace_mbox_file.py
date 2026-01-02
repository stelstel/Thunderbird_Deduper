# functions/replace_mbox_file.py

import os
import mailbox
import logging



def write_mbox_file(mbox_path, messages):
    # Remove old file
    if os.path.exists(mbox_path):
        try:
            os.remove(mbox_path)
        except Exception as e:
            # logging.error(f"Error deleting old MBOX file {mbox_path}: {str(e)}")
            logging.exception(f"Error deleting old MBOX file {mbox_path}: {str(e)}")

    # Create new mailbox
    mbox = mailbox.mbox(mbox_path)
    mbox.lock()

    try:
        for msg in messages:
            mbox.add(msg)
        
        """
        What flush() does:
            Forces all buffered writes to be written to disk
            Ensures data is physically stored
            Prevents partial mailboxes if program exits early
        """
        mbox.flush()
    except Exception as e:
        # logging.error(f"Error writing MBOX file {mbox_path}: {str(e)}")
        logging.exception(f"Error writing MBOX file {mbox_path}: {str(e)}")
    finally:
        mbox.unlock()
        mbox.close()


