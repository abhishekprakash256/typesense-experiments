# Typesense Experiments

This repo is for experimenting with [Typesense](https://typesense.org) — an open-source typo-tolerant search engine optimized for fast and relevant search experiences.

## 🔧 Setup

### 1. Run Typesense (Docker)
```bash
docker run -d \
  -p 8108:8108 \
  -v$(pwd)/data:/data \
  typesense/typesense:0.25.1 \
  --data-dir /data --api-key=test_key --enable-cors
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

```

