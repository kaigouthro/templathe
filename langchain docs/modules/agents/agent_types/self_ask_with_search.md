# Self-ask with search

This walkthrough showcases the self-ask with search chain.

```python
from langchain.llms import OpenAI  
from langchain.utilities import SerpAPIWrapper  
from langchain.agents import initialize\_agent, Tool  
from langchain.agents import AgentType  
  
llm = OpenAI(temperature=0)  
search = SerpAPIWrapper()  
tools = [  
 Tool(  
 name="Intermediate Answer",  
 func=search.run,  
 description="useful for when you need to ask with search",  
 )  
]  

```

## Using LangChain Expression Language[​](#using-langchain-expression-language "Direct link to Using LangChain Expression Language")

First we will show how to construct this agent from components using LangChain Expression Language

```python
from langchain.agents.output\_parsers import SelfAskOutputParser  
from langchain.agents.format\_scratchpad import format\_log\_to\_str  
from langchain import hub  

```

```python
prompt = hub.pull("hwchase17/self-ask-with-search")  

```

```python
llm\_with\_stop = llm.bind(stop=["\nIntermediate answer:"])  

```

```python
agent = {  
 "input": lambda x: x["input"],  
 # Use some custom observation\_prefix/llm\_prefix for formatting  
 "agent\_scratchpad": lambda x: format\_log\_to\_str(  
 x['intermediate\_steps'],   
 observation\_prefix="\nIntermediate answer: ",  
 llm\_prefix="",  
 ),  
} | prompt | llm\_with\_stop | SelfAskOutputParser()  

```

```python
from langchain.agents import AgentExecutor  

```

```python
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  

```

```python
agent\_executor.invoke({"input": "What is the hometown of the reigning men's U.S. Open champion?"})  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Yes.  
 Follow up: Who is the reigning men's U.S. Open champion?Men's US Open Tennis Champions Novak Djokovic earned his 24th major singles title against 2021 US Open champion Daniil Medvedev, 6-3, 7-6 (7-5), 6-3. The victory ties the Serbian player with the legendary Margaret Court for the most Grand Slam wins across both men's and women's singles.  
 Follow up: Where is Novak Djokovic from?Belgrade, Serbia  
 So the final answer is: Belgrade, Serbia  
   
 > Finished chain.  
  
  
  
  
  
 {'input': "What is the hometown of the reigning men's U.S. Open champion?",  
 'output': 'Belgrade, Serbia'}  

```

## Use off-the-shelf agent[​](#use-off-the-shelf-agent "Direct link to Use off-the-shelf agent")

```python
self\_ask\_with\_search = initialize\_agent(  
 tools, llm, agent=AgentType.SELF\_ASK\_WITH\_SEARCH, verbose=True  
)  
self\_ask\_with\_search.run(  
 "What is the hometown of the reigning men's U.S. Open champion?"  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Yes.  
 Follow up: Who is the reigning men's U.S. Open champion?  
 Intermediate answer: Men's US Open Tennis Champions Novak Djokovic earned his 24th major singles title against 2021 US Open champion Daniil Medvedev, 6-3, 7-6 (7-5), 6-3. The victory ties the Serbian player with the legendary Margaret Court for the most Grand Slam wins across both men's and women's singles.  
   
 Follow up: Where is Novak Djokovic from?  
 Intermediate answer: Belgrade, Serbia  
 So the final answer is: Belgrade, Serbia  
   
 > Finished chain.  
  
  
  
  
  
 'Belgrade, Serbia'  

```

- [Using LangChain Expression Language](#using-langchain-expression-language)
- [Use off-the-shelf agent](#use-off-the-shelf-agent)
