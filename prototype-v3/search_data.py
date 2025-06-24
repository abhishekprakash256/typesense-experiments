"""
search the data in the typesense 
"""

import typesense
import mongo_helper_kit



from config import DB_NAME, COLLECTION_NAME, MONGO_HOST_NAME, FILE_PATH


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




#make the search paramaters
search_parameters = {
  'q'         : 'neual',
  'query_by'  : 'article_data'

}


#get the res
res = client.collections['articles'].documents.search(search_parameters)


#get the id number from the data
id_numbers = [hit['document']['id'] for hit in res.get('hits', [])]
print(id_numbers)


#get the schema
#export_output = client.collections['articles'].documents.export()
#print(export_output)


#get the data from mongo using the id number 
mongo_helper = mongo_helper_kit.Helper_fun(MONGO_HOST_NAME)


