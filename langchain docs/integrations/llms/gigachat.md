# GigaChat

This notebook shows how to use LangChain with [GigaChat](https://developers.sber.ru/portal/products/gigachat).
To use you need to install `gigachat` python package.

```python
# !pip install gigachat  

```

To get GigaChat credentials you need to [create account](https://developers.sber.ru/studio/login) and [get access to API](https://developers.sber.ru/docs/ru/gigachat/api/integration)

## Example[​](#example "Direct link to Example")

```python
import os  
from getpass import getpass  
  
os.environ['GIGACHAT\_CREDENTIALS'] = getpass()  

```

```python
from langchain.llms import GigaChat  
  
llm = GigaChat(verify\_ssl\_certs=False)  

```

```python
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
  
template = "What is capital of {country}?"  
  
prompt = PromptTemplate(template=template, input\_variables=["country"])  
  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
  
generated = llm\_chain.run(country="Russia")  
print(generated)  

```

```text
 The capital of Russia is Moscow.  

```

- [Example](#example)
