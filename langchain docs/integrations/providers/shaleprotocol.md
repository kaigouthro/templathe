# Shale Protocol

[Shale Protocol](https://shaleprotocol.com) provides production-ready inference APIs for open LLMs. It's a Plug & Play API as it's hosted on a highly scalable GPU cloud infrastructure.

Our free tier supports up to 1K daily requests per key as we want to eliminate the barrier for anyone to start building genAI apps with LLMs.

With Shale Protocol, developers/researchers can create apps and explore the capabilities of open LLMs at no cost.

This page covers how Shale-Serve API can be incorporated with LangChain.

As of June 2023, the API supports Vicuna-13B by default. We are going to support more LLMs such as Falcon-40B in future releases.

## How to[​](#how-to "Direct link to How to")

### 1. Find the link to our Discord on <https://shaleprotocol.com.> Generate an API key through the "Shale Bot" on our Discord. No credit card is required and no free trials. It's a forever free tier with 1K limit per day per API key.[​](#1-find-the-link-to-our-discord-on-httpsshaleprotocolcom-generate-an-api-key-through-the-shale-bot-on-our-discord-no-credit-card-is-required-and-no-free-trials-its-a-forever-free-tier-with-1k-limit-per-day-per-api-key "Direct link to 1-find-the-link-to-our-discord-on-httpsshaleprotocolcom-generate-an-api-key-through-the-shale-bot-on-our-discord-no-credit-card-is-required-and-no-free-trials-its-a-forever-free-tier-with-1k-limit-per-day-per-api-key")

### 2. Use <https://shale.live/v1> as OpenAI API drop-in replacement[​](#2-use-httpsshalelivev1-as-openai-api-drop-in-replacement "Direct link to 2-use-httpsshalelivev1-as-openai-api-drop-in-replacement")

For example

```python
from langchain.llms import OpenAI  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
  
import os  
os.environ['OPENAI\_API\_BASE'] = "https://shale.live/v1"  
os.environ['OPENAI\_API\_KEY'] = "ENTER YOUR API KEY"  
  
llm = OpenAI()  
  
template = """Question: {question}  
  
# Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  
  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
  
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"  
  
llm\_chain.run(question)  
  

```

- [How to](#how-to)

  - [1. Find the link to our Discord on https://shaleprotocol.com. Generate an API key through the "Shale Bot" on our Discord. No credit card is required and no free trials. It's a forever free tier with 1K limit per day per API key.](#1-find-the-link-to-our-discord-on-httpsshaleprotocolcom-generate-an-api-key-through-the-shale-bot-on-our-discord-no-credit-card-is-required-and-no-free-trials-its-a-forever-free-tier-with-1k-limit-per-day-per-api-key)
  - [2. Use https://shale.live/v1 as OpenAI API drop-in replacement](#2-use-httpsshalelivev1-as-openai-api-drop-in-replacement)

- [1. Find the link to our Discord on https://shaleprotocol.com. Generate an API key through the "Shale Bot" on our Discord. No credit card is required and no free trials. It's a forever free tier with 1K limit per day per API key.](#1-find-the-link-to-our-discord-on-httpsshaleprotocolcom-generate-an-api-key-through-the-shale-bot-on-our-discord-no-credit-card-is-required-and-no-free-trials-its-a-forever-free-tier-with-1k-limit-per-day-per-api-key)

- [2. Use https://shale.live/v1 as OpenAI API drop-in replacement](#2-use-httpsshalelivev1-as-openai-api-drop-in-replacement)
