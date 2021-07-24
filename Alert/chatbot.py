from telegram import Bot
from datetime import datetime

CHAT_ID = "-1001158847222"
TOKEN = "1786196183:AAFyuJ-9KPkByqvpO6T6Wm671w0CQ-dXMV0"
bot = Bot(TOKEN)
now = datetime.now()
current_time = now.strftime("%H:%M:%S")


def sendBot(url, img_path):
    bot.sendPhoto(
        CHAT_ID,
        photo=open(img_path, "rb"),
        caption="⚠️" + "Website " + url + " was defaced!\n" + "At " + current_time,
    )
