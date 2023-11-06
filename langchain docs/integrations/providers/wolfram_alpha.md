# Wolfram Alpha

[WolframAlpha](https://en.wikipedia.org/wiki/WolframAlpha) is an answer engine developed by `Wolfram Research`.
It answers factual queries by computing answers from externally sourced data.

This page covers how to use the `Wolfram Alpha API` within LangChain.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install requirements with

```bash
pip install wolframalpha  

```

- Go to wolfram alpha and sign up for a developer account [here](https://developer.wolframalpha.com/)
- Create an app and get your `APP ID`
- Set your APP ID as an environment variable `WOLFRAM_ALPHA_APPID`

## Wrappers[​](#wrappers "Direct link to Wrappers")

### Utility[​](#utility "Direct link to Utility")

There exists a WolframAlphaAPIWrapper utility which wraps this API. To import this utility:

```python
from langchain.utilities.wolfram\_alpha import WolframAlphaAPIWrapper  

```

For a more detailed walkthrough of this wrapper, see [this notebook](/docs/integrations/tools/wolfram_alpha.html).

### Tool[​](#tool "Direct link to Tool")

You can also easily load this wrapper as a Tool (to use with an Agent).
You can do this with:

```python
from langchain.agents import load\_tools  
tools = load\_tools(["wolfram-alpha"])  

```

For more information on tools, see [this page](/docs/modules/agents/tools/).

- [Installation and Setup](#installation-and-setup)

- [Wrappers](#wrappers)

  - [Utility](#utility)
  - [Tool](#tool)

- [Utility](#utility)

- [Tool](#tool)
