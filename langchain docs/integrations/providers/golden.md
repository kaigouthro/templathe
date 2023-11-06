# Golden

[Golden](https://golden.com) provides a set of natural language APIs for querying and enrichment using the Golden Knowledge Graph e.g. queries such as: `Products from OpenAI`, `Generative ai companies with series a funding`, and `rappers who invest` can be used to retrieve structured data about relevant entities.

The `golden-query` langchain tool is a wrapper on top of the [Golden Query API](https://docs.golden.com/reference/query-api) which enables programmatic access to these results.
See the [Golden Query API docs](https://docs.golden.com/reference/query-api) for more information.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Go to the [Golden API docs](https://docs.golden.com/) to get an overview about the Golden API.
- Get your API key from the [Golden API Settings](https://golden.com/settings/api) page.
- Save your API key into GOLDEN_API_KEY env variable

## Wrappers[​](#wrappers "Direct link to Wrappers")

### Utility[​](#utility "Direct link to Utility")

There exists a GoldenQueryAPIWrapper utility which wraps this API. To import this utility:

```python
from langchain.utilities.golden\_query import GoldenQueryAPIWrapper  

```

For a more detailed walkthrough of this wrapper, see [this notebook](/docs/integrations/tools/golden_query.html).

### Tool[​](#tool "Direct link to Tool")

You can also easily load this wrapper as a Tool (to use with an Agent).
You can do this with:

```python
from langchain.agents import load\_tools  
tools = load\_tools(["golden-query"])  

```

For more information on tools, see [this page](/docs/modules/agents/tools/).

- [Installation and Setup](#installation-and-setup)

- [Wrappers](#wrappers)

  - [Utility](#utility)
  - [Tool](#tool)

- [Utility](#utility)

- [Tool](#tool)
