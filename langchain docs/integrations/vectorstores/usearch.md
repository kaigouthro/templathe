# USearch

[USearch](https://unum-cloud.github.io/usearch/) is a Smaller & Faster Single-File Vector Search Engine

USearch's base functionality is identical to FAISS, and the interface should look familiar if you have ever investigated Approximate Nearest Neigbors search. FAISS is a widely recognized standard for high-performance vector search engines. USearch and FAISS both employ the same HNSW algorithm, but they differ significantly in their design principles. USearch is compact and broadly compatible without sacrificing performance, with a primary focus on user-defined metrics and fewer dependencies.

```bash
pip install usearch  

```

We want to use OpenAIEmbeddings so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import USearch  
from langchain.document\_loaders import TextLoader  

```

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../../extras/modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

```python
db = USearch.from\_documents(docs, embeddings)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs = db.similarity\_search(query)  

```

```python
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

## Similarity Search with score[​](#similarity-search-with-score "Direct link to Similarity Search with score")

The `similarity_search_with_score` method allows you to return not only the documents but also the distance score of the query to them. The returned distance score is L2 distance. Therefore, a lower score is better.

```python
docs\_and\_scores = db.similarity\_search\_with\_score(query)  

```

```python
docs\_and\_scores[0]  

```

```text
 (Document(page\_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../../extras/modules/state\_of\_the\_union.txt'}),  
 0.1845687)  

```

- [Similarity Search with score](#similarity-search-with-score)
