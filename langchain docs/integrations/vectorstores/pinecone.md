# Pinecone

[Pinecone](https://docs.pinecone.io/docs/overview) is a vector database with broad functionality.

This notebook shows how to use functionality related to the `Pinecone` vector database.

To use Pinecone, you must have an API key.
Here are the [installation instructions](https://docs.pinecone.io/docs/quickstart).

```bash
pip install pinecone-client openai tiktoken langchain  

```

```python
import os  
import getpass  
  
os.environ["PINECONE\_API\_KEY"] = getpass.getpass("Pinecone API Key:")  

```

```python
os.environ["PINECONE\_ENV"] = getpass.getpass("Pinecone Environment:")  

```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.

```python
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Pinecone  
from langchain.document\_loaders import TextLoader  

```

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

```python
import pinecone  
  
# initialize pinecone  
pinecone.init(  
 api\_key=os.getenv("PINECONE\_API\_KEY"), # find at app.pinecone.io  
 environment=os.getenv("PINECONE\_ENV"), # next to api key in console  
)  
  
index\_name = "langchain-demo"  
  
# First, check if our index already exists. If it doesn't, we create it  
if index\_name not in pinecone.list\_indexes():  
 # we create a new index  
 pinecone.create\_index(  
 name=index\_name,  
 metric='cosine',  
 dimension=1536   
)  
# The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`  
docsearch = Pinecone.from\_documents(docs, embeddings, index\_name=index\_name)  
  
# if you already have an index, you can load it like this  
# docsearch = Pinecone.from\_existing\_index(index\_name, embeddings)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs = docsearch.similarity\_search(query)  

```

```python
print(docs[0].page\_content)  

```

### Adding More Text to an Existing Index[​](#adding-more-text-to-an-existing-index "Direct link to Adding More Text to an Existing Index")

More text can embedded and upserted to an existing Pinecone index using the `add_texts` function

```python
index = pinecone.Index("langchain-demo")  
vectorstore = Pinecone(index, embeddings.embed\_query, "text")  
  
vectorstore.add\_texts("More text!")  

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

- [Adding More Text to an Existing Index](#adding-more-text-to-an-existing-index)
- [Maximal Marginal Relevance Searches](#maximal-marginal-relevance-searches)
