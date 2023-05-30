# ezmail
easily send out emails via python or the cli using python's SMTP module.

---

# example

## `.env` file
This module uses environment files to handle sensitive info.
Make sure the following values are defined in it:
```.env
USERNAME=sender@exmaple.com
PASSWORD=<password>
SMTP=<provider's SMTP server>
PORT=<provider's port>
```
See examples for popular providers below.

## send from python
```python
from ezmail import send_mail

# by default, an env file named `.env` is searched.
send_mail(
  subject="Email sent with Python",
  recipients=["r1@example.com", "John Doe <john@example.com>"],
  message="Here go the contents of the message.",
)
```

## send from the cli
`python -m ezmail -s "Email sent from bash" -r "r1@example.com" "r2@example.com" -m "This is my message."`

# More advanced uses
This module allows adding attachments to the email, as well as reading in the message and / or recipients from a file instead of defining them directly.

## python
Python automatically detects the type of data that is passed into the different fields.

For example, to read the recipients from a file, simply pass in a Path or file object instead of a list of strings.

A file that defines the recipients must have one recipient per line:
```recipients.txt
r1@example.com
John Doe <john@example.com>
```
The message can also be taken from a Path or file object.

To add attachments, pass in a list of Paths or (read-binary) file objects. The type is automatically detected.

If an env file with a name different from `.env` is used, pass it into `envfile` as a Path object or a string
### For example:
```python
from pathlib import Path
from ezmail import send_mail

recipients_file = Path("path/to/recipients.txt")
messages_file = open("path/to/message.txt", "r")

attachments = [
  Path("path/to/attachment1.csv"),
  open("path/to/attachment2.jpg", "rb"),
]

envfile = Path("my/.envfile")

send_mail(
  subject="Email sent with Python",
  recipients=recipients_file,
  message=messages_file,
  attachments=attachments,
  envfile=envfile
)
```

## cli
`python -m ezmail --help` to see how to call from the command line

Possible flags:
- `-s` or `--subject`: the subject of the email (single argument)
- message:
  - `-m` or `--message`: the contents of the email OR
  - `-f` or `--file`: the file containing the contents of the email
- recipients:
  - `-r` or `--recipients`: the recipients of the email (one or more arguments) OR
  - `-rf` or `--recipientsfile`: the file containing the addresses of the recipients
- `-a` or `--attachments`: a list of files to attach to the email (one or more arguments)
- `-e` or `--env`: the env file where the credentials are defined (default `.env`)
