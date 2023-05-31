from email.message import EmailMessage
from io import BufferedReader, TextIOWrapper
from pathlib import Path
import ssl
import smtplib
from mimetypes import guess_type
from typing import Union

from dotenv import dotenv_values


def send_mail(
    *,
    envfile: Union[str, Path] = ".env",
    recipients: Union[list[str], Path, TextIOWrapper],
    subject: str,
    message: Union[str, Path, TextIOWrapper],
    attachments: Union[list[Path], list[BufferedReader]] = [],
):
    envfile = Path(envfile)
    assert (
        envfile.exists() and envfile.is_file()
    ), "Could not load specified environment file!"

    environ = dotenv_values(envfile)

    assert all(
        key in environ for key in ("PORT", "USERNAME", "PASSWORD", "SMTP")
    ), "environment found, but incomplete!"
    port = int(environ["PORT"])
    sender = environ["USERNAME"]
    password = environ["PASSWORD"]
    smtp_server = environ["SMTP"]

    def tofile(a: Union[Path, BufferedReader]) -> BufferedReader:
        if isinstance(a, Path):
            return open(a, "rb")

        assert type(a) is BufferedReader, type(a)
        return a

    assert any(
        isinstance(recipients, t)
        for t in (
            list,
            Path,
            TextIOWrapper,
        )
    ), f"Wrong type for recipients: {type(message)}"
    if type(recipients) is list:
        assert len(recipients) and all(type(r) == str for r in recipients)
    elif isinstance(recipients, Path):
        recipients = open(recipients).read().splitlines()
    else:
        recipients = recipients.read().splitlines()

    assert any(
        isinstance(message, t)
        for t in (
            str,
            Path,
            TextIOWrapper,
        )
    ), f"Wrong type for message: {type(message)}"
    if isinstance(message, Path):
        message = open(message).read()
    elif type(message) is TextIOWrapper:
        message = message.read()

    assert type(attachments) is list and all(
        isinstance(a, Path) or type(a) is BufferedReader for a in attachments
    ), f"Wrong type for attachments: {[type(a) for a in attachments]}"

    attachments = [tofile(a) for a in attachments]

    em = EmailMessage()
    em["From"] = sender
    em["To"] = ", ".join(recipients)
    em["Subject"] = subject
    em.set_content(message)

    for file in attachments:
        ctype, encoding = guess_type(file.name)
        if ctype is None or encoding is not None:
            # No guess could be made. use a generic bag-of-bits type.
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)

        em.add_attachment(
            file.read(),
            maintype=maintype,
            subtype=subtype,
            filename=file.name.rsplit("/", 1)[-1],
        )

    ### setup to connect to ssl (secure) server
    context = ssl.create_default_context()

    # establish connection and send email
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as smtp:
        # smtp.set_debuglevel(1)
        smtp.login(sender, password)
        smtp.send_message(em)

    print("mail sent successfully")


### parse arguments
if __name__ == "__main__":
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser(
        prog="Email sender",
        description="send an email to the specified recipients",
    )

    parser.add_argument("-s", "--subject", required=True)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--message")
    group.add_argument("-f", "--file", type=FileType("r"))

    group2 = parser.add_mutually_exclusive_group(required=True)
    group2.add_argument("-r", "--recipients", nargs="+")
    group2.add_argument("-rf", "--recipientsfile", type=FileType("r"))

    parser.add_argument(
        "-a", "--attachments", nargs="+", type=FileType("rb"), default=[]
    )

    args = parser.parse_args()

    if args.recipients:
        recipients = args.recipients
    else:
        recipients = args.recipientsfile.read().splitlines()

    if args.message:
        message = args.message
    else:
        message = args.file.read()

    send_mail(
        recipients=recipients,
        subject=args.subject,
        message=message,
        attachments=args.attachments,
    )
