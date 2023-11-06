# Conversational

This walkthrough demonstrates how to use an agent optimized for conversation. Other agents are often optimized for using tools to figure out the best response, which is not ideal in a conversational setting where you may want the agent to be able to chat with the user as well.

If we compare it to the standard ReAct agent, the main difference is the prompt.
We want it to be much more conversational.

```python
from langchain.agents import Tool  
from langchain.agents import AgentType  
from langchain.memory import ConversationBufferMemory  
from langchain.llms import OpenAI  
from langchain.utilities import SerpAPIWrapper  
from langchain.agents import initialize\_agent  

```

```python
search = SerpAPIWrapper()  
tools = [  
 Tool(  
 name="Current Search",  
 func=search.run,  
 description="useful for when you need to answer questions about current events or the current state of the world"  
 ),  
]  

```

```python
llm=OpenAI(temperature=0)  

```

## Using LCEL[​](#using-lcel "Direct link to Using LCEL")

We will first show how to create this agent using LCEL

```python
from langchain.tools.render import render\_text\_description  
from langchain.agents.output\_parsers import ReActSingleInputOutputParser  
from langchain.agents.format\_scratchpad import format\_log\_to\_str  
from langchain import hub  

```

```python
prompt = hub.pull("hwchase17/react-chat")  

```

```python
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
 "agent\_scratchpad": lambda x: format\_log\_to\_str(x['intermediate\_steps']),  
 "chat\_history": lambda x: x["chat\_history"]  
} | prompt | llm\_with\_stop | ReActSingleInputOutputParser()  

```

```python
from langchain.agents import AgentExecutor  

```

```python
memory = ConversationBufferMemory(memory\_key="chat\_history")  
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)  

```

```python
agent\_executor.invoke({"input": "hi, i am bob"})['output']  

```

```text
   
   
 > Entering new AgentExecutor chain...  
   
 Thought: Do I need to use a tool? No  
 Final Answer: Hi Bob, nice to meet you! How can I help you today?  
   
 > Finished chain.  
  
  
  
  
  
 'Hi Bob, nice to meet you! How can I help you today?'  

```

```python
agent\_executor.invoke({"input": "whats my name?"})['output']  

```

```text
   
   
 > Entering new AgentExecutor chain...  
   
 Thought: Do I need to use a tool? No  
 Final Answer: Your name is Bob.  
   
 > Finished chain.  
  
  
  
  
  
 'Your name is Bob.'  

```

```python
agent\_executor.invoke({"input": "what are some movies showing 9/21/2023?"})['output']  

```

```text
   
   
 > Entering new AgentExecutor chain...  
   
 Thought: Do I need to use a tool? Yes  
 Action: Current Search  
 Action Input: Movies showing 9/21/2023['September 2023 Movies: The Creator • Dumb Money • Expend4bles • The Kill Room • The Inventor • The Equalizer 3 • PAW Patrol: The Mighty Movie, ...'] Do I need to use a tool? No  
 Final Answer: According to current search, some movies showing on 9/21/2023 are The Creator, Dumb Money, Expend4bles, The Kill Room, The Inventor, The Equalizer 3, and PAW Patrol: The Mighty Movie.  
   
 > Finished chain.  
  
  
  
  
  
 'According to current search, some movies showing on 9/21/2023 are The Creator, Dumb Money, Expend4bles, The Kill Room, The Inventor, The Equalizer 3, and PAW Patrol: The Mighty Movie.'  

```

## Use the off-the-shelf agent[​](#use-the-off-the-shelf-agent "Direct link to Use the off-the-shelf agent")

We can also create this agent using the off-the-shelf agent class

```python
agent\_executor = initialize\_agent(tools, llm, agent=AgentType.CONVERSATIONAL\_REACT\_DESCRIPTION, verbose=True, memory=memory)  

```

## Use a chat model[​](#use-a-chat-model "Direct link to Use a chat model")

We can also use a chat model here. The main difference here is in the prompts used.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain import hub  

```

```python
prompt = hub.pull("hwchase17/react-chat-json")  
chat\_model = ChatOpenAI(temperature=0, model='gpt-4')  

