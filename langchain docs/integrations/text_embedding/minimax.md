# MiniMax

[MiniMax](https://api.minimax.chat/document/guides/embeddings?id=6464722084cdc277dfaa966a) offers an embeddings service.

This example goes over how to use LangChain to interact with MiniMax Inference for text embedding.

```python
import os  
  
os.environ["MINIMAX\_GROUP\_ID"] = "MINIMAX\_GROUP\_ID"  
os.environ["MINIMAX\_API\_KEY"] = "MINIMAX\_API\_KEY"  

```

```python
from langchain.embeddings import MiniMaxEmbeddings  

```

```python
embeddings = MiniMaxEmbeddings()  

```

```python
query\_text = "This is a test query."  
query\_result = embeddings.embed\_query(query\_text)  

```

```python
document\_text = "This is a test document."  
document\_result = embeddings.embed\_documents([document\_text])  

```

```python
import numpy as np  
  
query\_numpy = np.array(query\_result)  
document\_numpy = np.array(document\_result[0])  
similarity = np.dot(query\_numpy, document\_numpy) / (  
 np.linalg.norm(query\_numpy) \* np.linalg.norm(document\_numpy)  
)  
print(f"Cosine similarity between document and query: {similarity}")  

```

```text
 Cosine similarity between document and query: 0.1573236279277012  

```
