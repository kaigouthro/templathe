# Xorbits Inference (Xinference)

[Xinference](https://github.com/xorbitsai/inference) is a powerful and versatile library designed to serve LLMs,
speech recognition models, and multimodal models, even on your laptop. It supports a variety of models compatible with GGML, such as chatglm, baichuan, whisper, vicuna, orca, and many others. This notebook demonstrates how to use Xinference with LangChain.

## Installation[​](#installation "Direct link to Installation")

Install `Xinference` through PyPI:

```python
%pip install "xinference[all]"  

```

## Deploy Xinference Locally or in a Distributed Cluster.[​](#deploy-xinference-locally-or-in-a-distributed-cluster "Direct link to Deploy Xinference Locally or in a Distributed Cluster.")

For local deployment, run `xinference`.

To deploy Xinference in a cluster, first start an Xinference supervisor using the `xinference-supervisor`. You can also use the option -p to specify the port and -H to specify the host. The default port is 9997.

Then, start the Xinference workers using `xinference-worker` on each server you want to run them on.

You can consult the README file from [Xinference](https://github.com/xorbitsai/inference) for more information.

## Wrapper[​](#wrapper "Direct link to Wrapper")

To use Xinference with LangChain, you need to first launch a model. You can use command line interface (CLI) to do so:

```bash
xinference launch -n vicuna-v1.3 -f ggmlv3 -q q4\_0  

```

```text
 Model uid: 7167b2b0-2a04-11ee-83f0-d29396a3f064  

```

A model UID is returned for you to use. Now you can use Xinference with LangChain:

```python
from langchain.llms import Xinference  
  
llm = Xinference(  
 server\_url="http://0.0.0.0:9997",  
 model\_uid = "7167b2b0-2a04-11ee-83f0-d29396a3f064"  
)  
  
llm(  
 prompt="Q: where can we visit in the capital of France? A:",  
 generate\_config={"max\_tokens": 1024, "stream": True},  
)  

```

```text
 ' You can visit the Eiffel Tower, Notre-Dame Cathedral, the Louvre Museum, and many other historical sites in Paris, the capital of France.'  

```

### Integrate with a LLMChain[​](#integrate-with-a-llmchain "Direct link to Integrate with a LLMChain")

```python
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
  
template = "Where can we visit in the capital of {country}?"  
  
prompt = PromptTemplate(template=template, input\_variables=["country"])  
  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
  
generated = llm\_chain.run(country="France")  
print(generated)  

```

```text
   
 A: You can visit many places in Paris, such as the Eiffel Tower, the Louvre Museum, Notre-Dame Cathedral, the Champs-Elysées, Montmartre, Sacré-Cœur, and the Palace of Versailles.  

```

Lastly, terminate the model when you do not need to use it:

```bash
xinference terminate --model-uid "7167b2b0-2a04-11ee-83f0-d29396a3f064"  

```

- [Installation](#installation)

- [Deploy Xinference Locally or in a Distributed Cluster.](#deploy-xinference-locally-or-in-a-distributed-cluster)

- [Wrapper](#wrapper)

  - [Integrate with a LLMChain](#integrate-with-a-llmchain)

- [Integrate with a LLMChain](#integrate-with-a-llmchain)
