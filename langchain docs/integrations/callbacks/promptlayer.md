# PromptLayer

![PromptLayer](https://promptlayer.com/text_logo.png)

![PromptLayer](https://promptlayer.com/text_logo.png)

[PromptLayer](https://promptlayer.com) is a an LLM observability platform that lets you visualize requests, version prompts, and track usage. In this guide we will go over how to setup the `PromptLayerCallbackHandler`.

While PromptLayer does have LLMs that integrate directly with LangChain (e.g. [`PromptLayerOpenAI`](https://python.langchain.com/docs/integrations/llms/promptlayer_openai)), this callback is the recommended way to integrate PromptLayer with LangChain.

See [our docs](https://docs.promptlayer.com/languages/langchain) for more information.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

```bash
pip install promptlayer --upgrade  

```

### Getting API Credentials[​](#getting-api-credentials "Direct link to Getting API Credentials")

If you do not have a PromptLayer account, create one on [promptlayer.com](https://www.promptlayer.com). Then get an API key by clicking on the settings cog in the navbar and
set it as an environment variabled called `PROMPTLAYER_API_KEY`

### Usage[​](#usage "Direct link to Usage")

Getting started with `PromptLayerCallbackHandler` is fairly simple, it takes two optional arguments:

1. `pl_tags` - an optional list of strings that will be tracked as tags on PromptLayer.
1. `pl_id_callback` - an optional function that will take `promptlayer_request_id` as an argument. This ID can be used with all of PromptLayer's tracking features to track, metadata, scores, and prompt usage.

### Simple OpenAI Example[​](#simple-openai-example "Direct link to Simple OpenAI Example")

In this simple example we use `PromptLayerCallbackHandler` with `ChatOpenAI`. We add a PromptLayer tag named `chatopenai`

```python
import promptlayer # Don't forget this 🍰  
from langchain.callbacks import PromptLayerCallbackHandler  
from langchain.chat\_models import ChatOpenAI  
from langchain.schema import (  
 HumanMessage,  
)  
  
chat\_llm = ChatOpenAI(  
 temperature=0,  
 callbacks=[PromptLayerCallbackHandler(pl\_tags=["chatopenai"])],  
)  
llm\_results = chat\_llm(  
 [  
 HumanMessage(content="What comes after 1,2,3 ?"),  
 HumanMessage(content="Tell me another joke?"),  
 ]  
)  
print(llm\_results)  

```

### GPT4All Example[​](#gpt4all-example "Direct link to GPT4All Example")

```python
import promptlayer # Don't forget this 🍰  
from langchain.callbacks import PromptLayerCallbackHandler  
  
from langchain.llms import GPT4All  
  
model = GPT4All(model="./models/gpt4all-model.bin", n\_ctx=512, n\_threads=8)  
  
response = model(  
 "Once upon a time, ",  
 callbacks=[PromptLayerCallbackHandler(pl\_tags=["langchain", "gpt4all"])],  
)  

```

### Full Featured Example[​](#full-featured-example "Direct link to Full Featured Example")

In this example we unlock more of the power of PromptLayer.

PromptLayer allows you to visually create, version, and track prompt templates. Using the [Prompt Registry](https://docs.promptlayer.com/features/prompt-registry), we can programmatically fetch the prompt template called `example`.

We also define a `pl_id_callback` function which takes in the `promptlayer_request_id` and logs a score, metadata and links the prompt template used. Read more about tracking on [our docs](https://docs.promptlayer.com/features/prompt-history/request-id).

```python
import promptlayer # Don't forget this 🍰  
from langchain.callbacks import PromptLayerCallbackHandler  
from langchain.llms import OpenAI  
  
  
def pl\_id\_callback(promptlayer\_request\_id):  
 print("prompt layer id ", promptlayer\_request\_id)  
 promptlayer.track.score(  
 request\_id=promptlayer\_request\_id, score=100  
 ) # score is an integer 0-100  
 promptlayer.track.metadata(  
 request\_id=promptlayer\_request\_id, metadata={"foo": "bar"}  
 ) # metadata is a dictionary of key value pairs that is tracked on PromptLayer  
 promptlayer.track.prompt(  
 request\_id=promptlayer\_request\_id,  
 prompt\_name="example",  
 prompt\_input\_variables={"product": "toasters"},  
 version=1,  
 ) # link the request to a prompt template  
  
  
openai\_llm = OpenAI(  
 model\_name="text-davinci-002",  
 callbacks=[PromptLayerCallbackHandler(pl\_id\_callback=pl\_id\_callback)],  
)  
  
example\_prompt = promptlayer.prompts.get("example", version=1, langchain=True)  
openai\_llm(example\_prompt.format(product="toasters"))  

```

That is all it takes! After setup all your requests will show up on the PromptLayer dashboard.
This callback also works with any LLM implemented on LangChain.

- [Installation and Setup](#installation-and-setup)

  - [Getting API Credentials](#getting-api-credentials)
  - [Usage](#usage)
  - [Simple OpenAI Example](#simple-openai-example)
  - [GPT4All Example](#gpt4all-example)
  - [Full Featured Example](#full-featured-example)

- [Getting API Credentials](#getting-api-credentials)

- [Usage](#usage)

- [Simple OpenAI Example](#simple-openai-example)

- [GPT4All Example](#gpt4all-example)

- [Full Featured Example](#full-featured-example)
