# Tools as OpenAI Functions

This notebook goes over how to use LangChain tools as OpenAI functions.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.schema import HumanMessage  

```

```python
model = ChatOpenAI(model="gpt-3.5-turbo-0613")  

```

```python
from langchain.tools import MoveFileTool, format\_tool\_to\_openai\_function  

```

```python
tools = [MoveFileTool()]  
functions = [format\_tool\_to\_openai\_function(t) for t in tools]  

```

```python
message = model.predict\_messages(  
 [HumanMessage(content="move file foo to bar")], functions=functions  
)  

```

```python
message  

```

```text
 AIMessage(content='', additional\_kwargs={'function\_call': {'name': 'move\_file', 'arguments': '{\n "source\_path": "foo",\n "destination\_path": "bar"\n}'}}, example=False)  

```

```python
message.additional\_kwargs["function\_call"]  

```

```text
 {'name': 'move\_file',  
 'arguments': '{\n "source\_path": "foo",\n "destination\_path": "bar"\n}'}  

```
