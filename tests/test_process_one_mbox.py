import logging
from unittest.mock import patch, MagicMock

from functions.process_1_mbox import process_one_mbox


def test_process_one_mbox_removes_duplicates(caplog):
    mbox_path = "dummy.mbox"

    # Fake messages
    msg1 = MagicMock(name="msg1")
    msg2 = MagicMock(name="msg2")
    msg3 = MagicMock(name="msg3")

    fake_messages = [msg1, msg2, msg3]

    # First two are duplicates, third is unique
    fake_checksums = ["aaa", "aaa", "bbb"]

    fake_mbox = MagicMock()
    fake_mbox.__iter__.return_value = fake_messages

    with (
        patch("functions.process_1_mbox.mailbox.mbox", return_value=fake_mbox),
        patch(
            "functions.process_1_mbox.get_messages_fingerprint_hashed_list",
            return_value=fake_checksums,
        ),
        patch("functions.process_1_mbox.write_mbox_file") as mock_write,
        caplog.at_level(logging.INFO),
    ):
        _, msg, deleted_count = process_one_mbox(mbox_path)

    # One duplicate should be removed
    assert deleted_count == 1

    # Message text
    assert "Deleted 1 duplicate messages" in msg

    # Only unique messages should be written
    mock_write.assert_called_once()
    args, _ = mock_write.call_args

    assert args[0] == mbox_path
    assert args[1] == [msg1, msg3]  # first duplicate kept, second removed

    # Logging
    assert "Deleted 1 duplicate messages from mbox" in caplog.text
