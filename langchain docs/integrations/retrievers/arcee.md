# Arcee Retriever

This notebook demonstrates how to use the `ArceeRetriever` class to retrieve relevant document(s) for Arcee's Domain Adapted Language Models (DALMs).

### Setup[​](#setup "Direct link to Setup")

Before using `ArceeRetriever`, make sure the Arcee API key is set as `ARCEE_API_KEY` environment variable. You can also pass the api key as a named parameter.

```python
from langchain.retrievers import ArceeRetriever  
  
retriever = ArceeRetriever(  
 model="DALM-PubMed",  
 # arcee\_api\_key="ARCEE-API-KEY" # if not already set in the environment  
)  

```

### Additional Configuration[​](#additional-configuration "Direct link to Additional Configuration")

You can also configure `ArceeRetriever`'s parameters such as `arcee_api_url`, `arcee_app_url`, and `model_kwargs` as needed.
Setting the `model_kwargs` at the object initialization uses the filters and size as default for all the subsequent retrievals.

```python
retriever = ArceeRetriever(  
 model="DALM-PubMed",  
 # arcee\_api\_key="ARCEE-API-KEY", # if not already set in the environment  
 arcee\_api\_url="https://custom-api.arcee.ai", # default is https://api.arcee.ai  
 arcee\_app\_url="https://custom-app.arcee.ai", # default is https://app.arcee.ai  
 model\_kwargs={  
 "size": 5,  
 "filters": [  
 {  
 "field\_name": "document",  
 "filter\_type": "fuzzy\_search",  
 "value": "Einstein"  
 }  
 ]  
 }  
)  

```

### Retrieving documents[​](#retrieving-documents "Direct link to Retrieving documents")

You can retrieve relevant documents from uploaded contexts by providing a query. Here's an example:

```python
query = "Can AI-driven music therapy contribute to the rehabilitation of patients with disorders of consciousness?"  
documents = retriever.get\_relevant\_documents(query=query)  

```

### Additional parameters[​](#additional-parameters "Direct link to Additional parameters")

Arcee allows you to apply `filters` and set the `size` (in terms of count) of retrieved document(s). Filters help narrow down the results. Here's how to use these parameters:

```python
# Define filters  
filters = [  
 {  
 "field\_name": "document",  
 "filter\_type": "fuzzy\_search",  
 "value": "Music"  
 },  
 {  
 "field\_name": "year",  
 "filter\_type": "strict\_search",  
 "value": "1905"  
 }  
]  
  
# Retrieve documents with filters and size params  
documents = retriever.get\_relevant\_documents(query=query, size=5, filters=filters)  

```

- [Setup](#setup)
- [Additional Configuration](#additional-configuration)
- [Retrieving documents](#retrieving-documents)
- [Additional parameters](#additional-parameters)
