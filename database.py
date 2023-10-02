from pymongo import MongoClient
from dotenv import load_dotenv

import os

load_dotenv()

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# uri = "mongodb+srv://"+ DATABASE_USERNAME + ":" + DATABASE_PASSWORD + "@cluster0.cyg7ayc.mongodb.net/?retryWrites=true&w=majority"
uri = "mongodb://localhost:27017"
# create a client and connect to the database
client = MongoClient(uri)

db = client["Graphql-Table"]

collection = db["graphql_user"]
collection2 = db["graphql_user2"]#
