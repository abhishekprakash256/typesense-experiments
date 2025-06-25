# config.py

import os 

# MongoDB configurations
DB_NAME = "test-main-database"
COLLECTION_NAME = "test-article-collections"
MONGO_HOST_NAME = "localhost"

# File path
#FILE_PATH = "test_data.json"

#get the curr dir 
curr_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(curr_dir) 


#data file path 
FILE_PATH = parent_dir + "/test_data.json"