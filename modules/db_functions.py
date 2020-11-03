# -*- coding: utf-8 -*-
from pymongo import MongoClient, errors
import pychromecast

def write(dict,clave):
    try:
        client = MongoClient("mongodb://localhost/")
        db = client["cast"]
        col = db["events"]
        col.delete_many({clave: dict[clave]})
        col.insert_one(dict)
    except errors.ServerSelectionTimeoutError as err:
        client = None

def read():
    try:
        client = MongoClient("mongodb://localhost/")
        db = client["cast"]
        col = db["events"]
        return col.find()
    except errors.ServerSelectionTimeoutError as err:
        return None