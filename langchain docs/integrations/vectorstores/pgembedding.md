# Postgres Embedding

[Postgres Embedding](https://github.com/neondatabase/pg_embedding) is an open-source vector similarity search for `Postgres` that uses `Hierarchical Navigable Small Worlds (HNSW)` for approximate nearest neighbor search.

It supports:

- exact and approximate nearest neighbor search using HNSW
- L2 distance

This notebook shows how to use the Postgres vector database (`PGEmbedding`).

The PGEmbedding integration creates the pg_embedding extension for you, but you run the following Postgres query to add it:

```sql
CREATE EXTENSION embedding;  

```

```bash
# Pip install necessary package  
pip install openai  
pip install psycopg2-binary  
pip install tiktoken  

```

Add the OpenAI API Key to the environment variables to use `OpenAIEmbeddings`.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```text
 OpenAI API Key:········  

```

```python
## Loading Environment Variables  
from typing import List, Tuple  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import PGEmbedding  
from langchain.document\_loaders import TextLoader  
from langchain.docstore.document import Document  

```

```python
os.environ["DATABASE\_URL"] = getpass.getpass("Database Url:")  

```

```text
 Database Url:········  

```

```python
loader = TextLoader("state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  
connection\_string = os.environ.get("DATABASE\_URL")  
collection\_name = "state\_of\_the\_union"  

```

```python
db = PGEmbedding.from\_documents(  
 embedding=embeddings,  
 documents=docs,  
 collection\_name=collection\_name,  
 connection\_string=connection\_string,  
)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs\_with\_score: List[Tuple[Document, float]] = db.similarity\_search\_with\_score(query)  

```

```python
for doc, score in docs\_with\_score:  
 print("-" \* 80)  
 print("Score: ", score)  
 print(doc.page\_content)  
 print("-" \* 80)  

```

## Working with vectorstore in Postgres[​](#working-with-vectorstore-in-postgres "Direct link to Working with vectorstore in Postgres")

### Uploading a vectorstore in PG[​](#uploading-a-vectorstore-in-pg "Direct link to Uploading a vectorstore in PG")

```python
db = PGEmbedding.from\_documents(  
 embedding=embeddings,  
 documents=docs,  
 collection\_name=collection\_name,  
 connection\_string=connection\_string,  
 pre\_delete\_collection=False,  
)  

```

### Create HNSW Index[​](#create-hnsw-index "Direct link to Create HNSW Index")

By default, the extension performs a sequential scan search, with 100% recall. You might consider creating an HNSW index for approximate nearest neighbor (ANN) search to speed up `similarity_search_with_score` execution time. To create the HNSW index on your vector column, use a `create_hnsw_index` function:

```python
PGEmbedding.create\_hnsw\_index(  
 max\_elements=10000, dims=1536, m=8, ef\_construction=16, ef\_search=16  
)  

```

The function above is equivalent to running the below SQL query:

```sql
CREATE INDEX ON vectors USING hnsw(vec) WITH (maxelements=10000, dims=1536, m=3, efconstruction=16, efsearch=16);  

```

The HNSW index options used in the statement above include:

- maxelements: Defines the maximum number of elements indexed. This is a required parameter. The example shown above has a value of 3. A real-world example would have a much large value, such as 1000000. An "element" refers to a data point (a vector) in the dataset, which is represented as a node in the HNSW graph. Typically, you would set this option to a value able to accommodate the number of rows in your in your dataset.
- dims: Defines the number of dimensions in your vector data. This is a required parameter. A small value is used in the example above. If you are storing data generated using OpenAI's text-embedding-ada-002 model, which supports 1536 dimensions, you would define a value of 1536, for example.
- m: Defines the maximum number of bi-directional links (also referred to as "edges") created for each node during graph construction.
  The following additional index options are supported:
- efConstruction: Defines the number of nearest neighbors considered during index construction. The default value is 32.
- efsearch: Defines the number of nearest neighbors considered during index search. The default value is 32.
  For information about how you can configure these options to influence the HNSW algorithm, refer to [Tuning the HNSW algorithm](https://neon.tech/docs/extensions/pg_embedding#tuning-the-hnsw-algorithm).

maxelements: Defines the maximum number of elements indexed. This is a required parameter. The example shown above has a value of 3. A real-world example would have a much large value, such as 1000000. An "element" refers to a data point (a vector) in the dataset, which is represented as a node in the HNSW graph. Typically, you would set this option to a value able to accommodate the number of rows in your in your dataset.

dims: Defines the number of dimensions in your vector data. This is a required parameter. A small value is used in the example above. If you are storing data generated using OpenAI's text-embedding-ada-002 model, which supports 1536 dimensions, you would define a value of 1536, for example.

m: Defines the maximum number of bi-directional links (also referred to as "edges") created for each node during graph construction.
The following additional index options are supported:

efConstruction: Defines the number of nearest neighbors considered during index construction. The default value is 32.

efsearch: Defines the number of nearest neighbors considered during index search. The default value is 32.
For information about how you can configure these options to influence the HNSW algorithm, refer to [Tuning the HNSW algorithm](https://neon.tech/docs/extensions/pg_embedding#tuning-the-hnsw-algorithm).

### Retrieving a vectorstore in PG[​](#retrieving-a-vectorstore-in-pg "Direct link to Retrieving a vectorstore in PG")

```python
store = PGEmbedding(  
 connection\_string=connection\_string,  
 embedding\_function=embeddings,  
 collection\_name=collection\_name,  
)  
  
retriever = store.as\_retriever()  

```

```python
retriever  

```

```text
 VectorStoreRetriever(vectorstore=<langchain.vectorstores.pghnsw.HNSWVectoreStore object at 0x121d3c8b0>, search\_type='similarity', search\_kwargs={})  

```

```python
db1 = PGEmbedding.from\_existing\_index(  
 embedding=embeddings,  
 collection\_name=collection\_name,  
 pre\_delete\_collection=False,  
 connection\_string=connection\_string,  
)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs\_with\_score: List[Tuple[Document, float]] = db1.similarity\_search\_with\_score(query)  

```

```python
for doc, score in docs\_with\_score:  
 print("-" \* 80)  
 print("Score: ", score)  
 print(doc.page\_content)  
 print("-" \* 80)  

```

- [Working with vectorstore in Postgres](#working-with-vectorstore-in-postgres)

  - [Uploading a vectorstore in PG](#uploading-a-vectorstore-in-pg)
  - [Create HNSW Index](#create-hnsw-index)
  - [Retrieving a vectorstore in PG](#retrieving-a-vectorstore-in-pg)

- [Uploading a vectorstore in PG](#uploading-a-vectorstore-in-pg)

- [Create HNSW Index](#create-hnsw-index)

- [Retrieving a vectorstore in PG](#retrieving-a-vectorstore-in-pg)
