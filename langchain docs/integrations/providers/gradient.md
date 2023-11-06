# Gradient

[Gradient](https://gradient.ai/) allows to fine tune and get completions on LLMs with a simple web API.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install the Python SDK :

```bash
pip install gradientai  

```

Get a [Gradient access token and workspace](https://gradient.ai/) and set it as an environment variable (`Gradient_ACCESS_TOKEN`) and (`GRADIENT_WORKSPACE_ID`)

## LLM[​](#llm "Direct link to LLM")

There exists an Gradient LLM wrapper, which you can access with
See a [usage example](/docs/integrations/llms/gradient).

```python
from langchain.llms import GradientLLM  

```

## Text Embedding Model[​](#text-embedding-model "Direct link to Text Embedding Model")

There exists an Gradient Embedding model, which you can access with

```python
from langchain.embeddings import GradientEmbeddings  

```

For a more detailed walkthrough of this, see [this notebook](/docs/integrations/text_embedding/gradient.html)

- [Installation and Setup](#installation-and-setup)
- [LLM](#llm)
- [Text Embedding Model](#text-embedding-model)
