# Azure Cognitive Search

[Azure Cognitive Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search) (formerly known as `Azure Search`) is a cloud search service that gives developers infrastructure, APIs, and tools for building a rich search experience over private, heterogeneous content in web, mobile, and enterprise applications.

Search is foundational to any app that surfaces text to users, where common scenarios include catalog or document search, online retail apps, or data exploration over proprietary content. When you create a search service, you'll work with the following capabilities:

- A search engine for full text search over a search index containing user-owned content
- Rich indexing, with lexical analysis and optional AI enrichment for content extraction and transformation
- Rich query syntax for text search, fuzzy search, autocomplete, geo-search and more
- Programmability through REST APIs and client libraries in Azure SDKs
- Azure integration at the data layer, machine learning layer, and AI (Cognitive Services)

This notebook shows how to use Azure Cognitive Search (ACS) within LangChain.

## Set up Azure Cognitive Search[​](#set-up-azure-cognitive-search "Direct link to Set up Azure Cognitive Search")

To set up ACS, please follow the instructions [here](https://learn.microsoft.com/en-us/azure/search/search-create-service-portal).

Please note

1. the name of your ACS service,
1. the name of your ACS index,
1. your API key.

Your API key can be either Admin or Query key, but as we only read data it is recommended to use a Query key.

## Using the Azure Cognitive Search Retriever[​](#using-the-azure-cognitive-search-retriever "Direct link to Using the Azure Cognitive Search Retriever")

```python
import os  
  
from langchain.retrievers import AzureCognitiveSearchRetriever  

```

Set Service Name, Index Name and API key as environment variables (alternatively, you can pass them as arguments to `AzureCognitiveSearchRetriever`).

```python
os.environ["AZURE\_COGNITIVE\_SEARCH\_SERVICE\_NAME"] = "<YOUR\_ACS\_SERVICE\_NAME>"  
os.environ["AZURE\_COGNITIVE\_SEARCH\_INDEX\_NAME"] = "<YOUR\_ACS\_INDEX\_NAME>"  
os.environ["AZURE\_COGNITIVE\_SEARCH\_API\_KEY"] = "<YOUR\_API\_KEY>"  

```

Create the Retriever

```python
retriever = AzureCognitiveSearchRetriever(content\_key="content", top\_k=10)  

```

Now you can use retrieve documents from Azure Cognitive Search

```python
retriever.get\_relevant\_documents("what is langchain")  

```

You can change the number of results returned with the `top_k` parameter. The default value is `None`, which returns all results.

- [Set up Azure Cognitive Search](#set-up-azure-cognitive-search)
- [Using the Azure Cognitive Search Retriever](#using-the-azure-cognitive-search-retriever)
