# Llama.cpp

This page covers how to use [llama.cpp](https://github.com/ggerganov/llama.cpp) within LangChain.
It is broken into two parts: installation and setup, and then references to specific Llama-cpp wrappers.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install the Python package with `pip install llama-cpp-python`
- Download one of the [supported models](https://github.com/ggerganov/llama.cpp#description) and convert them to the llama.cpp format per the [instructions](https://github.com/ggerganov/llama.cpp)

## Wrappers[​](#wrappers "Direct link to Wrappers")

### LLM[​](#llm "Direct link to LLM")

There exists a LlamaCpp LLM wrapper, which you can access with

```python
from langchain.llms import LlamaCpp  

```

For a more detailed walkthrough of this, see [this notebook](/docs/integrations/llms/llamacpp.html)

### Embeddings[​](#embeddings "Direct link to Embeddings")

There exists a LlamaCpp Embeddings wrapper, which you can access with

```python
from langchain.embeddings import LlamaCppEmbeddings  

```

For a more detailed walkthrough of this, see [this notebook](/docs/integrations/text_embedding/llamacpp.html)

- [Installation and Setup](#installation-and-setup)

- [Wrappers](#wrappers)

  - [LLM](#llm)
  - [Embeddings](#embeddings)

- [LLM](#llm)

- [Embeddings](#embeddings)
