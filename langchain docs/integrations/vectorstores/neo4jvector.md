# Neo4j Vector Index

[Neo4j](https://neo4j.com/) is an open-source graph database with integrated support for vector similarity search

It supports:

- approximate nearest neighbor search
- Euclidean similarity and cosine similarity
- Hybrid search combining vector and keyword searches

This notebook shows how to use the Neo4j vector index (`Neo4jVector`).

See the [installation instruction](https://neo4j.com/docs/operations-manual/current/installation/).

```bash
# Pip install necessary package  
pip install neo4j  
pip install openai  
pip install tiktoken  

```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```text
 OpenAI API Key: ········  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Neo4jVector  
from langchain.document\_loaders import TextLoader  
from langchain.docstore.document import Document  

```

```python
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

```python
# Neo4jVector requires the Neo4j database credentials  
  
url = "bolt://localhost:7687"  
username = "neo4j"  
password = "pleaseletmein"  
  
# You can also use environment variables instead of directly passing named parameters  
#os.environ["NEO4J\_URI"] = "bolt://localhost:7687"  
#os.environ["NEO4J\_USERNAME"] = "neo4j"  
#os.environ["NEO4J\_PASSWORD"] = "pleaseletmein"  

```

## Similarity Search with Cosine Distance (Default)[​](#similarity-search-with-cosine-distance-default "Direct link to Similarity Search with Cosine Distance (Default)")

```python
# The Neo4jVector Module will connect to Neo4j and create a vector index if needed.  
  
db = Neo4jVector.from\_documents(  
 docs, OpenAIEmbeddings(), url=url, username=username, password=password  
)  

```

```text
 /home/tomaz/neo4j/langchain/libs/langchain/langchain/vectorstores/neo4j\_vector.py:165: ExperimentalWarning: The configuration may change in the future.  
 self.\_driver.verify\_connectivity()  

```

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs\_with\_score = db.similarity\_search\_with\_score(query, k=2)  

```

```python
for doc, score in docs\_with\_score:  
 print("-" \* 80)  
 print("Score: ", score)  
 print(doc.page\_content)  
 print("-" \* 80)  

```

```text
 --------------------------------------------------------------------------------  
 Score: 0.9099836349487305  
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  
 --------------------------------------------------------------------------------  
 --------------------------------------------------------------------------------  
 Score: 0.9099686145782471  
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  
 --------------------------------------------------------------------------------  

```

## Working with vectorstore[​](#working-with-vectorstore "Direct link to Working with vectorstore")

Above, we created a vectorstore from scratch. However, often times we want to work with an existing vectorstore.
In order to do that, we can initialize it directly.

```python
index\_name = "vector" # default index name  
  
store = Neo4jVector.from\_existing\_index(  
 OpenAIEmbeddings(),  
 url=url,  
 username=username,  
 password=password,  
 index\_name=index\_name,  
)  

```

```text
 /home/tomaz/neo4j/langchain/libs/langchain/langchain/vectorstores/neo4j\_vector.py:165: ExperimentalWarning: The configuration may change in the future.  
 self.\_driver.verify\_connectivity()  

```

We can also initialize a vectorstore from existing graph using the `from_existing_graph` method. This method pulls relevant text information from the database, and calculates and stores the text embeddings back to the database.

```python
# First we create sample data in graph  
store.query(  
 "CREATE (p:Person {name: 'Tomaz', location:'Slovenia', hobby:'Bicycle'})"  
)  

```

```text
 []  

```

```python
# Now we initialize from existing graph  
existing\_graph = Neo4jVector.from\_existing\_graph(  
 embedding=OpenAIEmbeddings(),  
 url=url,  
 username=username,  
 password=password,  
 index\_name="person\_index",  
 node\_label="Person",  
 text\_node\_properties=["name", "location"],  
 embedding\_node\_property="embedding",  
 )  
result = existing\_graph.similarity\_search("Slovenia", k = 1)  

```

```text
 /home/tomaz/neo4j/langchain/libs/langchain/langchain/vectorstores/neo4j\_vector.py:165: ExperimentalWarning: The configuration may change in the future.  
 self.\_driver.verify\_connectivity()  

```

```python
result[0]  

```

```text
 Document(page\_content='\nname: Tomaz\nlocation: Slovenia', metadata={'hobby': 'Bicycle'})  

```

### Add documents[​](#add-documents "Direct link to Add documents")

We can add documents to the existing vectorstore.

```python
store.add\_documents([Document(page\_content="foo")])  

```

```text
 ['187fc53a-5dde-11ee-ad78-1f6b05bf8513']  

```

```python
docs\_with\_score = store.similarity\_search\_with\_score("foo")  

```

```python
docs\_with\_score[0]  

```

```text
 (Document(page\_content='foo', metadata={}), 1.0)  

```

## Hybrid search (vector + keyword)[​](#hybrid-search-vector--keyword "Direct link to Hybrid search (vector + keyword)")

Neo4j integrates both vector and keyword indexes, which allows you to use a hybrid search approach

```python
# The Neo4jVector Module will connect to Neo4j and create a vector and keyword indices if needed.  
hybrid\_db = Neo4jVector.from\_documents(  
 docs,   
 OpenAIEmbeddings(),   
 url=url,   
 username=username,   
 password=password,  
 search\_type="hybrid"  
)  

```

```text
 /home/tomaz/neo4j/langchain/libs/langchain/langchain/vectorstores/neo4j\_vector.py:165: ExperimentalWarning: The configuration may change in the future.  
 self.\_driver.verify\_connectivity()  

```

To load the hybrid search from existing indexes, you have to provide both the vector and keyword indices

```python
index\_name = "vector" # default index name  
keyword\_index\_name = "keyword" #default keyword index name  
  
store = Neo4jVector.from\_existing\_index(  
 OpenAIEmbeddings(),  
 url=url,  
 username=username,  
 password=password,  
 index\_name=index\_name,  
 keyword\_index\_name=keyword\_index\_name,  
 search\_type="hybrid"  
)  

```

```text
 /home/tomaz/neo4j/langchain/libs/langchain/langchain/vectorstores/neo4j\_vector.py:165: ExperimentalWarning: The configuration may change in the future.  
 self.\_driver.verify\_connectivity()  

```

## Retriever options[​](#retriever-options "Direct link to Retriever options")

This section shows how to use `Neo4jVector` as a retriever.

```python
retriever = store.as\_retriever()  
retriever.get\_relevant\_documents(query)[0]  

```

```text
 Document(page\_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../modules/state\_of\_the\_union.txt'})  

```

## Question Answering with Sources[​](#question-answering-with-sources "Direct link to Question Answering with Sources")

This section goes over how to do question-answering with sources over an Index. It does this by using the `RetrievalQAWithSourcesChain`, which does the lookup of the documents from an Index.

```python
from langchain.chains import RetrievalQAWithSourcesChain  
from langchain.chat\_models import ChatOpenAI  

```

```python
chain = RetrievalQAWithSourcesChain.from\_chain\_type(  
 ChatOpenAI(temperature=0), chain\_type="stuff", retriever=retriever  
)  

```

```python
chain(  
 {"question": "What did the president say about Justice Breyer"},  
 return\_only\_outputs=True,  
)  

```

```text
 {'answer': "The president honored Justice Stephen Breyer, who is retiring from the United States Supreme Court. He thanked him for his service and mentioned that he nominated Circuit Court of Appeals Judge Ketanji Brown Jackson to continue Justice Breyer's legacy of excellence. \n",  
 'sources': '../../modules/state\_of\_the\_union.txt'}  

```

- [Similarity Search with Cosine Distance (Default)](#similarity-search-with-cosine-distance-default)

- [Working with vectorstore](#working-with-vectorstore)

  - [Add documents](#add-documents)

- [Hybrid search (vector + keyword)](#hybrid-search-vector--keyword)

- [Retriever options](#retriever-options)

- [Question Answering with Sources](#question-answering-with-sources)

- [Add documents](#add-documents)
