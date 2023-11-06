# ReAct

This walkthrough showcases using an agent to implement the [ReAct](https://react-lm.github.io/) logic.

```python
from langchain.agents import load\_tools  
from langchain.agents import initialize\_agent  
from langchain.agents import AgentType  
from langchain.llms import OpenAI  

```

First, let's load the language model we're going to use to control the agent.

```python
llm = OpenAI(temperature=0)  

```

Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.

```python
tools = load\_tools(["serpapi", "llm-math"], llm=llm)  

```

## Using LCEL[​](#using-lcel "Direct link to Using LCEL")

We will first show how to create the agent using LCEL

```python
from langchain.tools.render import render\_text\_description  
from langchain.agents.output\_parsers import ReActSingleInputOutputParser  
from langchain.agents.format\_scratchpad import format\_log\_to\_str  
from langchain import hub  

```

```python
prompt = hub.pull("hwchase17/react")  
prompt = prompt.partial(  
 tools=render\_text\_description(tools),  
 tool\_names=", ".join([t.name for t in tools]),  
)  

```

```python
llm\_with\_stop = llm.bind(stop=["\nObservation"])  

```

```python
agent = {  
 "input": lambda x: x["input"],  
 "agent\_scratchpad": lambda x: format\_log\_to\_str(x['intermediate\_steps'])  
} | prompt | llm\_with\_stop | ReActSingleInputOutputParser()  

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

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find out who Leo DiCaprio's girlfriend is and then calculate her age raised to the 0.43 power.  
 Action: Search  
 Action Input: "Leo DiCaprio girlfriend"model Vittoria Ceretti I need to find out Vittoria Ceretti's age  
 Action: Search  
 Action Input: "Vittoria Ceretti age"25 years I need to calculate 25 raised to the 0.43 power  
 Action: Calculator  
 Action Input: 25^0.43Answer: 3.991298452658078 I now know the final answer  
 Final Answer: Leo DiCaprio's girlfriend is Vittoria Ceretti and her current age raised to the 0.43 power is 3.991298452658078.  
   
 > Finished chain.  
  
  
  
  
  
 {'input': "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?",  
 'output': "Leo DiCaprio's girlfriend is Vittoria Ceretti and her current age raised to the 0.43 power is 3.991298452658078."}  

```

## Using ZeroShotReactAgent[​](#using-zeroshotreactagent "Direct link to Using ZeroShotReactAgent")

We will now show how to use the agent with an off-the-shelf agent implementation

```python
agent\_executor = initialize\_agent(tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True)  

```

```python
agent\_executor.invoke({"input": "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"})  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find out who Leo DiCaprio's girlfriend is and then calculate her age raised to the 0.43 power.  
 Action: Search  
 Action Input: "Leo DiCaprio girlfriend"  
 Observation: model Vittoria Ceretti  
 Thought: I need to find out Vittoria Ceretti's age  
 Action: Search  
 Action Input: "Vittoria Ceretti age"  
 Observation: 25 years  
 Thought: I need to calculate 25 raised to the 0.43 power  
 Action: Calculator  
 Action Input: 25^0.43  
 Observation: Answer: 3.991298452658078  
 Thought: I now know the final answer  
 Final Answer: Leo DiCaprio's girlfriend is Vittoria Ceretti and her current age raised to the 0.43 power is 3.991298452658078.  
   
 > Finished chain.  
  
  
  
  
  
 {'input': "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?",  
 'output': "Leo DiCaprio's girlfriend is Vittoria Ceretti and her current age raised to the 0.43 power is 3.991298452658078."}  

```

## Using chat models[​](#using-chat-models "Direct link to Using chat models")

You can also create ReAct agents that use chat models instead of LLMs as the agent driver.

The main difference here is a different prompt. We will use JSON to encode the agent's actions (chat models are a bit tougher to steet, so using JSON helps to enforce the output format).

```python
from langchain.chat\_models import ChatOpenAI  

```

```python
chat\_model = ChatOpenAI(temperature=0)  

```

```python
prompt = hub.pull("hwchase17/react-json")  
prompt = prompt.partial(  
 tools=render\_text\_description(tools),  
 tool\_names=", ".join([t.name for t in tools]),  
)  

```

```python
chat\_model\_with\_stop = chat\_model.bind(stop=["\nObservation"])  

```

```python
from langchain.agents.output\_parsers import ReActJsonSingleInputOutputParser  

```

```python
agent = {  
 "input": lambda x: x["input"],  
 "agent\_scratchpad": lambda x: format\_log\_to\_str(x['intermediate\_steps'])  
} | prompt | chat\_model\_with\_stop | ReActJsonSingleInputOutputParser()  

```

```python
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  

```

```python
agent\_executor.invoke({"input": "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"})  

```

We can also use an off-the-shelf agent class

```python
agent = initialize\_agent(tools, chat\_model, agent=AgentType.CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True)  
agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")  

```

- [Using LCEL](#using-lcel)
- [Using ZeroShotReactAgent](#using-zeroshotreactagent)
- [Using chat models](#using-chat-models)
