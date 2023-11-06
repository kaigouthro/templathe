# Vector stores

Head to [Integrations](/docs/integrations/vectorstores/) for documentation on built-in integrations with 3rd-party vector stores.

One of the most common ways to store and search over unstructured data is to embed it and store the resulting embedding
vectors, and then at query time to embed the unstructured query and retrieve the embedding vectors that are
'most similar' to the embedded query. A vector store takes care of storing embedded data and performing vector search
for you.

![vector store diagram](/assets/images/vector_stores-9dc1ecb68c4cb446df110764c9cc07e0.jpg)

![vector store diagram](/assets/images/vector_stores-9dc1ecb68c4cb446df110764c9cc07e0.jpg)

## Get started[​](#get-started "Direct link to Get started")

This walkthrough showcases basic functionality related to vector stores. A key part of working with vector stores is creating the vector to put in them, which is usually created via embeddings. Therefore, it is recommended that you familiarize yourself with the [text embedding model](/docs/modules/data_connection/text_embedding/) interfaces before diving into this.

There are many great vector store options, here are a few that are free, open-source, and run entirely on your local machine. Review all integrations for many great hosted offerings.

- Chroma
- FAISS
- Lance

This walkthrough uses the `chroma` vector database, which runs on your local machine as a library.

```bash
pip install chromadb  

```

We want to use OpenAIEmbeddings so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ['OPENAI\_API\_KEY'] = getpass.getpass('OpenAI API Key:')  

```

```python
from langchain.document\_loaders import TextLoader  
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Chroma  
  
# Load the document, split it into chunks, embed each chunk and load it into the vector store.  
raw\_documents = TextLoader('../../../state\_of\_the\_union.txt').load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
documents = text\_splitter.split\_documents(raw\_documents)  
db = Chroma.from\_documents(documents, OpenAIEmbeddings())  

```

This walkthrough uses the `FAISS` vector database, which makes use of the Facebook AI Similarity Search (FAISS) library.

```bash
pip install faiss-cpu  

```

We want to use OpenAIEmbeddings so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ['OPENAI\_API\_KEY'] = getpass.getpass('OpenAI API Key:')  

```

```python
from langchain.document\_loaders import TextLoader  
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import FAISS  
  
# Load the document, split it into chunks, embed each chunk and load it into the vector store.  
raw\_documents = TextLoader('../../../state\_of\_the\_union.txt').load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
documents = text\_splitter.split\_documents(raw\_documents)  
db = FAISS.from\_documents(documents, OpenAIEmbeddings())  

```

This notebook shows how to use functionality related to the LanceDB vector database based on the Lance data format.

```bash
pip install lancedb  

```

We want to use OpenAIEmbeddings so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ['OPENAI\_API\_KEY'] = getpass.getpass('OpenAI API Key:')  

```

```python
from langchain.document\_loaders import TextLoader  
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import LanceDB  
  
import lancedb  
  
db = lancedb.connect("/tmp/lancedb")  
table = db.create\_table(  
 "my\_table",  
 data=[  
 {  
 "vector": embeddings.embed\_query("Hello World"),  
 "text": "Hello World",  
 "id": "1",  
 }  
 ],  
 mode="overwrite",  
)  
  
# Load the document, split it into chunks, embed each chunk and load it into the vector store.  
raw\_documents = TextLoader('../../../state\_of\_the\_union.txt').load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
documents = text\_splitter.split\_documents(raw\_documents)  
db = LanceDB.from\_documents(documents, OpenAIEmbeddings(), connection=table)  

```

### Similarity search[​](#similarity-search "Direct link to Similarity search")

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs = db.similarity\_search(query)  
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.  
  
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.  
  
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.  
  
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

### Similarity search by vector[​](#similarity-search-by-vector "Direct link to Similarity search by vector")

It is also possible to do a search for documents similar to a given embedding vector using `similarity_search_by_vector` which accepts an embedding vector as a parameter instead of a string.

```python
embedding\_vector = OpenAIEmbeddings().embed\_query(query)  
docs = db.similarity\_search\_by\_vector(embedding\_vector)  
print(docs[0].page\_content)  

