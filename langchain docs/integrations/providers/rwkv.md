# RWKV-4

This page covers how to use the `RWKV-4` wrapper within LangChain.
It is broken into two parts: installation and setup, and then usage with an example.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install the Python package with `pip install rwkv`
- Install the tokenizer Python package with `pip install tokenizer`
- Download a [RWKV model](https://huggingface.co/BlinkDL/rwkv-4-raven/tree/main) and place it in your desired directory
- Download the [tokens file](https://raw.githubusercontent.com/BlinkDL/ChatRWKV/main/20B_tokenizer.json)

## Usage[​](#usage "Direct link to Usage")

### RWKV[​](#rwkv "Direct link to RWKV")

To use the RWKV wrapper, you need to provide the path to the pre-trained model file and the tokenizer's configuration.

````python
from langchain.llms import RWKV  
  
# Test the model  
  
```python  
  
def generate\_prompt(instruction, input=None):  
 if input:  
 return f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.  
  
# Instruction:  
{instruction}  
  
# Input:  
{input}  
  
# Response:  
"""  
 else:  
 return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.  
  
# Instruction:  
{instruction}  
  
# Response:  
"""  
  
  
model = RWKV(model="./models/RWKV-4-Raven-3B-v7-Eng-20230404-ctx4096.pth", strategy="cpu fp32", tokens\_path="./rwkv/20B\_tokenizer.json")  
response = model(generate\_prompt("Once upon a time, "))  

````

## Model File[​](#model-file "Direct link to Model File")

You can find links to model file downloads at the [RWKV-4-Raven](https://huggingface.co/BlinkDL/rwkv-4-raven/tree/main) repository.

### Rwkv-4 models -> recommended VRAM[​](#rwkv-4-models---recommended-vram "Direct link to Rwkv-4 models -> recommended VRAM")

```text
RWKV VRAM  
Model | 8bit | bf16/fp16 | fp32  
14B | 16GB | 28GB | >50GB  
7B | 8GB | 14GB | 28GB  
3B | 2.8GB| 6GB | 12GB  
1b5 | 1.3GB| 3GB | 6GB  

```

See the [rwkv pip](https://pypi.org/project/rwkv/) page for more information about strategies, including streaming and cuda support.

- [Installation and Setup](#installation-and-setup)

- [Usage](#usage)

  - [RWKV](#rwkv)

- [Model File](#model-file)

  - [Rwkv-4 models -> recommended VRAM](#rwkv-4-models---recommended-vram)

- [RWKV](#rwkv)

- [Rwkv-4 models -> recommended VRAM](#rwkv-4-models---recommended-vram)
