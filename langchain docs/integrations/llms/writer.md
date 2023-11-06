# Writer

[Writer](https://writer.com/) is a platform to generate different language content.

This example goes over how to use LangChain to interact with `Writer` [models](https://dev.writer.com/docs/models).

You have to get the WRITER_API_KEY [here](https://dev.writer.com/docs).

```python
from getpass import getpass  
  
WRITER\_API\_KEY = getpass()  

```

```text
 ········  

```

```python
import os  
  
os.environ["WRITER\_API\_KEY"] = WRITER\_API\_KEY  

```

```python
from langchain.llms import Writer  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

```python
# If you get an error, probably, you need to set up the "base\_url" parameter that can be taken from the error log.  
  
llm = Writer()  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"  
  
llm\_chain.run(question)  

```
