# OpenSearch

This page covers how to use the OpenSearch ecosystem within LangChain.
It is broken into two parts: installation and setup, and then references to specific OpenSearch wrappers.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install the Python package with `pip install opensearch-py`

## Wrappers[​](#wrappers "Direct link to Wrappers")

### VectorStore[​](#vectorstore "Direct link to VectorStore")

There exists a wrapper around OpenSearch vector databases, allowing you to use it as a vectorstore
for semantic search using approximate vector search powered by lucene, nmslib and faiss engines
or using painless scripting and script scoring functions for bruteforce vector search.

To import this vectorstore:

```python
from langchain.vectorstores import OpenSearchVectorSearch  

```

For a more detailed walkthrough of the OpenSearch wrapper, see [this notebook](/docs/integrations/vectorstores/opensearch.html)

- [Installation and Setup](#installation-and-setup)

- [Wrappers](#wrappers)

  - [VectorStore](#vectorstore)

- [VectorStore](#vectorstore)
