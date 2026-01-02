# functions/scanner.py

import os

from functions.parser import get_messages_from_mbox

def find_mbox_files(root_folder: str):
    """
    Recursively search for MBOX format email files in a directory tree.
    Scans the specified root folder and all subdirectories for MBOX files,
    identifying them by checking if they contain lines starting with "From "
    (a characteristic header of MBOX format). Skips summary files (.msf),
    hidden files (starting with '.'), and system files (desktop.ini).
    Args:
        root_folder (str): The root directory path to start searching from.
    Returns:
        list: A list of absolute file paths (str) to all identified MBOX files.
              Returns an empty list if no MBOX files are found.
    Note:
        Files that cannot be read are silently skipped. The function uses
        UTF-8 encoding with errors ignored to attempt reading files.
    """

    mbox_files = []

    for dirpath, dirnames, filenames in os.walk(root_folder): # we don’t use dirnames, but Python requires us to capture it.
        """
        os.walk() recursively walks through the folder:
            dirpath → current folder
            dirnames → subfolders
            filenames → files in that folder
        """

        for filename in filenames:
            # Skip summary/index files and hidden/system files
            if filename.endswith(".msf") or filename.startswith(".") or filename.lower() == "desktop.ini":
                continue

            # Skip Trash folders
            if "trash" in filename.lower() or "trash" in dirpath.lower():
                continue

            full_path = os.path.join(dirpath, filename)

            # Check if the file looks like an MBOX by reading first few lines
            try:
                f = open(full_path, "r", encoding="utf-8", errors="ignore")
                first_lines = []

                for i in range(10):
                    line = f.readline()

                    if not line:
                        break

                    first_lines.append(line)

                f.close()

                # Check if any of the lines starts with "From "
                found_from = False

                for line in first_lines:
                    if line.startswith("From "):
                        found_from = True
                        break

                if found_from:
                    mbox_files.append(full_path)

            except Exception:
                # Skip files we can't read
                continue

    return mbox_files

# def parse_all_mailboxes(mbox_files):
def parse_all_mailboxes(folder):
    mbox_files = find_mbox_files(folder)

    total_messages = 0
    
    for mbox_file in mbox_files:
        messages = get_messages_from_mbox(mbox_file)
        total_messages += len(messages)