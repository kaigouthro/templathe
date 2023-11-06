# Custom multi-action agent

This notebook goes through how to create your own custom agent.

An agent consists of two parts:

- Tools: The tools the agent has available to use.
- The agent class itself: this decides which action to take.

In this notebook we walk through how to create a custom agent that predicts/takes multiple steps at a time.

```python
from langchain.agents import Tool, AgentExecutor, BaseMultiActionAgent  
from langchain.llms import OpenAI  
from langchain.utilities import SerpAPIWrapper  

```

```python
def random\_word(query: str) -> str:  
 print("\nNow I'm doing this!")  
 return "foo"  

```

```python
search = SerpAPIWrapper()  
tools = [  
 Tool(  
 name="Search",  
 func=search.run,  
 description="useful for when you need to answer questions about current events",  
 ),  
 Tool(  
 name="RandomWord",  
 func=random\_word,  
 description="call this to get a random word.",  
 ),  
]  

```

```python
from typing import List, Tuple, Any, Union  
from langchain.schema import AgentAction, AgentFinish  
  
  
class FakeAgent(BaseMultiActionAgent):  
 """Fake Custom Agent."""  
  
 @property  
 def input\_keys(self):  
 return ["input"]  
  
 def plan(  
 self, intermediate\_steps: List[Tuple[AgentAction, str]], \*\*kwargs: Any  
 ) -> Union[List[AgentAction], AgentFinish]:  
 """Given input, decided what to do.  
  
 Args:  
 intermediate\_steps: Steps the LLM has taken to date,  
 along with observations  
 \*\*kwargs: User inputs.  
  
 Returns:  
 Action specifying what tool to use.  
 """  
 if len(intermediate\_steps) == 0:  
 return [  
 AgentAction(tool="Search", tool\_input=kwargs["input"], log=""),  
 AgentAction(tool="RandomWord", tool\_input=kwargs["input"], log=""),  
 ]  
 else:  
 return AgentFinish(return\_values={"output": "bar"}, log="")  
  
 async def aplan(  
 self, intermediate\_steps: List[Tuple[AgentAction, str]], \*\*kwargs: Any  
 ) -> Union[List[AgentAction], AgentFinish]:  
 """Given input, decided what to do.  
  
 Args:  
 intermediate\_steps: Steps the LLM has taken to date,  
 along with observations  
 \*\*kwargs: User inputs.  
  
 Returns:  
 Action specifying what tool to use.  
 """  
 if len(intermediate\_steps) == 0:  
 return [  
 AgentAction(tool="Search", tool\_input=kwargs["input"], log=""),  
 AgentAction(tool="RandomWord", tool\_input=kwargs["input"], log=""),  
 ]  
 else:  
 return AgentFinish(return\_values={"output": "bar"}, log="")  

```

```python
agent = FakeAgent()  

```

```python
agent\_executor = AgentExecutor.from\_agent\_and\_tools(  
 agent=agent, tools=tools, verbose=True  
)  

```

```python
agent\_executor.run("How many people live in canada as of 2023?")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 The current population of Canada is 38,669,152 as of Monday, April 24, 2023, based on Worldometer elaboration of the latest United Nations data.  
 Now I'm doing this!  
 foo  
   
 > Finished chain.  
  
  
  
  
  
 'bar'  

```
