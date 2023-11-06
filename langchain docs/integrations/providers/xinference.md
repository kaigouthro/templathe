# Xorbits Inference (Xinference)

This page demonstrates how to use [Xinference](https://github.com/xorbitsai/inference)
with LangChain.

`Xinference` is a powerful and versatile library designed to serve LLMs,
speech recognition models, and multimodal models, even on your laptop.
With Xorbits Inference, you can effortlessly deploy and serve your or
state-of-the-art built-in models using just a single command.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

Xinference can be installed via pip from PyPI:

```bash
pip install "xinference[all]"  

```

## LLM[​](#llm "Direct link to LLM")

Xinference supports various models compatible with GGML, including chatglm, baichuan, whisper,
vicuna, and orca. To view the builtin models, run the command:

```bash
xinference list --all  

```

### Wrapper for Xinference[​](#wrapper-for-xinference "Direct link to Wrapper for Xinference")

You can start a local instance of Xinference by running:

```bash
xinference  

```

You can also deploy Xinference in a distributed cluster. To do so, first start an Xinference supervisor
on the server you want to run it:

```bash
xinference-supervisor -H "${supervisor\_host}"  

```

Then, start the Xinference workers on each of the other servers where you want to run them on:

```bash
xinference-worker -e "http://${supervisor\_host}:9997"  

```

You can also start a local instance of Xinference by running:

```bash
xinference  

```

Once Xinference is running, an endpoint will be accessible for model management via CLI or
Xinference client.

For local deployment, the endpoint will be http://localhost:9997.

For cluster deployment, the endpoint will be http://${supervisor_host}:9997.

Then, you need to launch a model. You can specify the model names and other attributes
including model_size_in_billions and quantization. You can use command line interface (CLI) to
do it. For example,

```bash
xinference launch -n orca -s 3 -q q4\_0  

```

A model uid will be returned.

Example usage:

```python
from langchain.llms import Xinference  
  
llm = Xinference(  
 server\_url="http://0.0.0.0:9997",  
 model\_uid = {model\_uid} # replace model\_uid with the model UID return from launching the model  
)  
  
llm(  
 prompt="Q: where can we visit in the capital of France? A:",  
 generate\_config={"max\_tokens": 1024, "stream": True},  
)  
  

```

### Usage[​](#usage "Direct link to Usage")

For more information and detailed examples, refer to the
[example for xinference LLMs](/docs/integrations/llms/xinference.html)

### Embeddings[​](#embeddings "Direct link to Embeddings")

Xinference also supports embedding queries and documents. See
[example for xinference embeddings](/docs/integrations/text_embedding/xinference.html)
for a more detailed demo.

- [Installation and Setup](#installation-and-setup)

- [LLM](#llm)

  - [Wrapper for Xinference](#wrapper-for-xinference)
  - [Usage](#usage)
  - [Embeddings](#embeddings)

- [Wrapper for Xinference](#wrapper-for-xinference)

- [Usage](#usage)

- [Embeddings](#embeddings)
