# GigaChat

This notebook shows how to use LangChain with [GigaChat](https://developers.sber.ru/portal/products/gigachat).
To use you need to install `gigachat` python package.

```python
# !pip install gigachat  

```

To get GigaChat credentials you need to [create account](https://developers.sber.ru/studio/login) and [get access to API](https://developers.sber.ru/docs/ru/gigachat/api/integration)

## Example[​](#example "Direct link to Example")

```python
import os  
from getpass import getpass  
  
os.environ['GIGACHAT\_CREDENTIALS'] = getpass()  

```

```python
from langchain.chat\_models import GigaChat  
  
chat = GigaChat(verify\_ssl\_certs=False)  

```

```python
from langchain.schema import SystemMessage, HumanMessage  
  
messages = [  
 SystemMessage(  
 content="You are a helpful AI that shares everything you know. Talk in English."  
 ),  
 HumanMessage(  
 content="Tell me a joke"  
 ),  
]  
  
print(chat(messages).content)  

```

```text
 What do you get when you cross a goat and a skunk? A smelly goat!  

```

- [Example](#example)
