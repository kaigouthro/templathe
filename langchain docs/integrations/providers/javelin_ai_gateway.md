# Javelin AI Gateway

[The Javelin AI Gateway](https://www.getjavelin.io) service is a high-performance, enterprise grade API Gateway for AI applications.

It is designed to streamline the usage and access of various large language model (LLM) providers,
such as OpenAI, Cohere, Anthropic and custom large language models within an organization by incorporating
robust access security for all interactions with LLMs.

Javelin offers a high-level interface that simplifies the interaction with LLMs by providing a unified endpoint
to handle specific LLM related requests.

See the Javelin AI Gateway [documentation](https://docs.getjavelin.io) for more details.

[Javelin Python SDK](https://www.github.com/getjavelin/javelin-python) is an easy to use client library meant to be embedded into AI Applications

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

Install `javelin_sdk` to interact with Javelin AI Gateway:

```sh
pip install 'javelin\_sdk'  

```

Set the Javelin's API key as an environment variable:

```sh
export JAVELIN\_API\_KEY=...  

```

## Completions Example[​](#completions-example "Direct link to Completions Example")

```python
  
from langchain.chains import LLMChain  
from langchain.llms import JavelinAIGateway  
from langchain.prompts import PromptTemplate  
  
route\_completions = "eng\_dept03"  
  
gateway = JavelinAIGateway(  
 gateway\_uri="http://localhost:8000",  
 route=route\_completions,  
 model\_name="text-davinci-003",  
)  
  
llmchain = LLMChain(llm=gateway, prompt=prompt)  
result = llmchain.run("podcast player")  
  
print(result)  
  

```

## Embeddings Example[​](#embeddings-example "Direct link to Embeddings Example")

```python
from langchain.embeddings import JavelinAIGatewayEmbeddings  
from langchain.embeddings.openai import OpenAIEmbeddings  
  
embeddings = JavelinAIGatewayEmbeddings(  
 gateway\_uri="http://localhost:8000",  
 route="embeddings",  
)  
  
print(embeddings.embed\_query("hello"))  
print(embeddings.embed\_documents(["hello"]))  

```

## Chat Example[​](#chat-example "Direct link to Chat Example")

```python
from langchain.chat\_models import ChatJavelinAIGateway  
from langchain.schema import HumanMessage, SystemMessage  
  
messages = [  
 SystemMessage(  
 content="You are a helpful assistant that translates English to French."  
 ),  
 HumanMessage(  
 content="Artificial Intelligence has the power to transform humanity and make the world a better place"  
 ),  
]  
  
chat = ChatJavelinAIGateway(  
 gateway\_uri="http://localhost:8000",  
 route="mychatbot\_route",  
 model\_name="gpt-3.5-turbo"  
 params={  
 "temperature": 0.1  
 }  
)  
  
print(chat(messages))  
  

```

- [Installation and Setup](#installation-and-setup)
- [Completions Example](#completions-example)
- [Embeddings Example](#embeddings-example)
- [Chat Example](#chat-example)
