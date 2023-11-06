# Tencent Hunyuan

Hunyuan chat model API by Tencent. For more information, see <https://cloud.tencent.com/document/product/1729>

```python
from langchain.chat\_models import ChatHunyuan  
from langchain.schema import HumanMessage  

```

```python
chat = ChatHunyuan(  
 hunyuan\_app\_id='YOUR\_APP\_ID',  
 hunyuan\_secret\_id='YOUR\_SECRET\_ID',  
 hunyuan\_secret\_key='YOUR\_SECRET\_KEY',  
)  

```

```python
chat([  
 HumanMessage(content='You are a helpful assistant that translates English to French.Translate this sentence from English to French. I love programming.')  
])  

```

```text
 AIMessage(content="J'aime programmer.")  

```

## For ChatHunyuan with Streaming[​](#for-chathunyuan-with-streaming "Direct link to For ChatHunyuan with Streaming")

```python
chat = ChatHunyuan(  
 hunyuan\_app\_id='YOUR\_APP\_ID',  
 hunyuan\_secret\_id='YOUR\_SECRET\_ID',  
 hunyuan\_secret\_key='YOUR\_SECRET\_KEY',  
 streaming=True,  
)  

```

```python
chat([  
 HumanMessage(content='You are a helpful assistant that translates English to French.Translate this sentence from English to French. I love programming.')  
])  

```

```text
 AIMessageChunk(content="J'aime programmer.")  

```

- [For ChatHunyuan with Streaming](#for-chathunyuan-with-streaming)
