# -*- coding: utf-8 -*-
from pymongo import MongoClient, errors
import pychromecast
import configparser

def get_col():
    parser = configparser.RawConfigParser()
    configfile = r'db/db.cfg'
    parser.read(configfile)

    server=parser.get('mongo','server')
    base=parser.get('mongo','base')
    collection=parser.get('mongo','collection')    

    try:
        return MongoClient(server)[base][collection]
    except errors.ServerSelectionTimeoutError:
        return None

def write(dict,clave):
    col=get_col()
    delete(dict,clave,col)
    col.insert_one(dict)

def read():
    col=get_col()
    return col.find()

def delete(dict,clave,col=None):
    if(col==None):
        col=get_col()
    col.delete_many({clave: dict[clave]})
