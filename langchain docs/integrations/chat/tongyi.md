# Tongyi Qwen

Tongyi Qwen is a large language model developed by Alibaba's Damo Academy. It is capable of understanding user intent through natural language understanding and semantic analysis, based on user input in natural language. It provides services and assistance to users in different domains and tasks. By providing clear and detailed instructions, you can obtain results that better align with your expectations.
In this notebook, we will introduce how to use langchain with [Tongyi](https://www.aliyun.com/product/dashscope) mainly in `Chat` corresponding
to the package `langchain/chat_models` in langchain

```bash
# Install the package  
pip install dashscope  

```

```python
# Get a new token: https://help.aliyun.com/document\_detail/611472.html?spm=a2c4g.2399481.0.0  
from getpass import getpass  
  
DASHSCOPE\_API\_KEY = getpass()  

```

```text
 ········  

```

```python
import os  
  
os.environ["DASHSCOPE\_API\_KEY"] = DASHSCOPE\_API\_KEY  

```

```python
from langchain.chat\_models.tongyi import ChatTongyi  
from langchain.schema import HumanMessage  
  
chatLLM = ChatTongyi(  
 streaming=True,  
)  
res = chatLLM.stream([HumanMessage(content="hi")], streaming=True)  
for r in res:  
 print("chat resp:", r)  

```

```text
 chat resp: content='Hello! How' additional\_kwargs={} example=False  
 chat resp: content=' can I assist you today?' additional\_kwargs={} example=False  

```

```python
from langchain.schema import AIMessage, HumanMessage, SystemMessage  
messages = [  
 SystemMessage(  
 content="You are a helpful assistant that translates English to French."  
 ),  
 HumanMessage(  
 content="Translate this sentence from English to French. I love programming."  
 ),  
]  
chatLLM(messages)  

```

```text
 AIMessageChunk(content="J'aime programmer.", additional\_kwargs={}, example=False)  

```
