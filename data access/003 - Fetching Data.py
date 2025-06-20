from pymongo import MongoClient

# MongoDB Server se connect hona
client = MongoClient("mongodb://localhost:27017/")

# Database aur Collection Select Karna
db = client["CampusCore"]  # Database ka naam
collection = db["resourcePool"]  # Collection ka naam  

# Saare documents fetch karna
data = collection.find()  # resourcePool ki jagah collection use karein bcoz abi resourcePool var define nhi tha 

# Data Print Karna
for document in data:
    print(document)


"""if resourcePool collection me data h, to output me documents print honge.
Agar koi data nahi hai, to output kuch bhi print nahi karega.
Agar data dekhna hai, to MongoDB Compass me check kar sakte hain."""