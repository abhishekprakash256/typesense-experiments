"""
The file to search the data in the typesense 
in a particukaur collection 
"""

import typesense


#make the client
client = typesense.Client({
  'nodes': [{
    'host': 'localhost', # For Typesense Cloud use xxx.a1.typesense.net
    'port': '8108',      # For Typesense Cloud use 443
    'protocol': 'http'   # For Typesense Cloud use https
  }],
  'api_key': 'test_key',
  'connection_timeout_seconds': 2
})


#make the search paramaters
search_parameters = {
  'q'         : 'harry potter',
  'query_by'  : 'title',
  'sort_by'   : 'ratings_count:desc'
}


#get the res
res = client.collections['books'].documents.search(search_parameters)


#print the res
print(res)