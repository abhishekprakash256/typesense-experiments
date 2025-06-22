"""
The file to complete feed the data into the typesense container and fetch it out 

https://typesense.org/docs/28.0/api/collections.html#notes-on-indexing-common-types-of-data

"""

#the data
test_data = {
        "article_name": "Tinyurl Shortener",
        "slug" : "tinyurl",
        "article_image" :"https://meabhi.me/static/blog/section/project/tinyurl/tinyurl-icon.png",
        "article_para" : "The Tiny-URL Generator is a URL shortening service developed as a web application using the Flask framework. This project aims to simplify the process of sharing long URLs by generating shorter, more manageable links. The backend leverages Redis for efficient data storage and retrieval, ensuring quick access and collision-free management of shortened URLs.",
        "section_name":"project", 
        "id_number" : 1,

        "article_data": [
                
            {"title": "Tiny Url Generator", "image_src": "https://meabhi.me/static/blog/section/project/tinyurl/tinyurl-icon.png", "article_para": "", "markdown_data": ""},
            {"title": "Project Description", "image_src": "", "article_para": "", "markdown_data": ""},
            {"title": "", "image_src": "", "article_para": "The Tinyurl generator is a URL shortening service developed as a web application using the Flask framework. This project aims to simplify the process of sharing long URLs by generating shorter, more manageable links. The backend leverages Redis for efficient data storage and retrieval, ensuring quick access and collision-free management of shortened URLs.", "markdown_data": ""},
            {"title": "", "image_src": "", "article_para": "", "markdown_data": "#### Key Features \n1. **URL Shortening**: Users can input long URLs and receive a shortened version that redirects to the original link. \n2. **Custom Aliases**: Option to create custom aliases for the shortened URLs, enhancing readability and memorability. \n3. **High Performance**: Utilizes Redis for storing and fetching URLs, ensuring rapid response times and scalability."},
            {"title": "", "image_src": "", "article_para": "", "markdown_data": "#### Technical Details \n- **Flask Server**: The web application is built using the Flask framework, providing a lightweight and flexible environment for handling HTTP requests and responses.\n- **Redis Integration**: Redis is used as the primary database, chosen for its speed and efficiency in handling large volumes of read/write operations.\n- **Redis Hash**: Used to avoid collisions by ensuring unique shortened URLs and storing mappings of short URLs to their original counterparts.\n- **Redis Sets**: Pre-generated short URLs are stored in a Redis set for faster allocation and retrieval.\n- **Redirect Functionality**: The application redirects users from the shortened URL to the original URL seamlessly."},
            {"title": "", "image_src": "https://meabhi.me/static/blog/section/project/tinyurl/tinyurl-system-design.png", "article_para": "", "markdown_data": ""},
            {"title": "", "image_src": "", "article_para": "", "markdown_data": "#### Implementation\n1. **Adding Data**: A Redis helper function is used to add new URL mappings. It checks for collisions using Redis hash and ensures each short URL is unique.\n2. **Fetching Data**: For retrieving the original URL, the application fetches the corresponding value from the Redis hash, utilizing the pre-generated values from the Redis set for efficient data access.\n3. **Collision Avoidance**: By using Redis hash, the application effectively manages and prevents URL collisions, maintaining the integrity of the service."},
            {"title": "", "image_src": "", "article_para": "", "markdown_data": "#### Benefits\n- **Speed**: The use of Redis ensures quick read/write operations, making the URL shortening and redirection process almost instantaneous.\n- **Scalability**: The application is designed to handle a large number of URL mappings, making it suitable for high-traffic environments.\n- **Reliability**: The collision avoidance mechanisms and pre-generated URL values ensure consistent performance and reliability."},
            {"title": "", "image_src": "", "article_para": "", "markdown_data": "#### Motivation \nInspired by the system design principles of existing URL shortening services, this project was undertaken to create a custom solution tailored to specific needs. The choice of Redis as the database and the overall system architecture significantly improved the efficiency and reliability of URL shortening, making the service dependable for both personal and broader use cases."},
            {"title": "", "image_src": "", "article_para": "", "markdown_data": "#### Conclusion \nThe Tinyurl Generator project showcases the integration of Flask and Redis to build a robust, high-performance URL shortening service. With its emphasis on speed, scalability, and ease of use, this application serves as a reliable tool for managing and sharing URLs efficiently."}
    
        


        ],

        "github_url" : "https://github.com/abhishekprakash256/tinyurl-service",
        "linkedin_url" : "",
        "twitter_url" : "",
        "leetcode_url" : "",
        "gitlab_url" : "",
        "kaggle_url" : "",
        "medium_url" : "",
        "demo_link":"/demo/tinyurl",
        "article_link" : "/blog/section/project/article/tinyurl" , 
        "more_link": "/blog/section/project"

}









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
DATA_FILE_PATH = parent_dir + "/test_data.json"

#read the json data 
with open(DATA_FILE_PATH, 'r') as file:
    data = json.load(file)





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
client.collections['articles'].delete()



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
    "name": "articles",  # Collection name
    "enable_nested_fields" : True, 
    "fields": [

        {"name": "article_name", "type": "string"},
        {"name": "slug", "type": "string"},
        {"name": "article_image" , "type": "string" },
        {"name" : "article_para", "type" : "string"},
        {"name": "section_name", "type": "string", "facet": True},
        {"name": "id_number", "type": "int32", "facet": False},

        {"name": "article_data.title", "type" : "string[]" , "facet": True },
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
        {"name": "more_link", "type": "string"},

        # Nested/complex data: flatten or skip
        # Typesense does not support nested objects like 'article_data', so you can either:
        # 1. Skip it from indexing, or
        # 2. Flatten relevant text content into one field (recommended)
    ],
    "default_sorting_field": "id_number"
}



#create the collection 
#if not check_container_health and not check_client(): 

client.collections.create(article_schema)

#get the schema
retrieve_response = client.collections['articles'].retrieve()
print(retrieve_response)



#add the data to the schema or test_data
client.collections['articles'].documents.create(test_data)


export_output = client.collections['articles'].documents.export()
print(export_output)