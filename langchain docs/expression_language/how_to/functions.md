# Run arbitrary functions

You can use arbitrary functions in the pipeline

Note that all inputs to these functions need to be a SINGLE argument. If you have a function that accepts multiple arguments, you should write a wrapper that accepts a single input and unpacks it into multiple argument.

```python
from langchain.schema.runnable import RunnableLambda  
from langchain.prompts import ChatPromptTemplate  
from langchain.chat\_models import ChatOpenAI  
from operator import itemgetter  
  
def length\_function(text):  
 return len(text)  
  
def \_multiple\_length\_function(text1, text2):  
 return len(text1) \* len(text2)  
  
def multiple\_length\_function(\_dict):  
 return \_multiple\_length\_function(\_dict["text1"], \_dict["text2"])  
  
prompt = ChatPromptTemplate.from\_template("what is {a} + {b}")  
model = ChatOpenAI()  
  
chain1 = prompt | model  
  
chain = {  
 "a": itemgetter("foo") | RunnableLambda(length\_function),  
 "b": {"text1": itemgetter("foo"), "text2": itemgetter("bar")} | RunnableLambda(multiple\_length\_function)  
} | prompt | model  

```

```python
chain.invoke({"foo": "bar", "bar": "gah"})  

```

```text
 AIMessage(content='3 + 9 equals 12.', additional\_kwargs={}, example=False)  

```

## Accepting a Runnable Config[​](#accepting-a-runnable-config "Direct link to Accepting a Runnable Config")

Runnable lambdas can optionally accept a [RunnableConfig](https://api.python.langchain.com/en/latest/schema/langchain.schema.runnable.config.RunnableConfig.html?highlight=runnableconfig#langchain.schema.runnable.config.RunnableConfig), which they can use to pass callbacks, tags, and other configuration information to nested runs.

```python
from langchain.schema.runnable import RunnableConfig  
from langchain.schema.output\_parser import StrOutputParser  

```

````python
import json  
  
def parse\_or\_fix(text: str, config: RunnableConfig):  
 fixing\_chain = (  
 ChatPromptTemplate.from\_template(  
 "Fix the following text:\n\n```text\n{input}\n```\nError: {error}"  
 " Don't narrate, just respond with the fixed data."  
 )  
 | ChatOpenAI()  
 | StrOutputParser()  
 )  
 for \_ in range(3):  
 try:  
 return json.loads(text)  
 except Exception as e:  
 text = fixing\_chain.invoke({"input": text, "error": e}, config)  
 return "Failed to parse"  

````

```python
from langchain.callbacks import get\_openai\_callback  
  
with get\_openai\_callback() as cb:  
 RunnableLambda(parse\_or\_fix).invoke("{foo: bar}", {"tags": ["my-tag"], "callbacks": [cb]})  
 print(cb)  

```

```text
 Tokens Used: 65  
 Prompt Tokens: 56  
 Completion Tokens: 9  
 Successful Requests: 1  
 Total Cost (USD): $0.00010200000000000001  

```

- [Accepting a Runnable Config](#accepting-a-runnable-config)
