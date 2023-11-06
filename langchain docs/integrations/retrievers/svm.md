# SVM

[Support vector machines (SVMs)](https://scikit-learn.org/stable/modules/svm.html#support-vector-machines) are a set of supervised learning methods used for classification, regression and outliers detection.

This notebook goes over how to use a retriever that under the hood uses an `SVM` using `scikit-learn` package.

Largely based on <https://github.com/karpathy/randomfun/blob/master/knn_vs_svm.html>

```python
#!pip install scikit-learn  

```

```python
#!pip install lark  

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
from langchain.retrievers import SVMRetriever  
from langchain.embeddings import OpenAIEmbeddings  

```

## Create New Retriever with Texts[​](#create-new-retriever-with-texts "Direct link to Create New Retriever with Texts")

```python
retriever = SVMRetriever.from\_texts(  
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
 Document(page\_content='world', metadata={})]  

```

- [Create New Retriever with Texts](#create-new-retriever-with-texts)
- [Use Retriever](#use-retriever)
