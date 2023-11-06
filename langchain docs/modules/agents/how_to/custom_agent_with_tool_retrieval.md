# Custom agent with tool retrieval

This notebook builds off of [this notebook](/docs/modules/agents/how_to/custom_llm_agent.html) and assumes familiarity with how agents work.

The novel idea introduced in this notebook is the idea of using retrieval to select the set of tools to use to answer an agent query. This is useful when you have many many tools to select from. You cannot put the description of all the tools in the prompt (because of context length issues) so instead you dynamically select the N tools you do want to consider using at run time.

In this notebook we will create a somewhat contrived example. We will have one legitimate tool (search) and then 99 fake tools which are just nonsense. We will then add a step in the prompt template that takes the user input and retrieves tool relevant to the query.

## Set up environment[​](#set-up-environment "Direct link to Set up environment")

Do necessary imports, etc.

```python
from langchain.agents import (  
 Tool,  
 AgentExecutor,  
 LLMSingleActionAgent,  
 AgentOutputParser,  
)  
from langchain.prompts import StringPromptTemplate  
from langchain.llms import OpenAI  
from langchain.utilities import SerpAPIWrapper  
from langchain.chains import LLMChain  
from typing import List, Union  
from langchain.schema import AgentAction, AgentFinish  
import re  

```

## Set up tools[​](#set-up-tools "Direct link to Set up tools")

We will create one legitimate tool (search) and then 99 fake tools.

```python
# Define which tools the agent can use to answer user queries  
search = SerpAPIWrapper()  
search\_tool = Tool(  
 name="Search",  
 func=search.run,  
 description="useful for when you need to answer questions about current events",  
)  
  
  
def fake\_func(inp: str) -> str:  
 return "foo"  
  
  
fake\_tools = [  
 Tool(  
 name=f"foo-{i}",  
 func=fake\_func,  
 description=f"a silly function that you can use to get more information about the number {i}",  
 )  
 for i in range(99)  
]  
ALL\_TOOLS = [search\_tool] + fake\_tools  

```

## Tool Retriever[​](#tool-retriever "Direct link to Tool Retriever")

We will use a vector store to create embeddings for each tool description. Then, for an incoming query we can create embeddings for that query and do a similarity search for relevant tools.

```python
from langchain.vectorstores import FAISS  
from langchain.embeddings import OpenAIEmbeddings  
from langchain.schema import Document  

```

```python
docs = [  
 Document(page\_content=t.description, metadata={"index": i})  
 for i, t in enumerate(ALL\_TOOLS)  
]  

```

```python
vector\_store = FAISS.from\_documents(docs, OpenAIEmbeddings())  

```

```python
retriever = vector\_store.as\_retriever()  
  
  
def get\_tools(query):  
 docs = retriever.get\_relevant\_documents(query)  
 return [ALL\_TOOLS[d.metadata["index"]] for d in docs]  

```

We can now test this retriever to see if it seems to work.

```python
get\_tools("whats the weather?")  

```

```text
 [Tool(name='Search', description='useful for when you need to answer questions about current events', return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x114b28a90>, func=<bound method SerpAPIWrapper.run of SerpAPIWrapper(search\_engine=<class 'serpapi.google\_search.GoogleSearch'>, params={'engine': 'google', 'google\_domain': 'google.com', 'gl': 'us', 'hl': 'en'}, serpapi\_api\_key='', aiosession=None)>, coroutine=None),  
 Tool(name='foo-95', description='a silly function that you can use to get more information about the number 95', return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x114b28a90>, func=<function fake\_func at 0x15e5bd1f0>, coroutine=None),  
 Tool(name='foo-12', description='a silly function that you can use to get more information about the number 12', return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x114b28a90>, func=<function fake\_func at 0x15e5bd1f0>, coroutine=None),  
 Tool(name='foo-15', description='a silly function that you can use to get more information about the number 15', return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x114b28a90>, func=<function fake\_func at 0x15e5bd1f0>, coroutine=None)]  

```

```python
get\_tools("whats the number 13?")  

```

```text
 [Tool(name='foo-13', description='a silly function that you can use to get more information about the number 13', return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x114b28a90>, func=<function fake\_func at 0x15e5bd1f0>, coroutine=None),  
 Tool(name='foo-12', description='a silly function that you can use to get more information about the number 12', return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x114b28a90>, func=<function fake\_func at 0x15e5bd1f0>, coroutine=None),  
 Tool(name='foo-14', description='a silly function that you can use to get more information about the number 14', return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x114b28a90>, func=<function fake\_func at 0x15e5bd1f0>, coroutine=None),  
 Tool(name='foo-11', description='a silly function that you can use to get more information about the number 11', return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x114b28a90>, func=<function fake\_func at 0x15e5bd1f0>, coroutine=None)]  

```

## Prompt template[​](#prompt-template "Direct link to Prompt template")

The prompt template is pretty standard, because we're not actually changing that much logic in the actual prompt template, but rather we are just changing how retrieval is done.

```python
# Set up the base template  
template = """Answer the following questions as best you can, but speaking as a pirate might speak. You have access to the following tools:  
  
{tools}  
  
Use the following format:  
  
Question: the input question you must answer  
Thought: you should always think about what to do  
Action: the action to take, should be one of [{tool\_names}]  
Action Input: the input to the action  
Observation: the result of the action  
... (this Thought/Action/Action Input/Observation can repeat N times)  
Thought: I now know the final answer  
Final Answer: the final answer to the original input question  
  
Begin! Remember to speak as a pirate when giving your final answer. Use lots of "Arg"s  
  
Question: {input}  
{agent\_scratchpad}"""  

```

