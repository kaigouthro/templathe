# Trubrics

![Trubrics](https://miro.medium.com/v2/resize:fit:720/format:webp/1*AhYbKO-v8F4u3hx2aDIqKg.png)

![Trubrics](https://miro.medium.com/v2/resize:fit:720/format:webp/1*AhYbKO-v8F4u3hx2aDIqKg.png)

[Trubrics](https://trubrics.com) is an LLM user analytics platform that lets you collect, analyse and manage user
prompts & feedback on AI models. In this guide we will go over how to setup the `TrubricsCallbackHandler`.

Check out [our repo](https://github.com/trubrics/trubrics-sdk) for more information on Trubrics.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

```bash
pip install trubrics  

```

### Getting Trubrics Credentials[​](#getting-trubrics-credentials "Direct link to Getting Trubrics Credentials")

If you do not have a Trubrics account, create one on [here](https://trubrics.streamlit.app/). In this tutorial, we will use the `default` project that is built upon account creation.

Now set your credentials as environment variables:

```python
import os  
  
os.environ["TRUBRICS\_EMAIL"] = "\*\*\*@\*\*\*"  
os.environ["TRUBRICS\_PASSWORD"] = "\*\*\*"  

```

### Usage[​](#usage "Direct link to Usage")

The `TrubricsCallbackHandler` can receive various optional arguments. See [here](https://trubrics.github.io/trubrics-sdk/platform/user_prompts/#saving-prompts-to-trubrics) for kwargs that can be passed to Trubrics prompts.

```python
class TrubricsCallbackHandler(BaseCallbackHandler):  
  
 """  
 Callback handler for Trubrics.  
   
 Args:  
 project: a trubrics project, default project is "default"  
 email: a trubrics account email, can equally be set in env variables  
 password: a trubrics account password, can equally be set in env variables  
 \*\*kwargs: all other kwargs are parsed and set to trubrics prompt variables, or added to the `metadata` dict  
 """  

```

## Examples[​](#examples "Direct link to Examples")

Here are two examples of how to use the `TrubricsCallbackHandler` with Langchain [LLMs](https://python.langchain.com/docs/modules/model_io/models/llms/) or [Chat Models](https://python.langchain.com/docs/modules/model_io/models/chat/). We will use OpenAI models, so set your `OPENAI_API_KEY` key here:

```python
os.environ["OPENAI\_API\_KEY"] = "sk-\*\*\*"  

```

### 1. With an LLM[​](#1-with-an-llm "Direct link to 1. With an LLM")

```python
from langchain.llms import OpenAI  
from langchain.callbacks import TrubricsCallbackHandler  

```

```python
llm = OpenAI(callbacks=[TrubricsCallbackHandler()])  

```

```text
 [32m2023-09-26 11:30:02.149[0m | [1mINFO [0m | [36mtrubrics.platform.auth[0m:[36mget\_trubrics\_auth\_token[0m:[36m61[0m - [1mUser jeff.kayne@trubrics.com has been authenticated.[0m  

```

```python
res = llm.generate(["Tell me a joke", "Write me a poem"])  

```

```text
 [32m2023-09-26 11:30:07.760[0m | [1mINFO [0m | [36mtrubrics.platform[0m:[36mlog\_prompt[0m:[36m102[0m - [1mUser prompt saved to Trubrics.[0m  
 [32m2023-09-26 11:30:08.042[0m | [1mINFO [0m | [36mtrubrics.platform[0m:[36mlog\_prompt[0m:[36m102[0m - [1mUser prompt saved to Trubrics.[0m  

```

```python
print("--> GPT's joke: ", res.generations[0][0].text)  
print()  
print("--> GPT's poem: ", res.generations[1][0].text)  

```

```text
 --> GPT's joke:   
   
 Q: What did the fish say when it hit the wall?  
 A: Dam!  
   
 --> GPT's poem:   
   
 A Poem of Reflection  
   
 I stand here in the night,  
 The stars above me filling my sight.  
 I feel such a deep connection,  
 To the world and all its perfection.  
   
 A moment of clarity,  
 The calmness in the air so serene.  
 My mind is filled with peace,  
 And I am released.  
   
 The past and the present,  
 My thoughts create a pleasant sentiment.  
 My heart is full of joy,  
 My soul soars like a toy.  
   
 I reflect on my life,  
 And the choices I have made.  
 My struggles and my strife,  
 The lessons I have paid.  
   
 The future is a mystery,  
 But I am ready to take the leap.  
 I am ready to take the lead,  
 And to create my own destiny.  

```

### 2. With a chat model[​](#2-with-a-chat-model "Direct link to 2. With a chat model")

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.prompts import PromptTemplate  
from langchain.schema import HumanMessage, SystemMessage  
from langchain.callbacks import TrubricsCallbackHandler  

```

```python
chat\_llm = ChatOpenAI(  
 callbacks=[  
 TrubricsCallbackHandler(  
 project="default",  
 tags=["chat model"],  
 user\_id="user-id-1234",  
 some\_metadata={"hello": [1, 2]}  
 )  
 ]  
)  

```

```python
chat\_res = chat\_llm(  
 [  
 SystemMessage(content="Every answer of yours must be about OpenAI."),  
 HumanMessage(content="Tell me a joke"),  
 ]  
)  

```

```text
 [32m2023-09-26 11:30:10.550[0m | [1mINFO [0m | [36mtrubrics.platform[0m:[36mlog\_prompt[0m:[36m102[0m - [1mUser prompt saved to Trubrics.[0m  

```

```python
print(chat\_res.content)  

```

```text
 Why did the OpenAI computer go to the party?  
   
 Because it wanted to meet its AI friends and have a byte of fun!  

```

- [Installation and Setup](#installation-and-setup)

  - [Getting Trubrics Credentials](#getting-trubrics-credentials)
  - [Usage](#usage)

- [Examples](#examples)

  - [1. With an LLM](#1-with-an-llm)
  - [2. With a chat model](#2-with-a-chat-model)

- [Getting Trubrics Credentials](#getting-trubrics-credentials)

- [Usage](#usage)

- [1. With an LLM](#1-with-an-llm)

- [2. With a chat model](#2-with-a-chat-model)
