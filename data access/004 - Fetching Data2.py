from pymongo import MongoClient
from pprint import pprint  # For Pretty print ✅ Output aur Clean Hoga (Diff is here only)

client = MongoClient("mongodb://localhost:27017/")
db = client["CampusCore"]
collection = db["resourcePool"] 



print("Found a document")  # Debugging ke liye



# data = collection.find()
# for document in data:
#     pprint(document)  # Normal print ki jagah pprint use karein 
    


# Sirf Question aur Answer fetch karo

# data = collection.find({}, {"Question": 1, "Answer": 1, "_id": 0})   
# for document in data:
#     pprint(document) 



# Sirf 10 documents fetch honge   
 
# data = collection.find({}, {"Question": 1, "Answer": 1, "_id": 1}).limit(10)   # id me 1 ki place pr 0 denge to id exclude hogi
# for document in data:
#     print(document)
    
    
    
# Any specific Q, toh find() use karo:
 
# query = {"Question": "What are the eligibility criteria for the BBA program?"}
# data = collection.find(query, {"Question": 1, "Answer": 1, "_id": 0})   
# for document in data:
#     pprint(document) 
    
    
    
# Agar partial search karna ho (e.g., contains "fee structure"), Ye "fee structure" wale sare questions ko search karega (chahe lower/uppercase kuch bhi ho).
# Agar question ka exact text nahi pata, bas kuch keywords se search karna ho, toh Regular Expression ($regex) ka use karo:
 
query = {"Question": {"$regex": "fee structure", "$options": "i"}}  # "i" -> case-insensitive search
data = collection.find(query, {"Question": 1, "Answer": 1, "_id": 0})

for document in data:
    print(document) 
    
    
    
# Total Questions Count Karne Ke Liye 
total_questions = collection.count_documents({})
print("Total Questions:", total_questions)

 
# specific Q find krna h like fee structure kitne Q me exist krta h 
total_fee_questions = collection.count_documents({"Question": {"$regex": "fee structure", "$options": "i"}})
print("Total 'fee structure' Questions:", total_fee_questions)

"""
"Question": {"$regex": "fee structure", "$options": "i"} →  $regex "fee structure" ko search karega.  
"$options": "i" → Case-insensitive search karega (i.e., "Fee Structure" bhi match hoga).
count_documents({...}) → Matched documents ka count karega
"""
 