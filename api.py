import json
import os
import sys

import requests
from flask import Flask, request

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import re
import alert
import FlaskApp.database
from checkdefaced import check
from screenshot import screenshot


def slug(string):
    pattern = "|%[0-9]{1,}|%|--|#|;|/\*|'|\"|\\\*|\[|\]|xp_|\&gt|\&ne|\&lt|&"
    result = re.sub(pattern, "", string)
    return result


app = Flask(__name__)


@app.route("/checkdeface", methods=["POST"])
def checkdeface():
    db = FlaskApp.database.Database("site")
    al = alert.Alert()
    res = {}
    body = json.loads(request.data)
    if len(body["key"]) == 0 and len(body["path"]) == 0: 
        res = {"status": "400 Bad Request!"}
        return res
    else: 
        key = slug(body["key"])
    
    active_key = {"active_key": key}
    data = db.get_single_data(active_key)
    if data is None:
        res = {"status": "404 Key Invalid!"}
        return res
    url = data["url"] + body["path"]
    receiver = data["email"]

    try:
        response = requests.get(url)
    except requests.ConnectionError:
        res = {"status": "500 Internal Server Error!"}
        return res

    if (response.status_code != 200) and (response.status_code != 302):
        res = {"status": "URL Invalid! " + url}
    else:
        img_path = screenshot(url)
        defaced = check(img_path)
        if defaced:
            al.sendBot(url, img_path)
            subject = "Website Defacement"
            message = (
                f"You website was defaced!\nURL: {url} \nPath infected: {body['path']}"
            )
            al.sendMessage(receiver, subject, message, img_path)
            res = {"status": "Website was defaced!"}
            print("Website was defaced!")
        else:
            res = {"status": "Everything oke!"}
            print("Everything oke!")
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8088")
