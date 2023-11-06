# Elasticsearch

[Elasticsearch](https://www.elastic.co/elasticsearch/) is a distributed, RESTful search and analytics engine, capable of performing both vector and lexical search. It is built on top of the Apache Lucene library.

This notebook shows how to use functionality related to the `Elasticsearch` database.

```bash
pip install elasticsearch openai tiktoken langchain  

```

## Running and connecting to Elasticsearch[​](#running-and-connecting-to-elasticsearch "Direct link to Running and connecting to Elasticsearch")

There are two main ways to setup an Elasticsearch instance for use with:

1. Elastic Cloud: Elastic Cloud is a managed Elasticsearch service. Signup for a [free trial](https://cloud.elastic.co/registration?utm_source=langchain&utm_content=documentation).

To connect to an Elasticsearch instance that does not require
login credentials (starting the docker instance with security enabled), pass the Elasticsearch URL and index name along with the
embedding object to the constructor.

2. Local Install Elasticsearch: Get started with Elasticsearch by running it locally. The easiest way is to use the official Elasticsearch Docker image. See the [Elasticsearch Docker documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html) for more information.

### Running Elasticsearch via Docker[​](#running-elasticsearch-via-docker "Direct link to Running Elasticsearch via Docker")

Example: Run a single-node Elasticsearch instance with security disabled. This is not recommended for production use.

```bash
 docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.9.0  

```

Once the Elasticsearch instance is running, you can connect to it using the Elasticsearch URL and index name along with the embedding object to the constructor.

Example:

```python
 from langchain.vectorstores.elasticsearch import ElasticsearchStore  
 from langchain.embeddings.openai import OpenAIEmbeddings  
  
 embedding = OpenAIEmbeddings()  
 elastic\_vector\_search = ElasticsearchStore(  
 es\_url="http://localhost:9200",  
 index\_name="test\_index",  
 embedding=embedding  
 )  

```

### Authentication[​](#authentication "Direct link to Authentication")

For production, we recommend you run with security enabled. To connect with login credentials, you can use the parameters `api_key` or `es_user` and `es_password`.

Example:

```python
 from langchain.vectorstores import ElasticsearchStore  
 from langchain.embeddings import OpenAIEmbeddings  
  
 embedding = OpenAIEmbeddings()  
 elastic\_vector\_search = ElasticsearchStore(  
 es\_url="http://localhost:9200",  
 index\_name="test\_index",  
 embedding=embedding,  
 es\_user="elastic",  
 es\_password="changeme"  
 )  

```

#### How to obtain a password for the default "elastic" user?[​](#how-to-obtain-a-password-for-the-default-elastic-user "Direct link to How to obtain a password for the default \"elastic\" user?")

To obtain your Elastic Cloud password for the default "elastic" user:

1. Log in to the Elastic Cloud console at <https://cloud.elastic.co>
1. Go to "Security" > "Users"
1. Locate the "elastic" user and click "Edit"
1. Click "Reset password"
1. Follow the prompts to reset the password

#### How to obtain an API key?[​](#how-to-obtain-an-api-key "Direct link to How to obtain an API key?")

To obtain an API key:

1. Log in to the Elastic Cloud console at <https://cloud.elastic.co>
1. Open Kibana and go to Stack Management > API Keys
1. Click "Create API key"
1. Enter a name for the API key and click "Create"
1. Copy the API key and paste it into the `api_key` parameter

### Elastic Cloud[​](#elastic-cloud "Direct link to Elastic Cloud")

To connect to an Elasticsearch instance on Elastic Cloud, you can use either the `es_cloud_id` parameter or `es_url`.

Example:

```python
 from langchain.vectorstores.elasticsearch import ElasticsearchStore  
 from langchain.embeddings import OpenAIEmbeddings  
  
 embedding = OpenAIEmbeddings()  
 elastic\_vector\_search = ElasticsearchStore(  
 es\_cloud\_id="<cloud\_id>",  
 index\_name="test\_index",  
 embedding=embedding,  
 es\_user="elastic",  
 es\_password="changeme"  
 )  

```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

## Basic Example[​](#basic-example "Direct link to Basic Example")

This example we are going to load "state_of_the_union.txt" via the TextLoader, chunk the text into 500 word chunks, and then index each chunk into Elasticsearch.

Once the data is indexed, we perform a simple query to find the top 4 chunks that similar to the query "What did the president say about Ketanji Brown Jackson".

Elasticsearch is running locally on localhost:9200 with [docker](#running-elasticsearch-via-docker). For more details on how to connect to Elasticsearch from Elastic Cloud, see [connecting with authentication](#authentication) above.

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.vectorstores import ElasticsearchStore  

```

```python
from langchain.document\_loaders import TextLoader  
from langchain.text\_splitter import CharacterTextSplitter  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=500, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

```python
db = ElasticsearchStore.from\_documents(  
 docs, embeddings, es\_url="http://localhost:9200", index\_name="test-basic",   
)  
  
db.client.indices.refresh(index="test-basic")  
  
query = "What did the president say about Ketanji Brown Jackson"  
results = db.similarity\_search(query)  
print(results)  

```

```text
 [Document(page\_content='One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../modules/state\_of\_the\_union.txt'}), Document(page\_content='As I said last year, especially to our younger transgender Americans, I will always have your back as your President, so you can be yourself and reach your God-given potential. \n\nWhile it often appears that we never agree, that isn’t true. I signed 80 bipartisan bills into law last year. From preventing government shutdowns to protecting Asian-Americans from still-too-common hate crimes to reforming military justice.', metadata={'source': '../../modules/state\_of\_the\_union.txt'}), Document(page\_content='A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system.', metadata={'source': '../../modules/state\_of\_the\_union.txt'}), Document(page\_content='This is personal to me and Jill, to Kamala, and to so many of you. \n\nCancer is the #2 cause of death in America–second only to heart disease. \n\nLast month, I announced our plan to supercharge \nthe Cancer Moonshot that President Obama asked me to lead six years ago. \n\nOur goal is to cut the cancer death rate by at least 50% over the next 25 years, turn more cancers from death sentences into treatable diseases. \n\nMore support for patients and families.', metadata={'source': '../../modules/state\_of\_the\_union.txt'})]  

```

# Metadata

`ElasticsearchStore` supports metadata to stored along with the document. This metadata dict object is stored in a metadata object field in the Elasticsearch document. Based on the metadata value, Elasticsearch will automatically setup the mapping by infering the data type of the metadata value. For example, if the metadata value is a string, Elasticsearch will setup the mapping for the metadata object field as a string type.

```python
# Adding metadata to documents  
for i, doc in enumerate(docs):  
 doc.metadata["date"] = f"{range(2010, 2020)[i % 10]}-01-01"  
 doc.metadata["rating"] = range(1, 6)[i % 5]   
 doc.metadata["author"] = ["John Doe", "Jane Doe"][i % 2]  
  
db = ElasticsearchStore.from\_documents(  
 docs, embeddings, es\_url="http://localhost:9200", index\_name="test-metadata"  
)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs = db.similarity\_search(query)  
print(docs[0].metadata)  

```

```text
 {'source': '../../modules/state\_of\_the\_union.txt', 'date': '2016-01-01', 'rating': 2, 'author': 'John Doe'}  

```

## Filtering Metadata[​](#filtering-metadata "Direct link to Filtering Metadata")

With metadata added to the documents, you can add metadata filtering at query time.

### Example: Filter by Exact keyword[​](#example-filter-by-exact-keyword "Direct link to Example: Filter by Exact keyword")

Notice: We are using the keyword subfield thats not analyzed

```python
docs = db.similarity\_search(query, filter=[{ "term": { "metadata.author.keyword": "John Doe"}}])  
print(docs[0].metadata)  

```

```text
 {'source': '../../modules/state\_of\_the\_union.txt', 'date': '2016-01-01', 'rating': 2, 'author': 'John Doe'}  

```

### Example: Filter by Partial Match[​](#example-filter-by-partial-match "Direct link to Example: Filter by Partial Match")

This example shows how to filter by partial match. This is useful when you don't know the exact value of the metadata field. For example, if you want to filter by the metadata field `author` and you don't know the exact value of the author, you can use a partial match to filter by the author's last name. Fuzzy matching is also supported.

"Jon" matches on "John Doe" as "Jon" is a close match to "John" token.

```python
docs = db.similarity\_search(query, filter=[{ "match": { "metadata.author": { "query": "Jon", "fuzziness": "AUTO" } }}])  
print(docs[0].metadata)  

```

```text
 {'source': '../../modules/state\_of\_the\_union.txt', 'date': '2016-01-01', 'rating': 2, 'author': 'John Doe'}  

```

### Example: Filter by Date Range[​](#example-filter-by-date-range "Direct link to Example: Filter by Date Range")

```python
docs = db.similarity\_search("Any mention about Fred?", filter=[{ "range": { "metadata.date": { "gte": "2010-01-01" }}}])  
print(docs[0].metadata)  

```

```text
 {'source': '../../modules/state\_of\_the\_union.txt', 'date': '2012-01-01', 'rating': 3, 'author': 'John Doe', 'geo\_location': {'lat': 40.12, 'lon': -71.34}}  

```

### Example: Filter by Numeric Range[​](#example-filter-by-numeric-range "Direct link to Example: Filter by Numeric Range")

```python
docs = db.similarity\_search("Any mention about Fred?", filter=[{ "range": { "metadata.rating": { "gte": 2 }}}])  
print(docs[0].metadata)  

```

```text
 {'source': '../../modules/state\_of\_the\_union.txt', 'date': '2012-01-01', 'rating': 3, 'author': 'John Doe', 'geo\_location': {'lat': 40.12, 'lon': -71.34}}  

```

### Example: Filter by Geo Distance[​](#example-filter-by-geo-distance "Direct link to Example: Filter by Geo Distance")

Requires an index with a geo_point mapping to be declared for `metadata.geo_location`.

```python
docs = db.similarity\_search("Any mention about Fred?", filter=[{ "geo\_distance": { "distance": "200km", "metadata.geo\_location": { "lat": 40, "lon": -70 } } }])  
print(docs[0].metadata)  

```

Filter supports many more types of queries than above.

Read more about them in the [documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html).

# Distance Similarity Algorithm

Elasticsearch supports the following vector distance similarity algorithms:

- cosine
- euclidean
- dot_product

The cosine similarity algorithm is the default.

You can specify the similarity Algorithm needed via the similarity parameter.

**NOTE**
Depending on the retrieval strategy, the similarity algorithm cannot be changed at query time. It is needed to be set when creating the index mapping for field. If you need to change the similarity algorithm, you need to delete the index and recreate it with the correct distance_strategy.

```python
  
db = ElasticsearchStore.from\_documents(  
 docs,   
 embeddings,   
 es\_url="http://localhost:9200",   
 index\_name="test",  
 distance\_strategy="COSINE"  
 # distance\_strategy="EUCLIDEAN\_DISTANCE"  
 # distance\_strategy="DOT\_PRODUCT"  
)  
  

```

# Retrieval Strategies

Elasticsearch has big advantages over other vector only databases from its ability to support a wide range of retrieval strategies. In this notebook we will configure `ElasticsearchStore` to support some of the most common retrieval strategies.

By default, `ElasticsearchStore` uses the `ApproxRetrievalStrategy`.

## ApproxRetrievalStrategy[​](#approxretrievalstrategy "Direct link to ApproxRetrievalStrategy")

This will return the top `k` most similar vectors to the query vector. The `k` parameter is set when the `ElasticsearchStore` is initialized. The default value is `10`.

```python
db = ElasticsearchStore.from\_documents(  
 docs,   
 embeddings,   
 es\_url="http://localhost:9200",   
 index\_name="test",  
 strategy=ElasticsearchStore.ApproxRetrievalStrategy()  
)  
  
docs = db.similarity\_search(query="What did the president say about Ketanji Brown Jackson?", k=10)  

```

### Example: Approx with hybrid[​](#example-approx-with-hybrid "Direct link to Example: Approx with hybrid")

This example will show how to configure `ElasticsearchStore` to perform a hybrid retrieval, using a combination of approximate semantic search and keyword based search.

We use RRF to balance the two scores from different retrieval methods.

To enable hybrid retrieval, we need to set `hybrid=True` in `ElasticsearchStore` `ApproxRetrievalStrategy` constructor.

```python
  
db = ElasticsearchStore.from\_documents(  
 docs,   
 embeddings,   
 es\_url="http://localhost:9200",   
 index\_name="test",  
 strategy=ElasticsearchStore.ApproxRetrievalStrategy(  
 hybrid=True,  
 )  
)  

```

When `hybrid` is enabled, the query performed will be a combination of approximate semantic search and keyword based search.

It will use `rrf` (Reciprocal Rank Fusion) to balance the two scores from different retrieval methods.

**Note** RRF requires Elasticsearch 8.9.0 or above.

```json
{  
 "knn": {  
 "field": "vector",  
 "filter": [],  
 "k": 1,  
 "num\_candidates": 50,  
 "query\_vector": [1.0, ..., 0.0],  
 },  
 "query": {  
 "bool": {  
 "filter": [],  
 "must": [{"match": {"text": {"query": "foo"}}}],  
 }  
 },  
 "rank": {"rrf": {}},  
}  

```

### Example: Approx with Embedding Model in Elasticsearch[​](#example-approx-with-embedding-model-in-elasticsearch "Direct link to Example: Approx with Embedding Model in Elasticsearch")

This example will show how to configure `ElasticsearchStore` to use the embedding model deployed in Elasticsearch for approximate retrieval.

To use this, specify the model_id in `ElasticsearchStore` `ApproxRetrievalStrategy` constructor via the `query_model_id` argument.

**NOTE** This requires the model to be deployed and running in Elasticsearch ml node. See [notebook example](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/integrations/hugging-face/loading-model-from-hugging-face.ipynb) on how to deploy the model with eland.

```python
APPROX\_SELF\_DEPLOYED\_INDEX\_NAME = "test-approx-self-deployed"  
  
# Note: This does not have an embedding function specified  
# Instead, we will use the embedding model deployed in Elasticsearch  
db = ElasticsearchStore(   
 es\_cloud\_id="<your cloud id>",  
 es\_user="elastic",  
 es\_password="<your password>",   
 index\_name=APPROX\_SELF\_DEPLOYED\_INDEX\_NAME,  
 query\_field="text\_field",  
 vector\_query\_field="vector\_query\_field.predicted\_value",  
 strategy=ElasticsearchStore.ApproxRetrievalStrategy(  
 query\_model\_id="sentence-transformers\_\_all-minilm-l6-v2"  
 )  
)  
  
# Setup a Ingest Pipeline to perform the embedding  
# of the text field  
db.client.ingest.put\_pipeline(  
 id="test\_pipeline",  
 processors=[  
 {  
 "inference": {  
 "model\_id": "sentence-transformers\_\_all-minilm-l6-v2",  
 "field\_map": {"query\_field": "text\_field"},  
 "target\_field": "vector\_query\_field",  
 }  
 }  
 ],  
)  
  
# creating a new index with the pipeline,  
# not relying on langchain to create the index  
db.client.indices.create(  
 index=APPROX\_SELF\_DEPLOYED\_INDEX\_NAME,  
 mappings={  
 "properties": {  
 "text\_field": {"type": "text"},  
 "vector\_query\_field": {  
 "properties": {  
 "predicted\_value": {  
 "type": "dense\_vector",  
 "dims": 384,  
 "index": True,  
 "similarity": "l2\_norm",  
 }  
 }  
 },  
 }  
 },  
 settings={"index": {"default\_pipeline": "test\_pipeline"}},  
)  
  
db.from\_texts(["hello world"],   
 es\_cloud\_id="<cloud id>",  
 es\_user="elastic",  
 es\_password="<cloud password>",   
 index\_name=APPROX\_SELF\_DEPLOYED\_INDEX\_NAME,  
 query\_field="text\_field",  
 vector\_query\_field="vector\_query\_field.predicted\_value",  
 strategy=ElasticsearchStore.ApproxRetrievalStrategy(  
 query\_model\_id="sentence-transformers\_\_all-minilm-l6-v2"  
 ))  
  
# Perform search  
db.similarity\_search("hello world", k=10)  

```

## SparseVectorRetrievalStrategy (ELSER)[​](#sparsevectorretrievalstrategy-elser "Direct link to SparseVectorRetrievalStrategy (ELSER)")

This strategy uses Elasticsearch's sparse vector retrieval to retrieve the top-k results. We only support our own "ELSER" embedding model for now.

**NOTE** This requires the ELSER model to be deployed and running in Elasticsearch ml node.

To use this, specify `SparseVectorRetrievalStrategy` in `ElasticsearchStore` constructor.

```python
# Note that this example doesn't have an embedding function. This is because we infer the tokens at index time and at query time within Elasticsearch.   
# This requires the ELSER model to be loaded and running in Elasticsearch.  
db = ElasticsearchStore.from\_documents(  
 docs,   
 es\_cloud\_id="My\_deployment:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ2OGJhMjhmNDc1M2Y0MWVjYTk2NzI2ZWNkMmE5YzRkNyQ3NWI4ODRjNWQ2OTU0MTYzODFjOTkxNmQ1YzYxMGI1Mw==",  
 es\_user="elastic",  
 es\_password="GgUPiWKwEzgHIYdHdgPk1Lwi",  
 index\_name="test-elser",  
 strategy=ElasticsearchStore.SparseVectorRetrievalStrategy()  
)  
  
db.client.indices.refresh(index="test-elser")  
  
results = db.similarity\_search("What did the president say about Ketanji Brown Jackson", k=4)  
print(results[0])  

```

```text
 page\_content='One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.' metadata={'source': '../../modules/state\_of\_the\_union.txt'}  

```

## ExactRetrievalStrategy[​](#exactretrievalstrategy "Direct link to ExactRetrievalStrategy")

This strategy uses Elasticsearch's exact retrieval (also known as brute force) to retrieve the top-k results.

To use this, specify `ExactRetrievalStrategy` in `ElasticsearchStore` constructor.

```python
  
db = ElasticsearchStore.from\_documents(  
 docs,   
 embeddings,   
 es\_url="http://localhost:9200",   
 index\_name="test",  
 strategy=ElasticsearchStore.ExactRetrievalStrategy()  
)  

```

## Customise the Query[​](#customise-the-query "Direct link to Customise the Query")

With `custom_query` parameter at search, you are able to adjust the query that is used to retrieve documents from Elasticsearch. This is useful if you want to want to use a more complex query, to support linear boosting of fields.

```python
# Example of a custom query thats just doing a BM25 search on the text field.  
def custom\_query(query\_body: dict, query: str):  
 """Custom query to be used in Elasticsearch.  
 Args:  
 query\_body (dict): Elasticsearch query body.  
 query (str): Query string.  
 Returns:  
 dict: Elasticsearch query body.  
 """  
 print("Query Retriever created by the retrieval strategy:")  
 print(query\_body)  
 print()  
  
 new\_query\_body = {  
 "query": {  
 "match": {  
 "text": query  
 }  
 }  
 }  
  
 print("Query thats actually used in Elasticsearch:")  
 print(new\_query\_body)  
 print()  
  
 return new\_query\_body  
  
results = db.similarity\_search("What did the president say about Ketanji Brown Jackson", k=4, custom\_query=custom\_query)  
print("Results:")  
print(results[0])  

```

```text
 Query Retriever created by the retrieval strategy:  
 {'query': {'bool': {'must': [{'text\_expansion': {'vector.tokens': {'model\_id': '.elser\_model\_1', 'model\_text': 'What did the president say about Ketanji Brown Jackson'}}}], 'filter': []}}}  
   
 Query thats actually used in Elasticsearch:  
 {'query': {'match': {'text': 'What did the president say about Ketanji Brown Jackson'}}}  
   
 Results:  
 page\_content='One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.' metadata={'source': '../../modules/state\_of\_the\_union.txt'}  

```

# FAQ

## Question: Im getting timeout errors when indexing documents into Elasticsearch. How do I fix this?[​](#question-im-getting-timeout-errors-when-indexing-documents-into-elasticsearch-how-do-i-fix-this "Direct link to Question: Im getting timeout errors when indexing documents into Elasticsearch. How do I fix this?")

One possible issue is your documents might take longer to index into Elasticsearch. ElasticsearchStore uses the Elasticsearch bulk API which has a few defaults that you can adjust to reduce the chance of timeout errors.

This is also a good idea when you're using SparseVectorRetrievalStrategy.

The defaults are:

- `chunk_size`: 500
- `max_chunk_bytes`: 100MB

To adjust these, you can pass in the `chunk_size` and `max_chunk_bytes` parameters to the ElasticsearchStore `add_texts` method.

```python
 vector\_store.add\_texts(  
 texts,  
 bulk\_kwargs={  
 "chunk\_size": 50,  
 "max\_chunk\_bytes": 200000000  
 }  
 )  

```

# Upgrading to ElasticsearchStore

If you're already using Elasticsearch in your langchain based project, you may be using the old implementations: `ElasticVectorSearch` and `ElasticKNNSearch` which are now deprecated. We've introduced a new implementation called `ElasticsearchStore` which is more flexible and easier to use. This notebook will guide you through the process of upgrading to the new implementation.

## What's new?[​](#whats-new "Direct link to What's new?")

The new implementation is now one class called `ElasticsearchStore` which can be used for approx, exact, and ELSER search retrieval, via strategies.

## Im using ElasticKNNSearch[​](#im-using-elasticknnsearch "Direct link to Im using ElasticKNNSearch")

Old implementation:

```python
  
from langchain.vectorstores.elastic\_vector\_search import ElasticKNNSearch  
  
db = ElasticKNNSearch(  
 elasticsearch\_url="http://localhost:9200",  
 index\_name="test\_index",  
 embedding=embedding  
)  
  

```

New implementation:

```python
  
from langchain.vectorstores.elasticsearch import ElasticsearchStore  
  
db = ElasticsearchStore(  
 es\_url="http://localhost:9200",  
 index\_name="test\_index",  
 embedding=embedding,  
 # if you use the model\_id  
 # strategy=ElasticsearchStore.ApproxRetrievalStrategy( query\_model\_id="test\_model" )  
 # if you use hybrid search  
 # strategy=ElasticsearchStore.ApproxRetrievalStrategy( hybrid=True )  
)  
  

```

## Im using ElasticVectorSearch[​](#im-using-elasticvectorsearch "Direct link to Im using ElasticVectorSearch")

Old implementation:

```python
  
from langchain.vectorstores.elastic\_vector\_search import ElasticVectorSearch  
  
db = ElasticVectorSearch(  
 elasticsearch\_url="http://localhost:9200",  
 index\_name="test\_index",  
 embedding=embedding  
)  
  

```

New implementation:

```python
  
from langchain.vectorstores.elasticsearch import ElasticsearchStore  
  
db = ElasticsearchStore(  
 es\_url="http://localhost:9200",  
 index\_name="test\_index",  
 embedding=embedding,  
 strategy=ElasticsearchStore.ExactRetrievalStrategy()  
)  
  

```

```python
db.client.indices.delete(index='test-metadata, test-elser, test-basic', ignore\_unavailable=True, allow\_no\_indices=True)  

```

```text
 ObjectApiResponse({'acknowledged': True})  

```

- [Running and connecting to Elasticsearch](#running-and-connecting-to-elasticsearch)

  - [Running Elasticsearch via Docker](#running-elasticsearch-via-docker)
  - [Authentication](#authentication)
  - [Elastic Cloud](#elastic-cloud)

- [Basic Example](#basic-example)

- [Filtering Metadata](#filtering-metadata)

  - [Example: Filter by Exact keyword](#example-filter-by-exact-keyword)
  - [Example: Filter by Partial Match](#example-filter-by-partial-match)
  - [Example: Filter by Date Range](#example-filter-by-date-range)
  - [Example: Filter by Numeric Range](#example-filter-by-numeric-range)
  - [Example: Filter by Geo Distance](#example-filter-by-geo-distance)

- [ApproxRetrievalStrategy](#approxretrievalstrategy)

  - [Example: Approx with hybrid](#example-approx-with-hybrid)
  - [Example: Approx with Embedding Model in Elasticsearch](#example-approx-with-embedding-model-in-elasticsearch)

- [SparseVectorRetrievalStrategy (ELSER)](#sparsevectorretrievalstrategy-elser)

- [ExactRetrievalStrategy](#exactretrievalstrategy)

- [Customise the Query](#customise-the-query)

- [Question: Im getting timeout errors when indexing documents into Elasticsearch. How do I fix this?](#question-im-getting-timeout-errors-when-indexing-documents-into-elasticsearch-how-do-i-fix-this)

- [What's new?](#whats-new)

- [Im using ElasticKNNSearch](#im-using-elasticknnsearch)

- [Im using ElasticVectorSearch](#im-using-elasticvectorsearch)

- [Running Elasticsearch via Docker](#running-elasticsearch-via-docker)

- [Authentication](#authentication)

- [Elastic Cloud](#elastic-cloud)

- [Example: Filter by Exact keyword](#example-filter-by-exact-keyword)

- [Example: Filter by Partial Match](#example-filter-by-partial-match)

- [Example: Filter by Date Range](#example-filter-by-date-range)

- [Example: Filter by Numeric Range](#example-filter-by-numeric-range)

- [Example: Filter by Geo Distance](#example-filter-by-geo-distance)

- [Example: Approx with hybrid](#example-approx-with-hybrid)

- [Example: Approx with Embedding Model in Elasticsearch](#example-approx-with-embedding-model-in-elasticsearch)
