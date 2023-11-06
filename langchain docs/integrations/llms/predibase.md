# Predibase

[Predibase](https://predibase.com/) allows you to train, fine-tune, and deploy any ML model—from linear regression to large language model.

This example demonstrates using Langchain with models deployed on Predibase

# Setup

To run this notebook, you'll need a [Predibase account](https://predibase.com/free-trial/?utm_source=langchain) and an [API key](https://docs.predibase.com/sdk-guide/intro).

You'll also need to install the Predibase Python package:

```bash
pip install predibase  
import os  
  
os.environ["PREDIBASE\_API\_TOKEN"] = "{PREDIBASE\_API\_TOKEN}"  

```

## Initial Call[​](#initial-call "Direct link to Initial Call")

```python
from langchain.llms import Predibase  
  
model = Predibase(  
 model="vicuna-13b", predibase\_api\_key=os.environ.get("PREDIBASE\_API\_TOKEN")  
)  

```

```python
response = model("Can you recommend me a nice dry wine?")  
print(response)  

```

## Chain Call Setup[​](#chain-call-setup "Direct link to Chain Call Setup")

```python
llm = Predibase(  
 model="vicuna-13b", predibase\_api\_key=os.environ.get("PREDIBASE\_API\_TOKEN")  
)  

```

## SequentialChain[​](#sequentialchain "Direct link to SequentialChain")

```python
from langchain.chains import LLMChain  
from langchain.prompts import PromptTemplate  

```

```python
# This is an LLMChain to write a synopsis given a title of a play.  
template = """You are a playwright. Given the title of play, it is your job to write a synopsis for that title.  
  
Title: {title}  
Playwright: This is a synopsis for the above play:"""  
prompt\_template = PromptTemplate(input\_variables=["title"], template=template)  
synopsis\_chain = LLMChain(llm=llm, prompt=prompt\_template)  

```

```python
# This is an LLMChain to write a review of a play given a synopsis.  
template = """You are a play critic from the New York Times. Given the synopsis of play, it is your job to write a review for that play.  
  
Play Synopsis:  
{synopsis}  
Review from a New York Times play critic of the above play:"""  
prompt\_template = PromptTemplate(input\_variables=["synopsis"], template=template)  
review\_chain = LLMChain(llm=llm, prompt=prompt\_template)  

```

```python
# This is the overall chain where we run these two chains in sequence.  
from langchain.chains import SimpleSequentialChain  
  
overall\_chain = SimpleSequentialChain(  
 chains=[synopsis\_chain, review\_chain], verbose=True  
)  

```

```python
review = overall\_chain.run("Tragedy at sunset on the beach")  

```

## Fine-tuned LLM (Use your own fine-tuned LLM from Predibase)[​](#fine-tuned-llm-use-your-own-fine-tuned-llm-from-predibase "Direct link to Fine-tuned LLM (Use your own fine-tuned LLM from Predibase)")

```python
from langchain.llms import Predibase  
  
model = Predibase(  
 model="my-finetuned-LLM", predibase\_api\_key=os.environ.get("PREDIBASE\_API\_TOKEN")  
)  
# replace my-finetuned-LLM with the name of your model in Predibase  

```

```python
# response = model("Can you help categorize the following emails into positive, negative, and neutral?")  

```

- [Initial Call](#initial-call)
- [Chain Call Setup](#chain-call-setup)
- [SequentialChain](#sequentialchain)
- [Fine-tuned LLM (Use your own fine-tuned LLM from Predibase)](#fine-tuned-llm-use-your-own-fine-tuned-llm-from-predibase)
