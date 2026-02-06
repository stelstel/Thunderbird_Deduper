import hashlib
from email.message import EmailMessage

from functions.fingerprinting import (
    get_one_msg_fingerprint_simple,
    get_one_msg_fingerprint_with_body,
    get_one_msg_fingerprint_strict,
)


def make_message(
    msg_id="<123>",
    subject="Test Subject",
    sender="user@example.com",
    body="Hello World",
):
    msg = EmailMessage()
    msg["Message-ID"] = msg_id
    msg["Subject"] = subject
    msg["From"] = sender
    msg.set_content(body)
    return msg


# -------------------------------------------------
# SIMPLE FINGERPRINT
# -------------------------------------------------

def test_simple_fingerprint_same_headers_equal():
    msg1 = make_message()
    msg2 = make_message()

    fp1 = get_one_msg_fingerprint_simple(msg1)
    fp2 = get_one_msg_fingerprint_simple(msg2)

    assert fp1 == fp2


def test_simple_fingerprint_header_change_changes_fp():
    msg1 = make_message(subject="Hello")
    msg2 = make_message(subject="Different")

    assert get_one_msg_fingerprint_simple(msg1) != get_one_msg_fingerprint_simple(msg2)


# -------------------------------------------------
# FINGERPRINT WITH BODY
# -------------------------------------------------

def test_fingerprint_with_body_same_body_equal():
    msg1 = make_message(body="Same body text")
    msg2 = make_message(body="Same body text")

    fp1 = get_one_msg_fingerprint_with_body(msg1)
    fp2 = get_one_msg_fingerprint_with_body(msg2)

    assert fp1 == fp2


def test_fingerprint_with_body_detects_body_difference():
    msg1 = make_message(body="Hello world")
    msg2 = make_message(body="Hello WORLD!!!")

    fp1 = get_one_msg_fingerprint_with_body(msg1)
    fp2 = get_one_msg_fingerprint_with_body(msg2)

    assert fp1 != fp2


def test_fingerprint_with_body_respects_body_length_limit():
    body = "A" * 200
    msg = make_message(body=body)

    fp_short = get_one_msg_fingerprint_with_body(msg, body_chars=20)
    fp_long = get_one_msg_fingerprint_with_body(msg, body_chars=80)

    assert fp_short != fp_long


# -------------------------------------------------
# STRICT FINGERPRINT
# -------------------------------------------------

def test_strict_fingerprint_identical_messages_equal():
    msg1 = make_message()
    msg2 = make_message()

    fp1 = get_one_msg_fingerprint_strict(msg1)
    fp2 = get_one_msg_fingerprint_strict(msg2)

    assert fp1 == fp2


def test_strict_fingerprint_any_change_detected():
    msg1 = make_message()
    msg2 = make_message(body="Modified body")

    assert get_one_msg_fingerprint_strict(msg1) != get_one_msg_fingerprint_strict(msg2)


def test_strict_fingerprint_is_md5():
    msg = make_message()
    fp = get_one_msg_fingerprint_strict(msg)

    # MD5 hex digest is always 32 chars
    assert isinstance(fp, str)
    assert len(fp) == 32
