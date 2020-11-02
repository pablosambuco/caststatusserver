# -*- coding: utf-8 -*-
import pymongo
import pychromecast



def write(dict,clave):
    client = pymongo.MongoClient("mongodb://localhost/")
    db = client["cast"]
    col = db["events"]
    col.delete_many({clave: dict[clave]})
    col.insert_one(dict)
