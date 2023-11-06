# Postgres

[PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL) also known as `Postgres`, is a free and open-source relational database management system (RDBMS) emphasizing extensibility and SQL compliance.

This notebook goes over how to use Postgres to store chat message history.

```python
from langchain.memory import PostgresChatMessageHistory  
  
history = PostgresChatMessageHistory(  
 connection\_string="postgresql://postgres:mypassword@localhost/chat\_history",  
 session\_id="foo",  
)  
  
history.add\_user\_message("hi!")  
  
history.add\_ai\_message("whats up?")  

```

```python
history.messages  

```
