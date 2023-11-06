# Portkey

[Portkey](https://docs.portkey.ai/overview/introduction) is a platform designed to streamline the deployment
and management of Generative AI applications.
It provides comprehensive features for monitoring, managing models,
and improving the performance of your AI applications.

## LLMOps for Langchain[​](#llmops-for-langchain "Direct link to LLMOps for Langchain")

Portkey brings production readiness to Langchain. With Portkey, you can

- view detailed **metrics & logs** for all requests,
- enable **semantic cache** to reduce latency & costs,
- implement automatic **retries & fallbacks** for failed requests,
- add **custom tags** to requests for better tracking and analysis and [more](https://docs.portkey.ai).

### Using Portkey with Langchain[​](#using-portkey-with-langchain "Direct link to Using Portkey with Langchain")

Using Portkey is as simple as just choosing which Portkey features you want, enabling them via `headers=Portkey.Config` and passing it in your LLM calls.

To start, get your Portkey API key by [signing up here](https://app.portkey.ai/login). (Click the profile icon on the top left, then click on "Copy API Key")

For OpenAI, a simple integration with logging feature would look like this:

```python
from langchain.llms import OpenAI  
from langchain.utilities import Portkey  
  
# Add the Portkey API Key from your account  
headers = Portkey.Config(  
 api\_key = "<PORTKEY\_API\_KEY>"  
)  
  
llm = OpenAI(temperature=0.9, headers=headers)  
llm.predict("What would be a good company name for a company that makes colorful socks?")  

```

Your logs will be captured on your [Portkey dashboard](https://app.portkey.ai).

A common Portkey X Langchain use case is to **trace a chain or an agent** and view all the LLM calls originating from that request.

### **Tracing Chains & Agents**[​](#tracing-chains--agents "Direct link to tracing-chains--agents")

```python
from langchain.agents import AgentType, initialize\_agent, load\_tools   
from langchain.llms import OpenAI  
from langchain.utilities import Portkey  
  
# Add the Portkey API Key from your account  
headers = Portkey.Config(  
 api\_key = "<PORTKEY\_API\_KEY>",  
 trace\_id = "fef659"  
)  
  
llm = OpenAI(temperature=0, headers=headers)   
tools = load\_tools(["serpapi", "llm-math"], llm=llm)   
agent = initialize\_agent(tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True)   
   
# Let's test it out!   
agent.run("What was the high temperature in SF yesterday in Fahrenheit? What is that number raised to the .023 power?")  

```

**You can see the requests' logs along with the trace id on Portkey dashboard:**

![](/img/portkey-dashboard.gif)

![](/img/portkey-tracing.png)

## Advanced Features[​](#advanced-features "Direct link to Advanced Features")

1. **Logging:** Log all your LLM requests automatically by sending them through Portkey. Each request log contains `timestamp`, `model name`, `total cost`, `request time`, `request json`, `response json`, and additional Portkey features.
1. **Tracing:** Trace id can be passed along with each request and is visibe on the logs on Portkey dashboard. You can also set a **distinct trace id** for each request. You can [append user feedback](https://docs.portkey.ai/key-features/feedback-api) to a trace id as well.
1. **Caching:** Respond to previously served customers queries from cache instead of sending them again to OpenAI. Match exact strings OR semantically similar strings. Cache can save costs and reduce latencies by 20x.
1. **Retries:** Automatically reprocess any unsuccessful API requests **`upto 5`** times. Uses an **`exponential backoff`** strategy, which spaces out retry attempts to prevent network overload.
1. **Tagging:** Track and audit each user interaction in high detail with predefined tags.

| Feature | Config Key | Value (Type) | Required/Optional |
| --- | --- | --- | --- |
| API Key | `api_key` | API Key (`string`) | ✅ Required |
| [Tracing Requests](https://docs.portkey.ai/key-features/request-tracing) | `trace_id` | Custom `string` | ❔ Optional |
| [Automatic Retries](https://docs.portkey.ai/key-features/automatic-retries) | `retry_count` | `integer` \[1,2,3,4,5\] | ❔ Optional |
| [Enabling Cache](https://docs.portkey.ai/key-features/request-caching) | `cache` | `simple` OR `semantic` | ❔ Optional |
| Cache Force Refresh | `cache_force_refresh` | `True` | ❔ Optional |
| Set Cache Expiry | `cache_age` | `integer` (in seconds) | ❔ Optional |
| [Add User](https://docs.portkey.ai/key-features/custom-metadata) | `user` | `string` | ❔ Optional |
| [Add Organisation](https://docs.portkey.ai/key-features/custom-metadata) | `organisation` | `string` | ❔ Optional |
| [Add Environment](https://docs.portkey.ai/key-features/custom-metadata) | `environment` | `string` | ❔ Optional |
| [Add Prompt (version/id/string)](https://docs.portkey.ai/key-features/custom-metadata) | `prompt` | `string` | ❔ Optional |

## **Enabling all Portkey Features:**[​](#enabling-all-portkey-features "Direct link to enabling-all-portkey-features")

```py
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
 prompt="Frost"  
   
)  

```

For detailed information on each feature and how to use it, [please refer to the Portkey docs](https://docs.portkey.ai). If you have any questions or need further assistance, [reach out to us on Twitter.](https://twitter.com/portkeyai).

- [LLMOps for Langchain](#llmops-for-langchain)

  - [Using Portkey with Langchain](#using-portkey-with-langchain)
  - [**Tracing Chains & Agents**](#tracing-chains--agents)

- [Advanced Features](#advanced-features)

- [**Enabling all Portkey Features:**](#enabling-all-portkey-features)

- [Using Portkey with Langchain](#using-portkey-with-langchain)

- [**Tracing Chains & Agents**](#tracing-chains--agents)
