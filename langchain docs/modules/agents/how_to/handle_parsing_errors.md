# Handle parsing errors

Occasionally the LLM cannot determine what step to take because its outputs are not correctly formatted to be handled by the output parser. In this case, by default the agent errors. But you can easily control this functionality with `handle_parsing_errors`! Let's explore how.

## Setup[​](#setup "Direct link to Setup")

```python
from langchain.llms import OpenAI  
from langchain.chains import LLMMathChain  
from langchain.utilities import SerpAPIWrapper  
from langchain.utilities import SQLDatabase  
from langchain\_experimental.sql import SQLDatabaseChain  
from langchain.agents import initialize\_agent, Tool  
from langchain.agents import AgentType  
from langchain.chat\_models import ChatOpenAI  
from langchain.agents.types import AGENT\_TO\_CLASS  

```

```python
search = SerpAPIWrapper()  
tools = [  
 Tool(  
 name="Search",  
 func=search.run,  
 description="useful for when you need to answer questions about current events. You should ask targeted questions",  
 ),  
]  

```

## Error[​](#error "Direct link to Error")

In this scenario, the agent will error (because it fails to output an Action string)

```python
mrkl = initialize\_agent(  
 tools,  
 ChatOpenAI(temperature=0),  
 agent=AgentType.CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION,  
 verbose=True,  
)  

```

```python
mrkl.run("Who is Leo DiCaprio's girlfriend? No need to add Action")  

```

````text
   
   
 > Entering new AgentExecutor chain...  
  
  
  
 ---------------------------------------------------------------------------  
  
 IndexError Traceback (most recent call last)  
  
 File ~/workplace/langchain/langchain/agents/chat/output\_parser.py:21, in ChatOutputParser.parse(self, text)  
 20 try:  
 ---> 21 action = text.split("```")[1]  
 22 response = json.loads(action.strip())  
  
  
 IndexError: list index out of range  
  
   
 During handling of the above exception, another exception occurred:  
  
  
 OutputParserException Traceback (most recent call last)  
  
 Cell In[4], line 1  
 ----> 1 mrkl.run("Who is Leo DiCaprio's girlfriend? No need to add Action")  
  
  
 File ~/workplace/langchain/langchain/chains/base.py:236, in Chain.run(self, callbacks, \*args, \*\*kwargs)  
 234 if len(args) != 1:  
 235 raise ValueError("`run` supports only one positional argument.")  
 --> 236 return self(args[0], callbacks=callbacks)[self.output\_keys[0]]  
 238 if kwargs and not args:  
 239 return self(kwargs, callbacks=callbacks)[self.output\_keys[0]]  
  
  
 File ~/workplace/langchain/langchain/chains/base.py:140, in Chain.\_\_call\_\_(self, inputs, return\_only\_outputs, callbacks)  
 138 except (KeyboardInterrupt, Exception) as e:  
 139 run\_manager.on\_chain\_error(e)  
 --> 140 raise e  
 141 run\_manager.on\_chain\_end(outputs)  
 142 return self.prep\_outputs(inputs, outputs, return\_only\_outputs)  
  
  
 File ~/workplace/langchain/langchain/chains/base.py:134, in Chain.\_\_call\_\_(self, inputs, return\_only\_outputs, callbacks)  
 128 run\_manager = callback\_manager.on\_chain\_start(  
 129 {"name": self.\_\_class\_\_.\_\_name\_\_},  
 130 inputs,  
 131 )  
 132 try:  
 133 outputs = (  
 --> 134 self.\_call(inputs, run\_manager=run\_manager)  
 135 if new\_arg\_supported  
 136 else self.\_call(inputs)  
 137 )  
 138 except (KeyboardInterrupt, Exception) as e:  
 139 run\_manager.on\_chain\_error(e)  
  
  
 File ~/workplace/langchain/langchain/agents/agent.py:947, in AgentExecutor.\_call(self, inputs, run\_manager)  
 945 # We now enter the agent loop (until it returns something).  
 946 while self.\_should\_continue(iterations, time\_elapsed):  
 --> 947 next\_step\_output = self.\_take\_next\_step(  
 948 name\_to\_tool\_map,  
 949 color\_mapping,  
 950 inputs,  
 951 intermediate\_steps,  
 952 run\_manager=run\_manager,  
 953 )  
 954 if isinstance(next\_step\_output, AgentFinish):  
 955 return self.\_return(  
 956 next\_step\_output, intermediate\_steps, run\_manager=run\_manager  
 957 )  
  
  
 File ~/workplace/langchain/langchain/agents/agent.py:773, in AgentExecutor.\_take\_next\_step(self, name\_to\_tool\_map, color\_mapping, inputs, intermediate\_steps, run\_manager)  
 771 raise\_error = False  
 772 if raise\_error:  
 --> 773 raise e  
 774 text = str(e)  
 775 if isinstance(self.handle\_parsing\_errors, bool):  
  
  
 File ~/workplace/langchain/langchain/agents/agent.py:762, in AgentExecutor.\_take\_next\_step(self, name\_to\_tool\_map, color\_mapping, inputs, intermediate\_steps, run\_manager)  
 756 """Take a single step in the thought-action-observation loop.  
 757   
 758 Override this to take control of how the agent makes and acts on choices.  
 759 """  
 760 try:  
 761 # Call the LLM to see what to do.  
 --> 762 output = self.agent.plan(  
 763 intermediate\_steps,  
 764 callbacks=run\_manager.get\_child() if run\_manager else None,  
 765 \*\*inputs,  
 766 )  
 767 except OutputParserException as e:  
 768 if isinstance(self.handle\_parsing\_errors, bool):  
  
  
 File ~/workplace/langchain/langchain/agents/agent.py:444, in Agent.plan(self, intermediate\_steps, callbacks, \*\*kwargs)  
 442 full\_inputs = self.get\_full\_inputs(intermediate\_steps, \*\*kwargs)  
 443 full\_output = self.llm\_chain.predict(callbacks=callbacks, \*\*full\_inputs)  
 --> 444 return self.output\_parser.parse(full\_output)  
  
  
 File ~/workplace/langchain/langchain/agents/chat/output\_parser.py:26, in ChatOutputParser.parse(self, text)  
 23 return AgentAction(response["action"], response["action\_input"], text)  
 25 except Exception:  
 ---> 26 raise OutputParserException(f"Could not parse LLM output: {text}")  
  
  
 OutputParserException: Could not parse LLM output: I'm sorry, but I cannot provide an answer without an Action. Please provide a valid Action in the format specified above.  

