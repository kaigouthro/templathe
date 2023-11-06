# OpenLM

[OpenLM](https://github.com/r2d4/openlm) is a zero-dependency OpenAI-compatible LLM provider that can call different inference endpoints directly via HTTP.

It implements the OpenAI Completion class so that it can be used as a drop-in replacement for the OpenAI API. This changeset utilizes BaseOpenAI for minimal added code.

This examples goes over how to use LangChain to interact with both OpenAI and HuggingFace. You'll need API keys from both.

### Setup[​](#setup "Direct link to Setup")

Install dependencies and set API keys.

```python
# Uncomment to install openlm and openai if you haven't already  
  
# !pip install openlm  
# !pip install openai  

```

```python
from getpass import getpass  
import os  
import subprocess  
  
  
# Check if OPENAI\_API\_KEY environment variable is set  
if "OPENAI\_API\_KEY" not in os.environ:  
 print("Enter your OpenAI API key:")  
 os.environ["OPENAI\_API\_KEY"] = getpass()  
  
# Check if HF\_API\_TOKEN environment variable is set  
if "HF\_API\_TOKEN" not in os.environ:  
 print("Enter your HuggingFace Hub API key:")  
 os.environ["HF\_API\_TOKEN"] = getpass()  

```

### Using LangChain with OpenLM[​](#using-langchain-with-openlm "Direct link to Using LangChain with OpenLM")

Here we're going to call two models in an LLMChain, `text-davinci-003` from OpenAI and `gpt2` on HuggingFace.

```python
from langchain.llms import OpenLM  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
question = "What is the capital of France?"  
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  
  
for model in ["text-davinci-003", "huggingface.co/gpt2"]:  
 llm = OpenLM(model=model)  
 llm\_chain = LLMChain(prompt=prompt, llm=llm)  
 result = llm\_chain.run(question)  
 print(  
 """Model: {}  
Result: {}""".format(  
 model, result  
 )  
 )  

```

```text
 Model: text-davinci-003  
 Result: France is a country in Europe. The capital of France is Paris.  
 Model: huggingface.co/gpt2  
 Result: Question: What is the capital of France?  
   
 Answer: Let's think step by step. I am not going to lie, this is a complicated issue, and I don't see any solutions to all this, but it is still far more  

```

- [Setup](#setup)
- [Using LangChain with OpenLM](#using-langchain-with-openlm)
