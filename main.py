from screenshot import screenshot
from checkdefaced import check
from Alert.chatbot import sendBot
from sys import argv
from Alert.sendEmail import sendMessage

script, url, receiver = argv


def main(url, receiver):
    print(url)
    img_path = screenshot(url)

    defaced = check(img_path)
    if defaced:
        sendBot(url, img_path)
        subject = "Website Defacement"
        message = f"You website was defaced!\nURL: {url}"
        sendMessage(receiver, subject, message, img_path)
        print("Website was defaced!")
    else:
        print("Everything oke!")


main(url, receiver)
