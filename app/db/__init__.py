from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi


load_dotenv()

# MongoDB connection URI
MONGO_URI = os.environ.get("MONGO_URI")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())
db = client[DATABASE_NAME]

# Collection for users
users_collection = db["users"]
