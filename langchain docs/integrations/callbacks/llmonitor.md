# LLMonitor

[LLMonitor](https://llmonitor.com?utm_source=langchain&utm_medium=py&utm_campaign=docs) is an open-source observability platform that provides cost and usage analytics, user tracking, tracing and evaluation tools.

## Setup[​](#setup "Direct link to Setup")

Create an account on [llmonitor.com](https://llmonitor.com?utm_source=langchain&utm_medium=py&utm_campaign=docs), then copy your new app's `tracking id`.

Once you have it, set it as an environment variable by running:

```bash
export LLMONITOR\_APP\_ID="..."  

```

If you'd prefer not to set an environment variable, you can pass the key directly when initializing the callback handler:

```python
from langchain.callbacks import LLMonitorCallbackHandler  
  
handler = LLMonitorCallbackHandler(app\_id="...")  

```

## Usage with LLM/Chat models[​](#usage-with-llmchat-models "Direct link to Usage with LLM/Chat models")

```python
from langchain.llms import OpenAI  
from langchain.chat\_models import ChatOpenAI  
from langchain.callbacks import LLMonitorCallbackHandler  
  
handler = LLMonitorCallbackHandler()  
  
llm = OpenAI(  
 callbacks=[handler],  
)  
  
chat = ChatOpenAI(callbacks=[handler])  
  
llm("Tell me a joke")  
  

```

## Usage with chains and agents[​](#usage-with-chains-and-agents "Direct link to Usage with chains and agents")

Make sure to pass the callback handler to the `run` method so that all related chains and llm calls are correctly tracked.

It is also recommended to pass `agent_name` in the metadata to be able to distinguish between agents in the dashboard.

Example:

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.schema import SystemMessage, HumanMessage  
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor, tool  
from langchain.callbacks import LLMonitorCallbackHandler  
  
llm = ChatOpenAI(temperature=0)  
  
handler = LLMonitorCallbackHandler()  
  
@tool  
def get\_word\_length(word: str) -> int:  
 """Returns the length of a word."""  
 return len(word)  
  
tools = [get\_word\_length]  
  
prompt = OpenAIFunctionsAgent.create\_prompt(  
 system\_message=SystemMessage(  
 content="You are very powerful assistant, but bad at calculating lengths of words."  
 )  
)  
  
agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt, verbose=True)  
agent\_executor = AgentExecutor(  
 agent=agent, tools=tools, verbose=True, metadata={"agent\_name": "WordCount"} # <- recommended, assign a custom name  
)  
agent\_executor.run("how many letters in the word educa?", callbacks=[handler])  

```

Another example:

```python
from langchain.agents import load\_tools, initialize\_agent, AgentType  
from langchain.llms import OpenAI  
from langchain.callbacks import LLMonitorCallbackHandler  
  
handler = LLMonitorCallbackHandler()  
  
llm = OpenAI(temperature=0)  
tools = load\_tools(["serpapi", "llm-math"], llm=llm)  
agent = initialize\_agent(tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, metadata={ "agent\_name": "GirlfriendAgeFinder" }) # <- recommended, assign a custom name  
  
agent.run(  
 "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?",  
 callbacks=[handler],  
)  

```

## User Tracking[​](#user-tracking "Direct link to User Tracking")

User tracking allows you to identify your users, track their cost, conversations and more.

```python
from langchain.callbacks.llmonitor\_callback import LLMonitorCallbackHandler, identify  
  
with identify("user-123"):  
 llm("Tell me a joke")  
  
with identify("user-456", user\_props={"email": "user456@test.com"}):  
 agen.run("Who is Leo DiCaprio's girlfriend?")  

```

## Support[​](#support "Direct link to Support")

For any question or issue with integration you can reach out to the LLMonitor team on [Discord](http://discord.com/invite/8PafSG58kK) or via [email](mailto:vince@llmonitor.com).

- [Setup](#setup)
- [Usage with LLM/Chat models](#usage-with-llmchat-models)
- [Usage with chains and agents](#usage-with-chains-and-agents)
- [User Tracking](#user-tracking)
- [Support](#support)
