# -*- coding: utf-8 -*-
from pymongo import MongoClient, errors
import pychromecast

def get_col(mongo,base,collection):
    try:
        client = MongoClient(mongo)
        db = client[base]
        col = db[collection]
        return col
    except errors.ServerSelectionTimeoutError as err:
        return None

def write(dict,clave):
    col=get_col("mongodb://localhost/","cast","events")
    delete(dict,clave,col)
    col.insert_one(dict)

def read():
    col=get_col("mongodb://localhost/","cast","events")
    return col.find()

def delete(dict,clave,col=None):
    if(col==None):
        col=get_col("mongodb://localhost/","cast","events")
    col.delete_many({clave: dict[clave]})
