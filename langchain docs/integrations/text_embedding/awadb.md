# AwaDB

[AwaDB](https://github.com/awa-ai/awadb) is an AI Native database for the search and storage of embedding vectors used by LLM Applications.

This notebook explains how to use `AwaEmbeddings` in LangChain.

```python
# pip install awadb  

```

## import the library[​](#import-the-library "Direct link to import the library")

```python
from langchain.embeddings import AwaEmbeddings  

```

```python
Embedding = AwaEmbeddings()  

```

# Set embedding model

Users can use `Embedding.set_model()` to specify the embedding model. \
The input of this function is a string which represents the model's name. \
The list of currently supported models can be obtained [here](https://github.com/awa-ai/awadb) \\ \\

The **default model** is `all-mpnet-base-v2`, it can be used without setting.

```python
text = "our embedding test"  
  
Embedding.set\_model("all-mpnet-base-v2")  

```

```python
res\_query = Embedding.embed\_query("The test information")  
res\_document = Embedding.embed\_documents(["test1", "another test"])  

```

- [import the library](#import-the-library)
