# SQL (SQLAlchemy)

[Structured Query Language (SQL)](https://en.wikipedia.org/wiki/SQL) is a domain-specific language used in programming and designed for managing data held in a relational database management system (RDBMS), or for stream processing in a relational data stream management system (RDSMS). It is particularly useful in handling structured data, i.e., data incorporating relations among entities and variables.

[SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) is an open-source `SQL` toolkit and object-relational mapper (ORM) for the Python programming language released under the MIT License.

This notebook goes over a `SQLChatMessageHistory` class that allows to store chat history in any database supported by `SQLAlchemy`.

Please note that to use it with databases other than `SQLite`, you will need to install the corresponding database driver.

## Basic Usage[​](#basic-usage "Direct link to Basic Usage")

To use the storage you need to provide only 2 things:

1. Session Id - a unique identifier of the session, like user name, email, chat id etc.
1. Connection string - a string that specifies the database connection. It will be passed to SQLAlchemy create_engine function.
1. Install `SQLAlchemy` python package.

```bash
pip install SQLAlchemy  

```

```python
from langchain.memory.chat\_message\_histories import SQLChatMessageHistory  
  
chat\_message\_history = SQLChatMessageHistory(  
 session\_id='test\_session',  
 connection\_string='sqlite:///sqlite.db'  
)  
  
chat\_message\_history.add\_user\_message('Hello')  
chat\_message\_history.add\_ai\_message('Hi')  

```

```python
chat\_message\_history.messages  

```

```text
 [HumanMessage(content='Hello', additional\_kwargs={}, example=False),  
 AIMessage(content='Hi', additional\_kwargs={}, example=False)]  

```

## Custom Storage Format[​](#custom-storage-format "Direct link to Custom Storage Format")

By default, only the session id and message dictionary are stored in the table.

However, sometimes you might want to store some additional information, like message date, author, language etc.

To do that, you can create a custom message converter, by implementing **BaseMessageConverter** interface.

```python
from datetime import datetime  
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage  
from typing import Any  
from sqlalchemy import Column, Integer, Text, DateTime  
from sqlalchemy.orm import declarative\_base  
from langchain.memory.chat\_message\_histories.sql import BaseMessageConverter  
  
  
Base = declarative\_base()  
  
  
class CustomMessage(Base):  
 \_\_tablename\_\_ = 'custom\_message\_store'  
  
 id = Column(Integer, primary\_key=True)  
 session\_id = Column(Text)  
 type = Column(Text)  
 content = Column(Text)  
 created\_at = Column(DateTime)  
 author\_email = Column(Text)  
  
  
class CustomMessageConverter(BaseMessageConverter):  
 def \_\_init\_\_(self, author\_email: str):  
 self.author\_email = author\_email  
   
 def from\_sql\_model(self, sql\_message: Any) -> BaseMessage:  
 if sql\_message.type == 'human':  
 return HumanMessage(  
 content=sql\_message.content,  
 )  
 elif sql\_message.type == 'ai':  
 return AIMessage(  
 content=sql\_message.content,  
 )  
 elif sql\_message.type == 'system':  
 return SystemMessage(  
 content=sql\_message.content,  
 )  
 else:  
 raise ValueError(f'Unknown message type: {sql\_message.type}')  
   
 def to\_sql\_model(self, message: BaseMessage, session\_id: str) -> Any:  
 now = datetime.now()  
 return CustomMessage(  
 session\_id=session\_id,  
 type=message.type,  
 content=message.content,  
 created\_at=now,  
 author\_email=self.author\_email  
 )  
   
 def get\_sql\_model\_class(self) -> Any:  
 return CustomMessage  
  
  
chat\_message\_history = SQLChatMessageHistory(  
 session\_id='test\_session',  
 connection\_string='sqlite:///sqlite.db',  
 custom\_message\_converter=CustomMessageConverter(  
 author\_email='test@example.com'  
 )  
)  
  
chat\_message\_history.add\_user\_message('Hello')  
chat\_message\_history.add\_ai\_message('Hi')  

```

```python
chat\_message\_history.messages  

```

```text
 [HumanMessage(content='Hello', additional\_kwargs={}, example=False),  
 AIMessage(content='Hi', additional\_kwargs={}, example=False)]  

```

You also might want to change the name of session_id column. In this case you'll need to specify `session_id_field_name` parameter.

- [Basic Usage](#basic-usage)
- [Custom Storage Format](#custom-storage-format)
