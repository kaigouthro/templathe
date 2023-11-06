# LocalAI

Let's load the LocalAI Embedding class. In order to use the LocalAI Embedding class, you need to have the LocalAI service hosted somewhere and configure the embedding models. See the documentation at <https://localai.io/basics/getting_started/index.html> and <https://localai.io/features/embeddings/index.html>.

```python
from langchain.embeddings import LocalAIEmbeddings  

```

```python
embeddings = LocalAIEmbeddings(openai\_api\_base="http://localhost:8080", model="embedding-model-name")  

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

Let's load the LocalAI Embedding class with first generation models (e.g. text-search-ada-doc-001/text-search-ada-query-001). Note: These are not recommended models - see [here](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings)

```python
from langchain.embeddings import LocalAIEmbeddings  

```

```python
embeddings = LocalAIEmbeddings(openai\_api\_base="http://localhost:8080", model="embedding-model-name")  

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

```python
# if you are behind an explicit proxy, you can use the OPENAI\_PROXY environment variable to pass through  
os.environ["OPENAI\_PROXY"] = "http://proxy.yourcompany.com:8080"  

```
