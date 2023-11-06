# Combine agents and vector stores

This notebook covers how to combine agents and vector stores. The use case for this is that you've ingested your data into a vector store and want to interact with it in an agentic manner.

The recommended method for doing so is to create a `RetrievalQA` and then use that as a tool in the overall agent. Let's take a look at doing this below. You can do this with multiple different vector DBs, and use the agent as a way to route between them. There are two different ways of doing this - you can either let the agent use the vector stores as normal tools, or you can set `return_direct=True` to really just use the agent as a router.

## Create the vector store[​](#create-the-vector-store "Direct link to Create the vector store")

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.vectorstores import Chroma  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.llms import OpenAI  
from langchain.chains import RetrievalQA  
  
llm = OpenAI(temperature=0)  

```

```python
from pathlib import Path  
  
relevant\_parts = []  
for p in Path(".").absolute().parts:  
 relevant\_parts.append(p)  
 if relevant\_parts[-3:] == ["langchain", "docs", "modules"]:  
 break  
doc\_path = str(Path(\*relevant\_parts) / "state\_of\_the\_union.txt")  

```

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader(doc\_path)  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
texts = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  
docsearch = Chroma.from\_documents(texts, embeddings, collection\_name="state-of-union")  

```

```text
 Running Chroma using direct local API.  
 Using DuckDB in-memory for database. Data will be transient.  

```

```python
state\_of\_union = RetrievalQA.from\_chain\_type(  
 llm=llm, chain\_type="stuff", retriever=docsearch.as\_retriever()  
)  

```

```python
from langchain.document\_loaders import WebBaseLoader  

```

```python
loader = WebBaseLoader("https://beta.ruff.rs/docs/faq/")  

```

```python
docs = loader.load()  
ruff\_texts = text\_splitter.split\_documents(docs)  
ruff\_db = Chroma.from\_documents(ruff\_texts, embeddings, collection\_name="ruff")  
ruff = RetrievalQA.from\_chain\_type(  
 llm=llm, chain\_type="stuff", retriever=ruff\_db.as\_retriever()  
)  

```

```text
 Running Chroma using direct local API.  
 Using DuckDB in-memory for database. Data will be transient.  

```

## Create the Agent[​](#create-the-agent "Direct link to Create the Agent")

```python
# Import things that are needed generically  
from langchain.agents import initialize\_agent, Tool  
from langchain.agents import AgentType  
from langchain.tools import BaseTool  
from langchain.llms import OpenAI  
from langchain.chains import LLMMathChain  
from langchain.utilities import SerpAPIWrapper  

```

```python
tools = [  
 Tool(  
 name="State of Union QA System",  
 func=state\_of\_union.run,  
 description="useful for when you need to answer questions about the most recent state of the union address. Input should be a fully formed question.",  
 ),  
 Tool(  
 name="Ruff QA System",  
 func=ruff.run,  
 description="useful for when you need to answer questions about ruff (a python linter). Input should be a fully formed question.",  
 ),  
]  

```

```python
# Construct the agent. We will use the default agent type here.  
# See documentation for a full list of options.  
agent = initialize\_agent(  
 tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  

```

```python
agent.run(  
 "What did biden say about ketanji brown jackson in the state of the union address?"  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find out what Biden said about Ketanji Brown Jackson in the State of the Union address.  
 Action: State of Union QA System  
 Action Input: What did Biden say about Ketanji Brown Jackson in the State of the Union address?  
 Observation: Biden said that Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence.  
 Thought: I now know the final answer  
 Final Answer: Biden said that Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence.  
   
 > Finished chain.  
  
  
  
  
  
 "Biden said that Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence."  

```

```python
agent.run("Why use ruff over flake8?")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find out the advantages of using ruff over flake8  
 Action: Ruff QA System  
 Action Input: What are the advantages of using ruff over flake8?  
 Observation: Ruff can be used as a drop-in replacement for Flake8 when used (1) without or with a small number of plugins, (2) alongside Black, and (3) on Python 3 code. It also re-implements some of the most popular Flake8 plugins and related code quality tools natively, including isort, yesqa, eradicate, and most of the rules implemented in pyupgrade. Ruff also supports automatically fixing its own lint violations, which Flake8 does not.  
 Thought: I now know the final answer  
 Final Answer: Ruff can be used as a drop-in replacement for Flake8 when used (1) without or with a small number of plugins, (2) alongside Black, and (3) on Python 3 code. It also re-implements some of the most popular Flake8 plugins and related code quality tools natively, including isort, yesqa, eradicate, and most of the rules implemented in pyupgrade. Ruff also supports automatically fixing its own lint violations, which Flake8 does not.  
   
 > Finished chain.  
  
  
  
  
  
 'Ruff can be used as a drop-in replacement for Flake8 when used (1) without or with a small number of plugins, (2) alongside Black, and (3) on Python 3 code. It also re-implements some of the most popular Flake8 plugins and related code quality tools natively, including isort, yesqa, eradicate, and most of the rules implemented in pyupgrade. Ruff also supports automatically fixing its own lint violations, which Flake8 does not.'  

```

