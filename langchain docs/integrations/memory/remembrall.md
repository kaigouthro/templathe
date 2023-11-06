# Remembrall

This page covers how to use the [Remembrall](https://remembrall.dev) ecosystem within LangChain.

## What is Remembrall?[​](#what-is-remembrall "Direct link to What is Remembrall?")

Remembrall gives your language model long-term memory, retrieval augmented generation, and complete observability with just a few lines of code.

![Remembrall Dashboard](/assets/images/RemembrallDashboard-36b4f535ae0718f2f5923084caf111de.png)

![Remembrall Dashboard](/assets/images/RemembrallDashboard-36b4f535ae0718f2f5923084caf111de.png)

It works as a light-weight proxy on top of your OpenAI calls and simply augments the context of the chat calls at runtime with relevant facts that have been collected.

## Setup[​](#setup "Direct link to Setup")

To get started, [sign in with Github on the Remembrall platform](https://remembrall.dev/login) and copy your [API key from the settings page](https://remembrall.dev/dashboard/settings).

Any request that you send with the modified `openai_api_base` (see below) and Remembrall API key will automatically be tracked in the Remembrall dashboard. You **never** have to share your OpenAI key with our platform and this information is **never** stored by the Remembrall systems.

### Enable Long Term Memory[​](#enable-long-term-memory "Direct link to Enable Long Term Memory")

In addition to setting the `openai_api_base` and Remembrall API key via `x-gp-api-key`, you should specify a UID to maintain memory for. This will usually be a unique user identifier (like email).

```python
from langchain.chat\_models import ChatOpenAI  
chat\_model = ChatOpenAI(openai\_api\_base="https://remembrall.dev/api/openai/v1",  
 model\_kwargs={  
 "headers":{  
 "x-gp-api-key": "remembrall-api-key-here",  
 "x-gp-remember": "user@email.com",  
 }  
 })  
  
chat\_model.predict("My favorite color is blue.")  
import time; time.sleep(5) # wait for system to save fact via auto save  
print(chat\_model.predict("What is my favorite color?"))  

```

### Enable Retrieval Augmented Generation[​](#enable-retrieval-augmented-generation "Direct link to Enable Retrieval Augmented Generation")

First, create a document context in the [Remembrall dashboard](https://remembrall.dev/dashboard/spells). Paste in the document texts or upload documents as PDFs to be processed. Save the Document Context ID and insert it as shown below.

```python
from langchain.chat\_models import ChatOpenAI  
chat\_model = ChatOpenAI(openai\_api\_base="https://remembrall.dev/api/openai/v1",  
 model\_kwargs={  
 "headers":{  
 "x-gp-api-key": "remembrall-api-key-here",  
 "x-gp-context": "document-context-id-goes-here",  
 }  
 })  
  
print(chat\_model.predict("This is a question that can be answered with my document."))  

```

- [What is Remembrall?](#what-is-remembrall)

- [Setup](#setup)

  - [Enable Long Term Memory](#enable-long-term-memory)
  - [Enable Retrieval Augmented Generation](#enable-retrieval-augmented-generation)

- [Enable Long Term Memory](#enable-long-term-memory)

- [Enable Retrieval Augmented Generation](#enable-retrieval-augmented-generation)
