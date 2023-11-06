# YandexGPT

This notebook goes over how to use Langchain with [YandexGPT](https://cloud.yandex.com/en/services/yandexgpt).

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
from langchain.chains import LLMChain  
from langchain.llms import YandexGPT  
from langchain.prompts import PromptTemplate  

```

```python
template = "What is the capital of {country}?"  
prompt = PromptTemplate(template=template, input\_variables=["country"])  

```

```python
llm = YandexGPT()  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
country = "Russia"  
  
llm\_chain.run(country)  

```

```text
 'Moscow'  

```
