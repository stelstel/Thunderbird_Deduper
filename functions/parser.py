# functions/parser.py

import mailbox


def get_messages_from_mbox(mbox_path):
    """
    Extract messages from an mbox file and return their key information.
    This function reads an mbox mailbox file and parses each message to extract
    relevant metadata and content. It handles both simple and multipart email
    messages, gracefully handling encoding errors.
    Args:
        mbox_path (str): The file path to the mbox mailbox file to parse.
    Returns:
        list: A list of dictionaries, each containing the following keys:
            - 'subject' (str): The email subject line.
            - 'from' (str): The sender's email address.
            - 'date' (str): The email date/timestamp.
            - 'body' (str): The email body text content.
    Note:
        - For multipart messages, only text/plain parts are extracted and concatenated.
        - Encoding errors are ignored during decoding, with empty strings used as fallback.
        - If a message cannot be decoded, an empty string is used for the body.
    """
    mbox = mailbox.mbox(mbox_path)
    messages = []

    for msg in mbox:
        # Extract headers
        subject = msg.get('subject', '')
        sender = msg.get('from', '')
        date = msg.get('date', '')

        # Extract body
        body = ''
        
        if msg.is_multipart():
            # For multipart messages, concatenate the text parts
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    try:
                        body += part.get_payload(decode=True).decode(errors='ignore')
                    except:
                        continue
        else:
            try:
                body = msg.get_payload(decode=True).decode(errors='ignore')
            except:
                body = ''

        messages.append({
            'subject': subject,
            'from': sender,
            'date': date,
            'body': body
        })
    
    return messages
