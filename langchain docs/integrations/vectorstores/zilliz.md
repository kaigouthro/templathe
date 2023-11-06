# Zilliz

[Zilliz Cloud](https://zilliz.com/doc/quick_start) is a fully managed service on cloud for `LF AI Milvus®`,

This notebook shows how to use functionality related to the Zilliz Cloud managed vector database.

To run, you should have a `Zilliz Cloud` instance up and running. Here are the [installation instructions](https://zilliz.com/cloud)

```bash
pip install pymilvus  

```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```text
 OpenAI API Key:········  

```

```python
# replace  
ZILLIZ\_CLOUD\_URI = "" # example: "https://in01-17f69c292d4a5sa.aws-us-west-2.vectordb.zillizcloud.com:19536"  
ZILLIZ\_CLOUD\_USERNAME = "" # example: "username"  
ZILLIZ\_CLOUD\_PASSWORD = "" # example: "\*\*\*\*\*\*\*\*\*"  
ZILLIZ\_CLOUD\_API\_KEY = "" # example: "\*\*\*\*\*\*\*\*\*" (for serverless clusters which can be used as replacements for user and password)  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Milvus  
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
vector\_db = Milvus.from\_documents(  
 docs,  
 embeddings,  
 connection\_args={  
 "uri": ZILLIZ\_CLOUD\_URI,  
 "user": ZILLIZ\_CLOUD\_USERNAME,  
 "password": ZILLIZ\_CLOUD\_PASSWORD,  
 # "token": ZILLIZ\_CLOUD\_API\_KEY, # API key, for serverless clusters which can be used as replacements for user and password  
 "secure": True,  
 },  
)  

```

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs = vector\_db.similarity\_search(query)  

```

```python
docs[0].page\_content  

```

```text
 'Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.'  

```
