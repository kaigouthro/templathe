# Aleph Alpha

There are two possible ways to use Aleph Alpha's semantic embeddings. If you have texts with a dissimilar structure (e.g. a Document and a Query) you would want to use asymmetric embeddings. Conversely, for texts with comparable structures, symmetric embeddings are the suggested approach.

## Asymmetric[​](#asymmetric "Direct link to Asymmetric")

```python
from langchain.embeddings import AlephAlphaAsymmetricSemanticEmbedding  

```

```python
document = "This is a content of the document"  
query = "What is the content of the document?"  

```

```python
embeddings = AlephAlphaAsymmetricSemanticEmbedding(normalize=True, compress\_to\_size=128)  

```

```python
doc\_result = embeddings.embed\_documents([document])  

```

```python
query\_result = embeddings.embed\_query(query)  

```

## Symmetric[​](#symmetric "Direct link to Symmetric")

```python
from langchain.embeddings import AlephAlphaSymmetricSemanticEmbedding  

```

```python
text = "This is a test text"  

```

```python
embeddings = AlephAlphaSymmetricSemanticEmbedding(normalize=True, compress\_to\_size=128)  

```

```python
doc\_result = embeddings.embed\_documents([text])  

```

```python
query\_result = embeddings.embed\_query(text)  

```

- [Asymmetric](#asymmetric)
- [Symmetric](#symmetric)