## Use the Agent solely as a router[​](#use-the-agent-solely-as-a-router "Direct link to Use the Agent solely as a router")

You can also set `return_direct=True` if you intend to use the agent as a router and just want to directly return the result of the RetrievalQAChain.

Notice that in the above examples the agent did some extra work after querying the RetrievalQAChain. You can avoid that and just return the result directly.

```python
tools = [  
 Tool(  
 name="State of Union QA System",  
 func=state\_of\_union.run,  
 description="useful for when you need to answer questions about the most recent state of the union address. Input should be a fully formed question.",  
 return\_direct=True,  
 ),  
 Tool(  
 name="Ruff QA System",  
 func=ruff.run,  
 description="useful for when you need to answer questions about ruff (a python linter). Input should be a fully formed question.",  
 return\_direct=True,  
 ),  
]  

```

```python
agent = initialize\_agent(  
 tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  

```

```python
agent.run(  
 "What did biden say about ketanji brown jackson in the state of the union address?"  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find out what Biden said about Ketanji Brown Jackson in the State of the Union address.  
 Action: State of Union QA System  
 Action Input: What did Biden say about Ketanji Brown Jackson in the State of the Union address?  
 Observation: Biden said that Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence.  
   
   
 > Finished chain.  
  
  
  
  
  
 " Biden said that Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence."  

```

```python
agent.run("Why use ruff over flake8?")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find out the advantages of using ruff over flake8  
 Action: Ruff QA System  
 Action Input: What are the advantages of using ruff over flake8?  
 Observation: Ruff can be used as a drop-in replacement for Flake8 when used (1) without or with a small number of plugins, (2) alongside Black, and (3) on Python 3 code. It also re-implements some of the most popular Flake8 plugins and related code quality tools natively, including isort, yesqa, eradicate, and most of the rules implemented in pyupgrade. Ruff also supports automatically fixing its own lint violations, which Flake8 does not.  
   
   
 > Finished chain.  
  
  
  
  
  
 ' Ruff can be used as a drop-in replacement for Flake8 when used (1) without or with a small number of plugins, (2) alongside Black, and (3) on Python 3 code. It also re-implements some of the most popular Flake8 plugins and related code quality tools natively, including isort, yesqa, eradicate, and most of the rules implemented in pyupgrade. Ruff also supports automatically fixing its own lint violations, which Flake8 does not.'  

```

## Multi-Hop vector store reasoning[​](#multi-hop-vector-store-reasoning "Direct link to Multi-Hop vector store reasoning")

Because vector stores are easily usable as tools in agents, it is easy to use answer multi-hop questions that depend on vector stores using the existing agent framework.

```python
tools = [  
 Tool(  
 name="State of Union QA System",  
 func=state\_of\_union.run,  
 description="useful for when you need to answer questions about the most recent state of the union address. Input should be a fully formed question, not referencing any obscure pronouns from the conversation before.",  
 ),  
 Tool(  
 name="Ruff QA System",  
 func=ruff.run,  
 description="useful for when you need to answer questions about ruff (a python linter). Input should be a fully formed question, not referencing any obscure pronouns from the conversation before.",  
 ),  
]  

```

```python
# Construct the agent. We will use the default agent type here.  
# See documentation for a full list of options.  
agent = initialize\_agent(  
 tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  

```

```python
agent.run(  
 "What tool does ruff use to run over Jupyter Notebooks? Did the president mention that tool in the state of the union?"  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find out what tool ruff uses to run over Jupyter Notebooks, and if the president mentioned it in the state of the union.  
 Action: Ruff QA System  
 Action Input: What tool does ruff use to run over Jupyter Notebooks?  
 Observation: Ruff is integrated into nbQA, a tool for running linters and code formatters over Jupyter Notebooks. After installing ruff and nbqa, you can run Ruff over a notebook like so: > nbqa ruff Untitled.html  
 Thought: I now need to find out if the president mentioned this tool in the state of the union.  
 Action: State of Union QA System  
 Action Input: Did the president mention nbQA in the state of the union?  
 Observation: No, the president did not mention nbQA in the state of the union.  
 Thought: I now know the final answer.  
 Final Answer: No, the president did not mention nbQA in the state of the union.  
   
 > Finished chain.  
  
  
  
  
  
 'No, the president did not mention nbQA in the state of the union.'  

```

- [Create the vector store](#create-the-vector-store)
- [Create the Agent](#create-the-agent)
- [Use the Agent solely as a router](#use-the-agent-solely-as-a-router)
- [Multi-Hop vector store reasoning](#multi-hop-vector-store-reasoning)
