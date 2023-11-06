# Xorbits inference (Xinference)

This notebook goes over how to use Xinference embeddings within LangChain

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
 Model uid: 915845ee-2a04-11ee-8ed4-d29396a3f064  

```

A model UID is returned for you to use. Now you can use Xinference embeddings with LangChain:

```python
from langchain.embeddings import XinferenceEmbeddings  
  
xinference = XinferenceEmbeddings(  
 server\_url="http://0.0.0.0:9997",  
 model\_uid = "915845ee-2a04-11ee-8ed4-d29396a3f064"  
)  

```

```python
query\_result = xinference.embed\_query("This is a test query")  

```

```python
doc\_result = xinference.embed\_documents(["text A", "text B"])  

```

Lastly, terminate the model when you do not need to use it:

```bash
xinference terminate --model-uid "915845ee-2a04-11ee-8ed4-d29396a3f064"  

```

- [Installation](#installation)
- [Deploy Xinference Locally or in a Distributed Cluster.](#deploy-xinference-locally-or-in-a-distributed-cluster)
- [Wrapper](#wrapper)
