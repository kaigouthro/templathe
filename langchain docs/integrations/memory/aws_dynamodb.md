# AWS DynamoDB

[Amazon AWS DynamoDB](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/dynamodb/index.html) is a fully managed `NoSQL` database service that provides fast and predictable performance with seamless scalability.

This notebook goes over how to use `DynamoDB` to store chat message history.

First make sure you have correctly configured the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html). Then make sure you have installed `boto3`.

```bash
pip install boto3  

```

Next, create the `DynamoDB` Table where we will be storing messages:

```python
import boto3  
  
# Get the service resource.  
dynamodb = boto3.resource("dynamodb")  
  
# Create the DynamoDB table.  
table = dynamodb.create\_table(  
 TableName="SessionTable",  
 KeySchema=[{"AttributeName": "SessionId", "KeyType": "HASH"}],  
 AttributeDefinitions=[{"AttributeName": "SessionId", "AttributeType": "S"}],  
 BillingMode="PAY\_PER\_REQUEST",  
)  
  
# Wait until the table exists.  
table.meta.client.get\_waiter("table\_exists").wait(TableName="SessionTable")  
  
# Print out some data about the table.  
print(table.item\_count)  

```

```text
 0  

```

## DynamoDBChatMessageHistory[​](#dynamodbchatmessagehistory "Direct link to DynamoDBChatMessageHistory")

```python
from langchain.memory.chat\_message\_histories import DynamoDBChatMessageHistory  
  
history = DynamoDBChatMessageHistory(table\_name="SessionTable", session\_id="0")  
  
history.add\_user\_message("hi!")  
  
history.add\_ai\_message("whats up?")  

```

```python
history.messages  

```

```text
 [HumanMessage(content='hi!', additional\_kwargs={}, example=False),  
 AIMessage(content='whats up?', additional\_kwargs={}, example=False),  
 HumanMessage(content='hi!', additional\_kwargs={}, example=False),  
 AIMessage(content='whats up?', additional\_kwargs={}, example=False)]  

```

## DynamoDBChatMessageHistory with Custom Endpoint URL[​](#dynamodbchatmessagehistory-with-custom-endpoint-url "Direct link to DynamoDBChatMessageHistory with Custom Endpoint URL")

