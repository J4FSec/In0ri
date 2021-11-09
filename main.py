from sys import argv

import alert
from checkdefaced import check
from screenshot import screenshot

script, url, receiver = argv


def main(url, receiver):
    al = alert.Alert()
    print(url)
    img_path = screenshot(url)

    defaced = check(img_path)
    if defaced:
        al.sendBot(url, img_path)
        subject = "Website Defacement"
        message = f"You website was defaced!\nURL: {url}"
        al.sendMessage(receiver, subject, message, img_path)
        print("Website was defaced!")
    else:
        print("Everything oke!")


main(url, receiver)
