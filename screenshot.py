# coding=utf-8
import hashlib
import os
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

<<<<<<< HEAD
=======

>>>>>>> e3b46280aed34928603577d7a12b04d5c502a226
if not os.path.exists("/opt/In0ri/FlaskApp/static/images/"):
    os.makedirs("/opt/In0ri/FlaskApp/static/images/")


def screenshot(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

<<<<<<< HEAD
=======

>>>>>>> e3b46280aed34928603577d7a12b04d5c502a226
    name = hashlib.md5(url.encode())
    try:
        driver.get(url)
        print("Screenshoting..." + url)
        time.sleep(6)
<<<<<<< HEAD
        driver.get_screenshot_as_file(
            "/opt/In0ri/FlaskApp/static/images/" + name.hexdigest() + ".png"
        )
=======
        driver.get_screenshot_as_file("/opt/In0ri/FlaskApp/static/images/" + name.hexdigest() + ".png")
>>>>>>> e3b46280aed34928603577d7a12b04d5c502a226
        driver.quit()
    except RuntimeError:
        print("URL " + url + " was died!")
        pass
<<<<<<< HEAD
=======
    # resize gov_images
    # print("resizing...")
    # image = Image.open("/opt/In0ri/images/web_screenshot.png")
    # # new_image = image.resize((250, 250))
    # name = hashlib.md5(url.encode())
    # image.save("/opt/In0ri/images/" + name.hexdigest() + ".png")
>>>>>>> e3b46280aed34928603577d7a12b04d5c502a226

    return "/opt/In0ri/FlaskApp/static/images/" + name.hexdigest() + ".png"
