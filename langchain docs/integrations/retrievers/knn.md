# kNN

In statistics, the [k-nearest neighbors algorithm (k-NN)](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) is a non-parametric supervised learning method first developed by Evelyn Fix and Joseph Hodges in 1951, and later expanded by Thomas Cover. It is used for classification and regression.

This notebook goes over how to use a retriever that under the hood uses an kNN.

Largely based on <https://github.com/karpathy/randomfun/blob/master/knn_vs_svm.html>

```python
from langchain.retrievers import KNNRetriever  
from langchain.embeddings import OpenAIEmbeddings  

```

## Create New Retriever with Texts[​](#create-new-retriever-with-texts "Direct link to Create New Retriever with Texts")

```python
retriever = KNNRetriever.from\_texts(  
 ["foo", "bar", "world", "hello", "foo bar"], OpenAIEmbeddings()  
)  

```

## Use Retriever[​](#use-retriever "Direct link to Use Retriever")

We can now use the retriever!

```python
result = retriever.get\_relevant\_documents("foo")  

```

```python
result  

```

```text
 [Document(page\_content='foo', metadata={}),  
 Document(page\_content='foo bar', metadata={}),  
 Document(page\_content='hello', metadata={}),  
 Document(page\_content='bar', metadata={})]  

```

- [Create New Retriever with Texts](#create-new-retriever-with-texts)
- [Use Retriever](#use-retriever)
