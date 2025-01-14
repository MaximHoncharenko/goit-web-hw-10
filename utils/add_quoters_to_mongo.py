import json
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost')
db = client.hw

with open('D:/Projects/reps/goit-web-hw-10/utils/quotes.json', 'r', encoding='utf-8') as fd:
    quotes = json.load(fd)



for quote in quotes:
    author= db.authors.find_one({'fullname': quote['author']})
    if author:
        db.quoters.insert_one({'quote': quote['quote'],
                                'author': author['_id'],
                                'tags': quote['tags']})