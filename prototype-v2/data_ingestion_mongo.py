"""
Data CRUD Operations Script

This script handles data insertion, deletion, and retrieval for a MongoDB database.
It uses the mongo_helper_kit and loads data from a JSON file.

Author: Abhishek Prakash (meabhi.me)     
"""

import json
import mongo_helper_kit
from config import DB_NAME, COLLECTION_NAME, MONGO_HOST_NAME, FILE_PATH


def load_json_data(file_path):
    """
    Load data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict or list: Loaded JSON data.
    """
    with open(file_path, 'r') as file:
        return json.load(file)


def initialize_helper(host_name):
    """
    Initialize the MongoDB helper.

    Args:
        host_name (str): MongoDB host name.

    Returns:
        mongo_helper_kit.Helper_fun: Helper instance.
    """
    return mongo_helper_kit.Helper_fun(host_name)


def perform_database_operations():
    """
    Perform various database operations:
    - Create database and collection (optional)
    - Insert data
    - Delete database (CAUTION!)
    - Show all data
    - Get article data (example)
    """
    # Initialize helper
    db_helper = initialize_helper(MONGO_HOST_NAME)

    # Load data from JSON file
    data = load_json_data(FILE_PATH)  

    # --- Uncomment operations as needed ---

    # Create database and collection (if needed)
    db_helper.make_database_and_collection(DB_NAME, COLLECTION_NAME)

    # Insert data
    db_helper.insert_data(DB_NAME, COLLECTION_NAME, data)

    # Delete entire database (USE WITH CAUTION!)
    #db_helper.delete_db(DB_NAME)

    # Show all data (prints to console)
    db_helper.show_all_data(DB_NAME, COLLECTION_NAME)

    # Example: Get specific article data
    # result = db_helper.show_article_data(DB_NAME, COLLECTION_NAME, {'article_name': "test1"})
    # result = db_helper.get_article_data(DB_NAME, COLLECTION_NAME, "tech", "test2")
    # print(result)


if __name__ == "__main__":
    perform_database_operations()

