# Epsilla

This page covers how to use [Epsilla](https://github.com/epsilla-cloud/vectordb) within LangChain.
It is broken into two parts: installation and setup, and then references to specific Epsilla wrappers.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install the Python SDK with `pip/pip3 install pyepsilla`

## Wrappers[​](#wrappers "Direct link to Wrappers")

### VectorStore[​](#vectorstore "Direct link to VectorStore")

There exists a wrapper around Epsilla vector databases, allowing you to use it as a vectorstore,
whether for semantic search or example selection.

To import this vectorstore:

```python
from langchain.vectorstores import Epsilla  

```

For a more detailed walkthrough of the Epsilla wrapper, see [this notebook](/docs/integrations/vectorstores/epsilla.html)

- [Installation and Setup](#installation-and-setup)

- [Wrappers](#wrappers)

  - [VectorStore](#vectorstore)

- [VectorStore](#vectorstore)
