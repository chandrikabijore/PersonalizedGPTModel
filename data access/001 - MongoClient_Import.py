from pymongo import MongoClient                      # Yeh MongoClient ko import karega, jo ki MongoDB se connect hone ke liye use hota hai. 

client = MongoClient("mongodb://localhost:27017/")   #  Yeh aapke local MongoDB server se connect karne ka kaam karega.    # Local server ke liye
# client = MongoClient("mongodb+srv://<username>:<password>@cluster.mongodb.net/")             # Remote server ke liye

print("Connected to MongoDB successfully!")   

""" Agar koi error aata hai, to ensure karein ki:
MongoDB service chal rahi ho (mongod command se check karein).
Pymongo correctly install ho (pip install pymongo run karein).  """

print(client.list_database_names())  # Ye sabhi databases show karega 


