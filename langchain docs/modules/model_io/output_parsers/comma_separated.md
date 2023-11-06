# List parser

This output parser can be used when you want to return a list of comma-separated items.

```python
from langchain.output\_parsers import CommaSeparatedListOutputParser  
from langchain.prompts import PromptTemplate  
from langchain.llms import OpenAI  
  
output\_parser = CommaSeparatedListOutputParser()  
  
format\_instructions = output\_parser.get\_format\_instructions()  
prompt = PromptTemplate(  
 template="List five {subject}.\n{format\_instructions}",  
 input\_variables=["subject"],  
 partial\_variables={"format\_instructions": format\_instructions}  
)  
  
model = OpenAI(temperature=0)  
  
\_input = prompt.format(subject="ice cream flavors")  
output = model(\_input)  
  
output\_parser.parse(output)  

```

The resulting output will be:

```text
 ['Vanilla',  
 'Chocolate',  
 'Strawberry',  
 'Mint Chocolate Chip',  
 'Cookies and Cream']  

```
