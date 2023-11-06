# MongodDB

`MongoDB` is a source-available cross-platform document-oriented database program. Classified as a NoSQL database program, `MongoDB` uses `JSON`-like documents with optional schemas.

`MongoDB` is developed by MongoDB Inc. and licensed under the Server Side Public License (SSPL). - [Wikipedia](https://en.wikipedia.org/wiki/MongoDB)

This notebook goes over how to use Mongodb to store chat message history.

## Setting up[​](#setting-up "Direct link to Setting up")

```bash
pip install pymongo  

```

```python
# Provide the connection string to connect to the MongoDB database  
connection\_string = "mongodb://mongo\_user:password123@mongo:27017"  

```

## Example[​](#example "Direct link to Example")

```python
from langchain.memory import MongoDBChatMessageHistory  
  
message\_history = MongoDBChatMessageHistory(  
 connection\_string=connection\_string, session\_id="test-session"  
)  
  
message\_history.add\_user\_message("hi!")  
  
message\_history.add\_ai\_message("whats up?")  

```

```python
message\_history.messages  

```

```text
 [HumanMessage(content='hi!', additional\_kwargs={}, example=False),  
 AIMessage(content='whats up?', additional\_kwargs={}, example=False)]  

```

- [Setting up](#setting-up)
- [Example](#example)
