# Banana

[Banana](https://www.banana.dev/about-us) is focused on building the machine learning infrastructure.

This example goes over how to use LangChain to interact with Banana models

```bash
# Install the package https://docs.banana.dev/banana-docs/core-concepts/sdks/python  
pip install banana-dev  

```

```python
# get new tokens: https://app.banana.dev/  
# We need three parameters to make a Banana.dev API call:  
# \* a team api key  
# \* the model's unique key  
# \* the model's url slug  
  
import os  
from getpass import getpass  
  
# You can get this from the main dashboard  
# at https://app.banana.dev  
os.environ["BANANA\_API\_KEY"] = "YOUR\_API\_KEY"  
# OR  
# BANANA\_API\_KEY = getpass()  

```

```python
from langchain.llms import Banana  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

```python
# Both of these are found in your model's   
# detail page in https://app.banana.dev  
llm = Banana(model\_key="YOUR\_MODEL\_KEY", model\_url\_slug="YOUR\_MODEL\_URL\_SLUG")  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"  
  
llm\_chain.run(question)  

```
