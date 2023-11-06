# Introduction

**LangChain** is a framework for developing applications powered by language models. It enables applications that:

- **Are context-aware**: connect a language model to sources of context (prompt instructions, few shot examples, content to ground its response in, etc.)
- **Reason**: rely on a language model to reason (about how to answer based on provided context, what actions to take, etc.)

The main value props of LangChain are:

1. **Components**: abstractions for working with language models, along with a collection of implementations for each abstraction. Components are modular and easy-to-use, whether you are using the rest of the LangChain framework or not
1. **Off-the-shelf chains**: a structured assembly of components for accomplishing specific higher-level tasks

Off-the-shelf chains make it easy to get started. For complex applications, components make it easy to customize existing chains and build new ones.

## Get started[​](#get-started "Direct link to Get started")

[Here’s](/docs/get_started/installation) how to install LangChain, set up your environment, and start building.

We recommend following our [Quickstart](/docs/get_started/quickstart) guide to familiarize yourself with the framework by building your first LangChain application.

***Note**: These docs are for the LangChain [Python package](https://github.com/langchain-ai/langchain). For documentation on [LangChain.js](https://github.com/langchain-ai/langchainjs), the JS/TS version, [head here](https://js.langchain.com/docs).*

## Modules[​](#modules "Direct link to Modules")

LangChain provides standard, extendable interfaces and external integrations for the following modules, listed from least to most complex:

#### [Model I/O](/docs/modules/model_io/)[​](#model-io "Direct link to model-io")

Interface with language models

#### [Retrieval](/docs/modules/data_connection/)[​](#retrieval "Direct link to retrieval")

Interface with application-specific data

#### [Chains](/docs/modules/chains/)[​](#chains "Direct link to chains")

Construct sequences of calls

#### [Agents](/docs/modules/agents/)[​](#agents "Direct link to agents")

Let chains choose which tools to use given high-level directives

#### [Memory](/docs/modules/memory/)[​](#memory "Direct link to memory")

Persist application state between runs of a chain

#### [Callbacks](/docs/modules/callbacks/)[​](#callbacks "Direct link to callbacks")

Log and stream intermediate steps of any chain

## Examples, ecosystem, and resources[​](#examples-ecosystem-and-resources "Direct link to Examples, ecosystem, and resources")

### [Use cases](/docs/use_cases/question_answering/)[​](#use-cases "Direct link to use-cases")

Walkthroughs and best-practices for common end-to-end use cases, like:

- [Document question answering](/docs/use_cases/question_answering/)
- [Chatbots](/docs/use_cases/chatbots/)
- [Analyzing structured data](/docs/use_cases/qa_structured/sql/)
- and much more...

### [Guides](/docs/guides/)[​](#guides "Direct link to guides")

Learn best practices for developing with LangChain.

### [Ecosystem](/docs/integrations/providers/)[​](#ecosystem "Direct link to ecosystem")

LangChain is part of a rich ecosystem of tools that integrate with our framework and build on top of it. Check out our growing list of [integrations](/docs/integrations/providers/) and [dependent repos](/docs/additional_resources/dependents).

### [Additional resources](/docs/additional_resources/)[​](#additional-resources "Direct link to additional-resources")

Our community is full of prolific developers, creative builders, and fantastic teachers. Check out [YouTube tutorials](/docs/additional_resources/youtube) for great tutorials from folks in the community, and [Gallery](https://github.com/kyrolabs/awesome-langchain) for a list of awesome LangChain projects, compiled by the folks at [KyroLabs](https://kyrolabs.com).

### [Community](/docs/community)[​](#community "Direct link to community")

Head to the [Community navigator](/docs/community) to find places to ask questions, share feedback, meet other developers, and dream about the future of LLM’s.

## API reference[​](#api-reference "Direct link to API reference")

Head to the [reference](https://api.python.langchain.com) section for full documentation of all classes and methods in the LangChain Python package.

- [Get started](#get-started)

- [Modules](#modules)

- [Examples, ecosystem, and resources](#examples-ecosystem-and-resources)

  - [Use cases](#use-cases)
  - [Guides](#guides)
  - [Ecosystem](#ecosystem)
  - [Additional resources](#additional-resources)
  - [Community](#community)

- [API reference](#api-reference)

- [Use cases](#use-cases)

- [Guides](#guides)

- [Ecosystem](#ecosystem)

- [Additional resources](#additional-resources)

- [Community](#community)
