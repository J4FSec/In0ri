import os
import sys

# pyrefly: ignore [missing-import]
from flask import Flask, jsonify, render_template, request

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import hashlib
import re

import alert
import database
import json
import secrets
import string

# Import our unified worker tasks
import tasks


def slug(string_val):
    pattern = "|%[0-9]{1,}|%|--|#|;|/\*|'|\"|\\\*|\[|\]|\<|\>|xp_|\$gt|\$ne|\$lt|$"
    result = re.sub(pattern, "", string_val)
    return result

def generate_key(domain):
    """
    Generates a cryptographically secure random API key.
    Format: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX
    """
    alphabet = string.ascii_uppercase + string.digits
    random_str = ''.join(secrets.choice(alphabet) for _ in range(25))
    encoded_signature = "-".join(
        [random_str[i : i + 5] for i in range(0, len(random_str), 5)]
    )
    return encoded_signature


al = alert.Alert()

app = Flask(__name__, static_url_path="/static")


@app.route("/register", methods=["GET"])
def renderRegister():
    return render_template("register.html")


@app.route("/createAgent", methods=["GET"])
def renderAgent():
    return render_template("agent.html")


@app.route("/deleteURL", methods=["GET"])
def renderDeleteURL():
    return render_template("deleteurl.html")


@app.route("/", methods=["GET"])
def renderIndex():
    return render_template("index.html")


@app.route("/setting", methods=["GET"])
def renderSetting():
    return render_template("setting.html")


@app.route("/register", methods=["POST"])
def register():
    url = slug(request.form["url"])
    email = slug(request.form["email"])
    hours = slug(request.form["hours"])
    minutes = slug(request.form["minutes"])
    int_format = re.compile("^[0-9]+$")

    if len(url) == 0 or len(hours) == 0 or len(minutes) == 0:
        return "Null"

    if re.match(int_format, hours) is False or re.match(int_format, minutes) is False:
        return "Null"

    if hours == minutes == "0":
        return "Null"

    db = database.Database("site")
    time = f"{int(hours)} hours {int(minutes)} minutes"
    data = {"email": email, "time": time, "api_key": "", "url": url}
    
    existing = db.get_single_data({"url": url})
    if existing:
        response = "EXIST"
    else:
        db.insert_data(data)
        response = "OKE"
    return response


@app.route("/createAgent", methods=["POST"])
def createAgent():
    url = slug(request.form["url"])
    db = database.Database("site")
    data = db.get_single_data({"url": url})
    if not data:
        response = "ERROR"
    else:
        receiver = data["email"]
        api_key = generate_key(url)
        unique = {"url": url}
        key_update = {"api_key": api_key}
        db.update_existing(unique, key_update)
        subject = "Get API key!"
        message = f"Your Agent's API key is: {api_key}"
        al.sendMessage(receiver, subject, message)
        response = "OKE"
    return response


@app.route("/deleteURL", methods=["POST"])
def deleteURL():
    url = slug(request.form["url"])
    urlJson = {"url": url}
    db = database.Database("site")
    data = db.get_single_data(urlJson)
    if not data:
        response = "ERROR"
    else:
        print(url)
        db.remove_data(urlJson)
        response = "OKE"
    return response


@app.route("/listURL", methods=["GET"])
def listURL():
    db = database.Database("site")
    response = []
    i = 1
    for data in db.get_multiple_data():
        path_img = hashlib.md5(data["url"].encode()).hexdigest()
        response.append(
            {
                "stt": i,
                "email": data["email"],
                "time": data["time"],
                "url": data["url"],
                "api_key": data.get("api_key", ""),
                "path_img": path_img,
            }
        )
        i = i + 1
    return jsonify(response)


@app.route("/listSetting", methods=["GET"])
def listSetting():
    db = database.Database("setting")
    response = []
    for data in db.get_multiple_data():
        if "telegram" not in data or len(data["telegram"]) == 0:
            telegram = []
        else:
            telegram = [
                {
                    "first_name": data["telegram"][0]["first_name"],
                    "title": data["telegram"][0]["title"],
                }
            ]
        if "smtp" not in data or len(data["smtp"]) == 0:
            smtp = []
        else:
            smtp = [
                {
                    "smtp_server": data["smtp"][0]["smtp_server"],
                    "smtp_address": data["smtp"][0]["smtp_address"],
                }
            ]
        response.append({"smtp": smtp, "telegram": telegram})
    return jsonify(response)


@app.route("/setting", methods=["POST"])
def setting():
    bot = slug(request.form["bot"])

    if len(bot) == 0 or (bot != "telegram" and bot != "smtp"):
        return "Bad data!"
    else:
        db = database.Database("setting")
        if bot == "smtp":
            smtp_server = slug(request.form["smtp_server"])
            smtp_address = slug(request.form["smtp_address"])
            smtp_password = slug(request.form["smtp_password"])
            data = {
                "smtp": [
                    {
                        "smtp_server": smtp_server,
                        "smtp_address": smtp_address,
                        "smtp_password": smtp_password,
                    }
                ]
            }
            db.update_noexiting({"data": "setting"}, data)
            response = "OKE"
        elif bot == "telegram":
            chat_id = slug(request.form["chat_id"])
            token = slug(request.form["token"])
            bot_info = al.getBotInfo(chat_id, token)
            if bot_info == "ERROR":
                return "INVALID"
            else:
                data = {
                    "telegram": [
                        {
                            "chat_id": chat_id,
                            "token": token,
                            "first_name": bot_info[0],
                            "title": bot_info[1],
                        }
                    ]
                }
                db.update_noexiting({"data": "setting"}, data)
            response = "OKE"
        else:
            response = "Bad data!"
    return response


@app.route("/deleteSetting", methods=["POST"])
def deleteSetting():
    bot = slug(request.form["bot"])

    if len(bot) == 0 or (bot != "telegram" and bot != "smtp"):
        return "Bad data!"
    else:
        db = database.Database("setting")
        if bot == "smtp":
            data = {"smtp": {}}
            db.update_empty({"data": "setting"}, data)
            response = "OKE"
        elif bot == "telegram":
            data = {"telegram": {}}
            db.update_empty({"data": "setting"}, data)
            response = "OKE"
        else:
            response = "Bad data!"
    return response


@app.route("/checkdeface", methods=["POST"])
def checkdeface():
    db = database.Database("site")
    res = {}
    
    try:
        body = json.loads(request.data)
    except Exception:
        return {"status": "400 Bad Request!"}

    if len(body.get("key", "")) == 0 and len(body.get("path", "")) == 0: 
        return {"status": "400 Bad Request!"}
    
    key = slug(body["key"])
    api_key_query = {"api_key": key}
    data = db.get_single_data(api_key_query)
    
    if data is None:
        return {"status": "404 Key Invalid!"}
        
    url = data["url"] + body["path"]
    receiver = data["email"]

    # Push check task to Celery Queue so Flask doesn't block
    try:
        tasks.check_url_task.delay(url, receiver, infected_path=body["path"])
        res = {"status": "Website defacement check queued for processing!"}
        print(f"Queued check for agent URL: {url}")
    except Exception as e:
        print(f"Error queuing checkdeface API: {e}")
        return {"status": "500 Task Queue Error!"}
        
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
