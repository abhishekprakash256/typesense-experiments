"""
The test connection for the docker conrainer 
"""

import typesense

client = typesense.Client({
  'nodes': [{
    'host': 'localhost', # For Typesense Cloud use xxx.a1.typesense.net
    'port': '8108',      # For Typesense Cloud use 443
    'protocol': 'http'   # For Typesense Cloud use https
  }],
  'api_key': 'test_key',
  'connection_timeout_seconds': 2
})




try:
    collections = client.collections.retrieve()
    print("Client is connected. Collections available:", collections)
except Exception as e:
    print("Failed to connect to Typesense server:", str(e))