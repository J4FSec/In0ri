import os
import sys

from flask import Flask, escape, jsonify, render_template, request

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import hashlib
import re

import alert
import createLicense as license
import database
import schedule as sch


def slug(string):
    pattern = "|%[0-9]{1,}|%|--|#|;|/\*|'|\"|\\\*|\[|\]|\<|\>|xp_|\&gt|\&ne|\&lt|&"
    result = re.sub(pattern, "", string)
    return result


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

    if len(url) == 0 or len(email) == 0 or len(hours) == 0 or len(minutes) == 0:
        return "Null"

    if re.match(int_format, hours) is False or re.match(int_format, minutes) is False:
        return "Null"

    if hours == minutes == "0":
        return "Null"

    db = database.Database("site")
    time = f"{int(hours)} hours {int(minutes)} minutes"
    data = {"email": email, "time": time, "active_key": "", "url": url}
    check = 0
    for check in db.get_multiple_data():
        if check["url"] == url:
            check = 1
    if check == 1:
        response = "EXIST"
    else:
        db.insert_data(data)
        if int(hours) == 0:
            sch.create(url, email, None, minutes)
        if int(minutes) == 0:
            sch.create(url, email, hours, None)
        response = "OKE"
    return response


@app.route("/createAgent", methods=["POST"])
def createAgent():
    url = slug(request.form["url"])
    db = database.Database("site")
    check = 1
    for data in db.get_multiple_data():
        if data["url"] == url:
            receiver = data["email"]
            check = 0
    if check == 1:
        response = "ERROR"
    else:
        active_key = license.make_license(url)
        unique = {"url": url}
        key_update = {"active_key": active_key}
        db.update_existing(unique, key_update)
        subject = "Get active key!"
        message = f"You Agent's active key is: {active_key}"
        al.sendMessage(receiver, subject, message)
        response = "OKE"
    return response


@app.route("/deleteURL", methods=["POST"])
def deleteURL():
    url = slug(request.form["url"])
    urlJson = {"url": url}
    db = database.Database("site")
    check = 1
    for data in db.get_multiple_data():
        if data["url"] == url:
            check = 0
    if check == 1:
        response = "ERROR"
    else:
        print(url)
        db.remove_data(urlJson)
        sch.delete(url)
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
                "active_key": data["active_key"],
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
