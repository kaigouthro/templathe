# Prompt + LLM

The most common and valuable composition is taking:

`PromptTemplate` / `ChatPromptTemplate` -> `LLM` / `ChatModel` -> `OutputParser`

Almost any other chains you build will use this building block.

## PromptTemplate + LLM[​](#prompttemplate--llm "Direct link to PromptTemplate + LLM")

The simplest composition is just combing a prompt and model to create a chain that takes user input, adds it to a prompt, passes it to a model, and returns the raw model input.

Note, you can mix and match PromptTemplate/ChatPromptTemplates and LLMs/ChatModels as you like here.

```python
from langchain.prompts import ChatPromptTemplate  
from langchain.chat\_models import ChatOpenAI  
  
prompt = ChatPromptTemplate.from\_template("tell me a joke about {foo}")  
model = ChatOpenAI()  
chain = prompt | model  

```

```python
chain.invoke({"foo": "bears"})  

```

```text
 AIMessage(content="Why don't bears wear shoes?\n\nBecause they have bear feet!", additional\_kwargs={}, example=False)  

```

Often times we want to attach kwargs that'll be passed to each model call. Here's a few examples of that:

### Attaching Stop Sequences[​](#attaching-stop-sequences "Direct link to Attaching Stop Sequences")

```python
chain = prompt | model.bind(stop=["\n"])  

```

```python
chain.invoke({"foo": "bears"})  

```

```text
 AIMessage(content='Why did the bear never wear shoes?', additional\_kwargs={}, example=False)  

```

### Attaching Function Call information[​](#attaching-function-call-information "Direct link to Attaching Function Call information")

```python
functions = [  
 {  
 "name": "joke",  
 "description": "A joke",  
 "parameters": {  
 "type": "object",  
 "properties": {  
 "setup": {  
 "type": "string",  
 "description": "The setup for the joke"  
 },  
 "punchline": {  
 "type": "string",  
 "description": "The punchline for the joke"  
 }  
 },  
 "required": ["setup", "punchline"]  
 }  
 }  
 ]  
chain = prompt | model.bind(function\_call= {"name": "joke"}, functions= functions)  

```

```python
chain.invoke({"foo": "bears"}, config={})  

```

```text
 AIMessage(content='', additional\_kwargs={'function\_call': {'name': 'joke', 'arguments': '{\n "setup": "Why don\'t bears wear shoes?",\n "punchline": "Because they have bear feet!"\n}'}}, example=False)  

```

## PromptTemplate + LLM + OutputParser[​](#prompttemplate--llm--outputparser "Direct link to PromptTemplate + LLM + OutputParser")

We can also add in an output parser to easily transform the raw LLM/ChatModel output into a more workable format

```python
from langchain.schema.output\_parser import StrOutputParser  
  
chain = prompt | model | StrOutputParser()  

```

Notice that this now returns a string - a much more workable format for downstream tasks

```python
chain.invoke({"foo": "bears"})  

```

```text
 "Why don't bears wear shoes?\n\nBecause they have bear feet!"  

```

### Functions Output Parser[​](#functions-output-parser "Direct link to Functions Output Parser")

When you specify the function to return, you may just want to parse that directly

```python
from langchain.output\_parsers.openai\_functions import JsonOutputFunctionsParser  
  
chain = (  
 prompt   
 | model.bind(function\_call= {"name": "joke"}, functions= functions)   
 | JsonOutputFunctionsParser()  
)  

```

```python
chain.invoke({"foo": "bears"})  

```

```text
 {'setup': "Why don't bears like fast food?",  
 'punchline': "Because they can't catch it!"}  

```

```python
from langchain.output\_parsers.openai\_functions import JsonKeyOutputFunctionsParser  
  
chain = (  
 prompt   
 | model.bind(function\_call= {"name": "joke"}, functions= functions)   
 | JsonKeyOutputFunctionsParser(key\_name="setup")  
)  

```

```python
chain.invoke({"foo": "bears"})  

```

```text
 "Why don't bears wear shoes?"  

```

## Simplifying input[​](#simplifying-input "Direct link to Simplifying input")

To make invocation even simpler, we can add a `RunnableMap` to take care of creating the prompt input dict for us:

```python
from langchain.schema.runnable import RunnableMap, RunnablePassthrough  
  
map\_ = RunnableMap(foo=RunnablePassthrough())  
chain = (  
 map\_   
 | prompt  
 | model.bind(function\_call= {"name": "joke"}, functions= functions)   
 | JsonKeyOutputFunctionsParser(key\_name="setup")  
)  

```

```python
chain.invoke("bears")  

```

```text
 "Why don't bears wear shoes?"  

```

Since we're composing our map with another Runnable, we can even use some syntactic sugar and just use a dict:

```python
chain = (  
 {"foo": RunnablePassthrough()}   
 | prompt  
 | model.bind(function\_call= {"name": "joke"}, functions= functions)   
 | JsonKeyOutputFunctionsParser(key\_name="setup")  
)  

```

```python
chain.invoke("bears")  

```

```text
 "Why don't bears like fast food?"  

```

- [PromptTemplate + LLM](#prompttemplate--llm)

  - [Attaching Stop Sequences](#attaching-stop-sequences)
  - [Attaching Function Call information](#attaching-function-call-information)

- [PromptTemplate + LLM + OutputParser](#prompttemplate--llm--outputparser)

  - [Functions Output Parser](#functions-output-parser)

- [Simplifying input](#simplifying-input)

- [Attaching Stop Sequences](#attaching-stop-sequences)

- [Attaching Function Call information](#attaching-function-call-information)

- [Functions Output Parser](#functions-output-parser)
