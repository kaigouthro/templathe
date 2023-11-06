# MiniMax

[Minimax](https://api.minimax.chat) is a Chinese startup that provides LLM service for companies and individuals.

This example goes over how to use LangChain to interact with MiniMax Inference for Chat.

```python
import os  
  
os.environ["MINIMAX\_GROUP\_ID"] = "MINIMAX\_GROUP\_ID"  
os.environ["MINIMAX\_API\_KEY"] = "MINIMAX\_API\_KEY"  

```

```python
from langchain.chat\_models import MiniMaxChat  
from langchain.schema import HumanMessage  

```

```python
chat = MiniMaxChat()  

```

```python
chat(  
 [  
 HumanMessage(  
 content="Translate this sentence from English to French. I love programming."  
 )  
 ]  
)  

```
