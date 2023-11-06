# Chroma

[Chroma](https://docs.trychroma.com/getting-started) is a AI-native open-source vector database focused on developer productivity and happiness. Chroma is licensed under Apache 2.0.

Install Chroma with:

```sh
pip install chromadb  

```

Chroma runs in various modes. See below for examples of each integrated with LangChain.

- `in-memory` - in a python script or jupyter notebook
- `in-memory with persistance` - in a script or notebook and save/load to disk
- `in a docker container` - as a server running your local machine or in the cloud

Like any other database, you can:

- `.add`
- `.get`
- `.update`
- `.upsert`
- `.delete`
- `.peek`
- and `.query` runs the similarity search.

View full docs at [docs](https://docs.trychroma.com/reference/Collection). To access these methods directly, you can do `._collection.method()`

## Basic Example[​](#basic-example "Direct link to Basic Example")

In this basic example, we take the most recent State of the Union Address, split it into chunks, embed it using an open-source embedding model, load it into Chroma, and then query it.

```python
# import  
from langchain.embeddings.sentence\_transformer import SentenceTransformerEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Chroma  
from langchain.document\_loaders import TextLoader  
  
# load the document and split it into chunks  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
  
# split it into chunks  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
# create the open-source embedding function  
embedding\_function = SentenceTransformerEmbeddings(model\_name="all-MiniLM-L6-v2")  
  
# load it into Chroma  
db = Chroma.from\_documents(docs, embedding\_function)  
  
# query it  
query = "What did the president say about Ketanji Brown Jackson"  
docs = db.similarity\_search(query)  
  
# print results  
print(docs[0].page\_content)  

```

```text
 /Users/jeff/.pyenv/versions/3.10.10/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user\_install.html  
 from .autonotebook import tqdm as notebook\_tqdm  
  
  
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

## Basic Example (including saving to disk)[​](#basic-example-including-saving-to-disk "Direct link to Basic Example (including saving to disk)")

Extending the previous example, if you want to save to disk, simply initialize the Chroma client and pass the directory where you want the data to be saved to.

`Caution`: Chroma makes a best-effort to automatically save data to disk, however multiple in-memory clients can stomp each other's work. As a best practice, only have one client per path running at any given time.

```python
# save to disk  
db2 = Chroma.from\_documents(docs, embedding\_function, persist\_directory="./chroma\_db")  
docs = db2.similarity\_search(query)  
  
# load from disk  
db3 = Chroma(persist\_directory="./chroma\_db", embedding\_function=embedding\_function)  
docs = db3.similarity\_search(query)  
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

## Passing a Chroma Client into Langchain[​](#passing-a-chroma-client-into-langchain "Direct link to Passing a Chroma Client into Langchain")

You can also create a Chroma Client and pass it to LangChain. This is particularly useful if you want easier access to the underlying database.

You can also specify the collection name that you want LangChain to use.

```python
import chromadb  
  
persistent\_client = chromadb.PersistentClient()  
collection = persistent\_client.get\_or\_create\_collection("collection\_name")  
collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])  
  
langchain\_chroma = Chroma(  
 client=persistent\_client,  
 collection\_name="collection\_name",  
 embedding\_function=embedding\_function,  
)  
  
print("There are", langchain\_chroma.\_collection.count(), "in the collection")  

```

```text
 Add of existing embedding ID: 1  
 Add of existing embedding ID: 2  
 Add of existing embedding ID: 3  
 Add of existing embedding ID: 1  
 Add of existing embedding ID: 2  
 Add of existing embedding ID: 3  
 Add of existing embedding ID: 1  
 Insert of existing embedding ID: 1  
 Add of existing embedding ID: 2  
 Insert of existing embedding ID: 2  
 Add of existing embedding ID: 3  
 Insert of existing embedding ID: 3  
  
  
 There are 3 in the collection  

```

## Basic Example (using the Docker Container)[​](#basic-example-using-the-docker-container "Direct link to Basic Example (using the Docker Container)")

You can also run the Chroma Server in a Docker container separately, create a Client to connect to it, and then pass that to LangChain.

Chroma has the ability to handle multiple `Collections` of documents, but the LangChain interface expects one, so we need to specify the collection name. The default collection name used by LangChain is "langchain".

Here is how to clone, build, and run the Docker Image:

```sh
git clone git@github.com:chroma-core/chroma.git  

```

Edit the `docker-compose.yml` file and add `ALLOW_RESET=TRUE` under `environment`

```yaml
 ...  
 command: uvicorn chromadb.app:app --reload --workers 1 --host 0.0.0.0 --port 8000 --log-config log\_config.yml  
 environment:  
 - IS\_PERSISTENT=TRUE  
 - ALLOW\_RESET=TRUE  
 ports:  
 - 8000:8000  
 ...  

```

Then run `docker-compose up -d --build`

```python
# create the chroma client  
import chromadb  
import uuid  
from chromadb.config import Settings  
  
client = chromadb.HttpClient(settings=Settings(allow\_reset=True))  
client.reset() # resets the database  
collection = client.create\_collection("my\_collection")  
for doc in docs:  
 collection.add(  
 ids=[str(uuid.uuid1())], metadatas=doc.metadata, documents=doc.page\_content  
 )  
  
# tell LangChain to use our client and collection name  
db4 = Chroma(client=client, collection\_name="my\_collection", embedding\_function=embedding\_function)  
query = "What did the president say about Ketanji Brown Jackson"  
docs = db4.similarity\_search(query)  
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

## Update and Delete[​](#update-and-delete "Direct link to Update and Delete")

While building toward a real application, you want to go beyond adding data, and also update and delete data.

Chroma has users provide `ids` to simplify the bookkeeping here. `ids` can be the name of the file, or a combined has like `filename_paragraphNumber`, etc.

Chroma supports all these operations - though some of them are still being integrated all the way through the LangChain interface. Additional workflow improvements will be added soon.

Here is a basic example showing how to do various operations:

```python
# create simple ids  
ids = [str(i) for i in range(1, len(docs) + 1)]  
  
# add data  
example\_db = Chroma.from\_documents(docs, embedding\_function, ids=ids)  
docs = example\_db.similarity\_search(query)  
print(docs[0].metadata)  
  
# update the metadata for a document  
docs[0].metadata = {  
 "source": "../../modules/state\_of\_the\_union.txt",  
 "new\_value": "hello world",  
}  
example\_db.update\_document(ids[0], docs[0])  
print(example\_db.\_collection.get(ids=[ids[0]]))  
  
# delete the last document  
print("count before", example\_db.\_collection.count())  
example\_db.\_collection.delete(ids=[ids[-1]])  
print("count after", example\_db.\_collection.count())  

```

```text
 {'source': '../../../state\_of\_the\_union.txt'}  
 {'ids': ['1'], 'embeddings': None, 'metadatas': [{'new\_value': 'hello world', 'source': '../../../state\_of\_the\_union.txt'}], 'documents': ['Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.']}  
 count before 46  
 count after 45  

```

## Use OpenAI Embeddings[​](#use-openai-embeddings "Direct link to Use OpenAI Embeddings")

Many people like to use OpenAIEmbeddings, here is how to set that up.

```python
# get a token: https://platform.openai.com/account/api-keys  
  
from getpass import getpass  
from langchain.embeddings.openai import OpenAIEmbeddings  
  
OPENAI\_API\_KEY = getpass()  

```

```python
import os  
  
os.environ["OPENAI\_API\_KEY"] = OPENAI\_API\_KEY  

```

```python
embeddings = OpenAIEmbeddings()  
new\_client = chromadb.EphemeralClient()  
openai\_lc\_client = Chroma.from\_documents(  
 docs, embeddings, client=new\_client, collection\_name="openai\_collection"  
)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs = openai\_lc\_client.similarity\_search(query)  
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

## Other Information[​](#other-information "Direct link to Other Information")

### Similarity search with score[​](#similarity-search-with-score "Direct link to Similarity search with score")

The returned distance score is cosine distance. Therefore, a lower score is better.

```python
docs = db.similarity\_search\_with\_score(query)  

```

```python
docs[0]  

```

```text
 (Document(page\_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../../state\_of\_the\_union.txt'}),  
 1.1972057819366455)  

```

### Retriever options[​](#retriever-options "Direct link to Retriever options")

This section goes over different options for how to use Chroma as a retriever.

#### MMR[​](#mmr "Direct link to MMR")

In addition to using similarity search in the retriever object, you can also use `mmr`.

```python
retriever = db.as\_retriever(search\_type="mmr")  

```

```python
retriever.get\_relevant\_documents(query)[0]  

```

```text
 Document(page\_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../../state\_of\_the\_union.txt'})  

```

### Filtering on metadata[​](#filtering-on-metadata "Direct link to Filtering on metadata")

It can be helpful to narrow down the collection before working with it.

For example, collections can be filtered on metadata using the get method.

```python
# filter collection for updated source  
example\_db.get(where={"source": "some\_other\_source"})  

```

```text
 {'ids': [], 'embeddings': None, 'metadatas': [], 'documents': []}  

```

- [Basic Example](#basic-example)

- [Basic Example (including saving to disk)](#basic-example-including-saving-to-disk)

- [Passing a Chroma Client into Langchain](#passing-a-chroma-client-into-langchain)

- [Basic Example (using the Docker Container)](#basic-example-using-the-docker-container)

- [Update and Delete](#update-and-delete)

- [Use OpenAI Embeddings](#use-openai-embeddings)

- [Other Information](#other-information)

  - [Similarity search with score](#similarity-search-with-score)
  - [Retriever options](#retriever-options)
  - [Filtering on metadata](#filtering-on-metadata)

- [Similarity search with score](#similarity-search-with-score)

- [Retriever options](#retriever-options)

- [Filtering on metadata](#filtering-on-metadata)
