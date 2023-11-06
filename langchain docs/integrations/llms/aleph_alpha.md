# Aleph Alpha

[The Luminous series](https://docs.aleph-alpha.com/docs/introduction/luminous/) is a family of large language models.

This example goes over how to use LangChain to interact with Aleph Alpha models

```bash
# Install the package  
pip install aleph-alpha-client  

```

```python
# create a new token: https://docs.aleph-alpha.com/docs/account/#create-a-new-token  
  
from getpass import getpass  
  
ALEPH\_ALPHA\_API\_KEY = getpass()  

```

```text
 ········  

```

```python
from langchain.llms import AlephAlpha  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
template = """Q: {question}  
  
A:"""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

```python
llm = AlephAlpha(  
 model="luminous-extended",  
 maximum\_tokens=20,  
 stop\_sequences=["Q:"],  
 aleph\_alpha\_api\_key=ALEPH\_ALPHA\_API\_KEY,  
)  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
question = "What is AI?"  
  
llm\_chain.run(question)  

```

```text
 ' Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems.\n'  

```
