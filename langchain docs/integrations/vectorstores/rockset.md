# Rockset

[Rockset](https://rockset.com/) is a real-time search and analytics database built for the cloud. Rockset uses a [Converged Index™](https://rockset.com/blog/converged-indexing-the-secret-sauce-behind-rocksets-fast-queries/) with an efficient store for vector embeddings to serve low latency, high concurrency search queries at scale. Rockset has full support for metadata filtering and handles real-time ingestion for constantly updating, streaming data.

This notebook demonstrates how to use `Rockset` as a vector store in LangChain. Before getting started, make sure you have access to a `Rockset` account and an API key available. [Start your free trial today.](https://rockset.com/create/)

## Setting Up Your Environment[​](#setting-up-your-environment "Direct link to setting-up-your-environment")

1. Leverage the `Rockset` console to create a [collection](https://rockset.com/docs/collections/) with the Write API as your source. In this walkthrough, we create a collection named `langchain_demo`.

Configure the following [ingest transformation](https://rockset.com/docs/ingest-transformation/) to mark your embeddings field and take advantage of performance and storage optimizations:

Leverage the `Rockset` console to create a [collection](https://rockset.com/docs/collections/) with the Write API as your source. In this walkthrough, we create a collection named `langchain_demo`.

Configure the following [ingest transformation](https://rockset.com/docs/ingest-transformation/) to mark your embeddings field and take advantage of performance and storage optimizations:

(We used OpenAI `text-embedding-ada-002` for this examples, where #length_of_vector_embedding = 1536)

```python
SELECT \_input.\* EXCEPT(\_meta),   
VECTOR\_ENFORCE(\_input.description\_embedding, #length\_of\_vector\_embedding, 'float') as description\_embedding   
FROM \_input  

```

2. After creating your collection, use the console to retrieve an [API key](https://rockset.com/docs/iam/#users-api-keys-and-roles). For the purpose of this notebook, we assume you are using the `Oregon(us-west-2)` region.
1. Install the [rockset-python-client](https://github.com/rockset/rockset-python-client) to enable LangChain to communicate directly with `Rockset`.

After creating your collection, use the console to retrieve an [API key](https://rockset.com/docs/iam/#users-api-keys-and-roles). For the purpose of this notebook, we assume you are using the `Oregon(us-west-2)` region.

Install the [rockset-python-client](https://github.com/rockset/rockset-python-client) to enable LangChain to communicate directly with `Rockset`.

```python
pip install rockset  

```

## LangChain Tutorial[​](#langchain-tutorial "Direct link to LangChain Tutorial")

Follow along in your own Python notebook to generate and store vector embeddings in Rockset.
Start using Rockset to search for documents similar to your search queries.

### 1. Define Key Variables[​](#1-define-key-variables "Direct link to 1. Define Key Variables")

```python
import os  
import rockset  
  
ROCKSET\_API\_KEY = os.environ.get("ROCKSET\_API\_KEY") # Verify ROCKSET\_API\_KEY environment variable  
ROCKSET\_API\_SERVER = rockset.Regions.usw2a1 # Verify Rockset region  
rockset\_client = rockset.RocksetClient(ROCKSET\_API\_SERVER, ROCKSET\_API\_KEY)  
  
COLLECTION\_NAME='langchain\_demo'  
TEXT\_KEY='description'  
EMBEDDING\_KEY='description\_embedding'  

```

### 2. Prepare Documents[​](#2-prepare-documents "Direct link to 2. Prepare Documents")

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.document\_loaders import TextLoader  
from langchain.vectorstores import Rockset  
  
loader = TextLoader('../../modules/state\_of\_the\_union.txt')  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  

```

### 3. Insert Documents[​](#3-insert-documents "Direct link to 3. Insert Documents")

```python
embeddings = OpenAIEmbeddings() # Verify OPENAI\_API\_KEY environment variable  
  
docsearch = Rockset(  
 client=rockset\_client,  
 embeddings=embeddings,  
 collection\_name=COLLECTION\_NAME,  
 text\_key=TEXT\_KEY,  
 embedding\_key=EMBEDDING\_KEY,  
)  
  
ids=docsearch.add\_texts(  
 texts=[d.page\_content for d in docs],  
 metadatas=[d.metadata for d in docs],  
)  

```

### 4. Search for Similar Documents[​](#4-search-for-similar-documents "Direct link to 4. Search for Similar Documents")

```python
query = "What did the president say about Ketanji Brown Jackson"  
output = docsearch.similarity\_search\_with\_relevance\_scores(  
 query, 4, Rockset.DistanceFunction.COSINE\_SIM  
)  
print("output length:", len(output))  
for d, dist in output:  
 print(dist, d.metadata, d.page\_content[:20] + '...')  
  
##  
# output length: 4  
# 0.764990692109871 {'source': '../../../state\_of\_the\_union.txt'} Madam Speaker, Madam...  
# 0.7485416901622112 {'source': '../../../state\_of\_the\_union.txt'} And I’m taking robus...  
# 0.7468678973398306 {'source': '../../../state\_of\_the\_union.txt'} And so many families...  
# 0.7436231261419488 {'source': '../../../state\_of\_the\_union.txt'} Groups of citizens b...  

```

### 5. Search for Similar Documents with Filtering[​](#5-search-for-similar-documents-with-filtering "Direct link to 5. Search for Similar Documents with Filtering")

```python
output = docsearch.similarity\_search\_with\_relevance\_scores(  
 query,  
 4,  
 Rockset.DistanceFunction.COSINE\_SIM,  
 where\_str="{} NOT LIKE '%citizens%'".format(TEXT\_KEY),  
)  
print("output length:", len(output))  
for d, dist in output:  
 print(dist, d.metadata, d.page\_content[:20] + '...')  
  
##  
# output length: 4  
# 0.7651359650263554 {'source': '../../../state\_of\_the\_union.txt'} Madam Speaker, Madam...  
# 0.7486265516824893 {'source': '../../../state\_of\_the\_union.txt'} And I’m taking robus...  
# 0.7469625542348115 {'source': '../../../state\_of\_the\_union.txt'} And so many families...  
# 0.7344177777547739 {'source': '../../../state\_of\_the\_union.txt'} We see the unity amo...  

```

### 6. \[Optional\] Delete Inserted Documents[​](#6optionaldelete-inserted-documents "Direct link to 6optionaldelete-inserted-documents")

You must have the unique ID associated with each document to delete them from your collection.
Define IDs when inserting documents with `Rockset.add_texts()`. Rockset will otherwise generate a unique ID for each document. Regardless, `Rockset.add_texts()` returns the IDs of inserted documents.

To delete these docs, simply use the `Rockset.delete_texts()` function.

```python
docsearch.delete\_texts(ids)  

```

## Summary[​](#summary "Direct link to Summary")

In this tutorial, we successfully created a `Rockset` collection, `inserted` documents with OpenAI embeddings, and searched for similar documents with and without metadata filters.

Keep an eye on <https://rockset.com/> for future updates in this space.

- [Setting Up Your Environment](#setting-up-your-environment)

- [LangChain Tutorial](#langchain-tutorial)

  - [1. Define Key Variables](#1-define-key-variables)
  - [2. Prepare Documents](#2-prepare-documents)
  - [3. Insert Documents](#3-insert-documents)
  - [4. Search for Similar Documents](#4-search-for-similar-documents)
  - [5. Search for Similar Documents with Filtering](#5-search-for-similar-documents-with-filtering)
  - [6. Optional Delete Inserted Documents](#6optionaldelete-inserted-documents)

- [Summary](#summary)

- [1. Define Key Variables](#1-define-key-variables)

- [2. Prepare Documents](#2-prepare-documents)

- [3. Insert Documents](#3-insert-documents)

- [4. Search for Similar Documents](#4-search-for-similar-documents)

- [5. Search for Similar Documents with Filtering](#5-search-for-similar-documents-with-filtering)

- [6. Optional Delete Inserted Documents](#6optionaldelete-inserted-documents)
