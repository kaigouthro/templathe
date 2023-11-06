# Code writing

Example of how to use LCEL to write Python code.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate  
from langchain.schema.output\_parser import StrOutputParser  
from langchain.utilities import PythonREPL  

```

````python
template = """Write some python code to solve the user's problem.   
  
Return only python code in Markdown format, e.g.:  
  
```python  
....  
```"""  
prompt = ChatPromptTemplate.from\_messages(  
 [("system", template), ("human", "{input}")]  
)  
  
model = ChatOpenAI()  

````

````python
def \_sanitize\_output(text: str):  
 \_, after = text.split("```python")  
 return after.split("```")[0]  

````

```python
chain = prompt | model | StrOutputParser() | \_sanitize\_output | PythonREPL().run  

```

```python
chain.invoke({"input": "whats 2 plus 2"})  

```

```text
 Python REPL can execute arbitrary code. Use with caution.  
  
  
  
  
  
 '4\n'  

```
