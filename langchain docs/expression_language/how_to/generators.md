# Custom generator functions

You can use generator functions (ie. functions that use the `yield` keyword, and behave like iterators) in a LCEL pipeline.

The signature of these generators should be `Iterator[Input] -> Iterator[Output]`. Or for async generators: `AsyncIterator[Input] -> AsyncIterator[Output]`.

These are useful for:

- implementing a custom output parser
- modifying the output of a previous step, while preserving streaming capabilities

Let's implement a custom output parser for comma-separated lists.

```python
from typing import Iterator, List  
  
from langchain.chat\_models import ChatOpenAI  
from langchain.prompts.chat import ChatPromptTemplate  
from langchain.schema.output\_parser import StrOutputParser  
  
  
prompt = ChatPromptTemplate.from\_template(  
 "Write a comma-separated list of 5 animals similar to: {animal}"  
)  
model = ChatOpenAI(temperature=0.0)  
  
  
str\_chain = prompt | model | StrOutputParser()  
  
print(str\_chain.invoke({"animal": "bear"}))  

```

```text
 lion, tiger, wolf, gorilla, panda  

```

```python
# This is a custom parser that splits an iterator of llm tokens  
# into a list of strings separated by commas  
def split\_into\_list(input: Iterator[str]) -> Iterator[List[str]]:  
 # hold partial input until we get a comma  
 buffer = ""  
 for chunk in input:  
 # add current chunk to buffer  
 buffer += chunk  
 # while there are commas in the buffer  
 while "," in buffer:  
 # split buffer on comma  
 comma\_index = buffer.index(",")  
 # yield everything before the comma  
 yield [buffer[:comma\_index].strip()]  
 # save the rest for the next iteration  
 buffer = buffer[comma\_index + 1 :]  
 # yield the last chunk  
 yield [buffer.strip()]  

```

```python
list\_chain = str\_chain | split\_into\_list  
  
print(list\_chain.invoke({"animal": "bear"}))  

```

```text
 ['lion', 'tiger', 'wolf', 'gorilla', 'panda']  

```
