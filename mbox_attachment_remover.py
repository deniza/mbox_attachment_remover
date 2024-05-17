import mailbox
import email
import sys
import logging
from email.header import decode_header

"""
This script processes an mbox file to remove attachments from email messages.
It iterates through each message in the mbox file, cleans the headers, and removes attachments, 
saving the modified messages to a new mbox file.

Usage:
    python mbox_attachment_remover.py <input_mbox_file> <output_mbox_file> [max_messages]

Arguments:
    <input_mbox_file> : Path to the input mbox file.
    <output_mbox_file> : Path to the output mbox file where modified messages will be saved.
    [max_messages] : Optional. Maximum number of messages to process. If not provided, all messages will be processed.

Example:
    python mbox_attachment_remover.py my_emails.mbox cleaned_emails.mbox 1000

Dependencies:
    - Python 3
    - mailbox module
    - email module

Author:
    Deniz Aydinoglu (https://github.com/deniza)

License:
    This script is released under the MIT License.

Version:
    1.0.0

Release Date:
    2024-05-17
"""

def clean_header(header_value):
    """Remove linefeed and carriage return characters from header values."""
    if not header_value:
        return ''
    decoded_parts = decode_header(header_value)
    clean_value = ''
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                clean_value += part.decode(encoding if encoding else 'utf-8', errors='replace')
            except LookupError:
                clean_value += part.decode('latin1', errors='replace')
            except Exception as e:
                logging.error(f"Failed to decode part of header: {e}")
                continue
        else:
            clean_value += part
    return clean_value.replace('\n', '').replace('\r', '')

def remove_attachments(input_mbox_path, output_mbox_path, max_messages=None):
    """Process the input mbox file, remove attachments, and save the modified messages to the output mbox file."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    input_mbox = mailbox.mbox(input_mbox_path)
    output_mbox = mailbox.mbox(output_mbox_path, create=True)

    processed_count = 0
    total_count = len(input_mbox)

    # Using a generator to avoid loading all messages into memory at once
    for i, message in enumerate(iter(input_mbox)):
        if max_messages is not None and processed_count >= max_messages:
            break

        try:
            new_msg = email.message.EmailMessage()
            seen_headers = set()
            for header in message.keys():
                header_lower = header.lower()
                if header_lower in ['content-type', 'content-transfer-encoding', 'mime-version']:
                    if header_lower in seen_headers:
                        continue
                    seen_headers.add(header_lower)
                header_value = message[header]
                if header_value:
                    clean_value = clean_header(header_value)
                    new_msg[header] = clean_value

            if 'mime-version' not in seen_headers and 'MIME-Version' in message:
                new_msg['MIME-Version'] = message['MIME-Version']

            if message.is_multipart():
                new_msg.set_type(message.get_content_type())
                for part in message.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        new_msg.attach(part)
            else:
                payload = message.get_payload(decode=True)
                if payload:
                    maintype = message.get_content_maintype()
                    subtype = message.get_content_subtype()
                    new_msg.set_content(payload, maintype=maintype, subtype=subtype)

            output_mbox.add(new_msg)
            processed_count += 1
            logging.info(f"Processed {processed_count}/{total_count} messages")

        except Exception as e:
            logging.error(f"Failed to process message {i + 1}: {e}")

    output_mbox.flush()
    output_mbox.close()
    logging.info(f"Attachments removed from {processed_count} messages. Output saved to {output_mbox_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input mbox file> <output mbox file> [max messages]")
        sys.exit(1)
    
    input_mbox_path = sys.argv[1]
    output_mbox_path = sys.argv[2]
    max_messages = int(sys.argv[3]) if len(sys.argv) > 3 else None

    remove_attachments(input_mbox_path, output_mbox_path, max_messages)

