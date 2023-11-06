# Motherduck

[Motherduck](https://motherduck.com/) is a managed DuckDB-in-the-cloud service.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

First, you need to install `duckdb` python package.

```bash
pip install duckdb  

```

You will also need to sign up for an account at [Motherduck](https://motherduck.com/)

After that, you should set up a connection string - we mostly integrate with Motherduck through SQLAlchemy.
The connection string is likely in the form:

```text
token="..."  
  
conn\_str = f"duckdb:///md:{token}@my\_db"  

```

## SQLChain[​](#sqlchain "Direct link to SQLChain")

You can use the SQLChain to query data in your Motherduck instance in natural language.

```text
from langchain.llms import OpenAI, SQLDatabase, SQLDatabaseChain  
db = SQLDatabase.from\_uri(conn\_str)  
db\_chain = SQLDatabaseChain.from\_llm(OpenAI(temperature=0), db, verbose=True)  

```

From here, see the [SQL Chain](/docs/use_cases/tabular/sqlite.html) documentation on how to use.

## LLMCache[​](#llmcache "Direct link to LLMCache")

You can also easily use Motherduck to cache LLM requests.
Once again this is done through the SQLAlchemy wrapper.

```text
import sqlalchemy  
from langchain.globals import set\_llm\_cache  
eng = sqlalchemy.create\_engine(conn\_str)  
set\_llm\_cache(SQLAlchemyCache(engine=eng))  

```

From here, see the [LLM Caching](/docs/modules/model_io/models/llms/how_to/llm_caching) documentation on how to use.

- [Installation and Setup](#installation-and-setup)
- [SQLChain](#sqlchain)
- [LLMCache](#llmcache)
