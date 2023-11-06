# DocArray

[DocArray](https://docarray.jina.ai/) is a library for nested, unstructured, multimodal data in transit,
including text, image, audio, video, 3D mesh, etc. It allows deep-learning engineers to efficiently process,
embed, search, recommend, store, and transfer multimodal data with a Pythonic API.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

We need to install `docarray` python package.

```bash
pip install docarray  

```

## Vector Store[​](#vector-store "Direct link to Vector Store")

LangChain provides an access to the `In-memory` and `HNSW` vector stores from the `DocArray` library.

See a [usage example](/docs/integrations/vectorstores/docarray_hnsw).

```python
from langchain.vectorstores DocArrayHnswSearch  

```

See a [usage example](/docs/integrations/vectorstores/docarray_in_memory).

```python
from langchain.vectorstores DocArrayInMemorySearch  

```

- [Installation and Setup](#installation-and-setup)
- [Vector Store](#vector-store)
