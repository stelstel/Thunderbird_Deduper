# functions/backup_mail_folder.py

# import shutil # ////////////////////////////////////////////////// Not used?
import datetime
import os
import zipfile

def backup_folder(source_folder):
    backup_dir = "mail_folder_backups"
    backup_file_name_start = "ThunderB_Mail_Folder_Backup"
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
        compresslevel = 9   # ← balance of speed & size (1-9. 9 is strongest compression but slowest) This should be dynamic in future.
    ) as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, source_folder)
                zipf.write(full_path, arcname)

    return zip_path