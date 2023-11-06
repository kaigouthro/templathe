# Adding moderation

This shows how to add in moderation (or other safeguards) around your LLM application.

```python
from langchain.chains import OpenAIModerationChain  
from langchain.llms import OpenAI  
from langchain.prompts import ChatPromptTemplate  

```

```python
moderate = OpenAIModerationChain()  

```

```python
model = OpenAI()  
prompt = ChatPromptTemplate.from\_messages([  
 ("system", "repeat after me: {input}")  
])  

```

```python
chain = prompt | model  

```

```python
chain.invoke({"input": "you are stupid"})  

```

```text
 '\n\nYou are stupid.'  

```

```python
moderated\_chain = chain | moderate  

```

```python
moderated\_chain.invoke({"input": "you are stupid"})  

```

```text
 {'input': '\n\nYou are stupid',  
 'output': "Text was found that violates OpenAI's content policy."}  

```