````

## Default error handling[​](#default-error-handling "Direct link to Default error handling")

Handle errors with `Invalid or incomplete response`:

```python
mrkl = initialize\_agent(  
 tools,  
 ChatOpenAI(temperature=0),  
 agent=AgentType.CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION,  
 verbose=True,  
 handle\_parsing\_errors=True,  
)  

```

```python
mrkl.run("Who is Leo DiCaprio's girlfriend? No need to add Action")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
   
 Observation: Invalid or incomplete response  
 Thought:  
 Observation: Invalid or incomplete response  
 Thought:Search for Leo DiCaprio's current girlfriend  
 Action:  
```

{\
"action": "Search",\
"action_input": "Leo DiCaprio current girlfriend"\
}

```
  
Observation: Just Jared on Instagram: “Leonardo DiCaprio & girlfriend Camila Morrone couple up for a lunch date!  
Thought:Camila Morrone is currently Leo DiCaprio's girlfriend  
Final Answer: Camila Morrone  
  
> Finished chain.  
 
 
 
 
 
'Camila Morrone'  

```

## Custom error message[​](#custom-error-message "Direct link to Custom error message")

You can easily customize the message to use when there are parsing errors.

```python
mrkl = initialize\_agent(  
 tools,  
 ChatOpenAI(temperature=0),  
 agent=AgentType.CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION,  
 verbose=True,  
 handle\_parsing\_errors="Check your output and make sure it conforms!",  
)  

```

```python
mrkl.run("Who is Leo DiCaprio's girlfriend? No need to add Action")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
   
 Observation: Could not parse LLM output: I'm sorry, but I canno  
 Thought:I need to use the Search tool to find the answer to the question.  
 Action:  
```

{\
"action": "Search",\
"action_input": "Who is Leo DiCaprio's girlfriend?"\
}

```
  
Observation: DiCaprio broke up with girlfriend Camila Morrone, 25, in the summer of 2022, after dating for four years. He's since been linked to another famous supermodel – Gigi Hadid. The power couple were first supposedly an item in September after being spotted getting cozy during a party at New York Fashion Week.  
Thought:The answer to the question is that Leo DiCaprio's current girlfriend is Gigi Hadid.   
Final Answer: Gigi Hadid.  
  
> Finished chain.  
 
 
 
 
 
'Gigi Hadid.'  

```

## Custom Error Function[​](#custom-error-function "Direct link to Custom Error Function")

You can also customize the error to be a function that takes the error in and outputs a string.

```python
def \_handle\_error(error) -> str:  
 return str(error)[:50]  
  
  
mrkl = initialize\_agent(  
 tools,  
 ChatOpenAI(temperature=0),  
 agent=AgentType.CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION,  
 verbose=True,  
 handle\_parsing\_errors=\_handle\_error,  
)  

```

```python
mrkl.run("Who is Leo DiCaprio's girlfriend? No need to add Action")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
   
 Observation: Could not parse LLM output: I'm sorry, but I canno  
 Thought:I need to use the Search tool to find the answer to the question.  
 Action:  
```

{\
"action": "Search",\
"action_input": "Who is Leo DiCaprio's girlfriend?"\
}

```
  
Observation: DiCaprio broke up with girlfriend Camila Morrone, 25, in the summer of 2022, after dating for four years. He's since been linked to another famous supermodel – Gigi Hadid. The power couple were first supposedly an item in September after being spotted getting cozy during a party at New York Fashion Week.  
Thought:The current girlfriend of Leonardo DiCaprio is Gigi Hadid.   
Final Answer: Gigi Hadid.  
  
> Finished chain.  
 
 
 
 
 
'Gigi Hadid.'  

```

- [Setup](#setup)
- [Error](#error)
- [Default error handling](#default-error-handling)
- [Custom error message](#custom-error-message)
- [Custom Error Function](#custom-error-function)
