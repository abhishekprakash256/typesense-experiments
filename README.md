# Typesense Experiments

This repo is for experimenting with [Typesense](https://typesense.org) — an open-source typo-tolerant search engine optimized for fast and relevant search experiences.

## 🔧 Setup

### 1. Run Typesense (Docker)
```bash
export TYPESENSE_API_KEY=test_key

docker pull typesense/typesense:29.0.rc30   #use the tags , pull the docker image

docker run -d --name typesense -p 8108:8108 -v$(pwd)/typesense-data:/data typesense/typesense:29.0.rc30 --data-dir /data --api-key=$TYPESENSE_API_KEY --enable-cors

````

### 2. Python Client Install

```bash
pip install typesense
```

## 🧪 Sample Python Script

```python
import typesense

client = typesense.Client({
  'nodes': [{
    'host': 'localhost',
    'port': '8108',
    'protocol': 'http'
  }],
  'api_key': 'test_key',
  'connection_timeout_seconds': 2
})

# List collections
print(client.collections.retrieve())
```

## 🔄 Common Operations

### Create Collection

```python
schema = {
  "name": "books",
  "fields": [
    {"name": "title", "type": "string"},
    {"name": "author", "type": "string"},
    {"name": "year", "type": "int32"}
  ]
}
client.collections.create(schema)
```

### Add Document

```python
client.collections['books'].documents.create({
  "title": "Atomic Habits",
  "author": "James Clear",
  "year": 2018
})
```

### Search

```python
results = client.collections['books'].documents.search({
  "q": "Atomic",
  "query_by": "title"
})
print(results)
```

### Delete Collection

```python
client.collections['books'].delete()
```

---

## 📚 Docs

* [Typesense Docs](https://typesense.org/docs/)
* [Python Client Docs](https://typesense.org/docs/0.25.1/api/python.html)
- https://github.com/typesense/typesense-python/blob/master/examples/alias_operations.py
- https://typesense.org/docs/guide/installing-a-client.html

