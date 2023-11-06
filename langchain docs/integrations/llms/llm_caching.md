# LLM Caching integrations

This notebook covers how to cache results of individual LLM calls using different caches.

```python
from langchain.globals import set\_llm\_cache  
from langchain.llms import OpenAI  
  
# To make the caching really obvious, lets use a slower model.  
llm = OpenAI(model\_name="text-davinci-002", n=2, best\_of=2)  

```

## `In Memory` Cache[​](#in-memory-cache "Direct link to in-memory-cache")

```python
from langchain.cache import InMemoryCache  
  
set\_llm\_cache(InMemoryCache())  

```

```python
# The first time, it is not yet in cache, so it should take longer  
llm("Tell me a joke")  

```

```text
 CPU times: user 52.2 ms, sys: 15.2 ms, total: 67.4 ms  
 Wall time: 1.19 s  
  
  
  
  
  
 "\n\nWhy couldn't the bicycle stand up by itself? Because it was...two tired!"  

```

```python
# The second time it is, so it goes faster  
llm("Tell me a joke")  

```

```text
 CPU times: user 191 µs, sys: 11 µs, total: 202 µs  
 Wall time: 205 µs  
  
  
  
  
  
 "\n\nWhy couldn't the bicycle stand up by itself? Because it was...two tired!"  

```

## `SQLite` Cache[​](#sqlite-cache "Direct link to sqlite-cache")

```bash
rm .langchain.db  

```

```python
# We can do the same thing with a SQLite cache  
from langchain.cache import SQLiteCache  
  
set\_llm\_cache(SQLiteCache(database\_path=".langchain.db"))  

```

```python
# The first time, it is not yet in cache, so it should take longer  
llm("Tell me a joke")  

```

```text
 CPU times: user 33.2 ms, sys: 18.1 ms, total: 51.2 ms  
 Wall time: 667 ms  
  
  
  
  
  
 '\n\nWhy did the chicken cross the road?\n\nTo get to the other side.'  

```

```python
# The second time it is, so it goes faster  
llm("Tell me a joke")  

```

```text
 CPU times: user 4.86 ms, sys: 1.97 ms, total: 6.83 ms  
 Wall time: 5.79 ms  
  
  
  
  
  
 '\n\nWhy did the chicken cross the road?\n\nTo get to the other side.'  

```

## `Upstash Redis` Cache[​](#upstash-redis-cache "Direct link to upstash-redis-cache")

### Standard Cache[​](#standard-cache "Direct link to Standard Cache")