The custom prompt template now has the concept of a `tools_getter`, which we call on the input to select the tools to use.

```python
from typing import Callable  
  
  
# Set up a prompt template  
class CustomPromptTemplate(StringPromptTemplate):  
 # The template to use  
 template: str  
 ############## NEW ######################  
 # The list of tools available  
 tools\_getter: Callable  
  
 def format(self, \*\*kwargs) -> str:  
 # Get the intermediate steps (AgentAction, Observation tuples)  
 # Format them in a particular way  
 intermediate\_steps = kwargs.pop("intermediate\_steps")  
 thoughts = ""  
 for action, observation in intermediate\_steps:  
 thoughts += action.log  
 thoughts += f"\nObservation: {observation}\nThought: "  
 # Set the agent\_scratchpad variable to that value  
 kwargs["agent\_scratchpad"] = thoughts  
 ############## NEW ######################  
 tools = self.tools\_getter(kwargs["input"])  
 # Create a tools variable from the list of tools provided  
 kwargs["tools"] = "\n".join(  
 [f"{tool.name}: {tool.description}" for tool in tools]  
 )  
 # Create a list of tool names for the tools provided  
 kwargs["tool\_names"] = ", ".join([tool.name for tool in tools])  
 return self.template.format(\*\*kwargs)  

```

```python
prompt = CustomPromptTemplate(  
 template=template,  
 tools\_getter=get\_tools,  
 # This omits the `agent\_scratchpad`, `tools`, and `tool\_names` variables because those are generated dynamically  
 # This includes the `intermediate\_steps` variable because that is needed  
 input\_variables=["input", "intermediate\_steps"],  
)  

```

## Output parser[​](#output-parser "Direct link to Output parser")

The output parser is unchanged from the previous notebook, since we are not changing anything about the output format.

```python
class CustomOutputParser(AgentOutputParser):  
 def parse(self, llm\_output: str) -> Union[AgentAction, AgentFinish]:  
 # Check if agent should finish  
 if "Final Answer:" in llm\_output:  
 return AgentFinish(  
 # Return values is generally always a dictionary with a single `output` key  
 # It is not recommended to try anything else at the moment :)  
 return\_values={"output": llm\_output.split("Final Answer:")[-1].strip()},  
 log=llm\_output,  
 )  
 # Parse out the action and action input  
 regex = r"Action\s\*\d\*\s\*:(.\*?)\nAction\s\*\d\*\s\*Input\s\*\d\*\s\*:[\s]\*(.\*)"  
 match = re.search(regex, llm\_output, re.DOTALL)  
 if not match:  
 raise ValueError(f"Could not parse LLM output: `{llm\_output}`")  
 action = match.group(1).strip()  
 action\_input = match.group(2)  
 # Return the action and action input  
 return AgentAction(  
 tool=action, tool\_input=action\_input.strip(" ").strip('"'), log=llm\_output  
 )  

```

```python
output\_parser = CustomOutputParser()  

```

## Set up LLM, stop sequence, and the agent[​](#set-up-llm-stop-sequence-and-the-agent "Direct link to Set up LLM, stop sequence, and the agent")

Also the same as the previous notebook.

```python
llm = OpenAI(temperature=0)  

```

```python
# LLM chain consisting of the LLM and a prompt  
llm\_chain = LLMChain(llm=llm, prompt=prompt)  

```

```python
tools = get\_tools("whats the weather?")  
tool\_names = [tool.name for tool in tools]  
agent = LLMSingleActionAgent(  
 llm\_chain=llm\_chain,  
 output\_parser=output\_parser,  
 stop=["\nObservation:"],  
 allowed\_tools=tool\_names,  
)  

```

## Use the Agent[​](#use-the-agent "Direct link to Use the Agent")

Now we can use it!

```python
agent\_executor = AgentExecutor.from\_agent\_and\_tools(  
 agent=agent, tools=tools, verbose=True  
)  

```

```python
agent\_executor.run("What's the weather in SF?")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Thought: I need to find out what the weather is in SF  
 Action: Search  
 Action Input: Weather in SF  
   
 Observation:Mostly cloudy skies early, then partly cloudy in the afternoon. High near 60F. ENE winds shifting to W at 10 to 15 mph. Humidity71%. UV Index6 of 10. I now know the final answer  
 Final Answer: 'Arg, 'tis mostly cloudy skies early, then partly cloudy in the afternoon. High near 60F. ENE winds shiftin' to W at 10 to 15 mph. Humidity71%. UV Index6 of 10.  
   
 > Finished chain.  
  
  
  
  
  
 "'Arg, 'tis mostly cloudy skies early, then partly cloudy in the afternoon. High near 60F. ENE winds shiftin' to W at 10 to 15 mph. Humidity71%. UV Index6 of 10."  

```

- [Set up environment](#set-up-environment)
- [Set up tools](#set-up-tools)
- [Tool Retriever](#tool-retriever)
- [Prompt template](#prompt-template)
- [Output parser](#output-parser)
- [Set up LLM, stop sequence, and the agent](#set-up-llm-stop-sequence-and-the-agent)
- [Use the Agent](#use-the-agent)
