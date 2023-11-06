# Hugging Face Hub

The [Hugging Face Hub](https://huggingface.co/docs/hub/index) is a platform with over 120k models, 20k datasets, and 50k demo apps (Spaces), all open source and publicly available, in an online platform where people can easily collaborate and build ML together.

This example showcases how to connect to the `Hugging Face Hub` and use different models.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

To use, you should have the `huggingface_hub` python [package installed](https://huggingface.co/docs/huggingface_hub/installation).

```bash
pip install huggingface\_hub  

```

```python
# get a token: https://huggingface.co/docs/api-inference/quicktour#get-your-api-token  
  
from getpass import getpass  
  
HUGGINGFACEHUB\_API\_TOKEN = getpass()  

```

```text
 ········  

```

```python
import os  
  
os.environ["HUGGINGFACEHUB\_API\_TOKEN"] = HUGGINGFACEHUB\_API\_TOKEN  

```

## Prepare Examples[​](#prepare-examples "Direct link to Prepare Examples")

```python
from langchain.llms import HuggingFaceHub  

```

```python
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
question = "Who won the FIFA World Cup in the year 1994? "  
  
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

## Examples[​](#examples "Direct link to Examples")

Below are some examples of models you can access through the `Hugging Face Hub` integration.

### `Flan`, by `Google`[​](#flan-by-google "Direct link to flan-by-google")

```python
repo\_id = "google/flan-t5-xxl" # See https://huggingface.co/models?pipeline\_tag=text-generation&sort=downloads for some other options  

```

```python
llm = HuggingFaceHub(  
 repo\_id=repo\_id, model\_kwargs={"temperature": 0.5, "max\_length": 64}  
)  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
  
print(llm\_chain.run(question))  

```

```text
 The FIFA World Cup was held in the year 1994. West Germany won the FIFA World Cup in 1994  

```

### `Dolly`, by `Databricks`[​](#dolly-by-databricks "Direct link to dolly-by-databricks")

See [Databricks](https://huggingface.co/databricks) organization page for a list of available models.

```python
repo\_id = "databricks/dolly-v2-3b"  

```

```python
llm = HuggingFaceHub(  
 repo\_id=repo\_id, model\_kwargs={"temperature": 0.5, "max\_length": 64}  
)  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
print(llm\_chain.run(question))  

```

```text
 First of all, the world cup was won by the Germany. Then the Argentina won the world cup in 2022. So, the Argentina won the world cup in 1994.  
   
   
 Question: Who  

```

### `Camel`, by `Writer`[​](#camel-by-writer "Direct link to camel-by-writer")

See [Writer's](https://huggingface.co/Writer) organization page for a list of available models.

```python
repo\_id = "Writer/camel-5b-hf" # See https://huggingface.co/Writer for other options  

```

```python
llm = HuggingFaceHub(  
 repo\_id=repo\_id, model\_kwargs={"temperature": 0.5, "max\_length": 64}  
)  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
print(llm\_chain.run(question))  

```

### `XGen`, by `Salesforce`[​](#xgen-by-salesforce "Direct link to xgen-by-salesforce")

See [more information](https://github.com/salesforce/xgen).

```python
repo\_id = "Salesforce/xgen-7b-8k-base"  

```

```python
llm = HuggingFaceHub(  
 repo\_id=repo\_id, model\_kwargs={"temperature": 0.5, "max\_length": 64}  
)  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
print(llm\_chain.run(question))  

```

### `Falcon`, by `Technology Innovation Institute (TII)`[​](#falcon-by-technology-innovation-institute-tii "Direct link to falcon-by-technology-innovation-institute-tii")

See [more information](https://huggingface.co/tiiuae/falcon-40b).

```python
repo\_id = "tiiuae/falcon-40b"  

```

```python
llm = HuggingFaceHub(  
 repo\_id=repo\_id, model\_kwargs={"temperature": 0.5, "max\_length": 64}  
)  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
print(llm\_chain.run(question))  

```

### `InternLM-Chat`, by `Shanghai AI Laboratory`[​](#internlm-chat-by-shanghai-ai-laboratory "Direct link to internlm-chat-by-shanghai-ai-laboratory")

See [more information](https://huggingface.co/internlm/internlm-7b).

```python
repo\_id = "internlm/internlm-chat-7b"  

```

```python
llm = HuggingFaceHub(  
 repo\_id=repo\_id, model\_kwargs={"max\_length": 128, "temperature": 0.8}  
)  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
print(llm\_chain.run(question))  

```

### `Qwen`, by `Alibaba Cloud`[​](#qwen-by-alibaba-cloud "Direct link to qwen-by-alibaba-cloud")

`Tongyi Qianwen-7B` (`Qwen-7B`) is a model with a scale of 7 billion parameters in the `Tongyi Qianwen` large model series developed by `Alibaba Cloud`. `Qwen-7B` is a large language model based on Transformer, which is trained on ultra-large-scale pre-training data.

See [more information on HuggingFace](https://huggingface.co/Qwen/Qwen-7B) of on [GitHub](https://github.com/QwenLM/Qwen-7B).

See here a [big example for LangChain integration and Qwen](https://github.com/QwenLM/Qwen-7B/blob/main/examples/langchain_tooluse.ipynb).

```python
repo\_id = "Qwen/Qwen-7B"  

```

```python
llm = HuggingFaceHub(  
 repo\_id=repo\_id, model\_kwargs={"max\_length": 128, "temperature": 0.5}  
)  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
print(llm\_chain.run(question))  

```

- [Installation and Setup](#installation-and-setup)

- [Prepare Examples](#prepare-examples)

- [Examples](#examples)

  - [`Flan`, by `Google`](#flan-by-google)
  - [`Dolly`, by `Databricks`](#dolly-by-databricks)
  - [`Camel`, by `Writer`](#camel-by-writer)
  - [`XGen`, by `Salesforce`](#xgen-by-salesforce)
  - [`Falcon`, by `Technology Innovation Institute (TII)`](#falcon-by-technology-innovation-institute-tii)
  - [`InternLM-Chat`, by `Shanghai AI Laboratory`](#internlm-chat-by-shanghai-ai-laboratory)
  - [`Qwen`, by `Alibaba Cloud`](#qwen-by-alibaba-cloud)

- [`Flan`, by `Google`](#flan-by-google)

- [`Dolly`, by `Databricks`](#dolly-by-databricks)

- [`Camel`, by `Writer`](#camel-by-writer)

- [`XGen`, by `Salesforce`](#xgen-by-salesforce)

- [`Falcon`, by `Technology Innovation Institute (TII)`](#falcon-by-technology-innovation-institute-tii)

- [`InternLM-Chat`, by `Shanghai AI Laboratory`](#internlm-chat-by-shanghai-ai-laboratory)

- [`Qwen`, by `Alibaba Cloud`](#qwen-by-alibaba-cloud)
