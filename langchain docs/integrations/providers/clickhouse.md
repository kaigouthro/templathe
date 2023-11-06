# ClickHouse

[ClickHouse](https://clickhouse.com/) is the fast and resource efficient open-source database for real-time
apps and analytics with full SQL support and a wide range of functions to assist users in writing analytical queries.
It has data structures and distance search functions (like `L2Distance`) as well as
[approximate nearest neighbor search indexes](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/annindexes)
That enables ClickHouse to be used as a high performance and scalable vector database to store and search vectors with SQL.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

We need to install `clickhouse-connect` python package.

```bash
pip install clickhouse-connect  

```

## Vector Store[​](#vector-store "Direct link to Vector Store")

See a [usage example](/docs/integrations/vectorstores/clickhouse).

```python
from langchain.vectorstores import Clickhouse, ClickhouseSettings  

```

- [Installation and Setup](#installation-and-setup)
- [Vector Store](#vector-store)
