# CnosDB

[CnosDB](https://github.com/cnosdb/cnosdb) is an open-source distributed time series database with high performance, high compression rate and high ease of use.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

```python
pip install cnos-connector  

```

## Connecting to CnosDB[​](#connecting-to-cnosdb "Direct link to Connecting to CnosDB")

You can connect to CnosDB using the `SQLDatabase.from_cnosdb()` method.

### Syntax[​](#syntax "Direct link to Syntax")

```python
def SQLDatabase.from\_cnosdb(url: str = "127.0.0.1:8902",  
 user: str = "root",  
 password: str = "",  
 tenant: str = "cnosdb",  
 database: str = "public")  

```

Args:

1. url (str): The HTTP connection host name and port number of the CnosDB
   service, excluding "http://" or "https://", with a default value
   of "127.0.0.1:8902".
1. user (str): The username used to connect to the CnosDB service, with a
   default value of "root".
1. password (str): The password of the user connecting to the CnosDB service,
   with a default value of "".
1. tenant (str): The name of the tenant used to connect to the CnosDB service,
   with a default value of "cnosdb".
1. database (str): The name of the database in the CnosDB tenant.

## Examples[​](#examples "Direct link to Examples")

```python
# Connecting to CnosDB with SQLDatabase Wrapper  
from langchain.utilities import SQLDatabase  
  
db = SQLDatabase.from\_cnosdb()  

```

```python
# Creating a OpenAI Chat LLM Wrapper  
from langchain.chat\_models import ChatOpenAI  
  
llm = ChatOpenAI(temperature=0, model\_name="gpt-3.5-turbo")  

```

### SQL Database Chain[​](#sql-database-chain "Direct link to SQL Database Chain")

This example demonstrates the use of the SQL Chain for answering a question over a CnosDB.

```python
from langchain.utilities import SQLDatabaseChain  
  
db\_chain = SQLDatabaseChain.from\_llm(llm, db, verbose=True)  
  
db\_chain.run(  
 "What is the average temperature of air at station XiaoMaiDao between October 19, 2022 and Occtober 20, 2022?"  
)  

```

```shell
> Entering new chain...  
What is the average temperature of air at station XiaoMaiDao between October 19, 2022 and Occtober 20, 2022?  
SQLQuery:SELECT AVG(temperature) FROM air WHERE station = 'XiaoMaiDao' AND time >= '2022-10-19' AND time < '2022-10-20'  
SQLResult: [(68.0,)]  
Answer:The average temperature of air at station XiaoMaiDao between October 19, 2022 and October 20, 2022 is 68.0.  
> Finished chain.  

```

### SQL Database Agent[​](#sql-database-agent "Direct link to SQL Database Agent")

This example demonstrates the use of the SQL Database Agent for answering questions over a CnosDB.

```python
from langchain.agents import create\_sql\_agent  
from langchain.agents.agent\_toolkits import SQLDatabaseToolkit  
  
toolkit = SQLDatabaseToolkit(db=db, llm=llm)  
agent = create\_sql\_agent(llm=llm, toolkit=toolkit, verbose=True)  

```

```python
agent.run(  
 "What is the average temperature of air at station XiaoMaiDao between October 19, 2022 and Occtober 20, 2022?"  
)  

```

```shell
> Entering new chain...  
Action: sql\_db\_list\_tables  
Action Input: ""  
Observation: air  
Thought:The "air" table seems relevant to the question. I should query the schema of the "air" table to see what columns are available.  
Action: sql\_db\_schema  
Action Input: "air"  
Observation:  
CREATE TABLE air (  
 pressure FLOAT,  
 station STRING,  
 temperature FLOAT,  
 time TIMESTAMP,  
 visibility FLOAT  
)  
  
/\*  
3 rows from air table:  
pressure station temperature time visibility  
75.0 XiaoMaiDao 67.0 2022-10-19T03:40:00 54.0  
77.0 XiaoMaiDao 69.0 2022-10-19T04:40:00 56.0  
76.0 XiaoMaiDao 68.0 2022-10-19T05:40:00 55.0  
\*/  
Thought:The "temperature" column in the "air" table is relevant to the question. I can query the average temperature between the specified dates.  
Action: sql\_db\_query  
Action Input: "SELECT AVG(temperature) FROM air WHERE station = 'XiaoMaiDao' AND time >= '2022-10-19' AND time <= '2022-10-20'"  
Observation: [(68.0,)]  
Thought:The average temperature of air at station XiaoMaiDao between October 19, 2022 and October 20, 2022 is 68.0.  
Final Answer: 68.0  
  
> Finished chain.  

```

- [Installation and Setup](#installation-and-setup)

- [Connecting to CnosDB](#connecting-to-cnosdb)

  - [Syntax](#syntax)

- [Examples](#examples)

  - [SQL Database Chain](#sql-database-chain)
  - [SQL Database Agent](#sql-database-agent)

- [Syntax](#syntax)

- [SQL Database Chain](#sql-database-chain)

- [SQL Database Agent](#sql-database-agent)
