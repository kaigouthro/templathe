# DashVector

[DashVector](https://help.aliyun.com/document_detail/2510225.html) is a fully-managed vectorDB service that supports high-dimension dense and sparse vectors, real-time insertion and filtered search. It is built to scale automatically and can adapt to different application requirements.

This notebook shows how to use functionality related to the `DashVector` vector database.

To use DashVector, you must have an API key.
Here are the [installation instructions](https://help.aliyun.com/document_detail/2510223.html).

## Install[​](#install "Direct link to Install")

```bash
pip install dashvector dashscope  

```

We want to use `DashScopeEmbeddings` so we also have to get the Dashscope API Key.

```python
import os  
import getpass  
  
os.environ["DASHVECTOR\_API\_KEY"] = getpass.getpass("DashVector API Key:")  
os.environ["DASHSCOPE\_API\_KEY"] = getpass.getpass("DashScope API Key:")  

```

## Example[​](#example "Direct link to Example")

```python
from langchain.embeddings.dashscope import DashScopeEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import DashVector  

```

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = DashScopeEmbeddings()  

```

We can create DashVector from documents.

```python
dashvector = DashVector.from\_documents(docs, embeddings)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs = dashvector.similarity\_search(query)  
print(docs)  

```

We can add texts with meta datas and ids, and search with meta filter.

```python
texts = ["foo", "bar", "baz"]  
metadatas = [{"key": i} for i in range(len(texts))]  
ids = ["0", "1", "2"]  
  
dashvector.add\_texts(texts, metadatas=metadatas, ids=ids)  
  
docs = dashvector.similarity\_search("foo", filter="key = 2")  
print(docs)  

```

```text
 [Document(page\_content='baz', metadata={'key': 2})]  

```

- [Install](#install)
- [Example](#example)
