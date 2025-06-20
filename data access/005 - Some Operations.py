from pymongo import MongoClient
from pprint import pprint  # For Pretty print ✅ Output aur Clean Hoga (Diff is here only)

client = MongoClient("mongodb://localhost:27017/")
db = client["CampusCore"]
collection = db["resourcePool"] 

# 1) Count Questions Containing "DAVV"

count = collection.count_documents({"Question": {"$regex": "davv", "$options": "i"}})
print("Total Questions containing 'DAVV':", count)



# 2) Find Questions Containing "Admission"

# data = collection.find({"Question": {"$regex": "Admission", "$options": "i"}}, {"Question": 1, "Answer": 1, "_id": 0})
# for document in data:
#     print(document) 
    
# count = collection.count_documents({"Question": {"$regex": "Admission", "$options": "i"}}) 
# print("Total Questions containing 'Admission' : ", count)



# 3) Update a Question

# collection.update_one(
#     {"Question": "What is the fee structure for these programs?"},
#     {"$set": {"Answer": "The average annual fee is INR 80,000. It may vary based on the course."}}
# )



# collection.find_one({"Question": "What is the fee structure for these programs?"})

# for document in collection.find():
#     print(document) 
    


# Delete a Question Containing "fee structure" 

# collection.delete_one({"Question": {"$regex": "fee structure", "$options": "i"}})