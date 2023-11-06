# MosaicML

[MosaicML](https://docs.mosaicml.com/en/latest/inference.html) offers a managed inference service. You can either use a variety of open-source models, or deploy your own.

This example goes over how to use LangChain to interact with `MosaicML` Inference for text embedding.

```python
# sign up for an account: https://forms.mosaicml.com/demo?utm\_source=langchain  
  
from getpass import getpass  
  
MOSAICML\_API\_TOKEN = getpass()  

```

```python
import os  
  
os.environ["MOSAICML\_API\_TOKEN"] = MOSAICML\_API\_TOKEN  

```

```python
from langchain.embeddings import MosaicMLInstructorEmbeddings  

```

```python
embeddings = MosaicMLInstructorEmbeddings(  
 query\_instruction="Represent the query for retrieval: "  
)  

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
