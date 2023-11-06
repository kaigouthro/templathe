# GPT4All

This page covers how to use the `GPT4All` wrapper within LangChain. The tutorial is divided into two parts: installation and setup, followed by usage with an example.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install the Python package with `pip install pyllamacpp`
- Download a [GPT4All model](https://github.com/nomic-ai/pyllamacpp#supported-model) and place it in your desired directory

## Usage[​](#usage "Direct link to Usage")

### GPT4All[​](#gpt4all-1 "Direct link to GPT4All")

To use the GPT4All wrapper, you need to provide the path to the pre-trained model file and the model's configuration.

```python
from langchain.llms import GPT4All  
  
# Instantiate the model. Callbacks support token-wise streaming  
model = GPT4All(model="./models/gpt4all-model.bin", n\_ctx=512, n\_threads=8)  
  
# Generate text  
response = model("Once upon a time, ")  

```

You can also customize the generation parameters, such as n_predict, temp, top_p, top_k, and others.

To stream the model's predictions, add in a CallbackManager.

```python
from langchain.llms import GPT4All  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  
  
# There are many CallbackHandlers supported, such as  
# from langchain.callbacks.streamlit import StreamlitCallbackHandler  
  
callbacks = [StreamingStdOutCallbackHandler()]  
model = GPT4All(model="./models/gpt4all-model.bin", n\_ctx=512, n\_threads=8)  
  
# Generate text. Tokens are streamed through the callback manager.  
model("Once upon a time, ", callbacks=callbacks)  

```

## Model File[​](#model-file "Direct link to Model File")

You can find links to model file downloads in the [pyllamacpp](https://github.com/nomic-ai/pyllamacpp) repository.

For a more detailed walkthrough of this, see [this notebook](/docs/integrations/llms/gpt4all.html)

- [Installation and Setup](#installation-and-setup)

- [Usage](#usage)

  - [GPT4All](#gpt4all-1)

- [Model File](#model-file)

- [GPT4All](#gpt4all-1)
