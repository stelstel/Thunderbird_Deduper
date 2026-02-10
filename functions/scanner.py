import os

from functions.parser import get_messages_from_mbox


def find_mbox_files(root_folder: str, exclude_trash_files: bool):
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
    mbox_files = find_mbox_files(folder, exclude_trash_files)

    total_messages = 0
    for mbox_file in mbox_files:
        messages = get_messages_from_mbox(mbox_file)
        total_messages += len(messages)

    return total_messages