from pymongo import MongoClient

# Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

# Insert
data = {"name": "Rahul", "age": 25, "city": "Delhi"}
collection.insert_one(data)

# Read
for doc in collection.find():
    print(doc)

# Update
collection.update_one({"name": "Rahul"}, {"$set": {"age": 26}})

# Delete
collection.delete_one({"name": "Rahul"})

# Close connection
client.close()
   
  