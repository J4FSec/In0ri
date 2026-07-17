import os
import re
import hashlib
from datetime import datetime

from celery import Celery

import alert
from FlaskApp.database import Database

# Global state for Warm Start (Model and Browser)
_yolo_model = None
_playwright = None
_browser = None
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FlaskApp", "static", "images")
YOLO_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best.onnx")

redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("in0ri_tasks", broker=redis_url, backend=redis_url)

celery_app.conf.beat_schedule = {
    'dispatch-checks-every-minute': {
        'task': 'tasks.dispatch_checks',
        'schedule': 60.0,
    },
}
celery_app.conf.timezone = 'UTC'

def get_yolo_model():
    global _yolo_model
    if _yolo_model is None:
        from ultralytics import YOLO
        _yolo_model = YOLO(YOLO_MODEL_PATH, task='classify')
    return _yolo_model

def get_browser():
    global _playwright, _browser
    if _playwright is None:
        from playwright.sync_api import sync_playwright
        _playwright = sync_playwright().start()
        _browser = _playwright.chromium.launch(headless=True)
    return _browser

def take_screenshot(url):
    name = hashlib.md5(url.encode()).hexdigest()
    image_path = os.path.join(IMAGE_DIR, f"{name}.png")
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    browser = get_browser()
    page = browser.new_page()
    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.screenshot(path=image_path)
    finally:
        page.close()
    return image_path



@celery_app.task
def dispatch_checks():
    db = Database("site")
    try:
        sites = db.get_multiple_data()
    except Exception as e:
        print(f"DB Connection Error in Dispatcher: {e}")
        return

    now = datetime.now()
    
    for site in sites:
        time_str = site.get("time", "")
        # parse "X hours Y minutes"
        match = re.search(r"(\d+) hours (\d+) minutes", time_str)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            interval_seconds = hours * 3600 + minutes * 60
            
            last_checked = site.get("last_checked")
            if not last_checked:
                # Never checked before
                check_url_task.delay(site["url"], site["email"])
                db.update_existing({"url": site["url"]}, {"last_checked": now})
            else:
                elapsed = (now - last_checked).total_seconds()
                if elapsed >= interval_seconds:
                    check_url_task.delay(site["url"], site["email"])
                    db.update_existing({"url": site["url"]}, {"last_checked": now})

@celery_app.task(bind=True)
def check_url_task(self, url, email, infected_path=None):
    al = alert.Alert()
    print(f"[*] Checking {url}")
    
    # 1. Screenshot
    try:
        img_path = take_screenshot(url)
    except Exception as e:
        print(f"[-] Failed to screenshot {url}: {e}")
        return

    # 2. Inference
    model = get_yolo_model()
    
    results = model(img_path)
    
    result = "clean"
    conf = 0.0
    # In YOLO classification, results[0].probs contains top1 and top5
    # From our inspection, names are {0: 'clean', 1: 'defaced'}
    if results and len(results) > 0 and results[0].probs is not None:
        top_class = results[0].probs.top1
        conf = float(results[0].probs.top1conf)
        if top_class == 1:
            result = "defaced"

    # 2.5 Draw Custom Label
    try:
        import cv2
        img = cv2.imread(img_path)
        if img is not None:
            # BGR format: Red for defaced, Green for clean
            bg_color = (0, 0, 255) if result == "defaced" else (0, 200, 0)
            text = f"{result.upper()} {conf:.2f}"
            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 1.2
            thickness = 2
            
            # Calculate text size to draw background rectangle
            (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
            padding = 15
            
            cv2.rectangle(img, (0, 0), (text_w + padding*2, text_h + padding*2 + baseline), bg_color, -1)
            cv2.putText(img, text, (padding, text_h + padding), font, font_scale, (255, 255, 255), thickness)
            
            cv2.imwrite(img_path, img)
    except Exception as ex:
        print(f"[-] Failed to draw label: {ex}")
    
    # 3. Alert
    if result == "defaced":
        print(f"[!] Website was defaced: {url}")
        al.sendBot(url, img_path)
        subject = "Website Defacement"
        if infected_path:
            message = f"Your website was defaced!\nURL: {url}\nPath infected: {infected_path}"
        else:
            message = f"Your website was defaced!\nURL: {url}"
        al.sendMessage(email, subject, message, img_path)
    else:
        print(f"[+] Everything oke: {url}")
