"""
search the data in the typesense 
"""

import typesense


#make the client

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
  'query_by'  : 'article_data',
  

}


#get the res
res = client.collections['articles'].documents.search(search_parameters)


#print the res
print(res)


#parsing the json as results 

