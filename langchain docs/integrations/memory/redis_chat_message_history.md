# Redis

[Redis (Remote Dictionary Server)](https://en.wikipedia.org/wiki/Redis) is an open-source in-memory storage, used as a distributed, in-memory key–value database, cache and message broker, with optional durability. Because it holds all data in memory and because of its design, `Redis` offers low-latency reads and writes, making it particularly suitable for use cases that require a cache. Redis is the most popular NoSQL database, and one of the most popular databases overall.

This notebook goes over how to use `Redis` to store chat message history.

```python
from langchain.memory import RedisChatMessageHistory  
  
history = RedisChatMessageHistory("foo")  
  
history.add\_user\_message("hi!")  
  
history.add\_ai\_message("whats up?")  

```

```python
history.messages  

```

```text
 [AIMessage(content='whats up?', additional\_kwargs={}),  
 HumanMessage(content='hi!', additional\_kwargs={})]  

```
