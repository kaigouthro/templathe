# scikit-learn

[scikit-learn](https://scikit-learn.org/stable/) is an open-source collection of machine learning algorithms, including some implementations of the [k nearest neighbors](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html). `SKLearnVectorStore` wraps this implementation and adds the possibility to persist the vector store in json, bson (binary json) or Apache Parquet format.

This notebook shows how to use the `SKLearnVectorStore` vector database.

```python
# # if you plan to use bson serialization, install also:  
# %pip install bson  
  
# # if you plan to use parquet serialization, install also:  
%pip install pandas pyarrow  

```

To use OpenAI embeddings, you will need an OpenAI key. You can get one at <https://platform.openai.com/account/api-keys> or feel free to use any other embeddings.

```python
import os  
from getpass import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass("Enter your OpenAI key:")  

```

## Basic usage[​](#basic-usage "Direct link to Basic usage")

### Load a sample document corpus[​](#load-a-sample-document-corpus "Direct link to Load a sample document corpus")

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import SKLearnVectorStore  
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
embeddings = OpenAIEmbeddings()  

```

### Create the SKLearnVectorStore, index the document corpus and run a sample query[​](#create-the-sklearnvectorstore-index-the-document-corpus-and-run-a-sample-query "Direct link to Create the SKLearnVectorStore, index the document corpus and run a sample query")

```python
import tempfile  
  
persist\_path = os.path.join(tempfile.gettempdir(), "union.parquet")  
  
vector\_store = SKLearnVectorStore.from\_documents(  
 documents=docs,  
 embedding=embeddings,  
 persist\_path=persist\_path, # persist\_path and serializer are optional  
 serializer="parquet",  
)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs = vector\_store.similarity\_search(query)  
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

## Saving and loading a vector store[​](#saving-and-loading-a-vector-store "Direct link to Saving and loading a vector store")

```python
vector\_store.persist()  
print("Vector store was persisted to", persist\_path)  

```

```text
 Vector store was persisted to /var/folders/6r/wc15p6m13nl\_nl\_n\_xfqpc5c0000gp/T/union.parquet  

```

```python
vector\_store2 = SKLearnVectorStore(  
 embedding=embeddings, persist\_path=persist\_path, serializer="parquet"  
)  
print("A new instance of vector store was loaded from", persist\_path)  

```

```text
 A new instance of vector store was loaded from /var/folders/6r/wc15p6m13nl\_nl\_n\_xfqpc5c0000gp/T/union.parquet  

```

```python
docs = vector\_store2.similarity\_search(query)  
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

## Clean-up[​](#clean-up "Direct link to Clean-up")

```python
os.remove(persist\_path)  

```

- [Basic usage](#basic-usage)

  - [Load a sample document corpus](#load-a-sample-document-corpus)
  - [Create the SKLearnVectorStore, index the document corpus and run a sample query](#create-the-sklearnvectorstore-index-the-document-corpus-and-run-a-sample-query)

- [Saving and loading a vector store](#saving-and-loading-a-vector-store)

- [Clean-up](#clean-up)

- [Load a sample document corpus](#load-a-sample-document-corpus)

- [Create the SKLearnVectorStore, index the document corpus and run a sample query](#create-the-sklearnvectorstore-index-the-document-corpus-and-run-a-sample-query)
