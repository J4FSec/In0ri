import os
import smtplib
import sys
from datetime import datetime
from email.message import EmailMessage


from telegram import Bot

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import FlaskApp.database as database

db = database.Database("setting")


class Alert:
    def sendMessage(self, receiver, subject, message, imagePath=None):
        if not receiver:
            return
        try:
            data = db.get_single_data({"data": "setting"}) or {}
        except Exception:
            data = {}
        smtpArray = data.get("smtp", [])
        if len(smtpArray) == 0:
            return "1"
        for smtp in smtpArray:
            EMAIL_SERVER = smtp["smtp_server"]
            EMAIL_ADDRESS = smtp["smtp_address"]
            EMAIL_PASSWORD = smtp["smtp_password"]

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = receiver
        msg.set_content(message)

        try: 
            if imagePath is not None:
                import mimetypes
                with open(imagePath, "rb") as f:
                    file_data = f.read()
                    mime_type, _ = mimetypes.guess_type(imagePath)
                    maintype, subtype = (mime_type or "image/png").split("/", 1)
                    
                msg.add_attachment(
                    file_data, maintype=maintype, subtype=subtype, filename="Website image.png"
                )

            with smtplib.SMTP_SSL(EMAIL_SERVER, 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
        except smtplib.SMTPException as e:
            print(e)

    def sendBot(self, url, img_path):
        try:
            data = db.get_single_data({"data": "setting"}) or {}
        except Exception:
            data = {}
        telegramArray = data.get("telegram", [])

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if len(telegramArray) == 0:
            return "1"
        for telegram in telegramArray:
            CHAT_ID = telegram["chat_id"]
            TOKEN = telegram["token"]

        bot = Bot(TOKEN)
        try:
            bot.sendPhoto(
                CHAT_ID,
                photo=open(img_path, "rb"),
                caption="⚠️"
                + "Website "
                + url
                + " was defaced!\n"
                + "At "
                + current_time,
            )
        except:
            print("Looks like CHAT_ID or TOKEN of telegram-bot was wrong!")

    def getBotInfo(self, CHAT_ID, TOKEN):
        try:
            bot1 = Bot(TOKEN)
            first_name = bot1.getMe().first_name
            title = bot1.getChat(CHAT_ID).title
            return first_name, title
        except:
            return "ERROR"

