# ClickHouse

[ClickHouse](https://clickhouse.com/) is the fastest and most resource efficient open-source database for real-time apps and analytics with full SQL support and a wide range of functions to assist users in writing analytical queries. Lately added data structures and distance search functions (like `L2Distance`) as well as [approximate nearest neighbor search indexes](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/annindexes) enable ClickHouse to be used as a high performance and scalable vector database to store and search vectors with SQL.

This notebook shows how to use functionality related to the `ClickHouse` vector search.

## Setting up envrionments[​](#setting-up-envrionments "Direct link to Setting up envrionments")

Setting up local clickhouse server with docker (optional)

```bash
docker run -d -p 8123:8123 -p9000:9000 --name langchain-clickhouse-server --ulimit nofile=262144:262144 clickhouse/clickhouse-server:23.4.2.11  

```

Setup up clickhouse client driver

```bash
pip install clickhouse-connect  

```

We want to use OpenAIEmbeddings so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
if not os.environ["OPENAI\_API\_KEY"]:  
 os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Clickhouse, ClickhouseSettings  

```

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

```python
for d in docs:  
 d.metadata = {"some": "metadata"}  
settings = ClickhouseSettings(table="clickhouse\_vector\_search\_example")  
docsearch = Clickhouse.from\_documents(docs, embeddings, config=settings)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs = docsearch.similarity\_search(query)  

```

```text
 Inserting data...: 100%|██████████| 42/42 [00:00<00:00, 2801.49it/s]  

```

```python
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

## Get connection info and data schema[​](#get-connection-info-and-data-schema "Direct link to Get connection info and data schema")

```python
print(str(docsearch))  

```

```text
 default.clickhouse\_vector\_search\_example @ localhost:8123  
   
 username: None  
   
 Table Schema:  
 ---------------------------------------------------  
 |id |Nullable(String) |  
 |document |Nullable(String) |  
 |embedding |Array(Float32) |  
 |metadata |Object('json') |  
 |uuid |UUID |  
 ---------------------------------------------------  
   

```

### Clickhouse table schema[​](#clickhouse-table-schema "Direct link to Clickhouse table schema")

Clickhouse table will be automatically created if not exist by default. Advanced users could pre-create the table with optimized settings. For distributed Clickhouse cluster with sharding, table engine should be configured as `Distributed`.

```python
print(f"Clickhouse Table DDL:\n\n{docsearch.schema}")  

```

```text
 Clickhouse Table DDL:  
   
 CREATE TABLE IF NOT EXISTS default.clickhouse\_vector\_search\_example(  
 id Nullable(String),  
 document Nullable(String),  
 embedding Array(Float32),  
 metadata JSON,  
 uuid UUID DEFAULT generateUUIDv4(),  
 CONSTRAINT cons\_vec\_len CHECK length(embedding) = 1536,  
 INDEX vec\_idx embedding TYPE annoy(100,'L2Distance') GRANULARITY 1000  
 ) ENGINE = MergeTree ORDER BY uuid SETTINGS index\_granularity = 8192  

```

## Filtering[​](#filtering "Direct link to Filtering")

You can have direct access to ClickHouse SQL where statement. You can write `WHERE` clause following standard SQL.

**NOTE**: Please be aware of SQL injection, this interface must not be directly called by end-user.

If you custimized your `column_map` under your setting, you search with filter like this:

```python
from langchain.vectorstores import Clickhouse, ClickhouseSettings  
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  
  
for i, d in enumerate(docs):  
 d.metadata = {"doc\_id": i}  
  
docsearch = Clickhouse.from\_documents(docs, embeddings)  

```

```text
 Inserting data...: 100%|██████████| 42/42 [00:00<00:00, 6939.56it/s]  

```

```python
meta = docsearch.metadata\_column  
output = docsearch.similarity\_search\_with\_relevance\_scores(  
 "What did the president say about Ketanji Brown Jackson?",  
 k=4,  
 where\_str=f"{meta}.doc\_id<10",  
)  
for d, dist in output:  
 print(dist, d.metadata, d.page\_content[:20] + "...")  

```

```text
 0.6779101415357189 {'doc\_id': 0} Madam Speaker, Madam...  
 0.6997970363474885 {'doc\_id': 8} And so many families...  
 0.7044504914336727 {'doc\_id': 1} Groups of citizens b...  
 0.7053558702165094 {'doc\_id': 6} And I’m taking robus...  

```

## Deleting your data[​](#deleting-your-data "Direct link to Deleting your data")

```python
docsearch.drop()  

```

- [Setting up envrionments](#setting-up-envrionments)

- [Get connection info and data schema](#get-connection-info-and-data-schema)

  - [Clickhouse table schema](#clickhouse-table-schema)

- [Filtering](#filtering)

- [Deleting your data](#deleting-your-data)

- [Clickhouse table schema](#clickhouse-table-schema)
