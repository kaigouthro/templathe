# ERNIE-Bot Chat

[ERNIE-Bot](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/jlil56u11) is a large language model developed by Baidu, covering a huge amount of Chinese data.
This notebook covers how to get started with ErnieBot chat models.

```python
from langchain.chat\_models import ErnieBotChat  
from langchain.schema import HumanMessage  

```

```python
chat = ErnieBotChat(ernie\_client\_id='YOUR\_CLIENT\_ID', ernie\_client\_secret='YOUR\_CLIENT\_SECRET')  

```

or you can set `client_id` and `client_secret` in your environment variables

```bash
export ERNIE\_CLIENT\_ID=YOUR\_CLIENT\_ID  
export ERNIE\_CLIENT\_SECRET=YOUR\_CLIENT\_SECRET  

```

```python
chat([  
 HumanMessage(content='hello there, who are you?')  
])  

```

```text
 AIMessage(content='Hello, I am an artificial intelligence language model. My purpose is to help users answer questions or provide information. What can I do for you?', additional\_kwargs={}, example=False)  

```
