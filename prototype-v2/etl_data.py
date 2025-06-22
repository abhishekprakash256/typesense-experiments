"""
The file to take the data from mongodb and put into typesense 
"""


"""
steps - 

take the data out into a json file 
convert the json file to jonsl file 
insert that jsonl file to typesnese
"""


import mongo_helper_kit
from config import DB_NAME, COLLECTION_NAME, MONGO_HOST_NAME, FILE_PATH




mongo_client = mongo_helper_kit.create_mongo_client(MONGO_HOST_NAME)


def show_all_data(db_name,collection_name):
    """
    Show the data in the collection
    """
    db = mongo_client[db_name]
    collection = db[collection_name]


    if collection is not None:
        # Retrieve all documents in the collection
        documents = collection.find()

        # Print each document
        for document in documents:
            print(document)
    else:
        print("No collection available. Please create a collection first.")



show_all_data(DB_NAME,COLLECTION_NAME)