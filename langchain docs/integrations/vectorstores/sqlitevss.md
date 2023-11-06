# sqlite-vss

[sqlite-vss](https://alexgarcia.xyz/sqlite-vss/) is an SQLite extension designed for vector search, emphasizing local-first operations and easy integration into applications without external servers. Leveraging the Faiss library, it offers efficient similarity search and clustering capabilities.

This notebook shows how to use the `SQLiteVSS` vector database.

```python
# You need to install sqlite-vss as a dependency.  
%pip install sqlite-vss  

```

### Quickstart[​](#quickstart "Direct link to Quickstart")

```python
from langchain.embeddings.sentence\_transformer import SentenceTransformerEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import SQLiteVSS  
from langchain.document\_loaders import TextLoader  
  
# load the document and split it into chunks  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
  
# split it into chunks  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
texts = [doc.page\_content for doc in docs]  
  
  
# create the open-source embedding function  
embedding\_function = SentenceTransformerEmbeddings(model\_name="all-MiniLM-L6-v2")  
  
  
# load it in sqlite-vss in a table named state\_union.  
# the db\_file parameter is the name of the file you want  
# as your sqlite database.  
db = SQLiteVSS.from\_texts(  
 texts=texts,  
 embedding=embedding\_function,  
 table="state\_union",  
 db\_file="/tmp/vss.db"  
)  
  
# query it  
query = "What did the president say about Ketanji Brown Jackson"  
data = db.similarity\_search(query)  
  
# print results  
data[0].page\_content  

```

```text
 'Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.'  

```

### Using existing sqlite connection[​](#using-existing-sqlite-connection "Direct link to Using existing sqlite connection")

```python
from langchain.embeddings.sentence\_transformer import SentenceTransformerEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import SQLiteVSS  
from langchain.document\_loaders import TextLoader  
  
# load the document and split it into chunks  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
  
# split it into chunks  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
texts = [doc.page\_content for doc in docs]  
  
  
# create the open-source embedding function  
embedding\_function = SentenceTransformerEmbeddings(model\_name="all-MiniLM-L6-v2")  
connection = SQLiteVSS.create\_connection(db\_file="/tmp/vss.db")  
  
db1 = SQLiteVSS(  
 table="state\_union",  
 embedding=embedding\_function,  
 connection=connection  
)  
  
db1.add\_texts(["Ketanji Brown Jackson is awesome"])  
# query it again  
query = "What did the president say about Ketanji Brown Jackson"  
data = db1.similarity\_search(query)  
  
# print results  
data[0].page\_content  

```

```text
 'Ketanji Brown Jackson is awesome'  

```

```python
# Cleaning up  
import os  
os.remove("/tmp/vss.db")  

```

- [Quickstart](#quickstart)
- [Using existing sqlite connection](#using-existing-sqlite-connection)
