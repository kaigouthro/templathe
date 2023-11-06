# YandexGPT

This notebook goes over how to use Langchain with [YandexGPT](https://cloud.yandex.com/en/services/yandexgpt) chat model.

To use, you should have the `yandexcloud` python package installed.

```python
%pip install yandexcloud  

```

First, you should [create service account](https://cloud.yandex.com/en/docs/iam/operations/sa/create) with the `ai.languageModels.user` role.

Next, you have two authentication options:

- [IAM token](https://cloud.yandex.com/en/docs/iam/operations/iam-token/create-for-sa).
  You can specify the token in a constructor parameter `iam_token` or in an environment variable `YC_IAM_TOKEN`.
- [API key](https://cloud.yandex.com/en/docs/iam/operations/api-key/create)
  You can specify the key in a constructor parameter `api_key` or in an environment variable `YC_API_KEY`.

```python
from langchain.chat\_models import ChatYandexGPT  
from langchain.schema import HumanMessage, SystemMessage  

```

```python
chat\_model = ChatYandexGPT()  

```

```python
answer = chat\_model(  
 [  
 SystemMessage(content="You are a helpful assistant that translates English to French."),  
 HumanMessage(content="I love programming.")  
 ]  
)  
answer  

```

```text
 AIMessage(content="Je t'aime programmer.")  

```
