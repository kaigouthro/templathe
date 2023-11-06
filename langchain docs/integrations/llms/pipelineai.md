# PipelineAI

[PipelineAI](https://pipeline.ai) allows you to run your ML models at scale in the cloud. It also provides API access to [several LLM models](https://pipeline.ai).

This notebook goes over how to use Langchain with [PipelineAI](https://docs.pipeline.ai/docs).

## PipelineAI example[​](#pipelineai-example "Direct link to PipelineAI example")

[This example shows how PipelineAI integrated with LangChain](https://docs.pipeline.ai/docs/langchain) and it is created by PipelineAI.

## Setup[​](#setup "Direct link to Setup")

The `pipeline-ai` library is required to use the `PipelineAI` API, AKA `Pipeline Cloud`. Install `pipeline-ai` using `pip install pipeline-ai`.

```bash
# Install the package  
pip install pipeline-ai  

```

## Example[​](#example "Direct link to Example")

### Imports[​](#imports "Direct link to Imports")

```python
import os  
from langchain.llms import PipelineAI  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

### Set the Environment API Key[​](#set-the-environment-api-key "Direct link to Set the Environment API Key")

Make sure to get your API key from PipelineAI. Check out the [cloud quickstart guide](https://docs.pipeline.ai/docs/cloud-quickstart). You'll be given a 30 day free trial with 10 hours of serverless GPU compute to test different models.

```python
os.environ["PIPELINE\_API\_KEY"] = "YOUR\_API\_KEY\_HERE"  

```

## Create the PipelineAI instance[​](#create-the-pipelineai-instance "Direct link to Create the PipelineAI instance")

When instantiating PipelineAI, you need to specify the id or tag of the pipeline you want to use, e.g. `pipeline_key = "public/gpt-j:base"`. You then have the option of passing additional pipeline-specific keyword arguments:

```python
llm = PipelineAI(pipeline\_key="YOUR\_PIPELINE\_KEY", pipeline\_kwargs={...})  

```

### Create a Prompt Template[​](#create-a-prompt-template "Direct link to Create a Prompt Template")

We will create a prompt template for Question and Answer.

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

### Initiate the LLMChain[​](#initiate-the-llmchain "Direct link to Initiate the LLMChain")

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

### Run the LLMChain[​](#run-the-llmchain "Direct link to Run the LLMChain")

Provide a question and run the LLMChain.

```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"  
  
llm\_chain.run(question)  

```

- [PipelineAI example](#pipelineai-example)

- [Setup](#setup)

- [Example](#example)

  - [Imports](#imports)
  - [Set the Environment API Key](#set-the-environment-api-key)

- [Create the PipelineAI instance](#create-the-pipelineai-instance)

  - [Create a Prompt Template](#create-a-prompt-template)
  - [Initiate the LLMChain](#initiate-the-llmchain)
  - [Run the LLMChain](#run-the-llmchain)

- [Imports](#imports)

- [Set the Environment API Key](#set-the-environment-api-key)

- [Create a Prompt Template](#create-a-prompt-template)

- [Initiate the LLMChain](#initiate-the-llmchain)

- [Run the LLMChain](#run-the-llmchain)
