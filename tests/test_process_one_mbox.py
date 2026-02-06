import mailbox
from unittest.mock import patch, MagicMock

from functions.process_1_mbox import process_one_mbox


def test_process_one_mbox_removes_duplicates(tmp_path):
    # --- Arrange -------------------------------------------------

    # Fake mbox path
    mbox_path = tmp_path / "Inbox"

    # Create fake email messages
    msg1 = MagicMock()
    msg2 = MagicMock()
    msg3 = MagicMock()

    messages = [msg1, msg2, msg3]

    # Fake fingerprints:
    # msg1 and msg2 are duplicates, msg3 is unique
    fingerprints = [
        "fp-duplicate",
        "fp-duplicate",
        "fp-unique",
    ]

    # Mock mailbox.mbox to return our fake messages
    mock_mbox = MagicMock()
    mock_mbox.__iter__.return_value = messages

    with patch("functions.process_1_mbox.mailbox.mbox", return_value=mock_mbox), \
         patch(
             "functions.process_1_mbox.get_one_msg_fingerprint_with_body",
             side_effect=fingerprints,
         ), \
         patch("functions.process_1_mbox.write_mbox_file") as mock_write:

        # --- Act --------------------------------------------------
        _, msg, deleted_count = process_one_mbox(str(mbox_path))

        # --- Assert ----------------------------------------------
        assert deleted_count == 1
        assert "Deleted 1 duplicate" in msg

        # write_mbox_file should be called once
        mock_write.assert_called_once()

        # Extract arguments passed to write_mbox_file
        called_path, kept_messages = mock_write.call_args[0]

        assert called_path == str(mbox_path)
        assert kept_messages == [msg1, msg3]



def test_process_one_mbox_no_duplicates(tmp_path):
    print("Testing process_one_mbox with no duplicates...") #////////////////////////////////////////////
    mbox_path = tmp_path / "Inbox"

    msg1 = MagicMock()
    msg2 = MagicMock()

    messages = [msg1, msg2]

    mock_mbox = MagicMock()
    mock_mbox.__iter__.return_value = messages

    with patch("functions.process_1_mbox.mailbox.mbox", return_value=mock_mbox), \
         patch(
             "functions.process_1_mbox.get_one_msg_fingerprint_with_body",
             side_effect=["fp1", "fp2"],
         ), \
         patch("functions.process_1_mbox.write_mbox_file") as mock_write:

        _, msg, deleted_count = process_one_mbox(str(mbox_path))

        assert deleted_count == 0
        assert msg == ""
        mock_write.assert_not_called()
