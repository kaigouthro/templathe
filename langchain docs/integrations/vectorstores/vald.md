# Vald

[Vald](https://github.com/vdaas/vald) is a highly scalable distributed fast approximate nearest neighbor (ANN) dense vector search engine.

This notebook shows how to use functionality related to the `Vald` database.

To run this notebook you need a running Vald cluster.
Check [Get Started](https://github.com/vdaas/vald#get-started) for more information.

See the [installation instructions](https://github.com/vdaas/vald-client-python#install).

```bash
pip install vald-client-python  

```

## Basic Example[​](#basic-example "Direct link to Basic Example")

```python
from langchain.document\_loaders import TextLoader  
from langchain.embeddings import HuggingFaceEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Vald  
  
raw\_documents = TextLoader('state\_of\_the\_union.txt').load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
documents = text\_splitter.split\_documents(raw\_documents)  
embeddings = HuggingFaceEmbeddings()  
db = Vald.from\_documents(documents, embeddings, host="localhost", port=8080)  

```

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs = db.similarity\_search(query)  
docs[0].page\_content  

```

### Similarity search by vector[​](#similarity-search-by-vector "Direct link to Similarity search by vector")

```python
embedding\_vector = embeddings.embed\_query(query)  
docs = db.similarity\_search\_by\_vector(embedding\_vector)  
docs[0].page\_content  

```

### Similarity search with score[​](#similarity-search-with-score "Direct link to Similarity search with score")

```python
docs\_and\_scores = db.similarity\_search\_with\_score(query)  
docs\_and\_scores[0]  

```

## Maximal Marginal Relevance Search (MMR)[​](#maximal-marginal-relevance-search-mmr "Direct link to Maximal Marginal Relevance Search (MMR)")

In addition to using similarity search in the retriever object, you can also use `mmr` as retriever.

```python
retriever = db.as\_retriever(search\_type="mmr")  
retriever.get\_relevant\_documents(query)  

```

Or use `max_marginal_relevance_search` directly:

```python
db.max\_marginal\_relevance\_search(query, k=2, fetch\_k=10)  

```

- [Basic Example](#basic-example)

  - [Similarity search by vector](#similarity-search-by-vector)
  - [Similarity search with score](#similarity-search-with-score)

- [Maximal Marginal Relevance Search (MMR)](#maximal-marginal-relevance-search-mmr)

- [Similarity search by vector](#similarity-search-by-vector)

- [Similarity search with score](#similarity-search-with-score)
