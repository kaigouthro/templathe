# ModelScope

[ModelScope](https://www.modelscope.cn/home) is big repository of the models and datasets.

Let's load the ModelScope Embedding class.

```python
from langchain.embeddings import ModelScopeEmbeddings  

```

```python
model\_id = "damo/nlp\_corom\_sentence-embedding\_english-base"  

```

```python
embeddings = ModelScopeEmbeddings(model\_id=model\_id)  

```

```python
text = "This is a test document."  

```

```python
query\_result = embeddings.embed\_query(text)  

```

```python
doc\_results = embeddings.embed\_documents(["foo"])  

```
