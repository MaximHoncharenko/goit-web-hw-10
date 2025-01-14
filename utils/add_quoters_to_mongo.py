import json
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client.hw_10

with open('quotes.json', 'r', encoding='utf-8') as fd:
    quotes = json.load(fd)



for quote in quotes:
    author= db.authors.find_one({'fullname': quote['author']})
    if author:
        db.quotes.insert_one({'quote':quote['text'], 'author': ObjectId(author['_id']), 'tags': quote['tags']})