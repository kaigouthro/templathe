# Redis

Redis vector database introduction and langchain integration guide.

## What is Redis?[​](#what-is-redis "Direct link to What is Redis?")

Most developers from a web services background are probably familiar with Redis. At it's core, Redis is an open-source key-value store that can be used as a cache, message broker, and database. Developers choose Redis because it is fast, has a large ecosystem of client libraries, and has been deployed by major enterprises for years.

On top of these traditional use cases, Redis provides additional capabilities like the Search and Query capability that allows users to create secondary index structures within Redis. This allows Redis to be a Vector Database, at the speed of a cache.

## Redis as a Vector Database[​](#redis-as-a-vector-database "Direct link to Redis as a Vector Database")

Redis uses compressed, inverted indexes for fast indexing with a low memory footprint. It also supports a number of advanced features such as:

- Indexing of multiple fields in Redis hashes and JSON
- Vector similarity search (with HNSW (ANN) or FLAT (KNN))
- Vector Range Search (e.g. find all vectors within a radius of a query vector)
- Incremental indexing without performance loss
- Document ranking (using [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf), with optional user-provided weights)
- Field weighting
- Complex boolean queries with AND, OR, and NOT operators
- Prefix matching, fuzzy matching, and exact-phrase queries
- Support for [double-metaphone phonetic matching](https://redis.io/docs/stack/search/reference/phonetic_matching/)
- Auto-complete suggestions (with fuzzy prefix suggestions)
- Stemming-based query expansion in [many languages](https://redis.io/docs/stack/search/reference/stemming/) (using [Snowball](http://snowballstem.org/))
- Support for Chinese-language tokenization and querying (using [Friso](https://github.com/lionsoul2014/friso))
- Numeric filters and ranges
- Geospatial searches using [Redis geospatial indexing](/commands/georadius)
- A powerful aggregations engine
- Supports for all utf-8 encoded text
- Retrieve full documents, selected fields, or only the document IDs
- Sorting results (for example, by creation date)

## Clients[​](#clients "Direct link to Clients")

Since redis is much more than just a vector database, there are often use cases that demand usage of a Redis client besides just the langchain integration. You can use any standard Redis client library to run Search and Query commands, but it's easiest to use a library that wraps the Search and Query API. Below are a few examples, but you can find more client libraries [here](https://redis.io/resources/clients/).

| Project | Language | License | Author | Stars |
| --- | --- | --- | --- | --- |
| [jedis](https://github.com/redis/jedis) | Java | MIT | [Redis](https://redis.com) | Stars |
| [redisvl](https://github.com/RedisVentures/redisvl) | Python | MIT | [Redis](https://redis.com) | Stars |
| [redis-py](https://github.com/redis/redis-py) | Python | MIT | [Redis](https://redis.com) | Stars |
| [node-redis](https://github.com/redis/node-redis) | Node.js | MIT | [Redis](https://redis.com) | Stars |
| [nredisstack](https://github.com/redis/nredisstack) | .NET | MIT | [Redis](https://redis.com) | Stars |

![Stars](https://img.shields.io/github/stars/redis/jedis.svg?style=social&label=Star&maxAge=2592000)

![Stars](https://img.shields.io/github/stars/RedisVentures/redisvl.svg?style=social&label=Star&maxAge=2592000)

![Stars](https://img.shields.io/github/stars/redis/redis-py.svg?style=social&label=Star&maxAge=2592000)

![Stars](https://img.shields.io/github/stars/redis/node-redis.svg?style=social&label=Star&maxAge=2592000)

![Stars](https://img.shields.io/github/stars/redis/nredisstack.svg?style=social&label=Star&maxAge=2592000)

## Deployment Options[​](#deployment-options "Direct link to Deployment Options")

There are many ways to deploy Redis with RediSearch. The easiest way to get started is to use Docker, but there are are many potential options for deployment such as

- [Redis Cloud](https://redis.com/redis-enterprise-cloud/overview/)
- [Docker (Redis Stack)](https://hub.docker.com/r/redis/redis-stack)
- Cloud marketplaces: [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-e6y7ork67pjwg?sr=0-2&ref_=beagle&applicationId=AWSMPContessa), [Google Marketplace](https://console.cloud.google.com/marketplace/details/redislabs-public/redis-enterprise?pli=1), or [Azure Marketplace](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/garantiadata.redis_enterprise_1sp_public_preview?tab=Overview)
- On-premise: [Redis Enterprise Software](https://redis.com/redis-enterprise-software/overview/)
- Kubernetes: [Redis Enterprise Software on Kubernetes](https://docs.redis.com/latest/kubernetes/)

## Examples[​](#examples "Direct link to Examples")

Many examples can be found in the [Redis AI team's GitHub](https://github.com/RedisVentures/)

- [Awesome Redis AI Resources](https://github.com/RedisVentures/redis-ai-resources) - List of examples of using Redis in AI workloads
- [Azure OpenAI Embeddings Q&A](https://github.com/ruoccofabrizio/azure-open-ai-embeddings-qna) - OpenAI and Redis as a Q&A service on Azure.
- [ArXiv Paper Search](https://github.com/RedisVentures/redis-arXiv-search) - Semantic search over arXiv scholarly papers
- [Vector Search on Azure](https://learn.microsoft.com/azure/azure-cache-for-redis/cache-tutorial-vector-similarity) - Vector search on Azure using Azure Cache for Redis and Azure OpenAI

## More Resources[​](#more-resources "Direct link to More Resources")

For more information on how to use Redis as a vector database, check out the following resources:

- [RedisVL Documentation](https://redisvl.com) - Documentation for the Redis Vector Library Client
- [Redis Vector Similarity Docs](https://redis.io/docs/stack/search/reference/vectors/) - Redis official docs for Vector Search.
- [Redis-py Search Docs](https://redis.readthedocs.io/en/latest/redismodules.html#redisearch-commands) - Documentation for redis-py client library
- [Vector Similarity Search: From Basics to Production](https://mlops.community/vector-similarity-search-from-basics-to-production/) - Introductory blog post to VSS and Redis as a VectorDB.

## Install Redis Python Client[​](#install-redis-python-client "Direct link to Install Redis Python Client")

Redis-py is the officially supported client by Redis. Recently released is the RedisVL client which is purpose-built for the Vector Database use cases. Both can be installed with pip.

```bash
pip install redis redisvl openai tiktoken  

```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```python
from langchain.embeddings import OpenAIEmbeddings  
  
embeddings = OpenAIEmbeddings()  

```

## Sample Data[​](#sample-data "Direct link to Sample Data")

First we will describe some sample data so that the various attributes of the Redis vector store can be demonstrated.

```python
metadata = [  
 {  
 "user": "john",  
 "age": 18,  
 "job": "engineer",  
 "credit\_score": "high",  
 },  
 {  
 "user": "derrick",  
 "age": 45,  
 "job": "doctor",  
 "credit\_score": "low",  
 },  
 {  
 "user": "nancy",  
 "age": 94,  
 "job": "doctor",  
 "credit\_score": "high",  
 },  
 {  
 "user": "tyler",  
 "age": 100,  
 "job": "engineer",  
 "credit\_score": "high",  
 },  
 {  
 "user": "joe",  
 "age": 35,  
 "job": "dentist",  
 "credit\_score": "medium",  
 },  
]  
texts = ["foo", "foo", "foo", "bar", "bar"]  

```

## Initializing Redis[​](#initializing-redis "Direct link to Initializing Redis")

To locally deploy Redis, run:

```console
docker run -d -p 6379:6379 -p 8001:8001 redis/redis-stack:latest  

```

If things are running correctly you should see a nice Redis UI at http://localhost:8001. See the [Deployment Options](#deployment-options) section above for other ways to deploy.

The Redis VectorStore instance can be initialized in a number of ways. There are multiple class methods that can be used to initialize a Redis VectorStore instance.

- `Redis.__init__` - Initialize directly
- `Redis.from_documents` - Initialize from a list of `Langchain.docstore.Document` objects
- `Redis.from_texts` - Initialize from a list of texts (optionally with metadata)
- `Redis.from_texts_return_keys` - Initialize from a list of texts (optionally with metadata) and return the keys
- `Redis.from_existing_index` - Initialize from an existing Redis index

Below we will use the `Redis.from_texts` method.

```python
from langchain.vectorstores.redis import Redis  
  
rds = Redis.from\_texts(  
 texts,  
 embeddings,  
 metadatas=metadata,  
 redis\_url="redis://localhost:6379",  
 index\_name="users"  
)  

```

```python
rds.index\_name  

```

```text
 'users'  

```

## Inspecting the Created Index[​](#inspecting-the-created-index "Direct link to Inspecting the Created Index")

Once the `Redis` VectorStore object has been constructed, an index will have been created in Redis if it did not already exist. The index can be inspected with both the `rvl`and the `redis-cli` command line tool. If you installed `redisvl` above, you can use the `rvl` command line tool to inspect the index.

```bash
# assumes you're running Redis locally (use --host, --port, --password, --username, to change this)  
rvl index listall  

```

```text
 16:58:26 [RedisVL] INFO Indices:  
 16:58:26 [RedisVL] INFO 1. users  

```

The `Redis` VectorStore implementation will attempt to generate index schema (fields for filtering) for any metadata passed through the `from_texts`, `from_texts_return_keys`, and `from_documents` methods. This way, whatever metadata is passed will be indexed into the Redis search index allowing
for filtering on those fields.

Below we show what fields were created from the metadata we defined above

```bash
rvl index info -i users  

```

```text
   
   
 Index Information:  
 ╭──────────────┬────────────────┬───────────────┬─────────────────┬────────────╮  
 │ Index Name │ Storage Type │ Prefixes │ Index Options │ Indexing │  
 ├──────────────┼────────────────┼───────────────┼─────────────────┼────────────┤  
 │ users │ HASH │ ['doc:users'] │ [] │ 0 │  
 ╰──────────────┴────────────────┴───────────────┴─────────────────┴────────────╯  
 Index Fields:  
 ╭────────────────┬────────────────┬─────────┬────────────────┬────────────────╮  
 │ Name │ Attribute │ Type │ Field Option │ Option Value │  
 ├────────────────┼────────────────┼─────────┼────────────────┼────────────────┤  
 │ user │ user │ TEXT │ WEIGHT │ 1 │  
 │ job │ job │ TEXT │ WEIGHT │ 1 │  
 │ credit\_score │ credit\_score │ TEXT │ WEIGHT │ 1 │  
 │ content │ content │ TEXT │ WEIGHT │ 1 │  
 │ age │ age │ NUMERIC │ │ │  
 │ content\_vector │ content\_vector │ VECTOR │ │ │  
 ╰────────────────┴────────────────┴─────────┴────────────────┴────────────────╯  

```

```bash
rvl stats -i users  

```

```text
   
 Statistics:  
 ╭─────────────────────────────┬─────────────╮  
 │ Stat Key │ Value │  
 ├─────────────────────────────┼─────────────┤  
 │ num\_docs │ 5 │  
 │ num\_terms │ 15 │  
 │ max\_doc\_id │ 5 │  
 │ num\_records │ 33 │  
 │ percent\_indexed │ 1 │  
 │ hash\_indexing\_failures │ 0 │  
 │ number\_of\_uses │ 4 │  
 │ bytes\_per\_record\_avg │ 4.60606 │  
 │ doc\_table\_size\_mb │ 0.000524521 │  
 │ inverted\_sz\_mb │ 0.000144958 │  
 │ key\_table\_size\_mb │ 0.000193596 │  
 │ offset\_bits\_per\_record\_avg │ 8 │  
 │ offset\_vectors\_sz\_mb │ 2.19345e-05 │  
 │ offsets\_per\_term\_avg │ 0.69697 │  
 │ records\_per\_doc\_avg │ 6.6 │  
 │ sortable\_values\_size\_mb │ 0 │  
 │ total\_indexing\_time │ 0.32 │  
 │ total\_inverted\_index\_blocks │ 16 │  
 │ vector\_index\_sz\_mb │ 6.0126 │  
 ╰─────────────────────────────┴─────────────╯  

```

It's important to note that we have not specified that the `user`, `job`, `credit_score` and `age` in the metadata should be fields within the index, this is because the `Redis` VectorStore object automatically generate the index schema from the passed metadata. For more information on the generation of index fields, see the API documentation.

## Querying[​](#querying "Direct link to Querying")

There are multiple ways to query the `Redis` VectorStore implementation based on what use case you have:

- `similarity_search`: Find the most similar vectors to a given vector.
- `similarity_search_with_score`: Find the most similar vectors to a given vector and return the vector distance
- `similarity_search_limit_score`: Find the most similar vectors to a given vector and limit the number of results to the `score_threshold`
- `similarity_search_with_relevance_scores`: Find the most similar vectors to a given vector and return the vector similarities
- `max_marginal_relevance_search`: Find the most similar vectors to a given vector while also optimizing for diversity

```python
results = rds.similarity\_search("foo")  
print(results[0].page\_content)  

```

```text
 foo  

```

```python
# return metadata  
results = rds.similarity\_search("foo", k=3)  
meta = results[1].metadata  
print("Key of the document in Redis: ", meta.pop("id"))  
print("Metadata of the document: ", meta)  

```

```text
 Key of the document in Redis: doc:users:a70ca43b3a4e4168bae57c78753a200f  
 Metadata of the document: {'user': 'derrick', 'job': 'doctor', 'credit\_score': 'low', 'age': '45'}  

```

```python
# with scores (distances)  
results = rds.similarity\_search\_with\_score("foo", k=5)  
for result in results:  
 print(f"Content: {result[0].page\_content} --- Score: {result[1]}")  

```

```text
 Content: foo --- Score: 0.0  
 Content: foo --- Score: 0.0  
 Content: foo --- Score: 0.0  
 Content: bar --- Score: 0.1566  
 Content: bar --- Score: 0.1566  

```

```python
# limit the vector distance that can be returned  
results = rds.similarity\_search\_with\_score("foo", k=5, distance\_threshold=0.1)  
for result in results:  
 print(f"Content: {result[0].page\_content} --- Score: {result[1]}")  

```

```text
 Content: foo --- Score: 0.0  
 Content: foo --- Score: 0.0  
 Content: foo --- Score: 0.0  

```

```python
# with scores  
results = rds.similarity\_search\_with\_relevance\_scores("foo", k=5)  
for result in results:  
 print(f"Content: {result[0].page\_content} --- Similiarity: {result[1]}")  

```

```text
 Content: foo --- Similiarity: 1.0  
 Content: foo --- Similiarity: 1.0  
 Content: foo --- Similiarity: 1.0  
 Content: bar --- Similiarity: 0.8434  
 Content: bar --- Similiarity: 0.8434  

```

```python
# limit scores (similarities have to be over .9)  
results = rds.similarity\_search\_with\_relevance\_scores("foo", k=5, score\_threshold=0.9)  
for result in results:  
 print(f"Content: {result[0].page\_content} --- Similarity: {result[1]}")  

```

```text
 Content: foo --- Similarity: 1.0  
 Content: foo --- Similarity: 1.0  
 Content: foo --- Similarity: 1.0  

```

```python
# you can also add new documents as follows  
new\_document = ["baz"]  
new\_metadata = [{  
 "user": "sam",  
 "age": 50,  
 "job": "janitor",  
 "credit\_score": "high"  
}]  
# both the document and metadata must be lists  
rds.add\_texts(new\_document, new\_metadata)  

```

```text
 ['doc:users:b9c71d62a0a34241a37950b448dafd38']  

```

```python
# now query the new document  
results = rds.similarity\_search("baz", k=3)  
print(results[0].metadata)  

```

```text
 {'id': 'doc:users:b9c71d62a0a34241a37950b448dafd38', 'user': 'sam', 'job': 'janitor', 'credit\_score': 'high', 'age': '50'}  

```

```python
# use maximal marginal relevance search to diversify results  
results = rds.max\_marginal\_relevance\_search("foo")  

```

```python
# the lambda\_mult parameter controls the diversity of the results, the lower the more diverse  
results = rds.max\_marginal\_relevance\_search("foo", lambda\_mult=0.1)  

```

## Connect to an Existing Index[​](#connect-to-an-existing-index "Direct link to Connect to an Existing Index")

In order to have the same metadata indexed when using the `Redis` VectorStore. You will need to have the same `index_schema` passed in either as a path to a yaml file or as a dictionary. The following shows how to obtain the schema from an index and connect to an existing index.

```python
# write the schema to a yaml file  
rds.write\_schema("redis\_schema.yaml")  

```

The schema file for this example should look something like:

```yaml
numeric:  
- name: age  
 no\_index: false  
 sortable: false  
text:  
- name: user  
 no\_index: false  
 no\_stem: false  
 sortable: false  
 weight: 1  
 withsuffixtrie: false  
- name: job  
 no\_index: false  
 no\_stem: false  
 sortable: false  
 weight: 1  
 withsuffixtrie: false  
- name: credit\_score  
 no\_index: false  
 no\_stem: false  
 sortable: false  
 weight: 1  
 withsuffixtrie: false  
- name: content  
 no\_index: false  
 no\_stem: false  
 sortable: false  
 weight: 1  
 withsuffixtrie: false  
vector:  
- algorithm: FLAT  
 block\_size: 1000  
 datatype: FLOAT32  
 dims: 1536  
 distance\_metric: COSINE  
 initial\_cap: 20000  
 name: content\_vector  

```

**Notice**, this include **all** possible fields for the schema. You can remove any fields that you don't need.

```python
# now we can connect to our existing index as follows  
  
new\_rds = Redis.from\_existing\_index(  
 embeddings,  
 index\_name="users",  
 redis\_url="redis://localhost:6379",  
 schema="redis\_schema.yaml"  
)  
results = new\_rds.similarity\_search("foo", k=3)  
print(results[0].metadata)  

```

```text
 {'id': 'doc:users:8484c48a032d4c4cbe3cc2ed6845fabb', 'user': 'john', 'job': 'engineer', 'credit\_score': 'high', 'age': '18'}  

```

```python
# see the schemas are the same  
new\_rds.schema == rds.schema  

```

```text
 True  

```

## Custom Metadata Indexing[​](#custom-metadata-indexing "Direct link to Custom Metadata Indexing")

In some cases, you may want to control what fields the metadata maps to. For example, you may want the `credit_score` field to be a categorical field instead of a text field (which is the default behavior for all string fields). In this case, you can use the `index_schema` parameter in each of the initialization methods above to specify the schema for the index. Custom index schema can either be passed as a dictionary or as a path to a yaml file.

All arguments in the schema have defaults besides the name, so you can specify only the fields you want to change. All the names correspond to the snake/lowercase versions of the arguments you would use on the command line with `redis-cli` or in `redis-py`. For more on the arguments for each field, see the [documentation](https://redis.io/docs/interact/search-and-query/basic-constructs/field-and-type-options/)

The below example shows how to specify the schema for the `credit_score` field as a Tag (categorical) field instead of a text field.

```yaml
# index\_schema.yml  
tag:  
 - name: credit\_score  
text:  
 - name: user  
 - name: job  
numeric:  
 - name: age  

```

In Python this would look like:

```python
  
index\_schema = {  
 "tag": [{"name": "credit\_score"}],  
 "text": [{"name": "user"}, {"name": "job"}],  
 "numeric": [{"name": "age"}],  
}  
  

```

Notice that only the `name` field needs to be specified. All other fields have defaults.

```python
# create a new index with the new schema defined above  
index\_schema = {  
 "tag": [{"name": "credit\_score"}],  
 "text": [{"name": "user"}, {"name": "job"}],  
 "numeric": [{"name": "age"}],  
}  
  
rds, keys = Redis.from\_texts\_return\_keys(  
 texts,  
 embeddings,  
 metadatas=metadata,  
 redis\_url="redis://localhost:6379",  
 index\_name="users\_modified",  
 index\_schema=index\_schema, # pass in the new index schema  
)  

```

```text
 `index\_schema` does not match generated metadata schema.  
 If you meant to manually override the schema, please ignore this message.  
 index\_schema: {'tag': [{'name': 'credit\_score'}], 'text': [{'name': 'user'}, {'name': 'job'}], 'numeric': [{'name': 'age'}]}  
 generated\_schema: {'text': [{'name': 'user'}, {'name': 'job'}, {'name': 'credit\_score'}], 'numeric': [{'name': 'age'}], 'tag': []}  
   

```

The above warning is meant to notify users when they are overriding the default behavior. Ignore it if you are intentionally overriding the behavior.

## Hybrid Filtering[​](#hybrid-filtering "Direct link to Hybrid Filtering")

With the Redis Filter Expression language built into langchain, you can create arbitrarily long chains of hybrid filters
that can be used to filter your search results. The expression language is derived from the [RedisVL Expression Syntax](https://redisvl.com)
and is designed to be easy to use and understand.

The following are the available filter types:

- `RedisText`: Filter by full-text search against metadata fields. Supports exact, fuzzy, and wildcard matching.
- `RedisNum`: Filter by numeric range against metadata fields.
- `RedisTag`: Filter by exact match against string based categorical metadata fields. Multiple tags can be specified like "tag1,tag2,tag3".

The following are examples of utilizing these filters.

```python
  
from langchain.vectorstores.redis import RedisText, RedisNum, RedisTag  
  
# exact matching  
has\_high\_credit = RedisTag("credit\_score") == "high"  
does\_not\_have\_high\_credit = RedisTag("credit\_score") != "low"  
  
# fuzzy matching  
job\_starts\_with\_eng = RedisText("job") % "eng\*"  
job\_is\_engineer = RedisText("job") == "engineer"  
job\_is\_not\_engineer = RedisText("job") != "engineer"  
  
# numeric filtering  
age\_is\_18 = RedisNum("age") == 18  
age\_is\_not\_18 = RedisNum("age") != 18  
age\_is\_greater\_than\_18 = RedisNum("age") > 18  
age\_is\_less\_than\_18 = RedisNum("age") < 18  
age\_is\_greater\_than\_or\_equal\_to\_18 = RedisNum("age") >= 18  
age\_is\_less\_than\_or\_equal\_to\_18 = RedisNum("age") <= 18  
  

```

The `RedisFilter` class can be used to simplify the import of these filters as follows

```python
  
from langchain.vectorstores.redis import RedisFilter  
  
# same examples as above  
has\_high\_credit = RedisFilter.tag("credit\_score") == "high"  
does\_not\_have\_high\_credit = RedisFilter.num("age") > 8  
job\_starts\_with\_eng = RedisFilter.text("job") % "eng\*"  

```

The following are examples of using hybrid filter for search

```python
from langchain.vectorstores.redis import RedisText  
  
is\_engineer = RedisText("job") == "engineer"  
results = rds.similarity\_search("foo", k=3, filter=is\_engineer)  
  
print("Job:", results[0].metadata["job"])  
print("Engineers in the dataset:", len(results))  

```

```text
 Job: engineer  
 Engineers in the dataset: 2  

```

```python
# fuzzy match  
starts\_with\_doc = RedisText("job") % "doc\*"  
results = rds.similarity\_search("foo", k=3, filter=starts\_with\_doc)  
  
for result in results:  
 print("Job:", result.metadata["job"])  
print("Jobs in dataset that start with 'doc':", len(results))  

```

```text
 Job: doctor  
 Job: doctor  
 Jobs in dataset that start with 'doc': 2  

```

```python
from langchain.vectorstores.redis import RedisNum  
  
is\_over\_18 = RedisNum("age") > 18  
is\_under\_99 = RedisNum("age") < 99  
age\_range = is\_over\_18 & is\_under\_99  
results = rds.similarity\_search("foo", filter=age\_range)  
  
for result in results:  
 print("User:", result.metadata["user"], "is", result.metadata["age"])  

```

```text
 User: derrick is 45  
 User: nancy is 94  
 User: joe is 35  

```

```python
# make sure to use parenthesis around FilterExpressions  
# if initializing them while constructing them  
age\_range = (RedisNum("age") > 18) & (RedisNum("age") < 99)  
results = rds.similarity\_search("foo", filter=age\_range)  
  
for result in results:  
 print("User:", result.metadata["user"], "is", result.metadata["age"])  

```

```text
 User: derrick is 45  
 User: nancy is 94  
 User: joe is 35  

```

## Redis as Retriever[​](#redis-as-retriever "Direct link to Redis as Retriever")

Here we go over different options for using the vector store as a retriever.

There are three different search methods we can use to do retrieval. By default, it will use semantic similarity.

```python
query = "foo"  
results = rds.similarity\_search\_with\_score(query, k=3, return\_metadata=True)  
  
for result in results:  
 print("Content:", result[0].page\_content, " --- Score: ", result[1])  

```

```text
 Content: foo --- Score: 0.0  
 Content: foo --- Score: 0.0  
 Content: foo --- Score: 0.0  

```

```python
retriever = rds.as\_retriever(search\_type="similarity", search\_kwargs={"k": 4})  

```

```python
docs = retriever.get\_relevant\_documents(query)  
docs  

```

```text
 [Document(page\_content='foo', metadata={'id': 'doc:users\_modified:988ecca7574048e396756efc0e79aeca', 'user': 'john', 'job': 'engineer', 'credit\_score': 'high', 'age': '18'}),  
 Document(page\_content='foo', metadata={'id': 'doc:users\_modified:009b1afeb4084cc6bdef858c7a99b48e', 'user': 'derrick', 'job': 'doctor', 'credit\_score': 'low', 'age': '45'}),  
 Document(page\_content='foo', metadata={'id': 'doc:users\_modified:7087cee9be5b4eca93c30fbdd09a2731', 'user': 'nancy', 'job': 'doctor', 'credit\_score': 'high', 'age': '94'}),  
 Document(page\_content='bar', metadata={'id': 'doc:users\_modified:01ef6caac12b42c28ad870aefe574253', 'user': 'tyler', 'job': 'engineer', 'credit\_score': 'high', 'age': '100'})]  

```

There is also the `similarity_distance_threshold` retriever which allows the user to specify the vector distance

```python
retriever = rds.as\_retriever(search\_type="similarity\_distance\_threshold", search\_kwargs={"k": 4, "distance\_threshold": 0.1})  

```

```python
docs = retriever.get\_relevant\_documents(query)  
docs  

```

```text
 [Document(page\_content='foo', metadata={'id': 'doc:users\_modified:988ecca7574048e396756efc0e79aeca', 'user': 'john', 'job': 'engineer', 'credit\_score': 'high', 'age': '18'}),  
 Document(page\_content='foo', metadata={'id': 'doc:users\_modified:009b1afeb4084cc6bdef858c7a99b48e', 'user': 'derrick', 'job': 'doctor', 'credit\_score': 'low', 'age': '45'}),  
 Document(page\_content='foo', metadata={'id': 'doc:users\_modified:7087cee9be5b4eca93c30fbdd09a2731', 'user': 'nancy', 'job': 'doctor', 'credit\_score': 'high', 'age': '94'})]  

```

Lastly, the `similarity_score_threshold` allows the user to define the minimum score for similar documents

```python
retriever = rds.as\_retriever(search\_type="similarity\_score\_threshold", search\_kwargs={"score\_threshold": 0.9, "k": 10})  

```

```python
retriever.get\_relevant\_documents("foo")  

```

```text
 [Document(page\_content='foo', metadata={'id': 'doc:users\_modified:988ecca7574048e396756efc0e79aeca', 'user': 'john', 'job': 'engineer', 'credit\_score': 'high', 'age': '18'}),  
 Document(page\_content='foo', metadata={'id': 'doc:users\_modified:009b1afeb4084cc6bdef858c7a99b48e', 'user': 'derrick', 'job': 'doctor', 'credit\_score': 'low', 'age': '45'}),  
 Document(page\_content='foo', metadata={'id': 'doc:users\_modified:7087cee9be5b4eca93c30fbdd09a2731', 'user': 'nancy', 'job': 'doctor', 'credit\_score': 'high', 'age': '94'})]  

```

```python
retriever = rds.as\_retriever(search\_type="mmr", search\_kwargs={"fetch\_k": 20, "k": 4, "lambda\_mult": 0.1})  

```

```python
retriever.get\_relevant\_documents("foo")  

```

```text
 [Document(page\_content='foo', metadata={'id': 'doc:users:8f6b673b390647809d510112cde01a27', 'user': 'john', 'job': 'engineer', 'credit\_score': 'high', 'age': '18'}),  
 Document(page\_content='bar', metadata={'id': 'doc:users:93521560735d42328b48c9c6f6418d6a', 'user': 'tyler', 'job': 'engineer', 'credit\_score': 'high', 'age': '100'}),  
 Document(page\_content='foo', metadata={'id': 'doc:users:125ecd39d07845eabf1a699d44134a5b', 'user': 'nancy', 'job': 'doctor', 'credit\_score': 'high', 'age': '94'}),  
 Document(page\_content='foo', metadata={'id': 'doc:users:d6200ab3764c466082fde3eaab972a2a', 'user': 'derrick', 'job': 'doctor', 'credit\_score': 'low', 'age': '45'})]  

```

# Delete keys

To delete your entries you have to address them by their keys.

```python
Redis.delete(keys, redis\_url="redis://localhost:6379")  

```

```text
 True  

```

```python
# delete the indices too  
Redis.drop\_index(index\_name="users", delete\_documents=True, redis\_url="redis://localhost:6379")  
Redis.drop\_index(index\_name="users\_modified", delete\_documents=True, redis\_url="redis://localhost:6379")  

```

```text
 True  

```

### Redis connection Url examples[​](#redis-connection-url-examples "Direct link to Redis connection Url examples")

Valid Redis Url scheme are:

1. `redis://` - Connection to Redis standalone, unencrypted
1. `rediss://` - Connection to Redis standalone, with TLS encryption
1. `redis+sentinel://` - Connection to Redis server via Redis Sentinel, unencrypted
1. `rediss+sentinel://` - Connection to Redis server via Redis Sentinel, booth connections with TLS encryption

More information about additional connection parameter can be found in the redis-py documentation at <https://redis-py.readthedocs.io/en/stable/connections.html>

```python
# connection to redis standalone at localhost, db 0, no password  
redis\_url = "redis://localhost:6379"  
# connection to host "redis" port 7379 with db 2 and password "secret" (old style authentication scheme without username / pre 6.x)  
redis\_url = "redis://:secret@redis:7379/2"  
# connection to host redis on default port with user "joe", pass "secret" using redis version 6+ ACLs  
redis\_url = "redis://joe:secret@redis/0"  
  
# connection to sentinel at localhost with default group mymaster and db 0, no password  
redis\_url = "redis+sentinel://localhost:26379"  
# connection to sentinel at host redis with default port 26379 and user "joe" with password "secret" with default group mymaster and db 0  
redis\_url = "redis+sentinel://joe:secret@redis"  
# connection to sentinel, no auth with sentinel monitoring group "zone-1" and database 2  
redis\_url = "redis+sentinel://redis:26379/zone-1/2"  
  
# connection to redis standalone at localhost, db 0, no password but with TLS support  
redis\_url = "rediss://localhost:6379"  
# connection to redis sentinel at localhost and default port, db 0, no password  
# but with TLS support for booth Sentinel and Redis server  
redis\_url = "rediss+sentinel://localhost"  

```

- [What is Redis?](#what-is-redis)

- [Redis as a Vector Database](#redis-as-a-vector-database)

- [Clients](#clients)

- [Deployment Options](#deployment-options)

- [Examples](#examples)

- [More Resources](#more-resources)

- [Install Redis Python Client](#install-redis-python-client)

- [Sample Data](#sample-data)

- [Initializing Redis](#initializing-redis)

- [Inspecting the Created Index](#inspecting-the-created-index)

- [Querying](#querying)

- [Connect to an Existing Index](#connect-to-an-existing-index)

- [Custom Metadata Indexing](#custom-metadata-indexing)

- [Hybrid Filtering](#hybrid-filtering)

- [Redis as Retriever](#redis-as-retriever)

  - [Redis connection Url examples](#redis-connection-url-examples)

- [Redis connection Url examples](#redis-connection-url-examples)
