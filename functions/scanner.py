import os

from functions.parser import get_messages_from_mbox


def find_mbox_files(root_folder: str, exclude_trash_files: bool):
    """
    Recursively search for MBOX format files within a directory tree.
    This function walks through all subdirectories of the specified root folder
    and identifies files that follow the MBOX format by checking if they contain
    lines starting with "From " in their first 10 lines.
    Args:
        root_folder (str): The root directory path to start searching from.
        exclude_trash_files (bool): If True, excludes files and directories
            containing "trash" in their name or path (case-insensitive).
    Returns:
        list: A list of absolute file paths (str) that match the MBOX format criteria.
    Note:
        - Skips files with .msf extension, hidden files (starting with "."),
          and desktop.ini files.
        - Handles encoding errors gracefully by ignoring them.
        - Silently continues on any file read exceptions.
    """
    mbox_files = []

    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".msf") or filename.startswith(".") or filename.lower() == "desktop.ini":
                continue

            if exclude_trash_files:
                if "trash" in filename.lower() or "trash" in dirpath.lower():
                    continue

            full_path = os.path.join(dirpath, filename)

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    for _ in range(10):
                        line = f.readline()
                        if not line:
                            break
                        if line.startswith("From "):
                            mbox_files.append(full_path)
                            break
            except Exception:
                continue

    return mbox_files


def parse_all_mailboxes(folder, exclude_trash_files=True):
    """
    Parse all mailbox files in a given folder and count the total number of messages.
    Args:
        folder (str): The path to the folder containing mailbox files.
        exclude_trash_files (bool, optional): Whether to exclude trash-related files from parsing.
            Defaults to True.
    Returns:
        int: The total number of messages found across all mailbox files in the folder.
    """
    mbox_files = find_mbox_files(folder, exclude_trash_files)

    total_messages = 0
    for mbox_file in mbox_files:
        messages = get_messages_from_mbox(mbox_file)
        total_messages += len(messages)

    return total_messages