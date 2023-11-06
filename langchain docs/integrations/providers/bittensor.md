# NIBittensor

This page covers how to use the BittensorLLM inference runtime within LangChain.
It is broken into two parts: installation and setup, and then examples of NIBittensorLLM usage.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install the Python package with `pip install langchain`

## Wrappers[​](#wrappers "Direct link to Wrappers")

### LLM[​](#llm "Direct link to LLM")

There exists a NIBittensor LLM wrapper, which you can access with:

```python
from langchain.llms import NIBittensorLLM  

```

It provides a unified interface for all models:

```python
llm = NIBittensorLLM(system\_prompt="Your task is to provide concise and accurate response based on user prompt")  
  
print(llm('Write a fibonacci function in python with golder ratio'))  

```

Multiple responses from top miners can be accessible using the `top_responses` parameter:

```python
multi\_response\_llm = NIBittensorLLM(top\_responses=10)  
multi\_resp = multi\_response\_llm("What is Neural Network Feeding Mechanism?")  
json\_multi\_resp = json.loads(multi\_resp)  
  
print(json\_multi\_resp)  

```

- [Installation and Setup](#installation-and-setup)

- [Wrappers](#wrappers)

  - [LLM](#llm)

- [LLM](#llm)
