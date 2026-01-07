from email.message import EmailMessage

from functions.fingerprinting import get_one_msg_fingerprint_simple
from functions.normalizing import normalize


# -------------------------------------------------
# Helper
# -------------------------------------------------
def create_test_message(
    msg_id="<123@test>",
    subject="Test Subject",
    sender="user@test.com",
    date="Mon, 01 Jan 2024 12:00:00 +0000",
):
    msg = EmailMessage()
    msg["Message-ID"] = msg_id
    msg["Subject"] = subject
    msg["From"] = sender
    msg["Date"] = date
    return msg


# -------------------------------------------------
# Tests
# -------------------------------------------------
def test_get_one_msg_fingerprint_simple_all_fields():
    msg = create_test_message()

    result = get_one_msg_fingerprint_simple(msg)

    expected_raw = (
        "<123@test>|"
        "Test Subject|"
        "user@test.com|"
        "Mon, 01 Jan 2024 12:00:00 +0000"
    )

    expected = normalize(expected_raw)

    assert result == expected
    assert isinstance(result, str)


def test_get_one_msg_fingerprint_simple_missing_fields():
    msg = EmailMessage()  # No headers at all

    result = get_one_msg_fingerprint_simple(msg)

    expected = normalize("|||")

    assert result == expected


def test_get_one_msg_fingerprint_simple_partial_fields():
    msg = EmailMessage()
    msg["Subject"] = "Only subject"

    result = get_one_msg_fingerprint_simple(msg)

    expected = normalize("|Only subject||")

    assert result == expected


def test_fingerprint_is_deterministic():
    msg = create_test_message()

    fp1 = get_one_msg_fingerprint_simple(msg)
    fp2 = get_one_msg_fingerprint_simple(msg)

    assert fp1 == fp2
