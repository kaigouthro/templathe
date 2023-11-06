# Add Memory to OpenAI Functions Agent

This notebook goes over how to add memory to an OpenAI Functions agent.

```python
from langchain.chains import LLMMathChain  
from langchain.llms import OpenAI  
from langchain.utilities import SerpAPIWrapper  
from langchain.utilities import SQLDatabase  
from langchain\_experimental.sql import SQLDatabaseChain  
from langchain.agents import initialize\_agent, Tool  
from langchain.agents import AgentType  
from langchain.chat\_models import ChatOpenAI  

```

```python
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")  
search = SerpAPIWrapper()  
llm\_math\_chain = LLMMathChain.from\_llm(llm=llm, verbose=True)  
db = SQLDatabase.from\_uri("sqlite:///../../../../../notebooks/Chinook.db")  
db\_chain = SQLDatabaseChain.from\_llm(llm, db, verbose=True)  
tools = [  
 Tool(  
 name="Search",  
 func=search.run,  
 description="useful for when you need to answer questions about current events. You should ask targeted questions",  
 ),  
 Tool(  
 name="Calculator",  
 func=llm\_math\_chain.run,  
 description="useful for when you need to answer questions about math",  
 ),  
 Tool(  
 name="FooBar-DB",  
 func=db\_chain.run,  
 description="useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context",  
 ),  
]  

```

```python
from langchain.prompts import MessagesPlaceholder  
from langchain.memory import ConversationBufferMemory  
  
agent\_kwargs = {  
 "extra\_prompt\_messages": [MessagesPlaceholder(variable\_name="memory")],  
}  
memory = ConversationBufferMemory(memory\_key="memory", return\_messages=True)  

```

```python
agent = initialize\_agent(  
 tools,  
 llm,  
 agent=AgentType.OPENAI\_FUNCTIONS,  
 verbose=True,  
 agent\_kwargs=agent\_kwargs,  
 memory=memory,  
)  

```

```python
agent.run("hi")  

```

```text
   
   
 > Entering new chain...  
 Hello! How can I assist you today?  
   
 > Finished chain.  
  
  
  
  
  
 'Hello! How can I assist you today?'  

```

```python
agent.run("my name is bob")  

```

```text
   
   
 > Entering new chain...  
 Nice to meet you, Bob! How can I help you today?  
   
 > Finished chain.  
  
  
  
  
  
 'Nice to meet you, Bob! How can I help you today?'  

```

```python
agent.run("whats my name")  

```

```text
   
   
 > Entering new chain...  
 Your name is Bob.  
   
 > Finished chain.  
  
  
  
  
  
 'Your name is Bob.'  

```
