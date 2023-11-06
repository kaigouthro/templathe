# DeepInfra

[DeepInfra](https://deepinfra.com/?utm_source=langchain) is a serverless inference as a service that provides access to a [variety of LLMs](https://deepinfra.com/models?utm_source=langchain) and [embeddings models](https://deepinfra.com/models?type=embeddings&utm_source=langchain). This notebook goes over how to use LangChain with DeepInfra for text embeddings.

```python
# sign up for an account: https://deepinfra.com/login?utm\_source=langchain  
  
from getpass import getpass  
  
DEEPINFRA\_API\_TOKEN = getpass()  

```

```text
 ········  

```

```python
import os  
  
os.environ["DEEPINFRA\_API\_TOKEN"] = DEEPINFRA\_API\_TOKEN  

```

```python
from langchain.embeddings import DeepInfraEmbeddings  

```

```python
embeddings = DeepInfraEmbeddings(  
 model\_id="sentence-transformers/clip-ViT-B-32",  
 query\_instruction="",  
 embed\_instruction="",  
)  

```

```python
docs = ["Dog is not a cat", "Beta is the second letter of Greek alphabet"]  
document\_result = embeddings.embed\_documents(docs)  

```

```python
query = "What is the first letter of Greek alphabet"  
query\_result = embeddings.embed\_query(query)  

```

```python
import numpy as np  
  
query\_numpy = np.array(query\_result)  
for doc\_res, doc in zip(document\_result, docs):  
 document\_numpy = np.array(doc\_res)  
 similarity = np.dot(query\_numpy, document\_numpy) / (  
 np.linalg.norm(query\_numpy) \* np.linalg.norm(document\_numpy)  
 )  
 print(f'Cosine similarity between "{doc}" and query: {similarity}')  

```

```text
 Cosine similarity between "Dog is not a cat" and query: 0.7489097144129355  
 Cosine similarity between "Beta is the second letter of Greek alphabet" and query: 0.9519380640702013  

```
