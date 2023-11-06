# Modal

This page covers how to use the Modal ecosystem to run LangChain custom LLMs.
It is broken into two parts:

1. Modal installation and web endpoint deployment
1. Using deployed web endpoint with `LLM` wrapper class.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install with `pip install modal`
- Run `modal token new`

## Define your Modal Functions and Webhooks[​](#define-your-modal-functions-and-webhooks "Direct link to Define your Modal Functions and Webhooks")

You must include a prompt. There is a rigid response structure:

```python
class Item(BaseModel):  
 prompt: str  
  
@stub.function()  
@modal.web\_endpoint(method="POST")  
def get\_text(item: Item):  
 return {"prompt": run\_gpt2.call(item.prompt)}  

```

The following is an example with the GPT2 model:

```python
from pydantic import BaseModel  
  
import modal  
  
CACHE\_PATH = "/root/model\_cache"  
  
class Item(BaseModel):  
 prompt: str  
  
stub = modal.Stub(name="example-get-started-with-langchain")  
  
def download\_model():  
 from transformers import GPT2Tokenizer, GPT2LMHeadModel  
 tokenizer = GPT2Tokenizer.from\_pretrained('gpt2')  
 model = GPT2LMHeadModel.from\_pretrained('gpt2')  
 tokenizer.save\_pretrained(CACHE\_PATH)  
 model.save\_pretrained(CACHE\_PATH)  
  
# Define a container image for the LLM function below, which  
# downloads and stores the GPT-2 model.  
image = modal.Image.debian\_slim().pip\_install(  
 "tokenizers", "transformers", "torch", "accelerate"  
).run\_function(download\_model)  
  
@stub.function(  
 gpu="any",  
 image=image,  
 retries=3,  
)  
def run\_gpt2(text: str):  
 from transformers import GPT2Tokenizer, GPT2LMHeadModel  
 tokenizer = GPT2Tokenizer.from\_pretrained(CACHE\_PATH)  
 model = GPT2LMHeadModel.from\_pretrained(CACHE\_PATH)  
 encoded\_input = tokenizer(text, return\_tensors='pt').input\_ids  
 output = model.generate(encoded\_input, max\_length=50, do\_sample=True)  
 return tokenizer.decode(output[0], skip\_special\_tokens=True)  
  
@stub.function()  
@modal.web\_endpoint(method="POST")  
def get\_text(item: Item):  
 return {"prompt": run\_gpt2.call(item.prompt)}  

```

### Deploy the web endpoint[​](#deploy-the-web-endpoint "Direct link to Deploy the web endpoint")

Deploy the web endpoint to Modal cloud with the [`modal deploy`](https://modal.com/docs/reference/cli/deploy) CLI command.
Your web endpoint will acquire a persistent URL under the `modal.run` domain.

## LLM wrapper around Modal web endpoint[​](#llm-wrapper-around-modal-web-endpoint "Direct link to LLM wrapper around Modal web endpoint")

The `Modal` LLM wrapper class which will accept your deployed web endpoint's URL.

```python
from langchain.llms import Modal  
  
endpoint\_url = "https://ecorp--custom-llm-endpoint.modal.run" # REPLACE ME with your deployed Modal web endpoint's URL  
  
llm = Modal(endpoint\_url=endpoint\_url)  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
  
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"  
  
llm\_chain.run(question)  

```

- [Installation and Setup](#installation-and-setup)

- [Define your Modal Functions and Webhooks](#define-your-modal-functions-and-webhooks)

  - [Deploy the web endpoint](#deploy-the-web-endpoint)

- [LLM wrapper around Modal web endpoint](#llm-wrapper-around-modal-web-endpoint)

- [Deploy the web endpoint](#deploy-the-web-endpoint)
