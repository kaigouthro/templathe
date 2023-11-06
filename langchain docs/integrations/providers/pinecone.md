# Pinecone

[Pinecone](https://docs.pinecone.io/docs/overview) is a vector database with broad functionality.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

Install the Python SDK:

```bash
pip install pinecone-client  

```

## Vector store[​](#vector-store "Direct link to Vector store")

There exists a wrapper around Pinecone indexes, allowing you to use it as a vectorstore,
whether for semantic search or example selection.

```python
from langchain.vectorstores import Pinecone  

```

For a more detailed walkthrough of the Pinecone vectorstore, see [this notebook](/docs/integrations/vectorstores/pinecone.html)

- [Installation and Setup](#installation-and-setup)
- [Vector store](#vector-store)
