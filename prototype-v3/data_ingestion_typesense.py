"""
Insert the data into the typesene container from the mongo container 
"""



import json
import os
import sys
import requests
import typesense

from typesense.exceptions import TypesenseClientError

#get the curr dir 
curr_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(curr_dir) 


#data file path 
#DATA_FILE_PATH = parent_dir + "output.jsonl"


DATA_FILE_PATH = "flattened_output.jsonl"

#read the json data 
"""
with open(DATA_FILE_PATH, 'r') as file:
    data = json.load(file)
"""




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



def flatten_article_jsonl(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            doc = json.loads(line.strip())

            # Convert _id to id
            doc["id"] = str(doc.pop("_id"))

            # Flatten article_data
            titles = []
            paras = []
            markdowns = []

            for entry in doc.get("article_data", []):
                titles.append(entry.get("title", ""))
                paras.append(entry.get("article_para", ""))
                markdowns.append(entry.get("markdown_data", ""))

            doc["article_data.title"] = titles
            doc["article_data.article_para"] = paras
            doc["article_data.markdown_data"] = markdowns

            # Optional: remove the original article_data array
            doc.pop("article_data", None)

            # Write the flattened doc back to JSONL
            outfile.write(json.dumps(doc) + "\n")

    print(f"Flattened JSONL written to: {output_path}")




flatten_article_jsonl("output.jsonl", "flattened_output.jsonl")



#add the data to the schema or test_data
#client.collections['articles'].documents.create(test_data)
with open(DATA_FILE_PATH) as jsonl_file:
    data = jsonl_file.read().encode('utf-8')
    response = client.collections['articles'].documents.import_(data)
    print(response)




#export the data and check
export_output = client.collections['articles'].documents.export()
print(export_output)