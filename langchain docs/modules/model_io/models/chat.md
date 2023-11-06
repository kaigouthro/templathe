# Chat models

Head to [Integrations](/docs/integrations/chat/) for documentation on built-in integrations with chat model providers.

Chat models are a variation on language models.
While chat models use language models under the hood, the interface they use is a bit different.
Rather than using a "text in, text out" API, they use an interface where "chat messages" are the inputs and outputs.

## Get started[​](#get-started "Direct link to Get started")

### Setup[​](#setup "Direct link to Setup")

For this example we'll need to install the OpenAI Python package:

```bash
pip install openai  

```

Accessing the API requires an API key, which you can get by creating an account and heading [here](https://platform.openai.com/account/api-keys). Once we have a key we'll want to set it as an environment variable by running:

```bash
export OPENAI\_API\_KEY="..."  

```

If you'd prefer not to set an environment variable you can pass the key in directly via the `openai_api_key` named parameter when initiating the OpenAI LLM class:

```python
from langchain.chat\_models import ChatOpenAI  
  
chat = ChatOpenAI(openai\_api\_key="...")  

```

Otherwise you can initialize without any params:

```python
from langchain.chat\_models import ChatOpenAI  
  
chat = ChatOpenAI()  

```

### Messages[​](#messages "Direct link to Messages")

The chat model interface is based around messages rather than raw text.
The types of messages currently supported in LangChain are `AIMessage`, `HumanMessage`, `SystemMessage`, `FunctionMessage` and `ChatMessage` -- `ChatMessage` takes in an arbitrary role parameter. Most of the time, you'll just be dealing with `HumanMessage`, `AIMessage`, and `SystemMessage`

### LCEL[​](#lcel "Direct link to LCEL")

Chat models implement the [Runnable interface](/docs/expression_language/interface), the basic building block of the [LangChain Expression Language (LCEL)](/docs/expression_language/). This means they support `invoke`, `ainvoke`, `stream`, `astream`, `batch`, `abatch`, `astream_log` calls.

Chat models accept `List[BaseMessage]` as inputs, or objects which can be coerced to messages, including `str` (converted to `HumanMessage`) and `PromptValue`.

```python
from langchain.schema.messages import HumanMessage, SystemMessage  
  
messages = [  
 SystemMessage(content="You're a helpful assistant"),   
 HumanMessage(content="What is the purpose of model regularization?")  
]  

```

```python
chat.invoke(messages)  

```

```text
 AIMessage(content="The purpose of model regularization is to prevent overfitting in machine learning models. Overfitting occurs when a model becomes too complex and starts to fit the noise in the training data, leading to poor generalization on unseen data. Regularization techniques introduce additional constraints or penalties to the model's objective function, discouraging it from becoming overly complex and promoting simpler and more generalizable models. Regularization helps to strike a balance between fitting the training data well and avoiding overfitting, leading to better performance on new, unseen data.")  

```

```python
for chunk in chat.stream(messages):  
 print(chunk.content, end="", flush=True)  

```

```text
 The purpose of model regularization is to prevent overfitting and improve the generalization of a machine learning model. Overfitting occurs when a model is too complex and learns the noise or random variations in the training data, which leads to poor performance on new, unseen data. Regularization techniques introduce additional constraints or penalties to the model's learning process, discouraging it from fitting the noise and reducing the complexity of the model. This helps to improve the model's ability to generalize well and make accurate predictions on unseen data.  

```

```python
chat.batch([messages])  

```

```text
 [AIMessage(content="The purpose of model regularization is to prevent overfitting in machine learning models. Overfitting occurs when a model becomes too complex and starts to learn the noise or random fluctuations in the training data, rather than the underlying patterns or relationships. Regularization techniques add a penalty term to the model's objective function, which discourages the model from becoming too complex and helps it generalize better to new, unseen data. This improves the model's ability to make accurate predictions on new data by reducing the variance and increasing the model's overall performance.")]  

```

```python
await chat.ainvoke(messages)  

```

```text
 AIMessage(content='The purpose of model regularization is to prevent overfitting in machine learning models. Overfitting occurs when a model becomes too complex and starts to memorize the training data instead of learning general patterns and relationships. This leads to poor performance on new, unseen data.\n\nRegularization techniques introduce additional constraints or penalties to the model during training, discouraging it from becoming overly complex. This helps to strike a balance between fitting the training data well and generalizing to new data. Regularization techniques can include adding a penalty term to the loss function, such as L1 or L2 regularization, or using techniques like dropout or early stopping. By regularizing the model, it encourages it to learn the most relevant features and reduce the impact of noise or outliers in the data.')  

```

```python
async for chunk in chat.astream(messages):  
 print(chunk.content, end="", flush=True)  

```

```text
 The purpose of model regularization is to prevent overfitting in machine learning models. Overfitting occurs when a model becomes too complex and starts to memorize the training data instead of learning the underlying patterns. Regularization techniques help in reducing the complexity of the model by adding a penalty to the loss function. This penalty encourages the model to have smaller weights or fewer features, making it more generalized and less prone to overfitting. The goal is to find the right balance between fitting the training data well and being able to generalize well to unseen data.  

```

```python
async for chunk in chat.astream\_log(messages):  
 print(chunk)  

```

```text
 RunLogPatch({'op': 'replace',  
 'path': '',  
 'value': {'final\_output': None,  
 'id': '754c4143-2348-46c4-ad2b-3095913084c6',  
 'logs': {},  
 'streamed\_output': []}})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='The')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' purpose')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' of')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' model')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' regularization')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' is')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' to')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' prevent')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' a')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' machine')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' learning')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' model')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' from')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' over')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='fit')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='ting')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' the')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' training')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' data')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' and')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' improve')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' its')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' general')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='ization')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' ability')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='.')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' Over')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='fit')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='ting')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' occurs')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' when')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' a')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' model')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' becomes')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' too')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' complex')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' and')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' learns')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' to')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' fit')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' the')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' noise')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' or')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' random')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' fluctuations')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' in')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' the')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' training')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' data')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=',')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' instead')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' of')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' capturing')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' the')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' underlying')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' patterns')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' and')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' relationships')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='.')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' Regular')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='ization')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' techniques')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' introduce')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' a')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' penalty')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' term')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' to')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' the')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' model')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content="'s")})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' objective')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' function')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=',')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' which')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' discour')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='ages')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' the')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' model')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' from')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' becoming')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' too')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' complex')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='.')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' This')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' helps')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' to')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' control')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' the')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' model')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content="'s")})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' complexity')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' and')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' reduces')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' the')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' risk')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' of')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' over')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='fit')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='ting')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=',')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' leading')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' to')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' better')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' performance')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' on')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' unseen')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content=' data')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='.')})  
 RunLogPatch({'op': 'add',  
 'path': '/streamed\_output/-',  
 'value': AIMessageChunk(content='')})  
 RunLogPatch({'op': 'replace',  
 'path': '/final\_output',  
 'value': {'generations': [[{'generation\_info': {'finish\_reason': 'stop'},  
 'message': AIMessageChunk(content="The purpose of model regularization is to prevent a machine learning model from overfitting the training data and improve its generalization ability. Overfitting occurs when a model becomes too complex and learns to fit the noise or random fluctuations in the training data, instead of capturing the underlying patterns and relationships. Regularization techniques introduce a penalty term to the model's objective function, which discourages the model from becoming too complex. This helps to control the model's complexity and reduces the risk of overfitting, leading to better performance on unseen data."),  
 'text': 'The purpose of model regularization is '  
 'to prevent a machine learning model '  
 'from overfitting the training data and '  
 'improve its generalization ability. '  
 'Overfitting occurs when a model becomes '  
 'too complex and learns to fit the noise '  
 'or random fluctuations in the training '  
 'data, instead of capturing the '  
 'underlying patterns and relationships. '  
 'Regularization techniques introduce a '  
 "penalty term to the model's objective "  
 'function, which discourages the model '  
 'from becoming too complex. This helps '  
 "to control the model's complexity and "  
 'reduces the risk of overfitting, '  
 'leading to better performance on unseen '  
 'data.'}]],  
 'llm\_output': None,  
 'run': None}})  

```

### `__call__`[​](#__call__ "Direct link to __call__")

#### Messages in -> message out[​](#messages-in---message-out "Direct link to Messages in -> message out")

For convenience you can also treat chat models as callables. You can get chat completions by passing one or more messages to the chat model. The response will be a message.

```python
from langchain.schema import (  
 AIMessage,  
 HumanMessage,  
 SystemMessage  
)  
  
chat([HumanMessage(content="Translate this sentence from English to French: I love programming.")])  

```

```text
 AIMessage(content="J'adore la programmation.")  

```

OpenAI's chat model supports multiple messages as input. See [here](https://platform.openai.com/docs/guides/chat/chat-vs-completions) for more information. Here is an example of sending a system and user message to the chat model:

```python
messages = [  
 SystemMessage(content="You are a helpful assistant that translates English to French."),  
 HumanMessage(content="I love programming.")  
]  
chat(messages)  

```

```text
 AIMessage(content="J'adore la programmation.")  

```

### `generate`[​](#generate "Direct link to generate")

#### Batch calls, richer outputs[​](#batch-calls-richer-outputs "Direct link to Batch calls, richer outputs")

You can go one step further and generate completions for multiple sets of messages using `generate`. This returns an `LLMResult` with an additional `message` parameter. This will include additional information about each generation beyond the returned message (e.g. the finish reason) and additional information about the full API call (e.g. total tokens used).

```python
batch\_messages = [  
 [  
 SystemMessage(content="You are a helpful assistant that translates English to French."),  
 HumanMessage(content="I love programming.")  
 ],  
 [  
 SystemMessage(content="You are a helpful assistant that translates English to French."),  
 HumanMessage(content="I love artificial intelligence.")  
 ],  
]  
result = chat.generate(batch\_messages)  
result  

```

```text
 LLMResult(generations=[[ChatGeneration(text="J'adore programmer.", generation\_info={'finish\_reason': 'stop'}, message=AIMessage(content="J'adore programmer."))], [ChatGeneration(text="J'adore l'intelligence artificielle.", generation\_info={'finish\_reason': 'stop'}, message=AIMessage(content="J'adore l'intelligence artificielle."))]], llm\_output={'token\_usage': {'prompt\_tokens': 53, 'completion\_tokens': 18, 'total\_tokens': 71}, 'model\_name': 'gpt-3.5-turbo'}, run=[RunInfo(run\_id=UUID('077917a9-026c-47c4-b308-77b37c3a3bfa')), RunInfo(run\_id=UUID('0a70a0bf-c599-4f51-932a-c7d42202c984'))])  

```

You can recover things like token usage from this LLMResult:

```python
result.llm\_output  

```

```text
 {'token\_usage': {'prompt\_tokens': 53,  
 'completion\_tokens': 18,  
 'total\_tokens': 71},  
 'model\_name': 'gpt-3.5-turbo'}  

```

- [Get started](#get-started)

  - [Setup](#setup)
  - [Messages](#messages)
  - [LCEL](#lcel)
  - [`__call__`](#__call__)
  - [`generate`](#generate)

- [Setup](#setup)

- [Messages](#messages)

- [LCEL](#lcel)

- [`__call__`](#__call__)

- [`generate`](#generate)
