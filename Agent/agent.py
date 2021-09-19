import hashlib
import json
import re
import time

import requests
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

f = open("config.json", "r")
config = json.load(f)
key = config["key"]
excludePath = config["excludePath"]
server = config["apiServer"]
f.close()


def on_modified(event):
    if len(excludePath) != 0 and re.search(excludePath, event.src_path) is not None:
        return 0
    else:
        print(f"Notification, {event.src_path} has been modified")
        file_hash = hashlib.md5(open(event.src_path, "rb").read()).hexdigest()
        path = event.src_path
        path = path.replace(config["rootPath"], "")
        try:
            response = requests.post(
                server, json={"key": key, "path": path, "hash": file_hash}
            )
            print(response.json())
        except requests.ConnectionError as error:
            print("Server not found!")


def on_moved(event):
    if len(excludePath) != 0 and re.search(excludePath, event.src_path) is not None:
        return 0
    else:
        print(
            f"Notification, File {event.src_path} has been moved to {event.dest_path}"
        )
        file_hash = hashlib.md5(open(event.dest_path, "rb").read()).hexdigest()
        path = event.dest_path
        path = path.replace(config["rootPath"], "")
        try:
            response = requests.post(
                server, json={"key": key, "path": path, "hash": file_hash}
            )
            print(response.json())
        except requests.ConnectionError as error:
            print("Server not found!")


if __name__ == "__main__":
    patterns = [
        "*.html",
        "*.htm",
        "*.php",
        "*.txt",
        "*.jsp",
        "*.aspx",
        "*.shtml",
        "*.hta",
    ]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(
        patterns, ignore_patterns, ignore_directories, case_sensitive
    )
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path = config["rootPath"]
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
