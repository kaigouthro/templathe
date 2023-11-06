# Cohere

This notebook covers how to get started with Cohere chat models.

```python
from langchain.chat\_models import ChatCohere  
from langchain.schema import AIMessage, HumanMessage  

```

```python
chat = ChatCohere()  

```

```python
messages = [  
 HumanMessage(  
 content="knock knock"  
 )  
]  
chat(messages)  

```

```text
 AIMessage(content="Who's there?")  

```

## `ChatCohere` also supports async and streaming functionality:[​](#chatcohere-also-supports-async-and-streaming-functionality "Direct link to chatcohere-also-supports-async-and-streaming-functionality")

```python
from langchain.callbacks.manager import CallbackManager  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  

```

```python
await chat.agenerate([messages])  

```

```text
 Who's there?  
  
  
  
  
 LLMResult(generations=[[ChatGenerationChunk(text="Who's there?", message=AIMessageChunk(content="Who's there?"))]], llm\_output={}, run=[RunInfo(run\_id=UUID('1e9eaefc-9c99-4fa9-8297-ef9975d4751e'))])  

```

```python
chat = ChatCohere(  
 streaming=True,  
 verbose=True,  
 callback\_manager=CallbackManager([StreamingStdOutCallbackHandler()]),  
)  
chat(messages)  

```

```text
 Who's there?  
  
  
  
  
 AIMessageChunk(content="Who's there?")  

```

- [`ChatCohere` also supports async and streaming functionality:](#chatcohere-also-supports-async-and-streaming-functionality)
