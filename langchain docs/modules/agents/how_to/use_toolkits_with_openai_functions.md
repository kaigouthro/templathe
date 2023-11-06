# Use ToolKits with OpenAI Functions

This notebook shows how to use the OpenAI functions agent with arbitrary toolkits.

```python
from langchain.chains import LLMMathChain  
from langchain.llms import OpenAI  
from langchain.utilities import SerpAPIWrapper  
from langchain.utilities import SQLDatabase  
from langchain\_experimental.sql import SQLDatabaseChain  
from langchain.agents import initialize\_agent, Tool  
from langchain.agents import AgentType  
from langchain.chat\_models import ChatOpenAI  
from langchain.agents.agent\_toolkits import SQLDatabaseToolkit  
from langchain.schema import SystemMessage  

```

Load the toolkit:

```python
db = SQLDatabase.from\_uri("sqlite:///../../../../../notebooks/Chinook.db")  
toolkit = SQLDatabaseToolkit(llm=ChatOpenAI(), db=db)  

```

Set a system message specific to that toolkit:

```python
agent\_kwargs = {  
 "system\_message": SystemMessage(content="You are an expert SQL data analyst.")  
}  

```

```python
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")  
agent = initialize\_agent(  
 toolkit.get\_tools(),  
 llm,  
 agent=AgentType.OPENAI\_FUNCTIONS,  
 verbose=True,  
 agent\_kwargs=agent\_kwargs,  
)  

```

```python
agent.run("how many different artists are there?")  

```

```text
   
   
 > Entering new chain...  
   
 Invoking: `sql\_db\_query` with `{'query': 'SELECT COUNT(DISTINCT artist\_name) AS num\_artists FROM artists'}`  
   
   
 Error: (sqlite3.OperationalError) no such table: artists  
 [SQL: SELECT COUNT(DISTINCT artist\_name) AS num\_artists FROM artists]  
 (Background on this error at: https://sqlalche.me/e/20/e3q8)  
 Invoking: `sql\_db\_list\_tables` with `{}`  
   
   
 MediaType, Track, Playlist, sales\_table, Customer, Genre, PlaylistTrack, Artist, Invoice, Album, InvoiceLine, Employee  
 Invoking: `sql\_db\_query` with `{'query': 'SELECT COUNT(DISTINCT artist\_id) AS num\_artists FROM Artist'}`  
   
   
 Error: (sqlite3.OperationalError) no such column: artist\_id  
 [SQL: SELECT COUNT(DISTINCT artist\_id) AS num\_artists FROM Artist]  
 (Background on this error at: https://sqlalche.me/e/20/e3q8)  
 Invoking: `sql\_db\_query` with `{'query': 'SELECT COUNT(DISTINCT Name) AS num\_artists FROM Artist'}`  
   
   
 [(275,)]There are 275 different artists in the database.  
   
 > Finished chain.  
  
  
  
  
  
 'There are 275 different artists in the database.'  

```
