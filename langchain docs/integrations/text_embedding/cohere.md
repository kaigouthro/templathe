# Cohere

Let's load the Cohere Embedding class.

```python
from langchain.embeddings import CohereEmbeddings  

```

```python
embeddings = CohereEmbeddings(cohere\_api\_key=cohere\_api\_key)  

```

```python
text = "This is a test document."  

```

```python
query\_result = embeddings.embed\_query(text)  

```

```python
doc\_result = embeddings.embed\_documents([text])  

```
