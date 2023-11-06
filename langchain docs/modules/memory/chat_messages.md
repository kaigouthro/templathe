# Chat Messages

Head to [Integrations](/docs/integrations/memory/) for documentation on built-in memory integrations with 3rd-party databases and tools.

One of the core utility classes underpinning most (if not all) memory modules is the `ChatMessageHistory` class.
This is a super lightweight wrapper that provides convenience methods for saving HumanMessages, AIMessages, and then fetching them all.

You may want to use this class directly if you are managing memory outside of a chain.

```python
from langchain.memory import ChatMessageHistory  
  
history = ChatMessageHistory()  
  
history.add\_user\_message("hi!")  
  
history.add\_ai\_message("whats up?")  

```

```python
history.messages  

```

```text
 [HumanMessage(content='hi!', additional\_kwargs={}),  
 AIMessage(content='whats up?', additional\_kwargs={})]  

```
