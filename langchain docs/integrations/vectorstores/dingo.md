# DingoDB

[DingoDB](https://dingodb.readthedocs.io/en/latest/) is a distributed multi-mode vector database, which combines the characteristics of data lakes and vector databases, and can store data of any type and size (Key-Value, PDF, audio, video, etc.). It has real-time low-latency processing capabilities to achieve rapid insight and response, and can efficiently conduct instant analysis and process multi-modal data.

This notebook shows how to use functionality related to the DingoDB vector database.

To run, you should have a [DingoDB instance up and running](https://github.com/dingodb/dingo-deploy/blob/main/README.md).

```bash
pip install dingodb  
or install latest:  
pip install git+https://git@github.com/dingodb/pydingo.git  

```

We want to use OpenAIEmbeddings so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```text
 OpenAI API Key:········  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Dingo  
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
from dingodb import DingoDB  
  
index\_name = "langchain-demo"  
  
dingo\_client = DingoDB(user="", password="", host=["127.0.0.1:13000"])  
# First, check if our index already exists. If it doesn't, we create it  
if index\_name not in dingo\_client.get\_index():  
 # we create a new index, modify to your own  
 dingo\_client.create\_index(  
 index\_name=index\_name,  
 dimension=1536,  
 metric\_type='cosine',  
 auto\_id=False  
)  
  
# The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`  
docsearch = Dingo.from\_documents(docs, embeddings, client=dingo\_client, index\_name=index\_name)  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Dingo  
from langchain.document\_loaders import TextLoader  

```

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs = docsearch.similarity\_search(query)  

```

```python
print(docs[0].page\_content)  

```

### Adding More Text to an Existing Index[​](#adding-more-text-to-an-existing-index "Direct link to Adding More Text to an Existing Index")

More text can embedded and upserted to an existing Dingo index using the `add_texts` function

```python
vectorstore = Dingo(embeddings, "text", client=dingo\_client, index\_name=index\_name)  
  
vectorstore.add\_texts(["More text!"])  

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
