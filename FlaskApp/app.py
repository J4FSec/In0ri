from flask import (
    Flask,
    render_template,
    request,
    escape,
)
import sendEmail
import database as db
import schedule as sch
import createLicense as license
import re


def slug(string):
    pattern = "|%[0-9]{1,}|%|--|#|;|/\*|'|\"|\\\*|\[|\]|xp_|\&gt|\&ne|\&lt|&"
    result = re.sub(pattern, "", string)
    return result


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


@app.route("/register", methods=["POST"])
def register():
    url = slug(request.form["url"])
    email = slug(request.form["email"])
    time = slug(request.form["time"])
    data = {"email": email, "time": time, "active_key": "", "url": url}
    check = 0
    for check in db.get_multiple_data():
        if check["url"] == url:
            check = 1
    if check == 1:
        print(f"url {escape(url)} existed!")
        response = "EXIST"
    else:
        db.insert_data(data)
        sch.create(url, time, email)
        response = "OKE"
    return response


@app.route("/createAgent", methods=["POST"])
def createAgent():
    url = slug(request.form["url"])
    receiver = slug(request.form["email"])
    check = 1
    for data in db.get_multiple_data():
        if data["url"] == url:
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
        sendEmail.sendMessage(receiver, subject, message)
        response = "OKE"
    return response


@app.route("/deleteURL", methods=["POST"])
def deleteURL():
    url = slug(request.form["url"])
    urlJson = {"url": url}
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
