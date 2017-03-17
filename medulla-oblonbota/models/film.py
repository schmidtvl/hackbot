from mongothon import *
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.film_database

film_schema = Schema({
    "name": {"type": str, "required": True},
    "suggesters": {"type": Array(str), "required":True}
})

Film = create_model(film_schema, db['films'])
