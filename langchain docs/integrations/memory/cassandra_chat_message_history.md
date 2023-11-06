# Cassandra

[Apache Cassandra®](https://cassandra.apache.org) is a `NoSQL`, row-oriented, highly scalable and highly available database, well suited for storing large amounts of data.

`Cassandra` is a good choice for storing chat message history because it is easy to scale and can handle a large number of writes.

This notebook goes over how to use Cassandra to store chat message history.

## Setting up[​](#setting-up "Direct link to Setting up")

To run this notebook you need either a running `Cassandra` cluster or a `DataStax Astra DB` instance running in the cloud (you can get one for free at [datastax.com](https://astra.datastax.com)). Check [cassio.org](https://cassio.org/start_here/) for more information.

```bash
pip install "cassio>=0.1.0"  

```

### Set up the database connection parameters and secrets[​](#set-up-the-database-connection-parameters-and-secrets "Direct link to Set up the database connection parameters and secrets")

```python
import os  
import getpass  
  
database\_mode = (input("\n(C)assandra or (A)stra DB? ")).upper()  
  
keyspace\_name = input("\nKeyspace name? ")  
  
if database\_mode == "A":  
 ASTRA\_DB\_APPLICATION\_TOKEN = getpass.getpass('\nAstra DB Token ("AstraCS:...") ')  
 #  
 ASTRA\_DB\_SECURE\_BUNDLE\_PATH = input("Full path to your Secure Connect Bundle? ")  
elif database\_mode == "C":  
 CASSANDRA\_CONTACT\_POINTS = input(  
 "Contact points? (comma-separated, empty for localhost) "  
 ).strip()  

```

Depending on whether local or cloud-based Astra DB, create the corresponding database connection "Session" object.

```python
from cassandra.cluster import Cluster  
from cassandra.auth import PlainTextAuthProvider  
  
if database\_mode == "C":  
 if CASSANDRA\_CONTACT\_POINTS:  
 cluster = Cluster(  
 [cp.strip() for cp in CASSANDRA\_CONTACT\_POINTS.split(",") if cp.strip()]  
 )  
 else:  
 cluster = Cluster()  
 session = cluster.connect()  
elif database\_mode == "A":  
 ASTRA\_DB\_CLIENT\_ID = "token"  
 cluster = Cluster(  
 cloud={  
 "secure\_connect\_bundle": ASTRA\_DB\_SECURE\_BUNDLE\_PATH,  
 },  
 auth\_provider=PlainTextAuthProvider(  
 ASTRA\_DB\_CLIENT\_ID,  
 ASTRA\_DB\_APPLICATION\_TOKEN,  
 ),  
 )  
 session = cluster.connect()  
else:  
 raise NotImplementedError  

```

## Example[​](#example "Direct link to Example")

```python
from langchain.memory import CassandraChatMessageHistory  
  
message\_history = CassandraChatMessageHistory(  
 session\_id="test-session",  
 session=session,  
 keyspace=keyspace\_name,  
)  
  
message\_history.add\_user\_message("hi!")  
  
message\_history.add\_ai\_message("whats up?")  

```

```python
message\_history.messages  

```

- [Setting up](#setting-up)

  - [Set up the database connection parameters and secrets](#set-up-the-database-connection-parameters-and-secrets)

- [Example](#example)

- [Set up the database connection parameters and secrets](#set-up-the-database-connection-parameters-and-secrets)
