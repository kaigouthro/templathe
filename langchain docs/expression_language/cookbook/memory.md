# Adding memory

This shows how to add memory to an arbitrary chain. Right now, you can use the memory classes but need to hook it up manually

```python
from operator import itemgetter  
from langchain.chat\_models import ChatOpenAI  
from langchain.memory import ConversationBufferMemory  
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda  
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder  
  
model = ChatOpenAI()  
prompt = ChatPromptTemplate.from\_messages([  
 ("system", "You are a helpful chatbot"),  
 MessagesPlaceholder(variable\_name="history"),  
 ("human", "{input}")  
])  

```

```python
memory = ConversationBufferMemory(return\_messages=True)  

```

```python
memory.load\_memory\_variables({})  

```

```text
 {'history': []}  

```

```python
chain = RunnablePassthrough.assign(  
 memory=RunnableLambda(memory.load\_memory\_variables) | itemgetter("history")  
) | prompt | model  

```

```python
inputs = {"input": "hi im bob"}  
response = chain.invoke(inputs)  
response  

```

```text
 AIMessage(content='Hello Bob! How can I assist you today?', additional\_kwargs={}, example=False)  

```

```python
memory.save\_context(inputs, {"output": response.content})  

```

```python
memory.load\_memory\_variables({})  

```

```text
 {'history': [HumanMessage(content='hi im bob', additional\_kwargs={}, example=False),  
 AIMessage(content='Hello Bob! How can I assist you today?', additional\_kwargs={}, example=False)]}  

```

```python
inputs = {"input": "whats my name"}  
response = chain.invoke(inputs)  
response  

```

```text
 AIMessage(content='Your name is Bob.', additional\_kwargs={}, example=False)  

```
