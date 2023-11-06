# Xata

[Xata](https://xata.io) is a serverless data platform, based on PostgreSQL. It provides a Python SDK for interacting with your database, and a UI for managing your data.
Xata has a native vector type, which can be added to any table, and supports similarity search. LangChain inserts vectors directly to Xata, and queries it for the nearest neighbors of a given vector, so that you can use all the LangChain Embeddings integrations with Xata.

This notebook guides you how to use Xata as a VectorStore.

## Setup[​](#setup "Direct link to Setup")

### Create a database to use as a vector store[​](#create-a-database-to-use-as-a-vector-store "Direct link to Create a database to use as a vector store")

In the [Xata UI](https://app.xata.io) create a new database. You can name it whatever you want, in this notepad we'll use `langchain`.
Create a table, again you can name it anything, but we will use `vectors`. Add the following columns via the UI:

- `content` of type "Text". This is used to store the `Document.pageContent` values.
- `embedding` of type "Vector". Use the dimension used by the model you plan to use. In this notebook we use OpenAI embeddings, which have 1536 dimensions.
- `search` of type "Text". This is used as a metadata column by this example.
- any other columns you want to use as metadata. They are populated from the `Document.metadata` object. For example, if in the `Document.metadata` object you have a `title` property, you can create a `title` column in the table and it will be populated.

Let's first install our dependencies:

```bash
pip install xata openai tiktoken langchain  

```

Let's load the OpenAI key to the environemnt. If you don't have one you can create an OpenAI account and create a key on this [page](https://platform.openai.com/account/api-keys).

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

Similarly, we need to get the environment variables for Xata. You can create a new API key by visiting your [account settings](https://app.xata.io/settings). To find the database URL, go to the Settings page of the database that you have created. The database URL should look something like this: `https://demo-uni3q8.eu-west-1.xata.sh/db/langchain`.

```python
api\_key = getpass.getpass("Xata API key: ")  
db\_url = input("Xata database URL (copy it from your DB settings):")  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.document\_loaders import TextLoader  
from langchain.vectorstores.xata import XataVectorStore  

```

### Create the Xata vector store[​](#create-the-xata-vector-store "Direct link to Create the Xata vector store")

Let's import our test dataset:

```python
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

Now create the actual vector store, backed by the Xata table.

```python
vector\_store = XataVectorStore.from\_documents(docs, embeddings, api\_key=api\_key, db\_url=db\_url, table\_name="vectors")  

```

After running the above command, if you go to the Xata UI, you should see the documents loaded together with their embeddings.

### Similarity Search[​](#similarity-search "Direct link to Similarity Search")

```python
query = "What did the president say about Ketanji Brown Jackson"  
found\_docs = vector\_store.similarity\_search(query)  
print(found\_docs)  

```

### Similarity Search with score (vector distance)[​](#similarity-search-with-score-vector-distance "Direct link to Similarity Search with score (vector distance)")

```python
query = "What did the president say about Ketanji Brown Jackson"  
result = vector\_store.similarity\_search\_with\_score(query)  
for doc, score in result:  
 print(f"document={doc}, score={score}")  

```

- [Setup](#setup)

  - [Create a database to use as a vector store](#create-a-database-to-use-as-a-vector-store)
  - [Create the Xata vector store](#create-the-xata-vector-store)
  - [Similarity Search](#similarity-search)
  - [Similarity Search with score (vector distance)](#similarity-search-with-score-vector-distance)

- [Create a database to use as a vector store](#create-a-database-to-use-as-a-vector-store)

- [Create the Xata vector store](#create-the-xata-vector-store)

- [Similarity Search](#similarity-search)

- [Similarity Search with score (vector distance)](#similarity-search-with-score-vector-distance)
