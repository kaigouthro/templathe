# SemaDB

SemaDB is a no fuss vector similarity database for building AI applications. The hosted SemaDB Cloud offers a no fuss developer experience to get started.

The full documentation of the API along with examples and an interactive playground is available on [RapidAPI](https://rapidapi.com/semafind-semadb/api/semadb).

This notebook demonstrates how the `langchain` wrapper can be used with SemaDB Cloud.

## Load document embeddings[​](#load-document-embeddings "Direct link to Load document embeddings")

To run things locally, we are using [Sentence Transformers](https://www.sbert.net/) which are commonly used for embedding sentences. You can use any embedding model LangChain offers.

```bash
pip install sentence\_transformers  

```

```python
from langchain.embeddings import HuggingFaceEmbeddings  
  
embeddings = HuggingFaceEmbeddings()  

```

```python
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=400, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
print(len(docs))  

```

```text
 114  

```

## Connect to SemaDB[​](#connect-to-semadb "Direct link to Connect to SemaDB")

SemaDB Cloud uses [RapidAPI keys](https://rapidapi.com/semafind-semadb/api/semadb) to authenticate. You can obtain yours by creating a free RapidAPI account.

```python
import getpass  
import os  
  
os.environ['SEMADB\_API\_KEY'] = getpass.getpass("SemaDB API Key:")  

```

```text
 SemaDB API Key: ········  

```

```python
from langchain.vectorstores import SemaDB  
from langchain.vectorstores.utils import DistanceStrategy  

```

The parameters to the SemaDB vector store reflect the API directly:

- "mycollection": is the collection name in which we will store these vectors.
- 768: is dimensions of the vectors. In our case, the sentence transformer embeddings yield 768 dimensional vectors.
- API_KEY: is your RapidAPI key.
- embeddings: correspond to how the embeddings of documents, texts and queries will be generated.
- DistanceStrategy: is the distance metric used. The wrapper automatically normalises vectors if COSINE is used.

```python
db = SemaDB("mycollection", 768, embeddings, DistanceStrategy.COSINE)  
  
# Create collection if running for the first time. If the collection  
# already exists this will fail.  
db.create\_collection()  

```

```text
 True  

```

The SemaDB vector store wrapper adds the document text as point metadata to collect later. Storing large chunks of text is *not recommended*. If you are indexing a large collection, we instead recommend storing references to the documents such as external Ids.

```python
db.add\_documents(docs)[:2]  

```

```text
 ['813c7ef3-9797-466b-8afa-587115592c6c',  
 'fc392f7f-082b-4932-bfcc-06800db5e017']  

```

## Similarity Search[​](#similarity-search "Direct link to Similarity Search")

We use the default LangChain similarity search interface to search for the most similar sentences.

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs = db.similarity\_search(query)  
print(docs[0].page\_content)  

```

```text
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

```python
docs = db.similarity\_search\_with\_score(query)  
docs[0]  

```

```text
 (Document(page\_content='And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../modules/state\_of\_the\_union.txt', 'text': 'And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.'}),  
 0.42369342)  

```

## Clean up[​](#clean-up "Direct link to Clean up")

You can delete the collection to remove all data.

```python
db.delete\_collection()  

```

```text
 True  

```

- [Load document embeddings](#load-document-embeddings)
- [Connect to SemaDB](#connect-to-semadb)
- [Similarity Search](#similarity-search)
- [Clean up](#clean-up)