```

The query is the same, and so the result is also the same.

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.  
  
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.  
  
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.  
  
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

## Asynchronous operations[​](#asynchronous-operations "Direct link to Asynchronous operations")

Vector stores are usually run as a separate service that requires some IO operations, and therefore they might be called asynchronously. That gives performance benefits as you don't waste time waiting for responses from external services. That might also be important if you work with an asynchronous framework, such as [FastAPI](https://fastapi.tiangolo.com/).

LangChain supports async operation on vector stores. All the methods might be called using their async counterparts, with the prefix `a`, meaning `async`.

`Qdrant` is a vector store, which supports all the async operations, thus it will be used in this walkthrough.

```bash
pip install qdrant-client  

```

```python
from langchain.vectorstores import Qdrant  

```

### Create a vector store asynchronously[​](#create-a-vector-store-asynchronously "Direct link to Create a vector store asynchronously")

```python
db = await Qdrant.afrom\_documents(documents, embeddings, "http://localhost:6333")  

```

### Similarity search[​](#similarity-search-1 "Direct link to Similarity search")

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs = await db.asimilarity\_search(query)  
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.  
  
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.  
  
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.  
  
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

### Similarity search by vector[​](#similarity-search-by-vector-1 "Direct link to Similarity search by vector")

```python
embedding\_vector = embeddings.embed\_query(query)  
docs = await db.asimilarity\_search\_by\_vector(embedding\_vector)  

```

## Maximum marginal relevance search (MMR)[​](#maximum-marginal-relevance-search-mmr "Direct link to Maximum marginal relevance search (MMR)")

Maximal marginal relevance optimizes for similarity to query **and** diversity among selected documents. It is also supported in async API.

```python
query = "What did the president say about Ketanji Brown Jackson"  
found\_docs = await qdrant.amax\_marginal\_relevance\_search(query, k=2, fetch\_k=10)  
for i, doc in enumerate(found\_docs):  
 print(f"{i + 1}.", doc.page\_content, "\n")  

```

```text
1. Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.  
  
Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.  
  
One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.  
  
And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  
  
2. We can’t change how divided we’ve been. But we can change how we move forward—on COVID-19 and other issues we must face together.  
  
I recently visited the New York City Police Department days after the funerals of Officer Wilbert Mora and his partner, Officer Jason Rivera.  
  
They were responding to a 9-1-1 call when a man shot and killed them with a stolen gun.  
  
Officer Mora was 27 years old.  
  
Officer Rivera was 22.  
  
Both Dominican Americans who’d grown up on the same streets they later chose to patrol as police officers.  
  
I spoke with their families and told them that we are forever in debt for their sacrifice, and we will carry on their mission to restore the trust and safety every community deserves.  
  
I’ve worked on these issues a long time.  
  
I know what works: Investing in crime prevention and community police officers who’ll walk the beat, who’ll know the neighborhood, and who can restore trust and safety.  

```

- [Get started](#get-started)

  - [Similarity search](#similarity-search)
  - [Similarity search by vector](#similarity-search-by-vector)

- [Asynchronous operations](#asynchronous-operations)

  - [Create a vector store asynchronously](#create-a-vector-store-asynchronously)
  - [Similarity search](#similarity-search-1)
  - [Similarity search by vector](#similarity-search-by-vector-1)

- [Maximum marginal relevance search (MMR)](#maximum-marginal-relevance-search-mmr)

- [Similarity search](#similarity-search)

- [Similarity search by vector](#similarity-search-by-vector)

- [Create a vector store asynchronously](#create-a-vector-store-asynchronously)

- [Similarity search](#similarity-search-1)

- [Similarity search by vector](#similarity-search-by-vector-1)
