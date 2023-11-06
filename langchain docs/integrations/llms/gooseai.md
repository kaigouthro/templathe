# GooseAI

`GooseAI` is a fully managed NLP-as-a-Service, delivered via API. GooseAI provides access to [these models](https://goose.ai/docs/models).

This notebook goes over how to use Langchain with [GooseAI](https://goose.ai/).

## Install openai[​](#install-openai "Direct link to Install openai")

The `openai` package is required to use the GooseAI API. Install `openai` using `pip3 install openai`.

```python
$ pip3 install openai  

```

## Imports[​](#imports "Direct link to Imports")

```python
import os  
from langchain.llms import GooseAI  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

## Set the Environment API Key[​](#set-the-environment-api-key "Direct link to Set the Environment API Key")

Make sure to get your API key from GooseAI. You are given $10 in free credits to test different models.

```python
from getpass import getpass  
  
GOOSEAI\_API\_KEY = getpass()  

```

```python
os.environ["GOOSEAI\_API\_KEY"] = GOOSEAI\_API\_KEY  

```

## Create the GooseAI instance[​](#create-the-gooseai-instance "Direct link to Create the GooseAI instance")

You can specify different parameters such as the model name, max tokens generated, temperature, etc.

```python
llm = GooseAI()  

```

## Create a Prompt Template[​](#create-a-prompt-template "Direct link to Create a Prompt Template")

We will create a prompt template for Question and Answer.

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

## Initiate the LLMChain[​](#initiate-the-llmchain "Direct link to Initiate the LLMChain")

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

## Run the LLMChain[​](#run-the-llmchain "Direct link to Run the LLMChain")

Provide a question and run the LLMChain.

```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"  
  
llm\_chain.run(question)  

```

- [Install openai](#install-openai)
- [Imports](#imports)
- [Set the Environment API Key](#set-the-environment-api-key)
- [Create the GooseAI instance](#create-the-gooseai-instance)
- [Create a Prompt Template](#create-a-prompt-template)
- [Initiate the LLMChain](#initiate-the-llmchain)
- [Run the LLMChain](#run-the-llmchain)
