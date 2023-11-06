# OpenAI functions

Certain OpenAI models (like gpt-3.5-turbo-0613 and gpt-4-0613) have been fine-tuned to detect when a function should be called and respond with the inputs that should be passed to the function. In an API call, you can describe functions and have the model intelligently choose to output a JSON object containing arguments to call those functions. The goal of the OpenAI Function APIs is to more reliably return valid and useful function calls than a generic text completion or chat API.

The OpenAI Functions Agent is designed to work with these models.

Install `openai`, `google-search-results` packages which are required as the LangChain packages call them internally.

```bash
pip install openai google-search-results  

```

## Initialize tools[​](#initialize-tools "Direct link to Initialize tools")

We will first create some tools we can use

```python
from langchain.agents import initialize\_agent, AgentType, Tool  
from langchain.chains import LLMMathChain  
from langchain.chat\_models import ChatOpenAI  
from langchain.llms import OpenAI  
from langchain.utilities import SerpAPIWrapper, SQLDatabase  
from langchain\_experimental.sql import SQLDatabaseChain  

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
 description="useful for when you need to answer questions about current events. You should ask targeted questions"  
 ),  
 Tool(  
 name="Calculator",  
 func=llm\_math\_chain.run,  
 description="useful for when you need to answer questions about math"  
 ),  
 Tool(  
 name="FooBar-DB",  
 func=db\_chain.run,  
 description="useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context"  
 )  
]  

```

## Using LCEL[​](#using-lcel "Direct link to Using LCEL")

We will first use LangChain Expression Language to create this agent

```python
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder  

```

```python
prompt = ChatPromptTemplate.from\_messages([  
 ("system", "You are a helpful assistant"),  
 ("user", "{input}"),  
 MessagesPlaceholder(variable\_name="agent\_scratchpad"),  
])  

```

```python
from langchain.tools.render import format\_tool\_to\_openai\_function  

```

```python
llm\_with\_tools = llm.bind(  
 functions=[format\_tool\_to\_openai\_function(t) for t in tools]  
)  

```

```python
from langchain.agents.format\_scratchpad import format\_to\_openai\_functions  
from langchain.agents.output\_parsers import OpenAIFunctionsAgentOutputParser  

```

```python
agent = {  
 "input": lambda x: x["input"],  
 "agent\_scratchpad": lambda x: format\_to\_openai\_functions(x['intermediate\_steps'])  
} | prompt | llm\_with\_tools | OpenAIFunctionsAgentOutputParser()  

```

```python
from langchain.agents import AgentExecutor  

```

```python
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  

```

```python
agent\_executor.invoke({"input": "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"})  

```

````text
   
   
 > Entering new AgentExecutor chain...  
   
 Invoking: `Search` with `Leo DiCaprio's girlfriend`  
   
   
 ['Blake Lively and DiCaprio are believed to have enjoyed a whirlwind five-month romance in 2011. The pair were seen on a yacht together in Cannes, ...']  
 Invoking: `Calculator` with `0.43`  
   
   
   
   
 > Entering new LLMMathChain chain...  
 0.43```text  
 0.43  
````

...numexpr.evaluate("0.43")...

Answer: 0.43

> Finished chain.\
> Answer: 0.43I'm sorry, but I couldn't find any information about Leo DiCaprio's current girlfriend. As for raising her age to the power of 0.43, I'm not sure what her current age is, so I can't provide an answer for that.

> Finished chain.

{'input': "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?",\
'output': "I'm sorry, but I couldn't find any information about Leo DiCaprio's current girlfriend. As for raising her age to the power of 0.43, I'm not sure what her current age is, so I can't provide an answer for that."}

````


Using OpenAIFunctionsAgent[​](#using-openaifunctionsagent "Direct link to Using OpenAIFunctionsAgent")
------------------------------------------------------------------------------------------------------



We can now use `OpenAIFunctionsAgent`, which creates this agent under the hood




```python
agent\_executor = initialize\_agent(tools, llm, agent=AgentType.OPENAI\_FUNCTIONS, verbose=True)  

````

```python
agent\_executor.invoke({"input": "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"})  

```

- [Initialize tools](#initialize-tools)
- [Using LCEL](#using-lcel)
- [Using OpenAIFunctionsAgent](#using-openaifunctionsagent)
