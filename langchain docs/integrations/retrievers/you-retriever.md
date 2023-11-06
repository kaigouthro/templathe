# you-retriever

## Using the You.com Retriever[​](#using-the-youcom-retriever "Direct link to Using the You.com Retriever")

The retriever from You.com is good for retrieving lots of text. We return multiple of the best text snippets per URL we find to be relevant.

First you just need to initialize the retriever

```python
from langchain.retrievers.you\_retriever import YouRetriever  
from langchain.chains import RetrievalQA  
from langchain.llms import OpenAI  
  
yr = YouRetriever()  
qa = RetrievalQA.from\_chain\_type(llm=OpenAI(), chain\_type="map\_reduce", retriever=yr)  

```

```python
query = "what starting ohio state quarterback most recently went their entire college career without beating Michigan?"  
qa.run(query)  

```

- [Using the You.com Retriever](#using-the-youcom-retriever)
