# Log, Trace, and Monitor

When building apps or agents using Langchain, you end up making multiple API calls to fulfill a single user request. However, these requests are not chained when you want to analyse them. With [**Portkey**](/docs/ecosystem/integrations/portkey), all the embeddings, completion, and other requests from a single user request will get logged and traced to a common ID, enabling you to gain full visibility of user interactions.

This notebook serves as a step-by-step guide on how to log, trace, and monitor Langchain LLM calls using `Portkey` in your Langchain app.

First, let's import Portkey, OpenAI, and Agent tools

```python
import os  
  
from langchain.agents import AgentType, initialize\_agent, load\_tools  
from langchain.llms import OpenAI  
from langchain.utilities import Portkey  

```

Paste your OpenAI API key below. [(You can find it here)](https://platform.openai.com/account/api-keys)

```python
os.environ["OPENAI\_API\_KEY"] = "<OPENAI\_API\_KEY>"  

```

## Get Portkey API Key[​](#get-portkey-api-key "Direct link to Get Portkey API Key")

1. Sign up for [Portkey here](https://app.portkey.ai/login)
1. On your [dashboard](https://app.portkey.ai/), click on the profile icon on the top left, then click on "Copy API Key"
1. Paste it below

```python
PORTKEY\_API\_KEY = "<PORTKEY\_API\_KEY>" # Paste your Portkey API Key here  

```

## Set Trace ID[​](#set-trace-id "Direct link to Set Trace ID")

1. Set the trace id for your request below
1. The Trace ID can be common for all API calls originating from a single request

```python
TRACE\_ID = "portkey\_langchain\_demo" # Set trace id here  

```

## Generate Portkey Headers[​](#generate-portkey-headers "Direct link to Generate Portkey Headers")

```python
headers = Portkey.Config(  
 api\_key=PORTKEY\_API\_KEY,  
 trace\_id=TRACE\_ID,  
)  

```

Run your agent as usual. The **only** change is that we will **include the above headers** in the request now.

```python
llm = OpenAI(temperature=0, headers=headers)  
tools = load\_tools(["serpapi", "llm-math"], llm=llm)  
agent = initialize\_agent(  
 tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  
  
# Let's test it out!  
agent.run(  
 "What was the high temperature in SF yesterday in Fahrenheit? What is that number raised to the .023 power?"  
)  

```

## How Logging & Tracing Works on Portkey[​](#how-logging--tracing-works-on-portkey "Direct link to How Logging & Tracing Works on Portkey")

**Logging**

- Sending your request through Portkey ensures that all of the requests are logged by default
- Each request log contains `timestamp`, `model name`, `total cost`, `request time`, `request json`, `response json`, and additional Portkey features

**Tracing**

- Trace id is passed along with each request and is visibe on the logs on Portkey dashboard
- You can also set a **distinct trace id** for each request if you want
- You can append user feedback to a trace id as well. [More info on this here](https://docs.portkey.ai/key-features/feedback-api)

## Advanced LLMOps Features - Caching, Tagging, Retries[​](#advanced-llmops-features---caching-tagging-retries "Direct link to Advanced LLMOps Features - Caching, Tagging, Retries")

In addition to logging and tracing, Portkey provides more features that add production capabilities to your existing workflows:

**Caching**

Respond to previously served customers queries from cache instead of sending them again to OpenAI. Match exact strings OR semantically similar strings. Cache can save costs and reduce latencies by 20x.

**Retries**

Automatically reprocess any unsuccessful API requests **`upto 5`** times. Uses an **`exponential backoff`** strategy, which spaces out retry attempts to prevent network overload.

| Feature | Config Key | Value (Type) |
| --- | --- | --- |
| [🔁 Automatic Retries](https://docs.portkey.ai/key-features/automatic-retries) | `retry_count` | `integer` \[1,2,3,4,5\] |
| [🧠 Enabling Cache](https://docs.portkey.ai/key-features/request-caching) | `cache` | `simple` OR `semantic` |

**Tagging**

Track and audit ach user interaction in high detail with predefined tags.

| Tag | Config Key | Value (Type) |
| --- | --- | --- |
| User Tag | `user` | `string` |
| Organisation Tag | `organisation` | `string` |
| Environment Tag | `environment` | `string` |
| Prompt Tag (version/id/string) | `prompt` | `string` |

## Code Example With All Features[​](#code-example-with-all-features "Direct link to Code Example With All Features")

```python
headers = Portkey.Config(  
 # Mandatory  
 api\_key="<PORTKEY\_API\_KEY>",  
 # Cache Options  
 cache="semantic",  
 cache\_force\_refresh="True",  
 cache\_age=1729,  
 # Advanced  
 retry\_count=5,  
 trace\_id="langchain\_agent",  
 # Metadata  
 environment="production",  
 user="john",  
 organisation="acme",  
 prompt="Frost",  
)  
  
llm = OpenAI(temperature=0.9, headers=headers)  
  
print(llm("Two roads diverged in the yellow woods"))  

```

- [Get Portkey API Key](#get-portkey-api-key)
- [Set Trace ID](#set-trace-id)
- [Generate Portkey Headers](#generate-portkey-headers)
- [How Logging & Tracing Works on Portkey](#how-logging--tracing-works-on-portkey)
- [Advanced LLMOps Features - Caching, Tagging, Retries](#advanced-llmops-features---caching-tagging-retries)
- [Code Example With All Features](#code-example-with-all-features)
