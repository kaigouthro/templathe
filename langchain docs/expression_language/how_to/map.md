# Use RunnableParallel/RunnableMap

RunnableParallel (aka. RunnableMap) makes it easy to execute multiple Runnables in parallel, and to return the output of these Runnables as a map.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.prompts import ChatPromptTemplate  
from langchain.schema.runnable import RunnableParallel  
  
  
model = ChatOpenAI()  
joke\_chain = ChatPromptTemplate.from\_template("tell me a joke about {topic}") | model  
poem\_chain = ChatPromptTemplate.from\_template("write a 2-line poem about {topic}") | model  
  
map\_chain = RunnableParallel(joke=joke\_chain, poem=poem\_chain)  
  
map\_chain.invoke({"topic": "bear"})  

```

```text
 {'joke': AIMessage(content="Why don't bears wear shoes? \n\nBecause they have bear feet!", additional\_kwargs={}, example=False),  
 'poem': AIMessage(content="In woodland depths, bear prowls with might,\nSilent strength, nature's sovereign, day and night.", additional\_kwargs={}, example=False)}  

```

## Manipulating outputs/inputs[​](#manipulating-outputsinputs "Direct link to Manipulating outputs/inputs")

Maps can be useful for manipulating the output of one Runnable to match the input format of the next Runnable in a sequence.

```python
from langchain.embeddings import OpenAIEmbeddings  
from langchain.schema.output\_parser import StrOutputParser  
from langchain.schema.runnable import RunnablePassthrough  
from langchain.vectorstores import FAISS  
  
vectorstore = FAISS.from\_texts(["harrison worked at kensho"], embedding=OpenAIEmbeddings())  
retriever = vectorstore.as\_retriever()  
template = """Answer the question based only on the following context:  
{context}  
  
Question: {question}  
"""  
prompt = ChatPromptTemplate.from\_template(template)  
  
retrieval\_chain = (  
 {"context": retriever, "question": RunnablePassthrough()}   
 | prompt   
 | model   
 | StrOutputParser()  
)  
  
retrieval\_chain.invoke("where did harrison work?")  

```

```text
 'Harrison worked at Kensho.'  

```

Here the input to prompt is expected to be a map with keys "context" and "question". The user input is just the question. So we need to get the context using our retriever and passthrough the user input under the "question" key.

Note that when composing a RunnableMap when another Runnable we don't even need to wrap our dictionary in the RunnableMap class — the type conversion is handled for us.

## Parallelism[​](#parallelism "Direct link to Parallelism")

RunnableMaps are also useful for running independent processes in parallel, since each Runnable in the map is executed in parallel. For example, we can see our earlier `joke_chain`, `poem_chain` and `map_chain` all have about the same runtime, even though `map_chain` executes both of the other two.

```python
joke\_chain.invoke({"topic": "bear"})  

```

```text
 958 ms ± 402 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)  

```

```python
poem\_chain.invoke({"topic": "bear"})  

```

```text
 1.22 s ± 508 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)  

```

```python
map\_chain.invoke({"topic": "bear"})  

```

```text
 1.15 s ± 119 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)  

```

- [Manipulating outputs/inputs](#manipulating-outputsinputs)
- [Parallelism](#parallelism)
