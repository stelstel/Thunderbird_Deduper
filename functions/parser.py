# functions/parser.py

import mailbox

def get_messages_from_mbox(mbox_path):
    """
    Reads an mbox file and returns a list of messages.
    Each message is a dictionary with subject, from, date, body.
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
