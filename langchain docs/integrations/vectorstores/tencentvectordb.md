# Tencent Cloud VectorDB

[Tencent Cloud VectorDB](https://cloud.tencent.com/document/product/1709) is a fully managed, self-developed, enterprise-level distributed database service designed for storing, retrieving, and analyzing multi-dimensional vector data. The database supports multiple index types and similarity calculation methods. A single index can support a vector scale of up to 1 billion and can support millions of QPS and millisecond-level query latency. Tencent Cloud Vector Database can not only provide an external knowledge base for large models to improve the accuracy of large model responses but can also be widely used in AI fields such as recommendation systems, NLP services, computer vision, and intelligent customer service.

This notebook shows how to use functionality related to the Tencent vector database.

To run, you should have a [Database instance.](https://cloud.tencent.com/document/product/1709/95101).

```bash
pip3 install tcvectordb  

```

```python
from langchain.embeddings.fake import FakeEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import TencentVectorDB  
from langchain.vectorstores.tencentvectordb import ConnectionParams  
from langchain.document\_loaders import TextLoader  

```

```python
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
embeddings = FakeEmbeddings(size=128)  

```

```python
conn\_params = ConnectionParams(url="http://10.0.X.X",   
 key="eC4bLRy2va\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*",   
 username="root",   
 timeout=20)  
  
vector\_db = TencentVectorDB.from\_documents(  
 docs,  
 embeddings,  
 connection\_params=conn\_params,  
 # drop\_old=True,  
)  

```

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs = vector\_db.similarity\_search(query)  
docs[0].page\_content  

```

```python
vector\_db = TencentVectorDB(embeddings, conn\_params)  
  
vector\_db.add\_texts(["Ankush went to Princeton"])  
query = "Where did Ankush go to college?"  
docs = vector\_db.max\_marginal\_relevance\_search(query)  
docs[0].page\_content  

```
