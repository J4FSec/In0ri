# coding=utf-8
import hashlib
import os
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager

if not os.path.exists("/opt/In0ri/FlaskApp/static/images/"):
    os.makedirs("/opt/In0ri/FlaskApp/static/images/")

firefox_path=GeckoDriverManager().install()


def screenshot(url):
    options = webdriver.FirefoxOptions()
    options.headless = True
    options.add_argument("--start-maximized")
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--no-sandbox')
    driver = webdriver.Firefox(options=options, executable_path=firefox_path)


    name = hashlib.md5(url.encode())
    try:
        driver.get(url)
        print("Screenshoting..." + url)
        time.sleep(6)
        driver.get_screenshot_as_file(
            "/opt/In0ri/FlaskApp/static/images/" + name.hexdigest() + ".png"
        )
        driver.get_screenshot_as_file("/opt/In0ri/FlaskApp/static/images/" + name.hexdigest() + ".png")
        driver.quit()
    except Exception as e:
        print(e)
        print("URL " + url + " was died!")
        pass

    return "/opt/In0ri/FlaskApp/static/images/" + name.hexdigest() + ".png"
