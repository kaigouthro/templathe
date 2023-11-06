# Postgres Embedding

[pg_embedding](https://github.com/neondatabase/pg_embedding) is an open-source package for
vector similarity search using `Postgres` and the `Hierarchical Navigable Small Worlds`
algorithm for approximate nearest neighbor search.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

We need to install several python packages.

```bash
pip install openai  
pip install psycopg2-binary  
pip install tiktoken  

```

## Vector Store[​](#vector-store "Direct link to Vector Store")

See a [usage example](/docs/integrations/vectorstores/pgembedding).

```python
from langchain.vectorstores import PGEmbedding  

```

- [Installation and Setup](#installation-and-setup)
- [Vector Store](#vector-store)
