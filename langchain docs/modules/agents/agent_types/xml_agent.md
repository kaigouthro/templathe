# XML Agent

Some language models (like Anthropic's Claude) are particularly good at reasoning/writing XML. This goes over how to use an agent that uses XML when prompting.

## Initialize the tools[​](#initialize-the-tools "Direct link to Initialize the tools")

We will initialize some fake tools for demo purposes

```python
from langchain.agents import tool  
  
@tool  
def search(query: str) -> str:  
 """Search things about current events."""  
 return "32 degrees"  

```

```python
tools = [search]  

```

```python
from langchain.chat\_models import ChatAnthropic  
model = ChatAnthropic(model="claude-2")  

```

## Use LangChain Expression Language[​](#use-langchain-expression-language "Direct link to Use LangChain Expression Language")

We will first show how to create this agent using LangChain Expression Language

```python
from langchain.tools.render import render\_text\_description  
from langchain.agents.output\_parsers import XMLAgentOutputParser  
from langchain.agents.format\_scratchpad import format\_xml  
from langchain import hub  

```

```python
prompt = hub.pull("hwchase17/xml-agent")  

```

```python
prompt = prompt.partial(  
 tools=render\_text\_description(tools),  
 tool\_names=", ".join([t.name for t in tools]),  
)  

```

```python
llm\_with\_stop = model.bind(stop=["</tool\_input>"])  

```

```python
agent = {  
 "question": lambda x: x["question"],  
 "agent\_scratchpad": lambda x: format\_xml(x['intermediate\_steps']),  
} | prompt | llm\_with\_stop | XMLAgentOutputParser()  

```

```python
from langchain.agents import AgentExecutor  

```

```python
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  

```

```python
agent\_executor.invoke({"question": "whats the weather in New york?"})  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 <tool>search</tool>  
 <tool\_input>weather in new york32 degrees <tool>search</tool>  
 <tool\_input>weather in new york32 degrees <final\_answer>  
 The weather in New York is 32 degrees.  
 </final\_answer>  
   
 > Finished chain.  
  
  
  
  
  
 {'question': 'whats the weather in New york?',  
 'output': '\nThe weather in New York is 32 degrees.\n'}  

```

## Use off-the-shelf agent[​](#use-off-the-shelf-agent "Direct link to Use off-the-shelf agent")

```python
from langchain.chains import LLMChain  
from langchain.agents import XMLAgent  

```

```python
chain = LLMChain(  
 llm=model,  
 prompt=XMLAgent.get\_default\_prompt(),  
 output\_parser=XMLAgent.get\_default\_output\_parser()  
)  
agent = XMLAgent(tools=tools, llm\_chain=chain)  

```

```python
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  

```

```python
agent\_executor.invoke({"input": "whats the weather in New york?"})  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 <tool>search</tool>  
 <tool\_input>weather in new york32 degrees  
   
 <final\_answer>The weather in New York is 32 degrees  
   
 > Finished chain.  
  
  
  
  
  
 {'input': 'whats the weather in New york?',  
 'output': 'The weather in New York is 32 degrees'}  

```

- [Initialize the tools](#initialize-the-tools)
- [Use LangChain Expression Language](#use-langchain-expression-language)
- [Use off-the-shelf agent](#use-off-the-shelf-agent)
