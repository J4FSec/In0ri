![](img/logo_transparent.png)
![GitHub](https://img.shields.io/github/license/J4FSec/In0ri) ![](https://img.shields.io/badge/Python-3.6-informational) ![](https://img.shields.io/badge/uses-Flask-informational) ![](https://img.shields.io/badge/uses-Tensorflow-informational) ![](https://img.shields.io/badge/uses-Keras-informational) ![](https://img.shields.io/badge/uses-watchdog-informational)

In0ri is an automated, AI-powered website defacement detection system.

## Introduction
In0ri acts as an intelligent watchdog for your web applications. Instead of relying on traditional source code monitoring, it simulates real-user behavior by periodically taking screenshots of your target websites. These images are then analyzed by a trained model which is trained to identify visual anomalies and defacement patterns. Upon detecting a compromised page, In0ri immediately alerts administrators via Email or Telegram, enabling rapid incident response.

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

### Docker

You can also use In0ri via the official Docker container  [here](https://hub.docker.com/repository/docker/in0ri/defaced).

### Starting In0ri

```sh
docker-compose up --build -d
```
After running the In0ri, open an Internet browser to `https://<serverIP>:8080/` to show WebUI.

## Usage

There are two ways to deploy and using In0ri:
* Running off Celery Beat by periodically visiting the url.
* Internal agent running off the web server

### First Method: URL Check

Visit the Dashboard tab on WebUI, click on "Add URLs" then fill in the form and submit it.

### Second Method: Internal Agent

At the table listing all urls which were registered on WebUI, click on "Create Key" button at column Actions, the API Key will send to your email or click "Details" button to show it.

On the web server that you wants to be monitored by In0ri, download the Agent folder from Github repository

Installing the required packages for the internal Agent

```sh
python3 -m pip install -r requirements.txt
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
    "apiServer":"http://<serverIP>:8080/checkdeface"
}
```

And run the Agent:

```sh
python3 agent.py
```
## References

* [Black Hat Europe 2021](https://www.blackhat.com/eu-21/arsenal/schedule/index.html#inri-25045)
* [Black Hat Asia 2022](https://www.blackhat.com/asia-22/arsenal/schedule/#inri-open-source-defacement-detection-with-deep-learning-25866)
* [Black Hat USA 2022](https://www.blackhat.com/us-22/arsenal/schedule/index.html#inri-open-source-defacement-detection-with-deep-learning-27967)
* Mentioned by [Kitploit](https://www.kitploit.com/2021/07/in0ri-defacement-detection-with-deep.html)

## Authors

In0ri is built by Echidna with the help of Cu64 and Klone.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
