# Jina

This page covers how to use the Jina ecosystem within LangChain.
It is broken into two parts: installation and setup, and then references to specific Jina wrappers.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install the Python SDK with `pip install jina`
- Get a Jina AI Cloud auth token from [here](https://cloud.jina.ai/settings/tokens) and set it as an environment variable (`JINA_AUTH_TOKEN`)

## Wrappers[​](#wrappers "Direct link to Wrappers")

### Embeddings[​](#embeddings "Direct link to Embeddings")

There exists a Jina Embeddings wrapper, which you can access with

```python
from langchain.embeddings import JinaEmbeddings  

```

For a more detailed walkthrough of this, see [this notebook](/docs/integrations/text_embedding/jina.html)

## Deployment[​](#deployment "Direct link to Deployment")

[Langchain-serve](https://github.com/jina-ai/langchain-serve), powered by Jina, helps take LangChain apps to production with easy to use REST/WebSocket APIs and Slack bots.

### Usage[​](#usage "Direct link to Usage")

Install the package from PyPI.

```bash
pip install langchain-serve  

```

Wrap your LangChain app with the `@serving` decorator.

```python
# app.py  
from lcserve import serving  
  
@serving  
def ask(input: str) -> str:  
 from langchain.chains import LLMChain  
 from langchain.llms import OpenAI  
 from langchain.agents import AgentExecutor, ZeroShotAgent  
   
 tools = [...] # list of tools  
 prompt = ZeroShotAgent.create\_prompt(  
 tools, input\_variables=["input", "agent\_scratchpad"],  
 )  
 llm\_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)  
 agent = ZeroShotAgent(  
 llm\_chain=llm\_chain, allowed\_tools=[tool.name for tool in tools]  
 )  
 agent\_executor = AgentExecutor.from\_agent\_and\_tools(  
 agent=agent,   
 tools=tools,   
 verbose=True,  
 )  
 return agent\_executor.run(input)  

```

Deploy on Jina AI Cloud with `lc-serve deploy jcloud app`. Once deployed, we can send a POST request to the API endpoint to get a response.

```bash
curl -X 'POST' 'https://<your-app>.wolf.jina.ai/ask' \  
 -d '{  
 "input": "Your Question here?",  
 "envs": {  
 "OPENAI\_API\_KEY": "sk-\*\*\*"  
 }  
}'  

```

You can also self-host the app on your infrastructure with Docker-compose or Kubernetes. See [here](https://github.com/jina-ai/langchain-serve#-self-host-llm-apps-with-docker-compose-or-kubernetes) for more details.

Langchain-serve also allows to deploy the apps with WebSocket APIs and Slack Bots both on [Jina AI Cloud](https://cloud.jina.ai/) or self-hosted infrastructure.

- [Installation and Setup](#installation-and-setup)

- [Wrappers](#wrappers)

  - [Embeddings](#embeddings)

- [Deployment](#deployment)

  - [Usage](#usage)

- [Embeddings](#embeddings)

- [Usage](#usage)
