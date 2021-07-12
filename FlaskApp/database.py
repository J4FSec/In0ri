import pymongo
import os

connection = pymongo.MongoClient(
    "mongodb://"
    + os.environ["MONGODB_USERNAME"]
    + ":"
    + os.environ["MONGODB_PASSWORD"]
    + "@"
    + os.environ["MONGODB_HOSTNAME"]
    + ":27017/"
)
database = connection["deface"]
collection = database["site"]


def insert_data(data):
    document = collection.insert_one(data)
    return document.inserted_id


def get_single_data(data):
    data = collection.find_one(data)
    return data


def get_multiple_data():
    data = collection.find()
    return list(data)


def update_existing(unique, data):
    document = collection.update_one(unique, {"$set": data})
    return document.acknowledged


def remove_data(data):
    document = collection.delete_one(data)
    return document.acknowledged


# for x in get_multiple_data():
#       print(x)
