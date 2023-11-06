# Aleph Alpha

[Aleph Alpha](https://docs.aleph-alpha.com/) was founded in 2019 with the mission to research and build the foundational technology for an era of strong AI. The team of international scientists, engineers, and innovators researches, develops, and deploys transformative AI like large language and multimodal models and runs the fastest European commercial AI cluster.

[The Luminous series](https://docs.aleph-alpha.com/docs/introduction/luminous/) is a family of large language models.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

```bash
pip install aleph-alpha-client  

```

You have to create a new token. Please, see [instructions](https://docs.aleph-alpha.com/docs/account/#create-a-new-token).

```python
from getpass import getpass  
  
ALEPH\_ALPHA\_API\_KEY = getpass()  

```

## LLM[​](#llm "Direct link to LLM")

See a [usage example](/docs/integrations/llms/aleph_alpha).

```python
from langchain.llms import AlephAlpha  

```

## Text Embedding Models[​](#text-embedding-models "Direct link to Text Embedding Models")

See a [usage example](/docs/integrations/text_embedding/aleph_alpha).

```python
from langchain.embeddings import AlephAlphaSymmetricSemanticEmbedding, AlephAlphaAsymmetricSemanticEmbedding  

```

- [Installation and Setup](#installation-and-setup)
- [LLM](#llm)
- [Text Embedding Models](#text-embedding-models)