Use [Upstash Redis](https://upstash.com) to cache prompts and responses with a serverless HTTP API.

```python
from upstash\_redis import Redis  
from langchain.cache import UpstashRedisCache  
  
URL = "<UPSTASH\_REDIS\_REST\_URL>"  
TOKEN = "<UPSTASH\_REDIS\_REST\_TOKEN>"  
  
langchain.llm\_cache = UpstashRedisCache(redis\_=Redis(url=URL, token=TOKEN))  

```

```python
# The first time, it is not yet in cache, so it should take longer  
llm("Tell me a joke")  

```

```text
 CPU times: user 7.56 ms, sys: 2.98 ms, total: 10.5 ms  
 Wall time: 1.14 s  
  
  
  
  
  
 '\n\nWhy did the chicken cross the road?\n\nTo get to the other side!'  

```

```python
# The first time, it is not yet in cache, so it should take longer  
llm("Tell me a joke")  

```

```text
 CPU times: user 2.78 ms, sys: 1.95 ms, total: 4.73 ms  
 Wall time: 82.9 ms  
  
  
  
  
  
 '\n\nTwo guys stole a calendar. They got six months each.'  

```

## `Redis` Cache[​](#redis-cache "Direct link to redis-cache")

### Standard Cache[​](#standard-cache-1 "Direct link to Standard Cache")

Use [Redis](/docs/ecosystem/integrations/redis.html) to cache prompts and responses.

```python
# We can do the same thing with a Redis cache  
# (make sure your local Redis instance is running first before running this example)  
from redis import Redis  
from langchain.cache import RedisCache  
  
set\_llm\_cache(RedisCache(redis\_=Redis()))  

```

```python
# The first time, it is not yet in cache, so it should take longer  
llm("Tell me a joke")  

```

```text
 CPU times: user 6.88 ms, sys: 8.75 ms, total: 15.6 ms  
 Wall time: 1.04 s  
  
  
  
  
  
 '\n\nWhy did the chicken cross the road?\n\nTo get to the other side!'  

```

```python
# The second time it is, so it goes faster  
llm("Tell me a joke")  

```

```text
 CPU times: user 1.59 ms, sys: 610 µs, total: 2.2 ms  
 Wall time: 5.58 ms  
  
  
  
  
  
 '\n\nWhy did the chicken cross the road?\n\nTo get to the other side!'  

```

### Semantic Cache[​](#semantic-cache "Direct link to Semantic Cache")

Use [Redis](/docs/ecosystem/integrations/redis.html) to cache prompts and responses and evaluate hits based on semantic similarity.

```python
from langchain.embeddings import OpenAIEmbeddings  
from langchain.cache import RedisSemanticCache  
  
  
set\_llm\_cache(  
 RedisSemanticCache(  
 redis\_url="redis://localhost:6379", embedding=OpenAIEmbeddings()  
 )  
)  

```

```python
# The first time, it is not yet in cache, so it should take longer  
llm("Tell me a joke")  

```

```text
 CPU times: user 351 ms, sys: 156 ms, total: 507 ms  
 Wall time: 3.37 s  
  
  
  
  
  
 "\n\nWhy don't scientists trust atoms?\nBecause they make up everything."  

```

```python
# The second time, while not a direct hit, the question is semantically similar to the original question,  
# so it uses the cached result!  
llm("Tell me one joke")  

```

```text
 CPU times: user 6.25 ms, sys: 2.72 ms, total: 8.97 ms  
 Wall time: 262 ms  
  
  
  
  
  
 "\n\nWhy don't scientists trust atoms?\nBecause they make up everything."  

```

## `GPTCache`[​](#gptcache "Direct link to gptcache")

We can use [GPTCache](https://github.com/zilliztech/GPTCache) for exact match caching OR to cache results based on semantic similarity

Let's first start with an example of exact match

```python
from gptcache import Cache  
from gptcache.manager.factory import manager\_factory  
from gptcache.processor.pre import get\_prompt  
from langchain.cache import GPTCache  
import hashlib  
  
  
def get\_hashed\_name(name):  
 return hashlib.sha256(name.encode()).hexdigest()  
  
  
def init\_gptcache(cache\_obj: Cache, llm: str):  
 hashed\_llm = get\_hashed\_name(llm)  
 cache\_obj.init(  
 pre\_embedding\_func=get\_prompt,  
 data\_manager=manager\_factory(manager="map", data\_dir=f"map\_cache\_{hashed\_llm}"),  
 )  
  
  
set\_llm\_cache(GPTCache(init\_gptcache))  

```

```python
# The first time, it is not yet in cache, so it should take longer  
llm("Tell me a joke")  

```

```text
 CPU times: user 21.5 ms, sys: 21.3 ms, total: 42.8 ms  
 Wall time: 6.2 s  
  
  
  
  
  
 '\n\nWhy did the chicken cross the road?\n\nTo get to the other side!'  

```

```python
# The second time it is, so it goes faster  
llm("Tell me a joke")  

```

```text
 CPU times: user 571 µs, sys: 43 µs, total: 614 µs  
 Wall time: 635 µs  
  
  
  
  
  
 '\n\nWhy did the chicken cross the road?\n\nTo get to the other side!'  

```

Let's now show an example of similarity caching

```python
from gptcache import Cache  
from gptcache.adapter.api import init\_similar\_cache  
from langchain.cache import GPTCache  
import hashlib  
  
  
def get\_hashed\_name(name):  
 return hashlib.sha256(name.encode()).hexdigest()  
  
  
def init\_gptcache(cache\_obj: Cache, llm: str):  
 hashed\_llm = get\_hashed\_name(llm)  
 init\_similar\_cache(cache\_obj=cache\_obj, data\_dir=f"similar\_cache\_{hashed\_llm}")  
  
  
set\_llm\_cache(GPTCache(init\_gptcache))  

```

```python
# The first time, it is not yet in cache, so it should take longer  
llm("Tell me a joke")  

```

```text
 CPU times: user 1.42 s, sys: 279 ms, total: 1.7 s  
 Wall time: 8.44 s  
  
  
  
  
  
 '\n\nWhy did the chicken cross the road?\n\nTo get to the other side.'  

```

```python
# This is an exact match, so it finds it in the cache  
llm("Tell me a joke")  

```

```text
 CPU times: user 866 ms, sys: 20 ms, total: 886 ms  
 Wall time: 226 ms  
  
  
  
  
  
 '\n\nWhy did the chicken cross the road?\n\nTo get to the other side.'  

```

```python
# This is not an exact match, but semantically within distance so it hits!  
llm("Tell me joke")  

```

```text
 CPU times: user 853 ms, sys: 14.8 ms, total: 868 ms  
 Wall time: 224 ms  
  
  
  
  
  
 '\n\nWhy did the chicken cross the road?\n\nTo get to the other side.'  

```

## `Momento` Cache[​](#momento-cache "Direct link to momento-cache")

Use [Momento](/docs/ecosystem/integrations/momento.html) to cache prompts and responses.

Requires momento to use, uncomment below to install:

```python
# !pip install momento  

```

You'll need to get a Momento auth token to use this class. This can either be passed in to a momento.CacheClient if you'd like to instantiate that directly, as a named parameter `auth_token` to `MomentoChatMessageHistory.from_client_params`, or can just be set as an environment variable `MOMENTO_AUTH_TOKEN`.

```python
from datetime import timedelta  
  
from langchain.cache import MomentoCache  
  
  
cache\_name = "langchain"  
ttl = timedelta(days=1)  
set\_llm\_cache(MomentoCache.from\_client\_params(cache\_name, ttl))  

```

```python
# The first time, it is not yet in cache, so it should take longer  
llm("Tell me a joke")  

```

```text
 CPU times: user 40.7 ms, sys: 16.5 ms, total: 57.2 ms  
 Wall time: 1.73 s  
  
  
  
  
  
 '\n\nWhy did the chicken cross the road?\n\nTo get to the other side!'  

```

```python
# The second time it is, so it goes faster  
# When run in the same region as the cache, latencies are single digit ms  
llm("Tell me a joke")  

```

```text
 CPU times: user 3.16 ms, sys: 2.98 ms, total: 6.14 ms  
 Wall time: 57.9 ms  
  
  
  
  
  
 '\n\nWhy did the chicken cross the road?\n\nTo get to the other side!'  

```

## `SQLAlchemy` Cache[​](#sqlalchemy-cache "Direct link to sqlalchemy-cache")

You can use `SQLAlchemyCache` to cache with any SQL database supported by `SQLAlchemy`.

```python
# from langchain.cache import SQLAlchemyCache  
# from sqlalchemy import create\_engine  
  
# engine = create\_engine("postgresql://postgres:postgres@localhost:5432/postgres")  
# set\_llm\_cache(SQLAlchemyCache(engine))  

```

### Custom SQLAlchemy Schemas[​](#custom-sqlalchemy-schemas "Direct link to Custom SQLAlchemy Schemas")

```python
# You can define your own declarative SQLAlchemyCache child class to customize the schema used for caching. For example, to support high-speed fulltext prompt indexing with Postgres, use:  
  
from sqlalchemy import Column, Integer, String, Computed, Index, Sequence  
from sqlalchemy import create\_engine  
from sqlalchemy.ext.declarative import declarative\_base  
from sqlalchemy\_utils import TSVectorType  
from langchain.cache import SQLAlchemyCache  
  
Base = declarative\_base()  
  
  
class FulltextLLMCache(Base): # type: ignore  
 """Postgres table for fulltext-indexed LLM Cache"""  
  
 \_\_tablename\_\_ = "llm\_cache\_fulltext"  
 id = Column(Integer, Sequence("cache\_id"), primary\_key=True)  
 prompt = Column(String, nullable=False)  
 llm = Column(String, nullable=False)  
 idx = Column(Integer)  
 response = Column(String)  
 prompt\_tsv = Column(  
 TSVectorType(),  
 Computed("to\_tsvector('english', llm || ' ' || prompt)", persisted=True),  
 )  
 \_\_table\_args\_\_ = (  
 Index("idx\_fulltext\_prompt\_tsv", prompt\_tsv, postgresql\_using="gin"),  
 )  
  
  
engine = create\_engine("postgresql://postgres:postgres@localhost:5432/postgres")  
set\_llm\_cache(SQLAlchemyCache(engine, FulltextLLMCache))  

```

## `Cassandra` caches[​](#cassandra-caches "Direct link to cassandra-caches")

You can use Cassandra / Astra DB for caching LLM responses, choosing from the exact-match `CassandraCache` or the (vector-similarity-based) `CassandraSemanticCache`.

Let's see both in action in the following cells.

#### Connect to the DB[​](#connect-to-the-db "Direct link to Connect to the DB")

First you need to establish a `Session` to the DB and to specify a *keyspace* for the cache table(s). The following gets you started with an Astra DB instance (see e.g. [here](https://cassio.org/start_here/#vector-database) for more backends and connection options).

```python
import getpass  
  
keyspace = input("\nKeyspace name? ")  
ASTRA\_DB\_APPLICATION\_TOKEN = getpass.getpass('\nAstra DB Token ("AstraCS:...") ')  
ASTRA\_DB\_SECURE\_BUNDLE\_PATH = input("Full path to your Secure Connect Bundle? ")  

```

```text
   
 Keyspace name? my\_keyspace  
   
 Astra DB Token ("AstraCS:...") ········  
 Full path to your Secure Connect Bundle? /path/to/secure-connect-databasename.zip  

```

```python
from cassandra.cluster import Cluster  
from cassandra.auth import PlainTextAuthProvider  
  
cluster = Cluster(  
 cloud={  
 "secure\_connect\_bundle": ASTRA\_DB\_SECURE\_BUNDLE\_PATH,  
 },  
 auth\_provider=PlainTextAuthProvider("token", ASTRA\_DB\_APPLICATION\_TOKEN),  
)  
session = cluster.connect()  

```

### Exact cache[​](#exact-cache "Direct link to Exact cache")

This will avoid invoking the LLM when the supplied prompt is *exactly* the same as one encountered already:

```python
from langchain.globals import set\_llm\_cache  
from langchain.cache import CassandraCache  
  
set\_llm\_cache(CassandraCache(session=session, keyspace=keyspace))  

```

```python
print(llm("Why is the Moon always showing the same side?"))  

```

```text
   
   
 The Moon always shows the same side because it is tidally locked to Earth.  
 CPU times: user 41.7 ms, sys: 153 µs, total: 41.8 ms  
 Wall time: 1.96 s  

```

```python
print(llm("Why is the Moon always showing the same side?"))  

```

```text
   
   
 The Moon always shows the same side because it is tidally locked to Earth.  
 CPU times: user 4.09 ms, sys: 0 ns, total: 4.09 ms  
 Wall time: 119 ms  

```

### Semantic cache[​](#semantic-cache-1 "Direct link to Semantic cache")

This cache will do a semantic similarity search and return a hit if it finds a cached entry that is similar enough, For this, you need to provide an `Embeddings` instance of your choice.

```python
from langchain.embeddings import OpenAIEmbeddings  
  
embedding=OpenAIEmbeddings()  

```

```python
from langchain.cache import CassandraSemanticCache  
  
set\_llm\_cache(  
 CassandraSemanticCache(  
 session=session, keyspace=keyspace, embedding=embedding, table\_name="cass\_sem\_cache"  
 )  
)  

```

```python
print(llm("Why is the Moon always showing the same side?"))  

```

```text
   
   
 The Moon always shows the same side because it is tidally locked with Earth. This means that the same side of the Moon always faces Earth.  
 CPU times: user 21.3 ms, sys: 177 µs, total: 21.4 ms  
 Wall time: 3.09 s  

```

```python
print(llm("How come we always see one face of the moon?"))  

```

```text
   
   
 The Moon always shows the same side because it is tidally locked with Earth. This means that the same side of the Moon always faces Earth.  
 CPU times: user 10.9 ms, sys: 17 µs, total: 10.9 ms  
 Wall time: 461 ms  

```

## Optional Caching[​](#optional-caching "Direct link to Optional Caching")

You can also turn off caching for specific LLMs should you choose. In the example below, even though global caching is enabled, we turn it off for a specific LLM

```python
llm = OpenAI(model\_name="text-davinci-002", n=2, best\_of=2, cache=False)  

```

```python
llm("Tell me a joke")  

```

```text
 CPU times: user 5.8 ms, sys: 2.71 ms, total: 8.51 ms  
 Wall time: 745 ms  
  
  
  
  
  
 '\n\nWhy did the chicken cross the road?\n\nTo get to the other side!'  

```

```python
llm("Tell me a joke")  

```

```text
 CPU times: user 4.91 ms, sys: 2.64 ms, total: 7.55 ms  
 Wall time: 623 ms  
  
  
  
  
  
 '\n\nTwo guys stole a calendar. They got six months each.'  

```

## Optional Caching in Chains[​](#optional-caching-in-chains "Direct link to Optional Caching in Chains")

You can also turn off caching for particular nodes in chains. Note that because of certain interfaces, its often easier to construct the chain first, and then edit the LLM afterwards.

As an example, we will load a summarizer map-reduce chain. We will cache results for the map-step, but then not freeze it for the combine step.

```python
llm = OpenAI(model\_name="text-davinci-002")  
no\_cache\_llm = OpenAI(model\_name="text-davinci-002", cache=False)  

```

```python
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.chains.mapreduce import MapReduceChain  
  
text\_splitter = CharacterTextSplitter()  

```

```python
with open("../../modules/state\_of\_the\_union.txt") as f:  
 state\_of\_the\_union = f.read()  
texts = text\_splitter.split\_text(state\_of\_the\_union)  

```

```python
from langchain.docstore.document import Document  
  
docs = [Document(page\_content=t) for t in texts[:3]]  
from langchain.chains.summarize import load\_summarize\_chain  

```

```python
chain = load\_summarize\_chain(llm, chain\_type="map\_reduce", reduce\_llm=no\_cache\_llm)  

```

```python
chain.run(docs)  

```

```text
 CPU times: user 452 ms, sys: 60.3 ms, total: 512 ms  
 Wall time: 5.09 s  
  
  
  
  
  
 '\n\nPresident Biden is discussing the American Rescue Plan and the Bipartisan Infrastructure Law, which will create jobs and help Americans. He also talks about his vision for America, which includes investing in education and infrastructure. In response to Russian aggression in Ukraine, the United States is joining with European allies to impose sanctions and isolate Russia. American forces are being mobilized to protect NATO countries in the event that Putin decides to keep moving west. The Ukrainians are bravely fighting back, but the next few weeks will be hard for them. Putin will pay a high price for his actions in the long run. Americans should not be alarmed, as the United States is taking action to protect its interests and allies.'  

```

When we run it again, we see that it runs substantially faster but the final answer is different. This is due to caching at the map steps, but not at the reduce step.

```python
chain.run(docs)  

```

```text
 CPU times: user 11.5 ms, sys: 4.33 ms, total: 15.8 ms  
 Wall time: 1.04 s  
  
  
  
  
  
 '\n\nPresident Biden is discussing the American Rescue Plan and the Bipartisan Infrastructure Law, which will create jobs and help Americans. He also talks about his vision for America, which includes investing in education and infrastructure.'  

```

```bash
rm .langchain.db sqlite.db  

```

- [`In Memory` Cache](#in-memory-cache)

- [`SQLite` Cache](#sqlite-cache)

- [`Upstash Redis` Cache](#upstash-redis-cache)

  - [Standard Cache](#standard-cache)

- [`Redis` Cache](#redis-cache)

  - [Standard Cache](#standard-cache-1)
  - [Semantic Cache](#semantic-cache)

- [`GPTCache`](#gptcache)

- [`Momento` Cache](#momento-cache)

- [`SQLAlchemy` Cache](#sqlalchemy-cache)

  - [Custom SQLAlchemy Schemas](#custom-sqlalchemy-schemas)

- [`Cassandra` caches](#cassandra-caches)

  - [Exact cache](#exact-cache)
  - [Semantic cache](#semantic-cache-1)

- [Optional Caching](#optional-caching)

- [Optional Caching in Chains](#optional-caching-in-chains)

- [Standard Cache](#standard-cache)

- [Standard Cache](#standard-cache-1)

- [Semantic Cache](#semantic-cache)

- [Custom SQLAlchemy Schemas](#custom-sqlalchemy-schemas)

- [Exact cache](#exact-cache)

- [Semantic cache](#semantic-cache-1)
