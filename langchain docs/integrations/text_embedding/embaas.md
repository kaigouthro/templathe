# Embaas

[embaas](https://embaas.io) is a fully managed NLP API service that offers features like embedding generation, document text extraction, document to embeddings and more. You can choose a [variety of pre-trained models](https://embaas.io/docs/models/embeddings).

In this tutorial, we will show you how to use the embaas Embeddings API to generate embeddings for a given text.

### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Create your free embaas account at <https://embaas.io/register> and generate an [API key](https://embaas.io/dashboard/api-keys).

```python
# Set API key  
embaas\_api\_key = "YOUR\_API\_KEY"  
# or set environment variable  
os.environ["EMBAAS\_API\_KEY"] = "YOUR\_API\_KEY"  

```

```python
from langchain.embeddings import EmbaasEmbeddings  

```

```python
embeddings = EmbaasEmbeddings()  

```

```python
# Create embeddings for a single document  
doc\_text = "This is a test document."  
doc\_text\_embedding = embeddings.embed\_query(doc\_text)  

```

```python
# Print created embedding  
print(doc\_text\_embedding)  

```

```python
# Create embeddings for multiple documents  
doc\_texts = ["This is a test document.", "This is another test document."]  
doc\_texts\_embeddings = embeddings.embed\_documents(doc\_texts)  

```

```python
# Print created embeddings  
for i, doc\_text\_embedding in enumerate(doc\_texts\_embeddings):  
 print(f"Embedding for document {i + 1}: {doc\_text\_embedding}")  

```

```python
# Using a different model and/or custom instruction  
embeddings = EmbaasEmbeddings(  
 model="instructor-large",  
 instruction="Represent the Wikipedia document for retrieval",  
)  

```

For more detailed information about the embaas Embeddings API, please refer to [the official embaas API documentation](https://embaas.io/api-reference).

- [Prerequisites](#prerequisites)
