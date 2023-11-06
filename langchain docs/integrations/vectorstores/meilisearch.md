# Meilisearch

[Meilisearch](https://meilisearch.com) is an open-source, lightning-fast, and hyper relevant search engine. It comes with great defaults to help developers build snappy search experiences.

You can [self-host Meilisearch](https://www.meilisearch.com/docs/learn/getting_started/installation#local-installation) or run on [Meilisearch Cloud](https://www.meilisearch.com/pricing).

Meilisearch v1.3 supports vector search. This page guides you through integrating Meilisearch as a vector store and using it to perform vector search.

## Setup[​](#setup "Direct link to Setup")

### Launching a Meilisearch instance[​](#launching-a-meilisearch-instance "Direct link to Launching a Meilisearch instance")

You will need a running Meilisearch instance to use as your vector store. You can run [Meilisearch in local](https://www.meilisearch.com/docs/learn/getting_started/installation#local-installation) or create a [Meilisearch Cloud](https://cloud.meilisearch.com/) account.

As of Meilisearch v1.3, vector storage is an experimental feature. After launching your Meilisearch instance, you need to **enable vector storage**. For self-hosted Meilisearch, read the docs on [enabling experimental features](https://www.meilisearch.com/docs/learn/experimental/vector-search). On **Meilisearch Cloud**, enable *Vector Store* via your project *Settings* page.

You should now have a running Meilisearch instance with vector storage enabled. 🎉

### Credentials[​](#credentials "Direct link to Credentials")

To interact with your Meilisearch instance, the Meilisearch SDK needs a host (URL of your instance) and an API key.

**Host**

- In **local**, the default host is `localhost:7700`
- On **Meilisearch Cloud**, find the host in your project *Settings* page

**API keys**

Meilisearch instance provides you with three API keys out of the box:

- A `MASTER KEY` — it should only be used to create your Meilisearch instance
- A `ADMIN KEY` — use it only server-side to update your database and its settings
- A `SEARCH KEY` — a key that you can safely share in front-end applications

You can create [additional API keys](https://www.meilisearch.com/docs/learn/security/master_api_keys) as needed.

### Installing dependencies[​](#installing-dependencies "Direct link to Installing dependencies")

This guide uses the [Meilisearch Python SDK](https://github.com/meilisearch/meilisearch-python). You can install it by running:

```bash
pip install meilisearch  

```

For more information, refer to the [Meilisearch Python SDK documentation](https://meilisearch.github.io/meilisearch-python/).

## Examples[​](#examples "Direct link to Examples")

There are multiple ways to initialize the Meilisearch vector store: providing a Meilisearch client or the *URL* and *API key* as needed. In our examples, the credentials will be loaded from the environment.

You can make environment variables available in your Notebook environment by using `os` and `getpass`. You can use this technique for all the following examples.

```python
import os  
import getpass  
  
os.environ["MEILI\_HTTP\_ADDR"] = getpass.getpass("Meilisearch HTTP address and port:")  
os.environ["MEILI\_MASTER\_KEY"] = getpass.getpass("Meilisearch API Key:")  

```

We want to use OpenAIEmbeddings so we have to get the OpenAI API Key.

```python
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

### Adding text and embeddings[​](#adding-text-and-embeddings "Direct link to Adding text and embeddings")

This example adds text to the Meilisearch vector database without having to initialize a Meilisearch vector store.

```python
from langchain.vectorstores import Meilisearch  
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
  
embeddings = OpenAIEmbeddings()  

```

```python
with open("../../modules/state\_of\_the\_union.txt") as f:  
 state\_of\_the\_union = f.read()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
texts = text\_splitter.split\_text(state\_of\_the\_union)  

```

```python
# Use Meilisearch vector store to store texts & associated embeddings as vector  
vector\_store = Meilisearch.from\_texts(texts=texts, embedding=embeddings)  

```

Behind the scenes, Meilisearch will convert the text to multiple vectors. This will bring us to the same result as the following example.

### Adding documents and embeddings[​](#adding-documents-and-embeddings "Direct link to Adding documents and embeddings")

In this example, we'll use Langchain TextSplitter to split the text in multiple documents. Then, we'll store these documents along with their embeddings.

```python
from langchain.document\_loaders import TextLoader  
  
# Load text  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
  
# Create documents  
docs = text\_splitter.split\_documents(documents)  
  
# Import documents & embeddings in the vector store  
vector\_store = Meilisearch.from\_documents(documents=documents, embedding=embeddings)  
  
# Search in our vector store  
query = "What did the president say about Ketanji Brown Jackson"  
docs = vector\_store.similarity\_search(query)  
print(docs[0].page\_content)  

```

## Add documents by creating a Meilisearch Vectorstore[​](#add-documents-by-creating-a-meilisearch-vectorstore "Direct link to Add documents by creating a Meilisearch Vectorstore")

In this approach, we create a vector store object and add documents to it.

```python
from langchain.vectorstores import Meilisearch  
import meilisearch  
  
client = meilisearch.Client(url="http://127.0.0.1:7700", api\_key="\*\*\*")  
vector\_store = Meilisearch(  
 embedding=embeddings, client=client, index\_name="langchain\_demo", text\_key="text"  
)  
vector\_store.add\_documents(documents)  

```

## Similarity Search with score[​](#similarity-search-with-score "Direct link to Similarity Search with score")

This specific method allows you to return the documents and the distance score of the query to them.

```python
docs\_and\_scores = vector\_store.similarity\_search\_with\_score(query)  
docs\_and\_scores[0]  

```

## Similarity Search by vector[​](#similarity-search-by-vector "Direct link to Similarity Search by vector")

```python
embedding\_vector = embeddings.embed\_query(query)  
docs\_and\_scores = vector\_store.similarity\_search\_by\_vector(embedding\_vector)  
docs\_and\_scores[0]  

```

## Additional resources[​](#additional-resources "Direct link to Additional resources")

Documentation

- [Meilisearch](https://www.meilisearch.com/docs/)
- [Meilisearch Python SDK](https://python-sdk.meilisearch.com)

Open-source repositories

- [Meilisearch repository](https://github.com/meilisearch/meilisearch)

- [Meilisearch Python SDK](https://github.com/meilisearch/meilisearch-python)

- [Setup](#setup)

  - [Launching a Meilisearch instance](#launching-a-meilisearch-instance)
  - [Credentials](#credentials)
  - [Installing dependencies](#installing-dependencies)

- [Examples](#examples)

  - [Adding text and embeddings](#adding-text-and-embeddings)
  - [Adding documents and embeddings](#adding-documents-and-embeddings)

- [Add documents by creating a Meilisearch Vectorstore](#add-documents-by-creating-a-meilisearch-vectorstore)

- [Similarity Search with score](#similarity-search-with-score)

- [Similarity Search by vector](#similarity-search-by-vector)

- [Additional resources](#additional-resources)

- [Launching a Meilisearch instance](#launching-a-meilisearch-instance)

- [Credentials](#credentials)

- [Installing dependencies](#installing-dependencies)

- [Adding text and embeddings](#adding-text-and-embeddings)

- [Adding documents and embeddings](#adding-documents-and-embeddings)
