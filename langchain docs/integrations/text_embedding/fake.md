# Fake Embeddings

LangChain also provides a fake embedding class. You can use this to test your pipelines.

```python
from langchain.embeddings import FakeEmbeddings  

```

```python
embeddings = FakeEmbeddings(size=1352)  

```

```python
query\_result = embeddings.embed\_query("foo")  

```

```python
doc\_results = embeddings.embed\_documents(["foo"])  

```
