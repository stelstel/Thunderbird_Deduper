import mailbox
from email.message import EmailMessage

from functions.parser import get_messages_from_mbox


def test_get_messages_from_mbox_single_message(tmp_path):
    # Arrange: create a temporary mbox file
    mbox_path = tmp_path / "test.mbox"

    mbox = mailbox.mbox(mbox_path)

    msg = EmailMessage()
    msg["Subject"] = "Test subject"
    msg["From"] = "sender@example.com"
    msg["Date"] = "Mon, 1 Jan 2024 12:00:00 +0000"
    msg.set_content("Hello Thunderbird")

    mbox.add(msg)
    mbox.flush()
    mbox.close()

    # Act
    messages = get_messages_from_mbox(str(mbox_path))

    # Assert
    assert len(messages) == 1

    message = messages[0]
    assert message["subject"] == "Test subject"
    assert message["from"] == "sender@example.com"

    assert "Jan" in message["date"]
    assert "2024" in message["date"]

    assert "Hello Thunderbird" in message["body"]

