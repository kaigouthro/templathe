# DashScope

Let's load the DashScope Embedding class.

```python
from langchain.embeddings import DashScopeEmbeddings  

```

```python
embeddings = DashScopeEmbeddings(  
 model="text-embedding-v1", dashscope\_api\_key="your-dashscope-api-key"  
)  

```

```python
text = "This is a test document."  

```

```python
query\_result = embeddings.embed\_query(text)  
print(query\_result)  

```

```python
doc\_results = embeddings.embed\_documents(["foo"])  
print(doc\_results)  

```
