import smtplib
import imghdr
from email.message import EmailMessage

EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""


def sendMessage(receiver, subject, message, imagePath=None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver
    msg.set_content(message)

    if imagePath is not None:
        with open(imagePath, "rb") as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
        msg.add_attachment(
            file_data, maintype="image", subtype=file_type, filename="Website image"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


