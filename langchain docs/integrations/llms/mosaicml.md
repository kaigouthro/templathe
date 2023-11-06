# MosaicML

[MosaicML](https://docs.mosaicml.com/en/latest/inference.html) offers a managed inference service. You can either use a variety of open-source models, or deploy your own.

This example goes over how to use LangChain to interact with MosaicML Inference for text completion.

```python
# sign up for an account: https://forms.mosaicml.com/demo?utm\_source=langchain  
  
from getpass import getpass  
  
MOSAICML\_API\_TOKEN = getpass()  

```

```python
import os  
  
os.environ["MOSAICML\_API\_TOKEN"] = MOSAICML\_API\_TOKEN  

```

```python
from langchain.llms import MosaicML  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
template = """Question: {question}"""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

```python
llm = MosaicML(inject\_instruction\_format=True, model\_kwargs={"max\_new\_tokens": 128})  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
question = "What is one good reason why you should train a large language model on domain specific data?"  
  
llm\_chain.run(question)  

```
