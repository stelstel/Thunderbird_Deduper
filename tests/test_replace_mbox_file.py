from unittest.mock import MagicMock, patch
from functions.replace_mbox_file import write_mbox_file


def test_write_mbox_file_writes_messages(tmp_path):
    mbox_path = tmp_path / "Inbox"
    messages = [MagicMock(), MagicMock()]

    mock_mbox = MagicMock()

    with patch("functions.replace_mbox_file.mailbox.mbox", return_value=mock_mbox), \
         patch("functions.replace_mbox_file.shutil.move"):

        write_mbox_file(str(mbox_path), messages)

    assert mock_mbox.add.call_count == 2
    mock_mbox.flush.assert_called_once()
    mock_mbox.close.assert_called_once()