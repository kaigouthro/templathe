# OpenAI

All functionality related to OpenAI

[OpenAI](https://en.wikipedia.org/wiki/OpenAI) is American artificial intelligence (AI) research laboratory
consisting of the non-profit `OpenAI Incorporated`
and its for-profit subsidiary corporation `OpenAI Limited Partnership`.
`OpenAI` conducts AI research with the declared intention of promoting and developing a friendly AI.
`OpenAI` systems run on an `Azure`-based supercomputing platform from `Microsoft`.

The [OpenAI API](https://platform.openai.com/docs/models) is powered by a diverse set of models with different capabilities and price points.

[ChatGPT](https://chat.openai.com) is the Artificial Intelligence (AI) chatbot developed by `OpenAI`.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install the Python SDK with

```bash
pip install openai  

```

- Get an OpenAI api key and set it as an environment variable (`OPENAI_API_KEY`)
- If you want to use OpenAI's tokenizer (only available for Python 3.9+), install it

```bash
pip install tiktoken  

```

## LLM[​](#llm "Direct link to LLM")

See a [usage example](/docs/integrations/llms/openai).

```python
from langchain.llms import OpenAI  

```

If you are using a model hosted on `Azure`, you should use different wrapper for that:

```python
from langchain.llms import AzureOpenAI  

```

For a more detailed walkthrough of the `Azure` wrapper, see [here](/docs/integrations/llms/azure_openai_example)

## Chat model[​](#chat-model "Direct link to Chat model")

See a [usage example](/docs/integrations/chat/openai).

```python
from langchain.chat\_models import ChatOpenAI  

```

If you are using a model hosted on `Azure`, you should use different wrapper for that:

```python
from langchain.llms import AzureChatOpenAI  

```

For a more detailed walkthrough of the `Azure` wrapper, see [here](/docs/integrations/chat/azure_chat_openai)

## Text Embedding Model[​](#text-embedding-model "Direct link to Text Embedding Model")

See a [usage example](/docs/integrations/text_embedding/openai)

```python
from langchain.embeddings import OpenAIEmbeddings  

```

## Tokenizer[​](#tokenizer "Direct link to Tokenizer")

There are several places you can use the `tiktoken` tokenizer. By default, it is used to count tokens
for OpenAI LLMs.

You can also use it to count tokens when splitting documents with

```python
from langchain.text\_splitter import CharacterTextSplitter  
CharacterTextSplitter.from\_tiktoken\_encoder(...)  

```

For a more detailed walkthrough of this, see [this notebook](/docs/modules/data_connection/document_transformers/text_splitters/tiktoken)

## Document Loader[​](#document-loader "Direct link to Document Loader")

See a [usage example](/docs/integrations/document_loaders/chatgpt_loader).

```python
from langchain.document\_loaders.chatgpt import ChatGPTLoader  

```

## Retriever[​](#retriever "Direct link to Retriever")

See a [usage example](/docs/integrations/retrievers/chatgpt-plugin).

```python
from langchain.retrievers import ChatGPTPluginRetriever  

```

## Chain[​](#chain "Direct link to Chain")

See a [usage example](/docs/guides/safety/moderation).

```python
from langchain.chains import OpenAIModerationChain  

```

- [Installation and Setup](#installation-and-setup)
- [LLM](#llm)
- [Chat model](#chat-model)
- [Text Embedding Model](#text-embedding-model)
- [Tokenizer](#tokenizer)
- [Document Loader](#document-loader)
- [Retriever](#retriever)
- [Chain](#chain)
