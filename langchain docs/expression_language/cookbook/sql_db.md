# Querying a SQL DB

We can replicate our SQLDatabaseChain with Runnables.

```python
from langchain.prompts import ChatPromptTemplate  
  
template = """Based on the table schema below, write a SQL query that would answer the user's question:  
{schema}  
  
Question: {question}  
SQL Query:"""  
prompt = ChatPromptTemplate.from\_template(template)  

```

```python
from langchain.utilities import SQLDatabase  

```

We'll need the Chinook sample DB for this example. There's many places to download it from, e.g. <https://database.guide/2-sample-databases-sqlite/>

```python
db = SQLDatabase.from\_uri("sqlite:///./Chinook.db")  

```

```python
def get\_schema(\_):  
 return db.get\_table\_info()  

```

```python
def run\_query(query):  
 return db.run(query)  

```

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.schema.output\_parser import StrOutputParser  
from langchain.schema.runnable import RunnablePassthrough  
  
model = ChatOpenAI()  
  
sql\_response = (  
 RunnablePassthrough.assign(schema=get\_schema)  
 | prompt  
 | model.bind(stop=["\nSQLResult:"])  
 | StrOutputParser()  
 )  

```

```python
sql\_response.invoke({"question": "How many employees are there?"})  

```

```text
 'SELECT COUNT(\*) FROM Employee'  

```

```python
template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:  
{schema}  
  
Question: {question}  
SQL Query: {query}  
SQL Response: {response}"""  
prompt\_response = ChatPromptTemplate.from\_template(template)  

```

```python
full\_chain = (  
 RunnablePassthrough.assign(query=sql\_response)   
 | RunnablePassthrough.assign(  
 schema=get\_schema,  
 response=lambda x: db.run(x["query"]),  
 )  
 | prompt\_response   
 | model  
)  

```

```python
full\_chain.invoke({"question": "How many employees are there?"})  

```

```text
 AIMessage(content='There are 8 employees.', additional\_kwargs={}, example=False)  

```
