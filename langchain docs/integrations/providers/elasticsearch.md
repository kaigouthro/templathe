# Elasticsearch

[Elasticsearch](https://www.elastic.co/elasticsearch/) is a distributed, RESTful search and analytics engine.
It provides a distributed, multi-tenant-capable full-text search engine with an HTTP web interface and schema-free
JSON documents.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

There are two ways to get started with Elasticsearch:

#### Install Elasticsearch on your local machine via docker[​](#install-elasticsearch-on-your-local-machine-via-docker "Direct link to Install Elasticsearch on your local machine via docker")

Example: Run a single-node Elasticsearch instance with security disabled. This is not recommended for production use.

```bash
 docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.9.0  

```

#### Deploy Elasticsearch on Elastic Cloud[​](#deploy-elasticsearch-on-elastic-cloud "Direct link to Deploy Elasticsearch on Elastic Cloud")

Elastic Cloud is a managed Elasticsearch service. Signup for a [free trial](https://cloud.elastic.co/registration?utm_source=langchain&utm_content=documentation).

### Install Client[​](#install-client "Direct link to Install Client")

```bash
pip install elasticsearch  

```

## Vector Store[​](#vector-store "Direct link to Vector Store")

The vector store is a simple wrapper around Elasticsearch. It provides a simple interface to store and retrieve vectors.

```python
from langchain.vectorstores import ElasticsearchStore  
  
from langchain.document\_loaders import TextLoader  
from langchain.text\_splitter import CharacterTextSplitter  
  
loader = TextLoader("./state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=500, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  
  
db = ElasticsearchStore.from\_documents(  
 docs, embeddings, es\_url="http://localhost:9200", index\_name="test-basic",  
)  
  
db.client.indices.refresh(index="test-basic")  
  
query = "What did the president say about Ketanji Brown Jackson"  
results = db.similarity\_search(query)  

```

- [Installation and Setup](#installation-and-setup)

  - [Install Client](#install-client)

- [Vector Store](#vector-store)

- [Install Client](#install-client)
