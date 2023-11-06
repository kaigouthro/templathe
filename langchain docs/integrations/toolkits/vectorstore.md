# Vectorstore

This notebook showcases an agent designed to retrieve information from one or more vectorstores, either with or without sources.

## Create Vectorstores[​](#create-vectorstores "Direct link to Create Vectorstores")

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.vectorstores import Chroma  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.llms import OpenAI  
from langchain.chains import VectorDBQA  
  
llm = OpenAI(temperature=0)  

```

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
texts = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  
state\_of\_union\_store = Chroma.from\_documents(  
 texts, embeddings, collection\_name="state-of-union"  
)  

```

```text
 Running Chroma using direct local API.  
 Using DuckDB in-memory for database. Data will be transient.  

```

```python
from langchain.document\_loaders import WebBaseLoader  
  
loader = WebBaseLoader("https://beta.ruff.rs/docs/faq/")  
docs = loader.load()  
ruff\_texts = text\_splitter.split\_documents(docs)  
ruff\_store = Chroma.from\_documents(ruff\_texts, embeddings, collection\_name="ruff")  

```

```text
 Running Chroma using direct local API.  
 Using DuckDB in-memory for database. Data will be transient.  

```

## Initialize Toolkit and Agent[​](#initialize-toolkit-and-agent "Direct link to Initialize Toolkit and Agent")

First, we'll create an agent with a single vectorstore.

```python
from langchain.agents.agent\_toolkits import (  
 create\_vectorstore\_agent,  
 VectorStoreToolkit,  
 VectorStoreInfo,  
)  
  
vectorstore\_info = VectorStoreInfo(  
 name="state\_of\_union\_address",  
 description="the most recent state of the Union adress",  
 vectorstore=state\_of\_union\_store,  
)  
toolkit = VectorStoreToolkit(vectorstore\_info=vectorstore\_info)  
agent\_executor = create\_vectorstore\_agent(llm=llm, toolkit=toolkit, verbose=True)  

```

## Examples[​](#examples "Direct link to Examples")

```python
agent\_executor.run(  
 "What did biden say about ketanji brown jackson in the state of the union address?"  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find the answer in the state of the union address  
 Action: state\_of\_union\_address  
 Action Input: What did biden say about ketanji brown jackson  
 Observation: Biden said that Ketanji Brown Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence.  
 Thought: I now know the final answer  
 Final Answer: Biden said that Ketanji Brown Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence.  
   
 > Finished chain.  
  
  
  
  
  
 "Biden said that Ketanji Brown Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence."  

```

```python
agent\_executor.run(  
 "What did biden say about ketanji brown jackson in the state of the union address? List the source."  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to use the state\_of\_union\_address\_with\_sources tool to answer this question.  
 Action: state\_of\_union\_address\_with\_sources  
 Action Input: What did biden say about ketanji brown jackson  
 Observation: {"answer": " Biden said that he nominated Circuit Court of Appeals Judge Ketanji Brown Jackson to the United States Supreme Court, and that she is one of the nation's top legal minds who will continue Justice Breyer's legacy of excellence.\n", "sources": "../../state\_of\_the\_union.txt"}  
 Thought: I now know the final answer  
 Final Answer: Biden said that he nominated Circuit Court of Appeals Judge Ketanji Brown Jackson to the United States Supreme Court, and that she is one of the nation's top legal minds who will continue Justice Breyer's legacy of excellence. Sources: ../../state\_of\_the\_union.txt  
   
 > Finished chain.  
  
  
  
  
  
 "Biden said that he nominated Circuit Court of Appeals Judge Ketanji Brown Jackson to the United States Supreme Court, and that she is one of the nation's top legal minds who will continue Justice Breyer's legacy of excellence. Sources: ../../state\_of\_the\_union.txt"  

```

## Multiple Vectorstores[​](#multiple-vectorstores "Direct link to Multiple Vectorstores")

We can also easily use this initialize an agent with multiple vectorstores and use the agent to route between them. To do this. This agent is optimized for routing, so it is a different toolkit and initializer.

```python
from langchain.agents.agent\_toolkits import (  
 create\_vectorstore\_router\_agent,  
 VectorStoreRouterToolkit,  
 VectorStoreInfo,  
)  

```

```python
ruff\_vectorstore\_info = VectorStoreInfo(  
 name="ruff",  
 description="Information about the Ruff python linting library",  
 vectorstore=ruff\_store,  
)  
router\_toolkit = VectorStoreRouterToolkit(  
 vectorstores=[vectorstore\_info, ruff\_vectorstore\_info], llm=llm  
)  
agent\_executor = create\_vectorstore\_router\_agent(  
 llm=llm, toolkit=router\_toolkit, verbose=True  
)  

```

## Examples[​](#examples-1 "Direct link to Examples")

```python
agent\_executor.run(  
 "What did biden say about ketanji brown jackson in the state of the union address?"  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to use the state\_of\_union\_address tool to answer this question.  
 Action: state\_of\_union\_address  
 Action Input: What did biden say about ketanji brown jackson  
 Observation: Biden said that Ketanji Brown Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence.  
 Thought: I now know the final answer  
 Final Answer: Biden said that Ketanji Brown Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence.  
   
 > Finished chain.  
  
  
  
  
  
 "Biden said that Ketanji Brown Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence."  

```

```python
agent\_executor.run("What tool does ruff use to run over Jupyter Notebooks?")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find out what tool ruff uses to run over Jupyter Notebooks  
 Action: ruff  
 Action Input: What tool does ruff use to run over Jupyter Notebooks?  
 Observation: Ruff is integrated into nbQA, a tool for running linters and code formatters over Jupyter Notebooks. After installing ruff and nbqa, you can run Ruff over a notebook like so: > nbqa ruff Untitled.html  
 Thought: I now know the final answer  
 Final Answer: Ruff is integrated into nbQA, a tool for running linters and code formatters over Jupyter Notebooks. After installing ruff and nbqa, you can run Ruff over a notebook like so: > nbqa ruff Untitled.html  
   
 > Finished chain.  
  
  
  
  
  
 'Ruff is integrated into nbQA, a tool for running linters and code formatters over Jupyter Notebooks. After installing ruff and nbqa, you can run Ruff over a notebook like so: > nbqa ruff Untitled.html'  

```

```python
agent\_executor.run(  
 "What tool does ruff use to run over Jupyter Notebooks? Did the president mention that tool in the state of the union?"  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find out what tool ruff uses and if the president mentioned it in the state of the union.  
 Action: ruff  
 Action Input: What tool does ruff use to run over Jupyter Notebooks?  
 Observation: Ruff is integrated into nbQA, a tool for running linters and code formatters over Jupyter Notebooks. After installing ruff and nbqa, you can run Ruff over a notebook like so: > nbqa ruff Untitled.html  
 Thought: I need to find out if the president mentioned nbQA in the state of the union.  
 Action: state\_of\_union\_address  
 Action Input: Did the president mention nbQA in the state of the union?  
 Observation: No, the president did not mention nbQA in the state of the union.  
 Thought: I now know the final answer.  
 Final Answer: No, the president did not mention nbQA in the state of the union.  
   
 > Finished chain.  
  
  
  
  
  
 'No, the president did not mention nbQA in the state of the union.'  

```

- [Create Vectorstores](#create-vectorstores)
- [Initialize Toolkit and Agent](#initialize-toolkit-and-agent)
- [Examples](#examples)
- [Multiple Vectorstores](#multiple-vectorstores)
- [Examples](#examples-1)
