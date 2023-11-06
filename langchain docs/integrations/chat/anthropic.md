# Anthropic

This notebook covers how to get started with Anthropic chat models.

```python
from langchain.chat\_models import ChatAnthropic  
from langchain.prompts.chat import (  
 ChatPromptTemplate,  
 SystemMessagePromptTemplate,  
 AIMessagePromptTemplate,  
 HumanMessagePromptTemplate,  
)  
from langchain.schema import AIMessage, HumanMessage, SystemMessage  

```

```python
chat = ChatAnthropic()  

```

```python
messages = [  
 HumanMessage(  
 content="Translate this sentence from English to French. I love programming."  
 )  
]  
chat(messages)  

```

```text
 AIMessage(content=" J'aime la programmation.", additional\_kwargs={}, example=False)  

```

## `ChatAnthropic` also supports async and streaming functionality:[​](#chatanthropic-also-supports-async-and-streaming-functionality "Direct link to chatanthropic-also-supports-async-and-streaming-functionality")

```python
from langchain.callbacks.manager import CallbackManager  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  

```

```python
await chat.agenerate([messages])  

```

```text
 LLMResult(generations=[[ChatGeneration(text=" J'aime programmer.", generation\_info=None, message=AIMessage(content=" J'aime programmer.", additional\_kwargs={}, example=False))]], llm\_output={}, run=[RunInfo(run\_id=UUID('8cc8fb68-1c35-439c-96a0-695036a93652'))])  

```

```python
chat = ChatAnthropic(  
 streaming=True,  
 verbose=True,  
 callback\_manager=CallbackManager([StreamingStdOutCallbackHandler()]),  
)  
chat(messages)  

```

```text
 J'aime la programmation.  
  
  
  
  
 AIMessage(content=" J'aime la programmation.", additional\_kwargs={}, example=False)  

```

- [`ChatAnthropic` also supports async and streaming functionality:](#chatanthropic-also-supports-async-and-streaming-functionality)
