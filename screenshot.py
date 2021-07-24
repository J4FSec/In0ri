# coding=utf-8
import os
import time
import hashlib
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


if not os.path.exists("/opt/In0ri/images"):
    os.makedirs("/opt/In0ri/images")


def screenshot(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        print("Screenshoting..." + url)
        time.sleep(6)
        driver.get_screenshot_as_file("/opt/In0ri/images/web_screenshot.png")
        driver.quit()
    except RuntimeError:
        print("URL " + url + " was died!")
        pass
    # resize gov_images
    print("resizing...")
    image = Image.open("/opt/In0ri/images/web_screenshot.png")
    new_image = image.resize((250, 250))
    name = hashlib.md5(url.encode())
    new_image.save("/opt/In0ri/images/" + name.hexdigest() + ".png")

    return "/opt/In0ri/images/" + name.hexdigest() + ".png"
