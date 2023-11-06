# SingleStoreDB

This notebook goes over how to use SingleStoreDB to store chat message history.

```python
from langchain.memory import SingleStoreDBChatMessageHistory  
  
history = SingleStoreDBChatMessageHistory(  
 session\_id="foo",  
 host="root:pass@localhost:3306/db"  
)  
  
history.add\_user\_message("hi!")  
  
history.add\_ai\_message("whats up?")  

```

```python
history.messages  

```
