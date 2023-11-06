# Cassandra

[Apache Cassandra®](https://cassandra.apache.org) is a NoSQL, row-oriented, highly scalable and highly available database.

Newest Cassandra releases natively [support](<https://cwiki.apache.org/confluence/display/CASSANDRA/CEP-30%3A+Approximate+Nearest+Neighbor(ANN)+Vector+Search+via+Storage-Attached+Indexes>) Vector Similarity Search.

To run this notebook you need either a running Cassandra cluster equipped with Vector Search capabilities (in pre-release at the time of writing) or a DataStax Astra DB instance running in the cloud (you can get one for free at [datastax.com](https://astra.datastax.com)). Check [cassio.org](https://cassio.org/start_here/) for more information.

```bash
pip install "cassio>=0.1.0"  

```

### Please provide database connection parameters and secrets:[​](#please-provide-database-connection-parameters-and-secrets "Direct link to Please provide database connection parameters and secrets:")

```python
import os  
import getpass  
  
database\_mode = (input("\n(C)assandra or (A)stra DB? ")).upper()  
  
keyspace\_name = input("\nKeyspace name? ")  
  
if database\_mode == "A":  
 ASTRA\_DB\_APPLICATION\_TOKEN = getpass.getpass('\nAstra DB Token ("AstraCS:...") ')  
 #  
 ASTRA\_DB\_SECURE\_BUNDLE\_PATH = input("Full path to your Secure Connect Bundle? ")  
elif database\_mode == "C":  
 CASSANDRA\_CONTACT\_POINTS = input(  
 "Contact points? (comma-separated, empty for localhost) "  
 ).strip()  

```

#### depending on whether local or cloud-based Astra DB, create the corresponding database connection "Session" object[​](#depending-on-whether-local-or-cloud-based-astra-db-create-the-corresponding-database-connection-session-object "Direct link to depending on whether local or cloud-based Astra DB, create the corresponding database connection \"Session\" object")

```python
from cassandra.cluster import Cluster  
from cassandra.auth import PlainTextAuthProvider  
  
if database\_mode == "C":  
 if CASSANDRA\_CONTACT\_POINTS:  
 cluster = Cluster(  
 [cp.strip() for cp in CASSANDRA\_CONTACT\_POINTS.split(",") if cp.strip()]  
 )  
 else:  
 cluster = Cluster()  
 session = cluster.connect()  
elif database\_mode == "A":  
 ASTRA\_DB\_CLIENT\_ID = "token"  
 cluster = Cluster(  
 cloud={  
 "secure\_connect\_bundle": ASTRA\_DB\_SECURE\_BUNDLE\_PATH,  
 },  
 auth\_provider=PlainTextAuthProvider(  
 ASTRA\_DB\_CLIENT\_ID,  
 ASTRA\_DB\_APPLICATION\_TOKEN,  
 ),  
 )  
 session = cluster.connect()  
else:  
 raise NotImplementedError  

```

### Please provide OpenAI access key[​](#please-provide-openai-access-key "Direct link to Please provide OpenAI access key")

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.

```python
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

### Creation and usage of the Vector Store[​](#creation-and-usage-of-the-vector-store "Direct link to Creation and usage of the Vector Store")

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Cassandra  
from langchain.document\_loaders import TextLoader  

```

```python
from langchain.document\_loaders import TextLoader  
  
SOURCE\_FILE\_NAME = "../../modules/state\_of\_the\_union.txt"  
  
loader = TextLoader(SOURCE\_FILE\_NAME)  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embedding\_function = OpenAIEmbeddings()  

```

```python
table\_name = "my\_vector\_db\_table"  
  
docsearch = Cassandra.from\_documents(  
 documents=docs,  
 embedding=embedding\_function,  
 session=session,  
 keyspace=keyspace\_name,  
 table\_name=table\_name,  
)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs = docsearch.similarity\_search(query)  

```

```python
## if you already have an index, you can load it and use it like this:  
  
# docsearch\_preexisting = Cassandra(  
# embedding=embedding\_function,  
# session=session,  
# keyspace=keyspace\_name,  
# table\_name=table\_name,  
# )  
  
# docs = docsearch\_preexisting.similarity\_search(query, k=2)  

```

```python
print(docs[0].page\_content)  

```

### Maximal Marginal Relevance Searches[​](#maximal-marginal-relevance-searches "Direct link to Maximal Marginal Relevance Searches")

In addition to using similarity search in the retriever object, you can also use `mmr` as retriever.

```python
retriever = docsearch.as\_retriever(search\_type="mmr")  
matched\_docs = retriever.get\_relevant\_documents(query)  
for i, d in enumerate(matched\_docs):  
 print(f"\n## Document {i}\n")  
 print(d.page\_content)  

```

Or use `max_marginal_relevance_search` directly:

```python
found\_docs = docsearch.max\_marginal\_relevance\_search(query, k=2, fetch\_k=10)  
for i, doc in enumerate(found\_docs):  
 print(f"{i + 1}.", doc.page\_content, "\n")  

```

### Metadata filtering[​](#metadata-filtering "Direct link to Metadata filtering")

You can specify filtering on metadata when running searches in the vector store. By default, when inserting documents, the only metadata is the `"source"` (but you can customize the metadata at insertion time).

Since only one files was inserted, this is just a demonstration of how filters are passed:

```python
filter = {"source": SOURCE\_FILE\_NAME}  
filtered\_docs = docsearch.similarity\_search(query, filter=filter, k=5)  
print(f"{len(filtered\_docs)} documents retrieved.")  
print(f"{filtered\_docs[0].page\_content[:64]} ...")  

```

```python
filter = {"source": "nonexisting\_file.txt"}  
filtered\_docs2 = docsearch.similarity\_search(query, filter=filter)  
print(f"{len(filtered\_docs2)} documents retrieved.")  

```

Please visit the [cassIO documentation](https://cassio.org/frameworks/langchain/about/) for more on using vector stores with Langchain.

- [Please provide database connection parameters and secrets:](#please-provide-database-connection-parameters-and-secrets)
- [Please provide OpenAI access key](#please-provide-openai-access-key)
- [Creation and usage of the Vector Store](#creation-and-usage-of-the-vector-store)
- [Maximal Marginal Relevance Searches](#maximal-marginal-relevance-searches)
- [Metadata filtering](#metadata-filtering)
