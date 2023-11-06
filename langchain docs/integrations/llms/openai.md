# OpenAI

[OpenAI](https://platform.openai.com/docs/introduction) offers a spectrum of models with different levels of power suitable for different tasks.

This example goes over how to use LangChain to interact with `OpenAI` [models](https://platform.openai.com/docs/models)

```python
# get a token: https://platform.openai.com/account/api-keys  
  
from getpass import getpass  
  
OPENAI\_API\_KEY = getpass()  

```

```python
import os  
  
os.environ["OPENAI\_API\_KEY"] = OPENAI\_API\_KEY  

```

Should you need to specify your organization ID, you can use the following cell. However, it is not required if you are only part of a single organization or intend to use your default organization. You can check your default organization [here](https://platform.openai.com/account/api-keys).

To specify your organization, you can use this:

```python
OPENAI\_ORGANIZATION = getpass()  
  
os.environ["OPENAI\_ORGANIZATION"] = OPENAI\_ORGANIZATION  

```

```python
from langchain.llms import OpenAI  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

```python
llm = OpenAI()  

```

If you manually want to specify your OpenAI API key and/or organization ID, you can use the following:

```python
llm = OpenAI(openai\_api\_key="YOUR\_API\_KEY", openai\_organization="YOUR\_ORGANIZATION\_ID")  

```

Remove the openai_organization parameter should it not apply to you.

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"  
  
llm\_chain.run(question)  

```

```text
 ' Justin Bieber was born in 1994, so the NFL team that won the Super Bowl in 1994 was the Dallas Cowboys.'  

```

If you are behind an explicit proxy, you can use the OPENAI_PROXY environment variable to pass through

```python
os.environ["OPENAI\_PROXY"] = "http://proxy.yourcompany.com:8080"  

```
