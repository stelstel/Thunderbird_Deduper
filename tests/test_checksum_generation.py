import mailbox
import hashlib
from email.message import EmailMessage

from functions.checksum_generation import (
    get_one_msg_fingerprint_hashed,
    get_messages_fingerprint_hashed_list,
    get_messages_fingerprint_hashed_str,
)
from functions.fingerprinting import get_one_msg_fingerprint_simple


# -------------------------------------------------
# Helper: create a test email message
# -------------------------------------------------
def create_test_message(subject="Test", body="Hello"):
    msg = EmailMessage()
    msg["From"] = "a@test.com"
    msg["To"] = "b@test.com"
    msg["Subject"] = subject
    msg.set_content(body)
    return msg


# -------------------------------------------------
# Tests
# -------------------------------------------------
def test_get_one_msg_fingerprint_hashed():
    msg = create_test_message()

    simple_fp = get_one_msg_fingerprint_simple(msg)
    expected = hashlib.md5(simple_fp.encode()).hexdigest()

    result = get_one_msg_fingerprint_hashed(msg)

    assert result == expected
    assert isinstance(result, str)
    assert len(result) == 32  # MD5 hex length


def test_get_messages_fingerprint_hashed_list(tmp_path):
    mbox_path = tmp_path / "test.mbox"
    mbox = mailbox.mbox(mbox_path)

    mbox.add(create_test_message("A", "Body A"))
    mbox.add(create_test_message("B", "Body B"))
    mbox.flush()
    mbox.close()

    fingerprints = get_messages_fingerprint_hashed_list(str(mbox_path))

    assert isinstance(fingerprints, list)
    assert len(fingerprints) == 2
    assert all(len(fp) == 32 for fp in fingerprints)


def test_get_messages_fingerprint_hashed_str(tmp_path):
    mbox_path = tmp_path / "test.mbox"
    mbox = mailbox.mbox(mbox_path)

    mbox.add(create_test_message("A", "Body A"))
    mbox.add(create_test_message("B", "Body B"))
    mbox.flush()
    mbox.close()

    result = get_messages_fingerprint_hashed_str(str(mbox_path))

    lines = result.strip().split("\n")

    assert isinstance(result, str)
    assert len(lines) == 2
    assert all(len(line) == 32 for line in lines)


def test_empty_mbox_returns_empty_results(tmp_path):
    mbox_path = tmp_path / "empty.mbox"
    mailbox.mbox(mbox_path).close()

    assert get_messages_fingerprint_hashed_list(str(mbox_path)) == []
    assert get_messages_fingerprint_hashed_str(str(mbox_path)) == ""
