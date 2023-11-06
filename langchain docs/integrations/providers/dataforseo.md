# DataForSEO

This page provides instructions on how to use the DataForSEO search APIs within LangChain.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Get a DataForSEO API Access login and password, and set them as environment variables (`DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` respectively). You can find it in your dashboard.

## Wrappers[​](#wrappers "Direct link to Wrappers")

### Utility[​](#utility "Direct link to Utility")

The DataForSEO utility wraps the API. To import this utility, use:

```python
from langchain.utilities.dataforseo\_api\_search import DataForSeoAPIWrapper  

```

For a detailed walkthrough of this wrapper, see [this notebook](/docs/integrations/tools/dataforseo.ipynb).

### Tool[​](#tool "Direct link to Tool")

You can also load this wrapper as a Tool to use with an Agent:

```python
from langchain.agents import load\_tools  
tools = load\_tools(["dataforseo-api-search"])  

```

## Example usage[​](#example-usage "Direct link to Example usage")

```python
dataforseo = DataForSeoAPIWrapper(api\_login="your\_login", api\_password="your\_password")  
result = dataforseo.run("Bill Gates")  
print(result)  

```

## Environment Variables[​](#environment-variables "Direct link to Environment Variables")

You can store your DataForSEO API Access login and password as environment variables. The wrapper will automatically check for these environment variables if no values are provided:

```python
import os  
  
os.environ["DATAFORSEO\_LOGIN"] = "your\_login"  
os.environ["DATAFORSEO\_PASSWORD"] = "your\_password"  
  
dataforseo = DataForSeoAPIWrapper()  
result = dataforseo.run("weather in Los Angeles")  
print(result)  

```

- [Installation and Setup](#installation-and-setup)

- [Wrappers](#wrappers)

  - [Utility](#utility)
  - [Tool](#tool)

- [Example usage](#example-usage)

- [Environment Variables](#environment-variables)

- [Utility](#utility)

- [Tool](#tool)
