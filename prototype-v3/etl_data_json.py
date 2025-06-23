"""
The file to take the data from mongodb and put into typesense 
"""


"""
steps - 

take the data out into a json file 
convert the json file to jonsl file 
insert that jsonl file to typesnese
"""

import json
import subprocess
import mongo_helper_kit
from config import DB_NAME, COLLECTION_NAME, MONGO_HOST_NAME, FILE_PATH



#make the mongo cleint
mongo_client = mongo_helper_kit.create_mongo_client(MONGO_HOST_NAME)



def data_to_json(db_name, collection_name, output_file="output.json"):
    """
    Retrieve all documents from a MongoDB collection and save them into a JSON file.
    """
    db = mongo_client[db_name]
    collection = db[collection_name]

    if collection is not None:
        # Retrieve all documents
        documents = collection.find()

        # Convert to list and transform _id to string
        data_list = []
        for document in documents:
            document["_id"] = str(document["_id"])  # Convert ObjectId to string
            data_list.append(document)

        # Save to JSON file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data_list, f, indent=2, ensure_ascii=False)

        print(f"Data exported to {output_file}")
    else:
        print("No collection available. Please create a collection first.")




def create_jsonl_file():
    """
    create the jsonl file from the json file 
    """
    try:
        subprocess.run(
            ["jq", "-c", ".[]", "output.json"],
            stdout=open("output.jsonl", "w"),
            check=True
        )
        print("Converted output.json to output.jsonl")
    except subprocess.CalledProcessError as e:
        print("Error running jq:", e)







if __name__ == "__main__" :

    #make the data to json 
    data_to_json(DB_NAME,COLLECTION_NAME)

    #create the jsonl file
    create_jsonl_file()