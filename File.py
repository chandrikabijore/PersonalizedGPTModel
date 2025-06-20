import pymongo
from pymongo.errors import ConnectionFailure
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class MongoDBHandler:
    def __init__(self, uri: str, database: str, collection: str): 
        """
        Initialize MongoDB connection handler
        """
        self.uri = uri
        self.database_name = database
        self.collection_name = collection
        self.client = None
        self.db = None
        self.collection = None 

    def connect(self) -> bool:
        """Establish connection to MongoDB"""
        try:
            self.client = pymongo.MongoClient(self.uri, serverSelectionTimeoutMS=30000, connectTimeoutMS=20000)
            
            # Test the connection
            self.client.admin.command("ping")
            logger.info("Successfully connected to MongoDB")

            # Select database and collection
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            return True

        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False

        except Exception as e:
            logger.error(f"Unexpected error while connecting to MongoDB: {e}")
            return False

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

    def insert_xlsx(self, file_path: str) -> int:
        """
        Insert data from an XLSX/CSV file into MongoDB
        """
        try:
            # Read data from the file
            df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path, engine="openpyxl")

            if df.empty:
                logger.warning("No data found in the file")
                return 0

            # Convert DataFrame to list of dictionaries and insert
            data = df.to_dict(orient="records")
            result = self.collection.insert_many(data)
            inserted_count = len(result.inserted_ids)
            logger.info(f"Successfully inserted {inserted_count} documents")
            return inserted_count

        except Exception as e:
            logger.error(f"Error inserting file data: {e}")
            return 0

def main():
    # MongoDB Atlas connection string (Make sure your credentials are correct)
    MONGO_URI = "mongodb+srv://cookiki-MC:mqnwbe01@clusters.u6xoupg.mongodb.net/?retryWrites=true&w=majority"
    FILE_PATH = "Chandrika_Bijore.csv"

    # Initialize MongoDB handler
    mongo_handler = MongoDBHandler(uri=MONGO_URI, database="Ik_society", collection="question_answer")

    try:
        if mongo_handler.connect():
            # Insert CSV data
            inserted_count = mongo_handler.insert_xlsx(FILE_PATH)
            print(f"Successfully inserted {inserted_count} documents from {FILE_PATH}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        mongo_handler.close()

if __name__ == "__main__":
    main()  