# Auto-fixing parser

This output parser wraps another output parser, and in the event that the first one fails it calls out to another LLM to fix any errors.

But we can do other things besides throw errors. Specifically, we can pass the misformatted output, along with the formatted instructions, to the model and ask it to fix it.

For this example, we'll use the above Pydantic output parser. Here's what happens if we pass it a result that does not comply with the schema:

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.output\_parsers import PydanticOutputParser  
from langchain.pydantic\_v1 import BaseModel, Field  
from typing import List  

```

```python
class Actor(BaseModel):  
 name: str = Field(description="name of an actor")  
 film\_names: List[str] = Field(description="list of names of films they starred in")  
  
actor\_query = "Generate the filmography for a random actor."  
  
parser = PydanticOutputParser(pydantic\_object=Actor)  

```

```python
misformatted = "{'name': 'Tom Hanks', 'film\_names': ['Forrest Gump']}"  

```

```python
parser.parse(misformatted)  

```

```text
 ---------------------------------------------------------------------------  
  
 JSONDecodeError Traceback (most recent call last)  
  
 File ~/workplace/langchain/langchain/output\_parsers/pydantic.py:23, in PydanticOutputParser.parse(self, text)  
 22 json\_str = match.group()  
 ---> 23 json\_object = json.loads(json\_str)  
 24 return self.pydantic\_object.parse\_obj(json\_object)  
  
  
 File ~/.pyenv/versions/3.9.1/lib/python3.9/json/\_\_init\_\_.py:346, in loads(s, cls, object\_hook, parse\_float, parse\_int, parse\_constant, object\_pairs\_hook, \*\*kw)  
 343 if (cls is None and object\_hook is None and  
 344 parse\_int is None and parse\_float is None and  
 345 parse\_constant is None and object\_pairs\_hook is None and not kw):  
 --> 346 return \_default\_decoder.decode(s)  
 347 if cls is None:  
  
  
 File ~/.pyenv/versions/3.9.1/lib/python3.9/json/decoder.py:337, in JSONDecoder.decode(self, s, \_w)  
 333 """Return the Python representation of ``s`` (a ``str`` instance  
 334 containing a JSON document).  
 335  
 336 """  
 --> 337 obj, end = self.raw\_decode(s, idx=\_w(s, 0).end())  
 338 end = \_w(s, end).end()  
  
  
 File ~/.pyenv/versions/3.9.1/lib/python3.9/json/decoder.py:353, in JSONDecoder.raw\_decode(self, s, idx)  
 352 try:  
 --> 353 obj, end = self.scan\_once(s, idx)  
 354 except StopIteration as err:  
  
  
 JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)  
  
  
 During handling of the above exception, another exception occurred:  
  
  
 OutputParserException Traceback (most recent call last)  
  
 Cell In[6], line 1  
 ----> 1 parser.parse(misformatted)  
  
  
 File ~/workplace/langchain/langchain/output\_parsers/pydantic.py:29, in PydanticOutputParser.parse(self, text)  
 27 name = self.pydantic\_object.\_\_name\_\_  
 28 msg = f"Failed to parse {name} from completion {text}. Got: {e}"  
 ---> 29 raise OutputParserException(msg)  
  
  
 OutputParserException: Failed to parse Actor from completion {'name': 'Tom Hanks', 'film\_names': ['Forrest Gump']}. Got: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)  

```

Now we can construct and use a `OutputFixingParser`. This output parser takes as an argument another output parser but also an LLM with which to try to correct any formatting mistakes.

```python
from langchain.output\_parsers import OutputFixingParser  
  
new\_parser = OutputFixingParser.from\_llm(parser=parser, llm=ChatOpenAI())  

```

```python
new\_parser.parse(misformatted)  

```

```text
 Actor(name='Tom Hanks', film\_names=['Forrest Gump'])  

```
