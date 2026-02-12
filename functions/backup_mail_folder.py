# functions/backup_mail_folder.py

import datetime
import os
import zipfile

def backup_folder(source_folder, cfg):
    """
    Create a compressed backup of a mail folder.
    Compresses all files and subdirectories from the source folder into a ZIP archive
    and stores it in a local backup directory with a timestamp.
    Args:
        source_folder (str): Path to the mail folder to be backed up.
        cfg (dict): Configuration dictionary containing:
            - "backup_zip_file_compr_level" (str or int): Compression level for the ZIP file (0-9).
    Returns:
        str: Full path to the created ZIP backup file.
    Raises:
        OSError: If the backup directory cannot be created or the source folder is inaccessible.
        zipfile.BadZipFile: If there's an issue creating the ZIP file.
    """
    backup_dir = "mail_folder_backups"
    backup_file_name_start = "ThunderB_Mail_Folder_Backup"
    zip_compression_level = int( cfg["backup_zip_file_compr_level"] )
    os.makedirs(backup_dir, exist_ok = True) # Ensure backup directory exists

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")

    zip_path = os.path.join(
        backup_dir,
        f"{backup_file_name_start}_{timestamp}.zip"
    )

    with zipfile.ZipFile(
        zip_path,
        mode="w",
        compression = zipfile.ZIP_DEFLATED,
        compresslevel = zip_compression_level
    ) as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, source_folder)
                zipf.write(full_path, arcname)

    return zip_path