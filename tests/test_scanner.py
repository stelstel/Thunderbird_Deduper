import os
from unittest.mock import patch, mock_open

from functions.scanner import find_mbox_files


def test_find_mbox_files_detects_valid_mbox():
    fake_walk = [
        ("root", [], ["Inbox", "notes.txt", "archive.msf"]),
    ]

    mbox_content = (
        "From user@example.com Sat Jan 01 00:00:00 2022\n"
        "Subject: Test\n"
        "\n"
        "Hello\n"
    )

    with patch("functions.scanner.os.walk", return_value=fake_walk), \
         patch("builtins.open", mock_open(read_data=mbox_content)):

        result = find_mbox_files("root", exclude_trash_files=False)

    assert os.path.join("root", "Inbox") in result
    assert os.path.join("root", "notes.txt") in result
    assert len(result) == 2
    


def test_find_mbox_files_ignores_files_without_from_line():
    fake_walk = [
        ("root", [], ["file1", "file2"]),
    ]

    non_mbox_content = "Just some text\nAnother line\n"

    with patch("functions.scanner.os.walk", return_value=fake_walk), \
         patch("builtins.open", mock_open(read_data=non_mbox_content)):

        result = find_mbox_files("root", exclude_trash_files=False)

    assert result == []


def test_find_mbox_files_excludes_trash_when_enabled():
    fake_walk = [
        ("root", [], ["Inbox", "Trash"]),
    ]

    mbox_content = "From someone@example.com\nBody\n"

    with patch("functions.scanner.os.walk", return_value=fake_walk), \
         patch("builtins.open", mock_open(read_data=mbox_content)):

        result = find_mbox_files("root", exclude_trash_files=True)

    assert os.path.join("root", "Inbox") in result
    assert os.path.join("root", "Trash") not in result