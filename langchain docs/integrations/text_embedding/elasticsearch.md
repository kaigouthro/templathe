# Elasticsearch

Walkthrough of how to generate embeddings using a hosted embedding model in Elasticsearch

The easiest way to instantiate the `ElasticsearchEmbeddings` class it either

- using the `from_credentials` constructor if you are using Elastic Cloud
- or using the `from_es_connection` constructor with any Elasticsearch cluster

```bash
pip -q install elasticsearch langchain  

```

```python
import elasticsearch  
from langchain.embeddings.elasticsearch import ElasticsearchEmbeddings  

```

```python
# Define the model ID  
model\_id = "your\_model\_id"  

```

## Testing with `from_credentials`[​](#testing-with-from_credentials "Direct link to testing-with-from_credentials")

This required an Elastic Cloud `cloud_id`

```python
# Instantiate ElasticsearchEmbeddings using credentials  
embeddings = ElasticsearchEmbeddings.from\_credentials(  
 model\_id,  
 es\_cloud\_id="your\_cloud\_id",  
 es\_user="your\_user",  
 es\_password="your\_password",  
)  

```

```python
# Create embeddings for multiple documents  
documents = [  
 "This is an example document.",  
 "Another example document to generate embeddings for.",  
]  
document\_embeddings = embeddings.embed\_documents(documents)  

```

```python
# Print document embeddings  
for i, embedding in enumerate(document\_embeddings):  
 print(f"Embedding for document {i+1}: {embedding}")  

```

```python
# Create an embedding for a single query  
query = "This is a single query."  
query\_embedding = embeddings.embed\_query(query)  

```

```python
# Print query embedding  
print(f"Embedding for query: {query\_embedding}")  

```

## Testing with Existing Elasticsearch client connection[​](#testing-with-existing-elasticsearch-client-connection "Direct link to Testing with Existing Elasticsearch client connection")

This can be used with any Elasticsearch deployment

```python
# Create Elasticsearch connection  
es\_connection = Elasticsearch(  
 hosts=["https://es\_cluster\_url:port"], basic\_auth=("user", "password")  
)  

```

```python
# Instantiate ElasticsearchEmbeddings using es\_connection  
embeddings = ElasticsearchEmbeddings.from\_es\_connection(  
 model\_id,  
 es\_connection,  
)  

```

```python
# Create embeddings for multiple documents  
documents = [  
 "This is an example document.",  
 "Another example document to generate embeddings for.",  
]  
document\_embeddings = embeddings.embed\_documents(documents)  

```

```python
# Print document embeddings  
for i, embedding in enumerate(document\_embeddings):  
 print(f"Embedding for document {i+1}: {embedding}")  

```

```python
# Create an embedding for a single query  
query = "This is a single query."  
query\_embedding = embeddings.embed\_query(query)  

```

```python
# Print query embedding  
print(f"Embedding for query: {query\_embedding}")  

```

- [Testing with `from_credentials`](#testing-with-from_credentials)
- [Testing with Existing Elasticsearch client connection](#testing-with-existing-elasticsearch-client-connection)
