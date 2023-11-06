# Cassandra

[Apache Cassandra®](https://cassandra.apache.org/) is a free and open-source, distributed, wide-column
store, NoSQL database management system designed to handle large amounts of data across many commodity servers,
providing high availability with no single point of failure. Cassandra offers support for clusters spanning
multiple datacenters, with asynchronous masterless replication allowing low latency operations for all clients.
Cassandra was designed to implement a combination of *Amazon's Dynamo* distributed storage and replication
techniques combined with *Google's Bigtable* data and storage engine model.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

```bash
pip install cassandra-driver  
pip install cassio  

```

## Vector Store[​](#vector-store "Direct link to Vector Store")

See a [usage example](/docs/integrations/vectorstores/cassandra).

```python
from langchain.vectorstores import Cassandra  

```

## Memory[​](#memory "Direct link to Memory")

See a [usage example](/docs/integrations/memory/cassandra_chat_message_history).

```python
from langchain.memory import CassandraChatMessageHistory  

```

- [Installation and Setup](#installation-and-setup)
- [Vector Store](#vector-store)
- [Memory](#memory)
