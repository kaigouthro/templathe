# Upstash Redis Chat Message History

This notebook goes over how to use Upstash Redis to store chat message history.

```python
from langchain.memory.chat\_message\_histories.upstash\_redis import UpstashRedisChatMessageHistory  
  
URL = "<UPSTASH\_REDIS\_REST\_URL>"  
TOKEN = "<UPSTASH\_REDIS\_REST\_TOKEN>"  
  
history = UpstashRedisChatMessageHistory(url=URL, token=TOKEN, ttl=10, session\_id="my-test-session")  
  
history.add\_user\_message("hello llm!")  
history.add\_ai\_message("hello user!")  

```

```python
history.messages  

```
