![](img/logo_transparent.png)
![GitHub](https://img.shields.io/github/license/J4FSec/In0ri) ![](https://img.shields.io/badge/Python-3.6-informational) ![](https://img.shields.io/badge/uses-Flask-informational) ![](https://img.shields.io/badge/uses-Tensorflow-informational) ![](https://img.shields.io/badge/uses-Keras-informational) ![](https://img.shields.io/badge/uses-OpenSSL-informational) ![](https://img.shields.io/badge/uses-watchdog-informational)

In0ri is a defacement detection system utilizing a image-classification convolutional neural network.

## Introduction
When monitoring a website, In0ri will periodically take a screenshot of the website then put it through a preprocessor that will resize the image down to 250x250px and numericalize the image before passing it onto the classifier. The core of the classifier is a convolutional neural network that is trained to detect the defacement of a website. If the monitored website is indeed, defaced, In0ri will send out warnings via email to the user.

## Requirement
* Python3 (version >=3.6)
* Docker
* Docker-compose

## Installation

### Cloning the repository

```sh
git clone https://github.com/J4FSec/In0ri.git
cd In0ri
```

### Configuring email credentials to send notifications and agent keys from

Edit the file `FlaskApp/sendEmail.py`

```py
EMAIL_ADDRESS = "foo@gmail.com"
EMAIL_PASSWORD = "$uper$ecurePa$$word"
```

### Configure Telegram notification

Edit the file `chatbot.py`

```py
CHAT_ID= 'foo' // Channel ID to send notifications to
TOKEN = 'bar' // Bot token retrieved from @BotFather
```

### Starting In0ri

```sh
docker-compose up -d
```

## Usage

There's two ways to deploy In0ri:
* Running off crontab by periodically visiting the url.
* Internal agent running off the web server

### First Method: URL Check

Visit the WebUI on `https://<serverIP>:8080/` and click on "Register" then fill in the form and submit it.

### Second Method: Internal Agent

Visit the WebUI on `https://<serverIP>:8080/` and click on "Register" then fill in the form and submit it.

Click on "Create Agent" then fill in the form and check your email for the Agent's **key**.

On the web server that you wants to be monitored by In0ri, download the Agent folder from Github repository

Installing the required packages for the internal Agent

```sh
python3 -m pip install watchdog
python3 -m pip install requests
```

Edit the file `config.json` in the same folder as agent

```sh
nano config.json
```

A `key` is sent to your email after registering the Agent on the WebUI
`rootPath` is the root directory of the web application that you want to be monitored
`exludePath` are the subfolders that you wants excluded from the scans
`apiServer` is the URL to the API server of In0ri
`serverIP` is the IP of the API server of In0ri

```json
{
    "id":"01",
    "key":"123123123",
    "rootPath":"/var/www/html",
    "excludePath":"",
    "apiServer":"http://<serverIP>:8088/checkdeface"
}
```

And run the Agent:

```sh
python3 agent.py
```

## Authors

In0ri is built by Echidna with the help of Cu64 and Klone.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
