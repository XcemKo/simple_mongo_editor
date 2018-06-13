import pymongo
import sys
from tables import *

client = pymongo.MongoClient()

try:
    print(client.is_mongos)
except:
    print("Mongo not connected")
    sys.exit(1)

users = client['test'].users
db = client['test']

def checkUser(usr, pwd):
    col = users.find(projection={'_id': 0})
    ret = False
    for doc in col:
            user = [value for value in doc.values()][0]
            pswd = [value for value in doc.values()][1]
            if (user == usr and pswd == pwd):
                ret = True
    return ret

def getCollections():
    return db.collection_names()

def writeCol(name, keys, items):
    if name in tables and len(keys)==len(items):
        col = db[name]
        req = dict()
        for index, key in enumerate(keys):
            req[key] = items[index]
        find = col.find_one({keys[0]: items[0]})
        if find is None:
            col.insert_one(req)
        else:
            print("Есть  - {}".format(items[0]))
    else:
        if name not in tables.tables:
            print("Not have {}".format(name))
        elif len(keys) != len(items):
            print("Len keys != items")
        return None

def updateDoc(name, id, dict):
    db[name].update_many(   {'_id': id},
                            {'$set':dict})

def insertDoc(name, id, dict):
    db[name].insert(dict)

def getDocuments(name):
    ret = []
    for doc in db[name].find():
        ret.append(doc)
    return ret

def getColumnFromCollection(name_col, column):
    docs = getDocuments(name_col)
    ret = []
    for doc in docs:
        ret.append(doc[column])
    return ret

#print(getCollections())





