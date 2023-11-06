# DeepSparse

This page covers how to use the [DeepSparse](https://github.com/neuralmagic/deepsparse) inference runtime within LangChain.
It is broken into two parts: installation and setup, and then examples of DeepSparse usage.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install the Python package with `pip install deepsparse`
- Choose a [SparseZoo model](https://sparsezoo.neuralmagic.com/?useCase=text_generation) or export a support model to ONNX [using Optimum](https://github.com/neuralmagic/notebooks/blob/main/notebooks/opt-text-generation-deepsparse-quickstart/OPT_Text_Generation_DeepSparse_Quickstart.ipynb)

There exists a DeepSparse LLM wrapper, that provides a unified interface for all models:

```python
from langchain.llms import DeepSparse  
  
llm = DeepSparse(model='zoo:nlg/text\_generation/codegen\_mono-350m/pytorch/huggingface/bigpython\_bigquery\_thepile/base-none')  
  
print(llm('def fib():'))  

```

Additional parameters can be passed using the `config` parameter:

```python
config = {'max\_generated\_tokens': 256}  
  
llm = DeepSparse(model='zoo:nlg/text\_generation/codegen\_mono-350m/pytorch/huggingface/bigpython\_bigquery\_thepile/base-none', config=config)  

```

- [Installation and Setup](#installation-and-setup)
