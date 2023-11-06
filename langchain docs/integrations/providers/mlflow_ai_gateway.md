# MLflow AI Gateway

[The MLflow AI Gateway](https://www.mlflow.org/docs/latest/gateway/index.html) service is a powerful tool designed to streamline the usage and management of various large
language model (LLM) providers, such as OpenAI and Anthropic, within an organization. It offers a high-level interface
that simplifies the interaction with these services by providing a unified endpoint to handle specific LLM related requests.
See [the MLflow AI Gateway documentation](https://mlflow.org/docs/latest/gateway/index.html) for more details.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

Install `mlflow` with MLflow AI Gateway dependencies:

```sh
pip install 'mlflow[gateway]'  

```

Set the OpenAI API key as an environment variable:

```sh
export OPENAI\_API\_KEY=...  

```

Create a configuration file:

```yaml
routes:  
 - name: completions  
 route\_type: llm/v1/completions  
 model:  
 provider: openai  
 name: text-davinci-003  
 config:  
 openai\_api\_key: $OPENAI\_API\_KEY  
  
 - name: embeddings  
 route\_type: llm/v1/embeddings  
 model:  
 provider: openai  
 name: text-embedding-ada-002  
 config:  
 openai\_api\_key: $OPENAI\_API\_KEY  

```

Start the Gateway server:

```sh
mlflow gateway start --config-path /path/to/config.yaml  

```

## Example provided by `MLflow`[​](#example-provided-by-mlflow "Direct link to example-provided-by-mlflow")

The `mlflow.langchain` module provides an API for logging and loading `LangChain` models.
This module exports multivariate LangChain models in the langchain flavor and univariate LangChain
models in the pyfunc flavor.

See the [API documentation and examples](https://www.mlflow.org/docs/latest/python_api/mlflow.langchain.html).

## Completions Example[​](#completions-example "Direct link to Completions Example")

```python
import mlflow  
from langchain.chains import LLMChain, PromptTemplate  
from langchain.llms import MlflowAIGateway  
  
gateway = MlflowAIGateway(  
 gateway\_uri="http://127.0.0.1:5000",  
 route="completions",  
 params={  
 "temperature": 0.0,  
 "top\_p": 0.1,  
 },  
)  
  
llm\_chain = LLMChain(  
 llm=gateway,  
 prompt=PromptTemplate(  
 input\_variables=["adjective"],  
 template="Tell me a {adjective} joke",  
 ),  
)  
result = llm\_chain.run(adjective="funny")  
print(result)  
  
with mlflow.start\_run():  
 model\_info = mlflow.langchain.log\_model(chain, "model")  
  
model = mlflow.pyfunc.load\_model(model\_info.model\_uri)  
print(model.predict([{"adjective": "funny"}]))  

```

## Embeddings Example[​](#embeddings-example "Direct link to Embeddings Example")

```python
from langchain.embeddings import MlflowAIGatewayEmbeddings  
  
embeddings = MlflowAIGatewayEmbeddings(  
 gateway\_uri="http://127.0.0.1:5000",  
 route="embeddings",  
)  
  
print(embeddings.embed\_query("hello"))  
print(embeddings.embed\_documents(["hello"]))  

```

## Chat Example[​](#chat-example "Direct link to Chat Example")

```python
from langchain.chat\_models import ChatMLflowAIGateway  
from langchain.schema import HumanMessage, SystemMessage  
  
chat = ChatMLflowAIGateway(  
 gateway\_uri="http://127.0.0.1:5000",  
 route="chat",  
 params={  
 "temperature": 0.1  
 }  
)  
  
messages = [  
 SystemMessage(  
 content="You are a helpful assistant that translates English to French."  
 ),  
 HumanMessage(  
 content="Translate this sentence from English to French: I love programming."  
 ),  
]  
print(chat(messages))  

```

## Databricks MLflow AI Gateway[​](#databricks-mlflow-ai-gateway "Direct link to Databricks MLflow AI Gateway")

Databricks MLflow AI Gateway is in private preview.
Please contact a Databricks representative to enroll in the preview.

```python
from langchain.chains import LLMChain  
from langchain.prompts import PromptTemplate  
from langchain.llms import MlflowAIGateway  
  
gateway = MlflowAIGateway(  
 gateway\_uri="databricks",  
 route="completions",  
)  
  
llm\_chain = LLMChain(  
 llm=gateway,  
 prompt=PromptTemplate(  
 input\_variables=["adjective"],  
 template="Tell me a {adjective} joke",  
 ),  
)  
result = llm\_chain.run(adjective="funny")  
print(result)  

```

- [Installation and Setup](#installation-and-setup)
- [Example provided by `MLflow`](#example-provided-by-mlflow)
- [Completions Example](#completions-example)
- [Embeddings Example](#embeddings-example)
- [Chat Example](#chat-example)
- [Databricks MLflow AI Gateway](#databricks-mlflow-ai-gateway)
