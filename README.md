# Mbox Attachment Remover

Mbox Attachment Remover is a Python script designed to efficiently remove attachments from mbox files. This tool helps in reducing file size and ensuring the privacy of email archives by stripping out attachments from the email messages.

## Features

- **Remove Attachments**: Strips attachments from mbox files, leaving the rest of the email content intact.
- **Preserve Headers**: Maintains original email headers for integrity.
- **Command Line Interface**: Easy to use from the command line with minimal dependencies.

## Requirements

- Python 3.x

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/mbox-attachment-remover.git
    cd mbox-attachment-remover
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the script, use the following command format:

```bash
python mbox_attachment_remover.py <input mbox file> <output mbox file> [max messages]
```

### Arguments

- `<input mbox file>`: Path to the input mbox file.
- `<output mbox file>`: Path to the output mbox file where cleaned messages will be saved.
- `[max messages]`: (Optional) Maximum number of messages to process.

### Example

```bash
python mbox_attachment_remover.py input.mbox output.mbox 100
```

This command will process the first 100 messages in `input.mbox`, remove their attachments, and save the cleaned messages to `output.mbox`.

## How It Works

The script processes each message in the input mbox file:
1. Cleans the email headers by decoding them and removing any linefeed and carriage return characters.
2. Removes attachments from multipart messages.
3. Preserves the main content of the emails without attachments.
4. Saves the processed messages to a new mbox file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.