```

```python
prompt = prompt.partial(  
 tools=render\_text\_description(tools),  
 tool\_names=", ".join([t.name for t in tools]),  
)  

```

```python
chat\_model\_with\_stop = chat\_model.bind(stop=["\nObservation"])  

```

```python
from langchain.agents.output\_parsers import JSONAgentOutputParser  
from langchain.agents.format\_scratchpad import format\_log\_to\_messages  

```

```python
# We need some extra steering, or the chat model forgets how to respond sometimes  
TEMPLATE\_TOOL\_RESPONSE = """TOOL RESPONSE:   
---------------------  
{observation}  
  
USER'S INPUT  
--------------------  
  
Okay, so what is the response to my last comment? If using information obtained from the tools you must mention it explicitly without mentioning the tool names - I have forgotten all TOOL RESPONSES! Remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else - even if you just want to respond to the user. Do NOT respond with anything except a JSON snippet no matter what!"""  
  
agent = {  
 "input": lambda x: x["input"],  
 "agent\_scratchpad": lambda x: format\_log\_to\_messages(x['intermediate\_steps'], template\_tool\_response=TEMPLATE\_TOOL\_RESPONSE),  
 "chat\_history": lambda x: x["chat\_history"],  
} | prompt | chat\_model\_with\_stop | JSONAgentOutputParser()  

```

```python
from langchain.agents import AgentExecutor  

```

```python
memory = ConversationBufferMemory(memory\_key="chat\_history", return\_messages=True)  
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)  

```

```python
agent\_executor.invoke({"input": "hi, i am bob"})['output']  

```

````text
   
   
 > Entering new AgentExecutor chain...  
 ```json  
 {  
 "action": "Final Answer",  
 "action\_input": "Hello Bob, how can I assist you today?"  
 }  
````

> Finished chain.

'Hello Bob, how can I assist you today?'

````



```python
agent\_executor.invoke({"input": "whats my name?"})['output']  

````

````text
   
   
 > Entering new AgentExecutor chain...  
 ```json  
 {  
 "action": "Final Answer",  
 "action\_input": "Your name is Bob."  
 }  
````

> Finished chain.

'Your name is Bob.'

````



```python
agent\_executor.invoke({"input": "what are some movies showing 9/21/2023?"})['output']  

````

````text
   
   
 > Entering new AgentExecutor chain...  
 ```json  
 {  
 "action": "Current Search",  
 "action\_input": "movies showing on 9/21/2023"  
 }  
 ```['September 2023 Movies: The Creator • Dumb Money • Expend4bles • The Kill Room • The Inventor • The Equalizer 3 • PAW Patrol: The Mighty Movie, ...']```json  
 {  
 "action": "Final Answer",  
 "action\_input": "Some movies that are showing on 9/21/2023 include 'The Creator', 'Dumb Money', 'Expend4bles', 'The Kill Room', 'The Inventor', 'The Equalizer 3', and 'PAW Patrol: The Mighty Movie'."  
 }  
````

> Finished chain.

"Some movies that are showing on 9/21/2023 include 'The Creator', 'Dumb Money', 'Expend4bles', 'The Kill Room', 'The Inventor', 'The Equalizer 3', and 'PAW Patrol: The Mighty Movie'."

````


We can also initialize the agent executor with a predefined agent type




```python
from langchain.memory import ConversationBufferMemory  
from langchain.chat\_models import ChatOpenAI  

````

```python
memory = ConversationBufferMemory(memory\_key="chat\_history", return\_messages=True)  
llm = ChatOpenAI(openai\_api\_key=OPENAI\_API\_KEY, temperature=0)  
agent\_chain = initialize\_agent(tools, llm, agent=AgentType.CHAT\_CONVERSATIONAL\_REACT\_DESCRIPTION, verbose=True, memory=memory)  

```

- [Using LCEL](#using-lcel)
- [Use the off-the-shelf agent](#use-the-off-the-shelf-agent)
- [Use a chat model](#use-a-chat-model)
