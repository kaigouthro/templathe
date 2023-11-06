# Baichuan Chat

Baichuan chat models API by Baichuan Intelligent Technology. For more information, see <https://platform.baichuan-ai.com/docs/api>

```python
from langchain.chat\_models import ChatBaichuan  
from langchain.schema import HumanMessage  

```

```python
chat = ChatBaichuan(  
 baichuan\_api\_key='YOUR\_API\_KEY',  
 baichuan\_secret\_key='YOUR\_SECRET\_KEY'  
)  

```

or you can set `api_key` and `secret_key` in your environment variables

```bash
export BAICHUAN\_API\_KEY=YOUR\_API\_KEY  
export BAICHUAN\_SECRET\_KEY=YOUR\_SECRET\_KEY  

```

```python
chat([  
 HumanMessage(content='我日薪8块钱，请问在闰年的二月，我月薪多少')  
])  

```

```text
 AIMessage(content='首先，我们需要确定闰年的二月有多少天。闰年的二月有29天。\n\n然后，我们可以计算你的月薪：\n\n日薪 = 月薪 / (当月天数)\n\n所以，你的月薪 = 日薪 \* 当月天数\n\n将数值代入公式：\n\n月薪 = 8元/天 \* 29天 = 232元\n\n因此，你在闰年的二月的月薪是232元。')  

```

## For ChatBaichuan with Streaming[​](#for-chatbaichuan-with-streaming "Direct link to For ChatBaichuan with Streaming")

```python
chat = ChatBaichuan(  
 baichuan\_api\_key='YOUR\_API\_KEY',  
 baichuan\_secret\_key='YOUR\_SECRET\_KEY',  
 streaming=True  
)  

```

```python
chat([  
 HumanMessage(content='我日薪8块钱，请问在闰年的二月，我月薪多少')  
])  

```

```text
 AIMessageChunk(content='首先，我们需要确定闰年的二月有多少天。闰年的二月有29天。\n\n然后，我们可以计算你的月薪：\n\n日薪 = 月薪 / (当月天数)\n\n所以，你的月薪 = 日薪 \* 当月天数\n\n将数值代入公式：\n\n月薪 = 8元/天 \* 29天 = 232元\n\n因此，你在闰年的二月的月薪是232元。')  

```

- [For ChatBaichuan with Streaming](#for-chatbaichuan-with-streaming)
