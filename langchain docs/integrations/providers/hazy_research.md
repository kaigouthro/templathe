# Hazy Research

This page covers how to use the Hazy Research ecosystem within LangChain.
It is broken into two parts: installation and setup, and then references to specific Hazy Research wrappers.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- To use the `manifest`, install it with `pip install manifest-ml`

## Wrappers[​](#wrappers "Direct link to Wrappers")

### LLM[​](#llm "Direct link to LLM")

There exists an LLM wrapper around Hazy Research's `manifest` library.
`manifest` is a python library which is itself a wrapper around many model providers, and adds in caching, history, and more.

To use this wrapper:

```python
from langchain.llms.manifest import ManifestWrapper  

```

- [Installation and Setup](#installation-and-setup)

- [Wrappers](#wrappers)

  - [LLM](#llm)

- [LLM](#llm)
