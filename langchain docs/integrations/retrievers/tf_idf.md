# TF-IDF

[TF-IDF](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting) means term-frequency times inverse document-frequency.

This notebook goes over how to use a retriever that under the hood uses [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) using `scikit-learn` package.

For more information on the details of TF-IDF see [this blog post](https://medium.com/data-science-bootcamp/tf-idf-basics-of-information-retrieval-48de122b2a4c).

```python
# !pip install scikit-learn  

```

```python
from langchain.retrievers import TFIDFRetriever  

```

## Create New Retriever with Texts[​](#create-new-retriever-with-texts "Direct link to Create New Retriever with Texts")

```python
retriever = TFIDFRetriever.from\_texts(["foo", "bar", "world", "hello", "foo bar"])  

```

## Create a New Retriever with Documents[​](#create-a-new-retriever-with-documents "Direct link to Create a New Retriever with Documents")

You can now create a new retriever with the documents you created.

```python
from langchain.schema import Document  
  
retriever = TFIDFRetriever.from\_documents(  
 [  
 Document(page\_content="foo"),  
 Document(page\_content="bar"),  
 Document(page\_content="world"),  
 Document(page\_content="hello"),  
 Document(page\_content="foo bar"),  
 ]  
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

## Save and load[​](#save-and-load "Direct link to Save and load")

You can easily save and load this retriever, making it handy for local development!

```python
retriever.save\_local("testing.pkl")  

```

```python
retriever\_copy = TFIDFRetriever.load\_local("testing.pkl")  

```

```python
retriever\_copy.get\_relevant\_documents("foo")  

```

```text
 [Document(page\_content='foo', metadata={}),  
 Document(page\_content='foo bar', metadata={}),  
 Document(page\_content='hello', metadata={}),  
 Document(page\_content='world', metadata={})]  

```

- [Create New Retriever with Texts](#create-new-retriever-with-texts)
- [Create a New Retriever with Documents](#create-a-new-retriever-with-documents)
- [Use Retriever](#use-retriever)
- [Save and load](#save-and-load)
