# Agents

You can pass a Runnable into an agent.

```python
from langchain.agents import XMLAgent, tool, AgentExecutor  
from langchain.chat\_models import ChatAnthropic  

```

```python
model = ChatAnthropic(model="claude-2")  

```

```python
@tool  
def search(query: str) -> str:  
 """Search things about current events."""  
 return "32 degrees"  

```

```python
tool\_list = [search]  

```

```python
# Get prompt to use  
prompt = XMLAgent.get\_default\_prompt()  

```

```python
# Logic for going from intermediate steps to a string to pass into model  
# This is pretty tied to the prompt  
def convert\_intermediate\_steps(intermediate\_steps):  
 log = ""  
 for action, observation in intermediate\_steps:  
 log += (  
 f"<tool>{action.tool}</tool><tool\_input>{action.tool\_input}"  
 f"</tool\_input><observation>{observation}</observation>"  
 )  
 return log  
  
  
# Logic for converting tools to string to go in prompt  
def convert\_tools(tools):  
 return "\n".join([f"{tool.name}: {tool.description}" for tool in tools])  

```

Building an agent from a runnable usually involves a few things:

1. Data processing for the intermediate steps. These need to represented in a way that the language model can recognize them. This should be pretty tightly coupled to the instructions in the prompt
1. The prompt itself
1. The model, complete with stop tokens if needed
1. The output parser - should be in sync with how the prompt specifies things to be formatted.

Data processing for the intermediate steps. These need to represented in a way that the language model can recognize them. This should be pretty tightly coupled to the instructions in the prompt

The prompt itself

The model, complete with stop tokens if needed

The output parser - should be in sync with how the prompt specifies things to be formatted.

```python
agent = (  
 {  
 "question": lambda x: x["question"],  
 "intermediate\_steps": lambda x: convert\_intermediate\_steps(x["intermediate\_steps"])  
 }  
 | prompt.partial(tools=convert\_tools(tool\_list))  
 | model.bind(stop=["</tool\_input>", "</final\_answer>"])  
 | XMLAgent.get\_default\_output\_parser()  
)  

```

```python
agent\_executor = AgentExecutor(agent=agent, tools=tool\_list, verbose=True)  

```

```python
agent\_executor.invoke({"question": "whats the weather in New york?"})  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 <tool>search</tool>  
 <tool\_input>weather in new york32 degrees  
   
 <final\_answer>The weather in New York is 32 degrees  
   
 > Finished chain.  
  
  
  
  
  
 {'question': 'whats the weather in New york?',  
 'output': 'The weather in New York is 32 degrees'}  

```
