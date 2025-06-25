"""
The file to ingest the data into the typesense using monogo
"""



import json
import os
import sys
import requests
import typesense
import mongo_helper_kit
from bson import ObjectId
from config import DB_NAME, COLLECTION_NAME, MONGO_HOST_NAME, FILE_PATH
from typesense.exceptions import TypesenseClientError



#make the client 
client = typesense.Client({
  'api_key': 'test_key',
  'nodes': [{
    'host': 'localhost',
    'port': '8108',
    'protocol': 'http'
  }],
  'connection_timeout_seconds': 2
})



#delete the collection if created 
#client.collections['articles'].delete()



def check_client():
    """
    The function to check the client health
    """
    try:
        collections = client.collections.retrieve()
        print("Connected successfully!")
        return True

    except Exception as e:
        print("Connection failed!")
        print("Error:", e)
        return False


def check_container_health():
    """
    The function to check the container health
    """
    url = "http://localhost:8108/health"

    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return True
        else:
            print(f"Typesense health check failed with status: {response.status_code}")
            return False
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Typesense: {e}")
        return False



#check the container health
print(check_container_health())

#check the client container
print(check_client())



#make the schema
#this is the nested schema 
#other stragety can be using the flatten the data and then use it 

article_schema = {
    "name": "articles",
    "enable_nested_fields": True,
    "fields": [
        {"name": "id", "type": "string"},  # Required primary key
        {"name": "article_name", "type": "string"},
        {"name": "slug", "type": "string"},
        {"name": "article_image", "type": "string"},
        {"name": "article_para", "type": "string"},
        {"name": "section_name", "type": "string", "facet": True},
        {"name": "id_number", "type": "int32"},

        # Flattened nested fields
        {"name": "article_data.title", "type": "string[]"},
        {"name": "article_data.article_para", "type": "string[]"},
        {"name": "article_data.markdown_data", "type": "string[]"},

        # Links
        {"name": "github_url", "type": "string"},
        {"name": "linkedin_url", "type": "string"},
        {"name": "twitter_url", "type": "string"},
        {"name": "leetcode_url", "type": "string"},
        {"name": "gitlab_url", "type": "string"},
        {"name": "kaggle_url", "type": "string"},
        {"name": "medium_url", "type": "string"},
        {"name": "demo_link", "type": "string"},
        {"name": "article_link", "type": "string"},
        {"name": "more_link", "type": "string"}
    ],
    "default_sorting_field": "id_number"
}




#create the collection
#if not check_container_health and not check_client(): 

client.collections.create(article_schema)

#get the schema
retrieve_response = client.collections['articles'].retrieve()
print(retrieve_response)


# Convert _id to id as string, keep the rest unchanged
def convert_id(doc):
    doc['id'] = str(doc['_id'])  # Rename and convert ObjectId
    del doc['_id']               # Remove original _id
    return doc


#make the mongo cleint
mongo_client = mongo_helper_kit.create_mongo_client(MONGO_HOST_NAME)

#the db name
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]


# Example: Fetching documents from MongoDB
mongo_documents = list(collection.find({}))

#get all mongo data
#print(mongo_documents)


# Convert _id to string for Typesense
cleaned_docs = [convert_id(doc) for doc in mongo_documents]

#insert the data into the typesnse 

response = client.collections['articles'].documents.import_(
    cleaned_docs,
    {'action': 'upsert'}  # 'upsert' means insert or update
)


#export the data and check
export_output = client.collections['articles'].documents.export()
print(export_output)