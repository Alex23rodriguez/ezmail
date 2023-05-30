from .ezmail import send_mail

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

parser.add_argument("-a", "--attachments", nargs="+", type=FileType("rb"), default=[])

parser.add_argument("-e", "--env", required=False, default=".env")

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
    envfile=args.env,
    recipients=recipients,
    subject=args.subject,
    message=message,
    attachments=args.attachments,
)
