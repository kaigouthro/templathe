# Anyscale

This page covers how to use the Anyscale ecosystem within LangChain.
It is broken into two parts: installation and setup, and then references to specific Anyscale wrappers.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Get an Anyscale Service URL, route and API key and set them as environment variables (`ANYSCALE_SERVICE_URL`,`ANYSCALE_SERVICE_ROUTE`, `ANYSCALE_SERVICE_TOKEN`).
- Please see [the Anyscale docs](https://docs.anyscale.com/productionize/services-v2/get-started) for more details.

## Wrappers[​](#wrappers "Direct link to Wrappers")

### LLM[​](#llm "Direct link to LLM")

There exists an Anyscale LLM wrapper, which you can access with

```python
from langchain.llms import Anyscale  

```

- [Installation and Setup](#installation-and-setup)

- [Wrappers](#wrappers)

  - [LLM](#llm)

- [LLM](#llm)
