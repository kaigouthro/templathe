# Tair

[Tair](https://www.alibabacloud.com/help/en/tair/latest/what-is-tair) is a cloud native in-memory database service developed by `Alibaba Cloud`.
It provides rich data models and enterprise-grade capabilities to support your real-time online scenarios while maintaining full compatibility with open-source `Redis`. `Tair` also introduces persistent memory-optimized instances that are based on the new non-volatile memory (NVM) storage medium.

This notebook shows how to use functionality related to the `Tair` vector database.

To run, you should have a `Tair` instance up and running.

```python
from langchain.embeddings.fake import FakeEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Tair  

```

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = FakeEmbeddings(size=128)  

```

Connect to Tair using the `TAIR_URL` environment variable

```text
export TAIR\_URL="redis://{username}:{password}@{tair\_address}:{tair\_port}"  

```

or the keyword argument `tair_url`.

Then store documents and embeddings into Tair.

```python
tair\_url = "redis://localhost:6379"  
  
# drop first if index already exists  
Tair.drop\_index(tair\_url=tair\_url)  
  
vector\_store = Tair.from\_documents(docs, embeddings, tair\_url=tair\_url)  

```

Query similar documents.

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs = vector\_store.similarity\_search(query)  
docs[0]  

```

Tair Hybrid Search Index build

```python
# drop first if index already exists  
Tair.drop\_index(tair\_url=tair\_url)  
  
vector\_store = Tair.from\_documents(docs, embeddings, tair\_url=tair\_url, index\_params={"lexical\_algorithm":"bm25"})  

```

Tair Hybrid Search

```python
query = "What did the president say about Ketanji Brown Jackson"  
# hybrid\_ratio: 0.5 hybrid search, 0.9999 vector search, 0.0001 text search  
kwargs = {"TEXT" : query, "hybrid\_ratio" : 0.5}  
docs = vector\_store.similarity\_search(query, \*\*kwargs)  
docs[0]  

```
