# Token counting

LangChain offers a context manager that allows you to count tokens.

```python
import asyncio  
  
from langchain.callbacks import get\_openai\_callback  
from langchain.llms import OpenAI  
  
llm = OpenAI(temperature=0)  
with get\_openai\_callback() as cb:  
 llm("What is the square root of 4?")  
  
total\_tokens = cb.total\_tokens  
assert total\_tokens > 0  
  
with get\_openai\_callback() as cb:  
 llm("What is the square root of 4?")  
 llm("What is the square root of 4?")  
  
assert cb.total\_tokens == total\_tokens \* 2  
  
# You can kick off concurrent runs from within the context manager  
with get\_openai\_callback() as cb:  
 await asyncio.gather(  
 \*[llm.agenerate(["What is the square root of 4?"]) for \_ in range(3)]  
 )  
  
assert cb.total\_tokens == total\_tokens \* 3  
  
# The context manager is concurrency safe  
task = asyncio.create\_task(llm.agenerate(["What is the square root of 4?"]))  
with get\_openai\_callback() as cb:  
 await llm.agenerate(["What is the square root of 4?"])  
  
await task  
assert cb.total\_tokens == total\_tokens  

```
