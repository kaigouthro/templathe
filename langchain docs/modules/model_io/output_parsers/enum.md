# Enum parser

This notebook shows how to use an Enum output parser.

```python
from langchain.output\_parsers.enum import EnumOutputParser  

```

```python
from enum import Enum  
  
  
class Colors(Enum):  
 RED = "red"  
 GREEN = "green"  
 BLUE = "blue"  

```

```python
parser = EnumOutputParser(enum=Colors)  

```

```python
parser.parse("red")  

```

```text
 <Colors.RED: 'red'>  

```

```python
# Can handle spaces  
parser.parse(" green")  

```

```text
 <Colors.GREEN: 'green'>  

```

```python
# And new lines  
parser.parse("blue\n")  

```

```text
 <Colors.BLUE: 'blue'>  

```

```python
# And raises errors when appropriate  
parser.parse("yellow")  

```

```text
 ---------------------------------------------------------------------------  
  
 ValueError Traceback (most recent call last)  
  
 File ~/workplace/langchain/langchain/output\_parsers/enum.py:25, in EnumOutputParser.parse(self, response)  
 24 try:  
 ---> 25 return self.enum(response.strip())  
 26 except ValueError:  
  
  
 File ~/.pyenv/versions/3.9.1/lib/python3.9/enum.py:315, in EnumMeta.\_\_call\_\_(cls, value, names, module, qualname, type, start)  
 314 if names is None: # simple value lookup  
 --> 315 return cls.\_\_new\_\_(cls, value)  
 316 # otherwise, functional API: we're creating a new Enum type  
  
  
 File ~/.pyenv/versions/3.9.1/lib/python3.9/enum.py:611, in Enum.\_\_new\_\_(cls, value)  
 610 if result is None and exc is None:  
 --> 611 raise ve\_exc  
 612 elif exc is None:  
  
  
 ValueError: 'yellow' is not a valid Colors  
  
   
 During handling of the above exception, another exception occurred:  
  
  
 OutputParserException Traceback (most recent call last)  
  
 Cell In[8], line 2  
 1 # And raises errors when appropriate  
 ----> 2 parser.parse("yellow")  
  
  
 File ~/workplace/langchain/langchain/output\_parsers/enum.py:27, in EnumOutputParser.parse(self, response)  
 25 return self.enum(response.strip())  
 26 except ValueError:  
 ---> 27 raise OutputParserException(  
 28 f"Response '{response}' is not one of the "  
 29 f"expected values: {self.\_valid\_values}"  
 30 )  
  
  
 OutputParserException: Response 'yellow' is not one of the expected values: ['red', 'green', 'blue']  

```
