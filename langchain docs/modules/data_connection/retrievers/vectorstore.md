# Vector store-backed retriever

A vector store retriever is a retriever that uses a vector store to retrieve documents. It is a lightweight wrapper around the vector store class to make it conform to the retriever interface.
It uses the search methods implemented by a vector store, like similarity search and MMR, to query the texts in the vector store.

Once you construct a vector store, it's very easy to construct a retriever. Let's walk through an example.

```python
from langchain.document\_loaders import TextLoader  
loader = TextLoader('../../../state\_of\_the\_union.txt')  

```

```python
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import FAISS  
from langchain.embeddings import OpenAIEmbeddings  
  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
texts = text\_splitter.split\_documents(documents)  
embeddings = OpenAIEmbeddings()  
db = FAISS.from\_documents(texts, embeddings)  

```

```text
 Exiting: Cleaning up .chroma directory  

```

```python
retriever = db.as\_retriever()  

```

```python
docs = retriever.get\_relevant\_documents("what did he say about ketanji brown jackson")  

```

## Maximum marginal relevance retrieval[​](#maximum-marginal-relevance-retrieval "Direct link to Maximum marginal relevance retrieval")

By default, the vector store retriever uses similarity search. If the underlying vector store supports maximum marginal relevance search, you can specify that as the search type.

```python
retriever = db.as\_retriever(search\_type="mmr")  

```

```python
docs = retriever.get\_relevant\_documents("what did he say about ketanji brown jackson")  

```

## Similarity score threshold retrieval[​](#similarity-score-threshold-retrieval "Direct link to Similarity score threshold retrieval")

You can also a retrieval method that sets a similarity score threshold and only returns documents with a score above that threshold.

```python
retriever = db.as\_retriever(search\_type="similarity\_score\_threshold", search\_kwargs={"score\_threshold": .5})  

```

```python
docs = retriever.get\_relevant\_documents("what did he say about ketanji brown jackson")  

```

## Specifying top k[​](#specifying-top-k "Direct link to Specifying top k")

You can also specify search kwargs like `k` to use when doing retrieval.

```python
retriever = db.as\_retriever(search\_kwargs={"k": 1})  

```

```python
docs = retriever.get\_relevant\_documents("what did he say about ketanji brown jackson")  

```

```python
len(docs)  

```

```text
 1  

```

- [Maximum marginal relevance retrieval](#maximum-marginal-relevance-retrieval)
- [Similarity score threshold retrieval](#similarity-score-threshold-retrieval)
- [Specifying top k](#specifying-top-k)
