# Serper - Google Search API

This page covers how to use the [Serper](https://serper.dev) Google Search API within LangChain. Serper is a low-cost Google Search API that can be used to add answer box, knowledge graph, and organic results data from Google Search.
It is broken into two parts: setup, and then references to the specific Google Serper wrapper.

## Setup[​](#setup "Direct link to Setup")

- Go to [serper.dev](https://serper.dev) to sign up for a free account
- Get the api key and set it as an environment variable (`SERPER_API_KEY`)

## Wrappers[​](#wrappers "Direct link to Wrappers")

### Utility[​](#utility "Direct link to Utility")

There exists a GoogleSerperAPIWrapper utility which wraps this API. To import this utility:

```python
from langchain.utilities import GoogleSerperAPIWrapper  

```

You can use it as part of a Self Ask chain:

```python
from langchain.utilities import GoogleSerperAPIWrapper  
from langchain.llms.openai import OpenAI  
from langchain.agents import initialize\_agent, Tool  
from langchain.agents import AgentType  
  
import os  
  
os.environ["SERPER\_API\_KEY"] = ""  
os.environ['OPENAI\_API\_KEY'] = ""  
  
llm = OpenAI(temperature=0)  
search = GoogleSerperAPIWrapper()  
tools = [  
 Tool(  
 name="Intermediate Answer",  
 func=search.run,  
 description="useful for when you need to ask with search"  
 )  
]  
  
self\_ask\_with\_search = initialize\_agent(tools, llm, agent=AgentType.SELF\_ASK\_WITH\_SEARCH, verbose=True)  
self\_ask\_with\_search.run("What is the hometown of the reigning men's U.S. Open champion?")  

```

#### Output[​](#output "Direct link to Output")

```text
Entering new AgentExecutor chain...  
 Yes.  
Follow up: Who is the reigning men's U.S. Open champion?  
Intermediate answer: Current champions Carlos Alcaraz, 2022 men's singles champion.  
Follow up: Where is Carlos Alcaraz from?  
Intermediate answer: El Palmar, Spain  
So the final answer is: El Palmar, Spain  
  
> Finished chain.  
  
'El Palmar, Spain'  

```

For a more detailed walkthrough of this wrapper, see [this notebook](/docs/integrations/tools/google_serper.html).

### Tool[​](#tool "Direct link to Tool")

You can also easily load this wrapper as a Tool (to use with an Agent).
You can do this with:

```python
from langchain.agents import load\_tools  
tools = load\_tools(["google-serper"])  

```

For more information on tools, see [this page](/docs/modules/agents/tools/).

- [Setup](#setup)

- [Wrappers](#wrappers)

  - [Utility](#utility)
  - [Tool](#tool)

- [Utility](#utility)

- [Tool](#tool)
