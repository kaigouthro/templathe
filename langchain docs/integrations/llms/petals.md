# Petals

`Petals` runs 100B+ language models at home, BitTorrent-style.

This notebook goes over how to use Langchain with [Petals](https://github.com/bigscience-workshop/petals).

## Install petals[​](#install-petals "Direct link to Install petals")

The `petals` package is required to use the Petals API. Install `petals` using `pip3 install petals`.

For Apple Silicon(M1/M2) users please follow this guide <https://github.com/bigscience-workshop/petals/issues/147#issuecomment-1365379642> to install petals

```bash
pip3 install petals  

```

## Imports[​](#imports "Direct link to Imports")

```python
import os  
from langchain.llms import Petals  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

## Set the Environment API Key[​](#set-the-environment-api-key "Direct link to Set the Environment API Key")

Make sure to get [your API key](https://huggingface.co/docs/api-inference/quicktour#get-your-api-token) from Huggingface.

```python
from getpass import getpass  
  
HUGGINGFACE\_API\_KEY = getpass()  

```

```text
 ········  

```

```python
os.environ["HUGGINGFACE\_API\_KEY"] = HUGGINGFACE\_API\_KEY  

```

## Create the Petals instance[​](#create-the-petals-instance "Direct link to Create the Petals instance")

You can specify different parameters such as the model name, max new tokens, temperature, etc.

```python
# this can take several minutes to download big files!  
  
llm = Petals(model\_name="bigscience/bloom-petals")  

```

```text
 Downloading: 1%|▏ | 40.8M/7.19G [00:24<15:44, 7.57MB/s]  

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

- [Install petals](#install-petals)
- [Imports](#imports)
- [Set the Environment API Key](#set-the-environment-api-key)
- [Create the Petals instance](#create-the-petals-instance)
- [Create a Prompt Template](#create-a-prompt-template)
- [Initiate the LLMChain](#initiate-the-llmchain)
- [Run the LLMChain](#run-the-llmchain)
