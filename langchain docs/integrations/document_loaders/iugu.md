# Iugu

[Iugu](https://www.iugu.com/) is a Brazilian services and software as a service (SaaS) company. It offers payment-processing software and application programming interfaces for e-commerce websites and mobile applications.

This notebook covers how to load data from the `Iugu REST API` into a format that can be ingested into LangChain, along with example usage for vectorization.

```python
import os  
  
  
from langchain.document\_loaders import IuguLoader  
from langchain.indexes import VectorstoreIndexCreator  

```

The Iugu API requires an access token, which can be found inside of the Iugu dashboard.

This document loader also requires a `resource` option which defines what data you want to load.

Following resources are available:

`Documentation` [Documentation](https://dev.iugu.com/reference/metadados)

```python
iugu\_loader = IuguLoader("charges")  

```

```python
# Create a vectorstore retriever from the loader  
# see https://python.langchain.com/en/latest/modules/data\_connection/getting\_started.html for more details  
  
index = VectorstoreIndexCreator().from\_loaders([iugu\_loader])  
iugu\_doc\_retriever = index.vectorstore.as\_retriever()  

```
