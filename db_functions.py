# -*- coding: utf-8 -*-
import pymongo
client = pymongo.MongoClient("mongodb://localhost/")
db = client["cast"]
col = db["events"]