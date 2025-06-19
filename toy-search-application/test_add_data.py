"""
The python file to make the collection and search
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



#make the collection , name books is used 
books_collection = {
  'name': 'books',
  'fields': [
    {'name': 'title', 'type': 'string' },
    {'name': 'authors', 'type': 'string[]', 'facet': True },

    {'name': 'publication_year', 'type': 'int32', 'facet': True },
    {'name': 'ratings_count', 'type': 'int32' },
    {'name': 'average_rating', 'type': 'float' }
  ],
  'default_sorting_field': 'ratings_count'
}

client.collections['books'].delete()

#make the collection
client.collections.create(books_collection)

#add the data to the schema 
with open('books.jsonl') as jsonl_file:
  client.collections['books'].documents.import_(jsonl_file.read().encode('utf-8'))





