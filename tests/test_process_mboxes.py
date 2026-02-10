from unittest.mock import MagicMock, patch
from functions.process_mboxes import process_mboxes


def test_process_mboxes_aggregates_results():
    mboxes = ["mbox1", "mbox2"]

    progress = MagicMock()
    progress.value.return_value = 0

    with patch(
        "functions.process_mboxes.process_one_mbox",
        side_effect=[
            (None, "msg1\n", 2),
            (None, "msg2\n", 3),
        ]
    ), patch(
        "functions.process_mboxes.QApplication.processEvents"
    ):

        result_mboxes, msg_out, total_deleted = process_mboxes(mboxes, progress)

    assert total_deleted == 5
    assert msg_out == "msg1\nmsg2\n"
    assert progress.setValue.call_count == 2
    assert len(result_mboxes) == 2
