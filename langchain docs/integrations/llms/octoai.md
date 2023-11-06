# OctoAI

[OctoML](https://docs.octoai.cloud/docs) is a service with efficient compute. It enables users to integrate their choice of AI models into applications. The `OctoAI` compute service helps you run, tune, and scale AI applications.

This example goes over how to use LangChain to interact with `OctoAI` [LLM endpoints](https://octoai.cloud/templates)

## Setup[​](#setup "Direct link to Setup")

To run our example app, there are four simple steps to take:

1. Clone the MPT-7B demo template to your OctoAI account by visiting <https://octoai.cloud/templates/mpt-7b-demo> then clicking "Clone Template."

   1. If you want to use a different LLM model, you can also containerize the model and make a custom OctoAI endpoint yourself, by following [Build a Container from Python](doc:create-custom-endpoints-from-python-code) and [Create a Custom Endpoint from a Container](doc:create-custom-endpoints-from-a-container)

1. Paste your Endpoint URL in the code cell below

1. Get an API Token from [your OctoAI account page](https://octoai.cloud/settings).

1. Paste your API key in in the code cell below

Clone the MPT-7B demo template to your OctoAI account by visiting <https://octoai.cloud/templates/mpt-7b-demo> then clicking "Clone Template."

1. If you want to use a different LLM model, you can also containerize the model and make a custom OctoAI endpoint yourself, by following [Build a Container from Python](doc:create-custom-endpoints-from-python-code) and [Create a Custom Endpoint from a Container](doc:create-custom-endpoints-from-a-container)

Paste your Endpoint URL in the code cell below

Get an API Token from [your OctoAI account page](https://octoai.cloud/settings).

Paste your API key in in the code cell below

```python
import os  
  
os.environ["OCTOAI\_API\_TOKEN"] = "OCTOAI\_API\_TOKEN"  
os.environ["ENDPOINT\_URL"] = "https://mpt-7b-demo-f1kzsig6xes9.octoai.run/generate"  

```

```python
from langchain.llms.octoai\_endpoint import OctoAIEndpoint  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

## Example[​](#example "Direct link to Example")

```python
template = """Below is an instruction that describes a task. Write a response that appropriately completes the request.\n Instruction:\n{question}\n Response: """  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

```python
llm = OctoAIEndpoint(  
 model\_kwargs={  
 "max\_new\_tokens": 200,  
 "temperature": 0.75,  
 "top\_p": 0.95,  
 "repetition\_penalty": 1,  
 "seed": None,  
 "stop": [],  
 },  
)  

```

```python
question = "Who was leonardo davinci?"  
  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
  
llm\_chain.run(question)  

```

```text
 '\nLeonardo da Vinci was an Italian polymath and painter regarded by many as one of the greatest painters of all time. He is best known for his masterpieces including Mona Lisa, The Last Supper, and The Virgin of the Rocks. He was a draftsman, sculptor, architect, and one of the most important figures in the history of science. Da Vinci flew gliders, experimented with water turbines and windmills, and invented the catapult and a joystick-type human-powered aircraft control. He may have pioneered helicopters. As a scholar, he was interested in anatomy, geology, botany, engineering, mathematics, and astronomy.\nOther painters and patrons claimed to be more talented, but Leonardo da Vinci was an incredibly productive artist, sculptor, engineer, anatomist, and scientist.'  

```

- [Setup](#setup)
- [Example](#example)
