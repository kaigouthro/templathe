# Ensemble Retriever

The `EnsembleRetriever` takes a list of retrievers as input and ensemble the results of their `get_relevant_documents()` methods and rerank the results based on the [Reciprocal Rank Fusion](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) algorithm.

By leveraging the strengths of different algorithms, the `EnsembleRetriever` can achieve better performance than any single algorithm.

The most common pattern is to combine a sparse retriever (like BM25) with a dense retriever (like embedding similarity), because their strengths are complementary. It is also known as "hybrid search". The sparse retriever is good at finding relevant documents based on keywords, while the dense retriever is good at finding relevant documents based on semantic similarity.

```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever  
from langchain.vectorstores import FAISS  

```

```python
doc\_list = [  
 "I like apples",  
 "I like oranges",  
 "Apples and oranges are fruits",  
]  
  
# initialize the bm25 retriever and faiss retriever  
bm25\_retriever = BM25Retriever.from\_texts(doc\_list)  
bm25\_retriever.k = 2  
  
embedding = OpenAIEmbeddings()  
faiss\_vectorstore = FAISS.from\_texts(doc\_list, embedding)  
faiss\_retriever = faiss\_vectorstore.as\_retriever(search\_kwargs={"k": 2})  
  
# initialize the ensemble retriever  
ensemble\_retriever = EnsembleRetriever(retrievers=[bm25\_retriever, faiss\_retriever], weights=[0.5, 0.5])  

```

```python
docs = ensemble\_retriever.get\_relevant\_documents("apples")  
docs  

```

```text
 [Document(page\_content='I like apples', metadata={}),  
 Document(page\_content='Apples and oranges are fruits', metadata={})]  

```