Sometimes it is useful to specify the URL to the AWS endpoint to connect to. For instance, when you are running locally against [Localstack](https://localstack.cloud/). For those cases you can specify the URL via the `endpoint_url` parameter in the constructor.

```python
from langchain.memory.chat\_message\_histories import DynamoDBChatMessageHistory  
  
history = DynamoDBChatMessageHistory(  
 table\_name="SessionTable",  
 session\_id="0",  
 endpoint\_url="http://localhost.localstack.cloud:4566",  
)  

```

## DynamoDBChatMessageHistory With Different Keys Composite Keys[​](#dynamodbchatmessagehistory-with-different-keys-composite-keys "Direct link to DynamoDBChatMessageHistory With Different Keys Composite Keys")

The default key for DynamoDBChatMessageHistory is `{"SessionId": self.session_id}`, but you can modify this to match your table design.

### Primary Key Name[​](#primary-key-name "Direct link to Primary Key Name")

You may modify the primary key by passing in a primary_key_name value in the constructor, resulting in the following:
`{self.primary_key_name: self.session_id}`

### Composite Keys[​](#composite-keys "Direct link to Composite Keys")

When using an existing DynamoDB table, you may need to modify the key structure from the default of to something including a Sort Key. To do this you may use the `key` parameter.

Passing a value for key will override the primary_key parameter, and the resulting key structure will be the passed value.

```python
from langchain.memory.chat\_message\_histories import DynamoDBChatMessageHistory  
  
composite\_table = dynamodb.create\_table(  
 TableName="CompositeTable",  
 KeySchema=[{"AttributeName": "PK", "KeyType": "HASH"}, {"AttributeName": "SK", "KeyType": "RANGE"}],  
 AttributeDefinitions=[{"AttributeName": "PK", "AttributeType": "S"}, {"AttributeName": "SK", "AttributeType": "S"}],  
 BillingMode="PAY\_PER\_REQUEST",  
)  
  
# Wait until the table exists.  
composite\_table.meta.client.get\_waiter("table\_exists").wait(TableName="CompositeTable")  
  
# Print out some data about the table.  
print(composite\_table.item\_count)  
  
my\_key = {  
 "PK": "session\_id::0",  
 "SK": "langchain\_history",  
}  
  
composite\_key\_history = DynamoDBChatMessageHistory(  
 table\_name="CompositeTable",  
 session\_id="0",  
 endpoint\_url="http://localhost.localstack.cloud:4566",  
 key=my\_key,  
)  
  
composite\_key\_history.add\_user\_message("hello, composite dynamodb table!")  
  
composite\_key\_history.messages  

```

```text
 0  
  
  
  
  
  
 [HumanMessage(content='hello, composite dynamodb table!', additional\_kwargs={}, example=False)]  

```

## Agent with DynamoDB Memory[​](#agent-with-dynamodb-memory "Direct link to Agent with DynamoDB Memory")

```python
from langchain.agents import Tool  
from langchain.memory import ConversationBufferMemory  
from langchain.chat\_models import ChatOpenAI  
from langchain.agents import initialize\_agent  
from langchain.agents import AgentType  
from langchain.utilities import PythonREPL  
from getpass import getpass  
  
message\_history = DynamoDBChatMessageHistory(table\_name="SessionTable", session\_id="1")  
memory = ConversationBufferMemory(  
 memory\_key="chat\_history", chat\_memory=message\_history, return\_messages=True  
)  

```

```python
python\_repl = PythonREPL()  
  
# You can create the tool to pass to an agent  
tools = [  
 Tool(  
 name="python\_repl",  
 description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",  
 func=python\_repl.run,  
 )  
]  

```

```python
llm = ChatOpenAI(temperature=0)  
agent\_chain = initialize\_agent(  
 tools,  
 llm,  
 agent=AgentType.CHAT\_CONVERSATIONAL\_REACT\_DESCRIPTION,  
 verbose=True,  
 memory=memory,  
)  

```

```text
 ---------------------------------------------------------------------------  
  
 ValidationError Traceback (most recent call last)  
  
 Cell In[17], line 1  
 ----> 1 llm = ChatOpenAI(temperature=0)  
 2 agent\_chain = initialize\_agent(  
 3 tools,  
 4 llm,  
 (...)  
 7 memory=memory,  
 8 )  
  
  
 File ~/Documents/projects/langchain/libs/langchain/langchain/load/serializable.py:74, in Serializable.\_\_init\_\_(self, \*\*kwargs)  
 73 def \_\_init\_\_(self, \*\*kwargs: Any) -> None:  
 ---> 74 super().\_\_init\_\_(\*\*kwargs)  
 75 self.\_lc\_kwargs = kwargs  
  
  
 File ~/Documents/projects/langchain/.venv/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.\_\_init\_\_()  
  
  
 ValidationError: 1 validation error for ChatOpenAI  
 \_\_root\_\_  
 Did not find openai\_api\_key, please add an environment variable `OPENAI\_API\_KEY` which contains it, or pass `openai\_api\_key` as a named parameter. (type=value\_error)  

```

```python
agent\_chain.run(input="Hello!")  

```

```python
agent\_chain.run(input="Who owns Twitter?")  

```

```python
agent\_chain.run(input="My name is Bob.")  

```

```python
agent\_chain.run(input="Who am I?")  

```

- [DynamoDBChatMessageHistory](#dynamodbchatmessagehistory)

- [DynamoDBChatMessageHistory with Custom Endpoint URL](#dynamodbchatmessagehistory-with-custom-endpoint-url)

- [DynamoDBChatMessageHistory With Different Keys Composite Keys](#dynamodbchatmessagehistory-with-different-keys-composite-keys)

  - [Primary Key Name](#primary-key-name)
  - [Composite Keys](#composite-keys)

- [Agent with DynamoDB Memory](#agent-with-dynamodb-memory)

- [Primary Key Name](#primary-key-name)

- [Composite Keys](#composite-keys)
