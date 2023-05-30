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
# if the environment file has a different name, please pass it into envfile=
send_mail(
  subject="Email sent with Python"
  recipients=["r1@example.com", "John Doe <john@example.com>"]
  message="Here go the contents of the message."
)
```

## send from the cli
`python -m ezmail -s "Email sent from bash" -r "r1@example.com" "r2@example.com" -m "This is my message."`
