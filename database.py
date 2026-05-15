import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
database_name = os.getenv("MONGO_DATABASE", "english_b2_trainer")
collection_name = os.getenv("MONGO_COLLECTION", "vocabulary")

client = MongoClient(mongo_uri)

db = client[database_name]
vocabulary_collection = db[collection_name]