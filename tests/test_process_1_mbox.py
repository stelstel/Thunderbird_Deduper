from unittest.mock import MagicMock, patch
from functions.process_1_mbox import process_one_mbox


def test_process_one_mbox_removes_duplicates(tmp_path):
    mbox_path = tmp_path / "Inbox"

    msg1 = MagicMock()
    msg2 = MagicMock()
    msg3 = MagicMock()

    messages = [msg1, msg2, msg3]

    fingerprints = [
        "dup",
        "dup",
        "unique",
    ]

    mock_mbox = MagicMock()
    mock_mbox.__iter__.return_value = messages

    with patch("functions.process_1_mbox.mailbox.mbox", return_value=mock_mbox), \
         patch("functions.process_1_mbox.get_one_msg_fingerprint_strict", side_effect=fingerprints), \
         patch("functions.process_1_mbox.write_mbox_file") as mock_write:

        _, msg, deleted = process_one_mbox(str(mbox_path))

    assert deleted == 1
    assert "Deleted 1 duplicate" in msg
    mock_write.assert_called_once()


def test_process_one_mbox_no_duplicates(tmp_path):
    mbox_path = tmp_path / "Inbox"

    msg1 = MagicMock()
    msg2 = MagicMock()

    mock_mbox = MagicMock()
    mock_mbox.__iter__.return_value = [msg1, msg2]

    with patch("functions.process_1_mbox.mailbox.mbox", return_value=mock_mbox), \
         patch("functions.process_1_mbox.get_one_msg_fingerprint_strict", side_effect=["a", "b"]), \
         patch("functions.process_1_mbox.write_mbox_file") as mock_write:

        _, msg, deleted = process_one_mbox(str(mbox_path))

    assert deleted == 0
    assert msg == ""
    mock_write.assert_not_called()
