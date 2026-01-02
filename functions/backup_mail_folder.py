# functions/backup_mail_folder.py

import shutil
import datetime
import os

def backup_folder(source_folder):
    """
    Create a timestamped backup of a mail folder as a ZIP archive.
    Args:
        source_folder (str): The path to the mail folder to be backed up.
    Returns:
        str: The full path to the created ZIP archive file.
    Raises:
        OSError: If the backup directory cannot be created or the archive cannot be written.
    Notes:
        - Backup files are stored in a 'backups' directory relative to the current working directory.
        - Each backup is named with the pattern 'ThunderB_Mail_Folder_Backup_YYYYMMDD_HH_MM_SS.zip'.
        - The function creates the backup directory if it does not already exist.
    """
    backup_dir = "mail_folder_backups"
    os.makedirs(backup_dir, exist_ok = True) # Ensure backup directory exists
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")
    backup_name = f"ThunderB_Mail_Folder_Backup_{timestamp}"
    backup_path = os.path.join(backup_dir, backup_name)

    # Creates: backup_path + ".zip"
    zip_file = shutil.make_archive(backup_path, "zip", source_folder)

    return zip_file