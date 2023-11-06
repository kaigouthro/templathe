# Context

![Context - User Analytics for LLM Powered Products](https://with.context.ai/langchain.png)

![Context - User Analytics for LLM Powered Products](https://with.context.ai/langchain.png)

[Context](https://context.ai/) provides user analytics for LLM powered products and features.

With Context, you can start understanding your users and improving their experiences in less than 30 minutes.

In this guide we will show you how to integrate with Context.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

```python
$ pip install context-python --upgrade  

```

### Getting API Credentials[​](#getting-api-credentials "Direct link to Getting API Credentials")

To get your Context API token:

1. Go to the settings page within your Context account (<https://with.context.ai/settings>).
1. Generate a new API Token.
1. Store this token somewhere secure.

### Setup Context[​](#setup-context "Direct link to Setup Context")

To use the `ContextCallbackHandler`, import the handler from Langchain and instantiate it with your Context API token.

Ensure you have installed the `context-python` package before using the handler.

```python
import os  
  
from langchain.callbacks import ContextCallbackHandler  
  
token = os.environ["CONTEXT\_API\_TOKEN"]  
  
context\_callback = ContextCallbackHandler(token)  

```

## Usage[​](#usage "Direct link to Usage")

### Using the Context callback within a chat model[​](#using-the-context-callback-within-a-chat-model "Direct link to Using the Context callback within a chat model")

The Context callback handler can be used to directly record transcripts between users and AI assistants.

#### Example[​](#example "Direct link to Example")

```python
import os  
  
from langchain.chat\_models import ChatOpenAI  
from langchain.schema import (  
 SystemMessage,  
 HumanMessage,  
)  
from langchain.callbacks import ContextCallbackHandler  
  
token = os.environ["CONTEXT\_API\_TOKEN"]  
  
chat = ChatOpenAI(  
 headers={"user\_id": "123"}, temperature=0, callbacks=[ContextCallbackHandler(token)]  
)  
  
messages = [  
 SystemMessage(  
 content="You are a helpful assistant that translates English to French."  
 ),  
 HumanMessage(content="I love programming."),  
]  
  
print(chat(messages))  

```

### Using the Context callback within Chains[​](#using-the-context-callback-within-chains "Direct link to Using the Context callback within Chains")

The Context callback handler can also be used to record the inputs and outputs of chains. Note that intermediate steps of the chain are not recorded - only the starting inputs and final outputs.

**Note:** Ensure that you pass the same context object to the chat model and the chain.

Wrong:

```python
chat = ChatOpenAI(temperature=0.9, callbacks=[ContextCallbackHandler(token)])  
chain = LLMChain(llm=chat, prompt=chat\_prompt\_template, callbacks=[ContextCallbackHandler(token)])  

```

Correct:

```python
handler = ContextCallbackHandler(token)  
chat = ChatOpenAI(temperature=0.9, callbacks=[callback])  
chain = LLMChain(llm=chat, prompt=chat\_prompt\_template, callbacks=[callback])  

```

#### Example[​](#example-1 "Direct link to Example")

```python
import os  
  
from langchain.chat\_models import ChatOpenAI  
from langchain.chains import LLMChain  
from langchain.prompts import PromptTemplate  
from langchain.prompts.chat import (  
 ChatPromptTemplate,  
 HumanMessagePromptTemplate,  
)  
from langchain.callbacks import ContextCallbackHandler  
  
token = os.environ["CONTEXT\_API\_TOKEN"]  
  
human\_message\_prompt = HumanMessagePromptTemplate(  
 prompt=PromptTemplate(  
 template="What is a good name for a company that makes {product}?",  
 input\_variables=["product"],  
 )  
)  
chat\_prompt\_template = ChatPromptTemplate.from\_messages([human\_message\_prompt])  
callback = ContextCallbackHandler(token)  
chat = ChatOpenAI(temperature=0.9, callbacks=[callback])  
chain = LLMChain(llm=chat, prompt=chat\_prompt\_template, callbacks=[callback])  
print(chain.run("colorful socks"))  

```

- [Installation and Setup](#installation-and-setup)

  - [Getting API Credentials](#getting-api-credentials)
  - [Setup Context](#setup-context)

- [Usage](#usage)

  - [Using the Context callback within a chat model](#using-the-context-callback-within-a-chat-model)
  - [Using the Context callback within Chains](#using-the-context-callback-within-chains)

- [Getting API Credentials](#getting-api-credentials)

- [Setup Context](#setup-context)

- [Using the Context callback within a chat model](#using-the-context-callback-within-a-chat-model)

- [Using the Context callback within Chains](#using-the-context-callback-within-chains)
