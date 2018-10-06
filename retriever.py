from pymongo import MongoClient

uri = "MONGODB_URI"

client = MongoClient(uri,
        connectTimeoutMS=30000,
        socketTimeoutMS=None)

db = client.get_database()
logs = db.logs

# maximum number of listing to display from db
listings_limit = 3
# cursor of db objects with most recent objects first
cursor = logs.find().sort([('_id', -1)]).limit(listings_limit)
for log in cursor:
    print(log["contents"] + "\n")
