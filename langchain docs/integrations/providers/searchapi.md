# SearchApi

This page covers how to use the [SearchApi](https://www.searchapi.io/) Google Search API within LangChain. SearchApi is a real-time SERP API for easy SERP scraping.

## Setup[​](#setup "Direct link to Setup")

- Go to <https://www.searchapi.io/> to sign up for a free account
- Get the api key and set it as an environment variable (`SEARCHAPI_API_KEY`)

## Wrappers[​](#wrappers "Direct link to Wrappers")

### Utility[​](#utility "Direct link to Utility")

There is a SearchApiAPIWrapper utility which wraps this API. To import this utility:

```python
from langchain.utilities import SearchApiAPIWrapper  

```

You can use it as part of a Self Ask chain:

```python
from langchain.utilities import SearchApiAPIWrapper  
from langchain.llms.openai import OpenAI  
from langchain.agents import initialize\_agent, Tool  
from langchain.agents import AgentType  
  
import os  
  
os.environ["SEARCHAPI\_API\_KEY"] = ""  
os.environ['OPENAI\_API\_KEY'] = ""  
  
llm = OpenAI(temperature=0)  
search = SearchApiAPIWrapper()  
tools = [  
 Tool(  
 name="Intermediate Answer",  
 func=search.run,  
 description="useful for when you need to ask with search"  
 )  
]  
  
self\_ask\_with\_search = initialize\_agent(tools, llm, agent=AgentType.SELF\_ASK\_WITH\_SEARCH, verbose=True)  
self\_ask\_with\_search.run("Who lived longer: Plato, Socrates, or Aristotle?")  

```

#### Output[​](#output "Direct link to Output")

```text
> Entering new AgentExecutor chain...  
 Yes.  
Follow up: How old was Plato when he died?  
Intermediate answer: eighty  
Follow up: How old was Socrates when he died?  
Intermediate answer: | Socrates |   
| -------- |   
| Born | c. 470 BC Deme Alopece, Athens |   
| Died | 399 BC (aged approximately 71) Athens |   
| Cause of death | Execution by forced suicide by poisoning |   
| Spouse(s) | Xanthippe, Myrto |   
  
Follow up: How old was Aristotle when he died?  
Intermediate answer: 62 years  
So the final answer is: Plato  
  
> Finished chain.  
'Plato'  

```

### Tool[​](#tool "Direct link to Tool")

You can also easily load this wrapper as a Tool (to use with an Agent).
You can do this with:

```python
from langchain.agents import load\_tools  
tools = load\_tools(["searchapi"])  

```

For more information on tools, see [this page](/docs/modules/agents/tools/).

- [Setup](#setup)

- [Wrappers](#wrappers)

  - [Utility](#utility)
  - [Tool](#tool)

- [Utility](#utility)

- [Tool](#tool)
