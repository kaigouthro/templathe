# Embaas

[embaas](https://embaas.io) is a fully managed NLP API service that offers features like embedding generation, document text extraction, document to embeddings and more. You can choose a [variety of pre-trained models](https://embaas.io/docs/models/embeddings).

### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Create a free embaas account at <https://embaas.io/register> and generate an [API key](https://embaas.io/dashboard/api-keys)

### Document Text Extraction API[​](#document-text-extraction-api "Direct link to Document Text Extraction API")

The document text extraction API allows you to extract the text from a given document. The API supports a variety of document formats, including PDF, mp3, mp4 and more. For a full list of supported formats, check out the API docs (link below).

```python
# Set API key  
embaas\_api\_key = "YOUR\_API\_KEY"  
# or set environment variable  
os.environ["EMBAAS\_API\_KEY"] = "YOUR\_API\_KEY"  

```

#### Using a blob (bytes)[​](#using-a-blob-bytes "Direct link to Using a blob (bytes)")

```python
from langchain.document\_loaders.embaas import EmbaasBlobLoader  
from langchain.document\_loaders.blob\_loaders import Blob  

```

```python
blob\_loader = EmbaasBlobLoader()  
blob = Blob.from\_path("example.pdf")  
documents = blob\_loader.load(blob)  

```

```python
# You can also directly create embeddings with your preferred embeddings model  
blob\_loader = EmbaasBlobLoader(params={"model": "e5-large-v2", "should\_embed": True})  
blob = Blob.from\_path("example.pdf")  
documents = blob\_loader.load(blob)  
  
print(documents[0]["metadata"]["embedding"])  

```

#### Using a file[​](#using-a-file "Direct link to Using a file")

```python
from langchain.document\_loaders.embaas import EmbaasLoader  

```

```python
file\_loader = EmbaasLoader(file\_path="example.pdf")  
documents = file\_loader.load()  

```

```python
# Disable automatic text splitting  
file\_loader = EmbaasLoader(file\_path="example.mp3", params={"should\_chunk": False})  
documents = file\_loader.load()  

```

For more detailed information about the embaas document text extraction API, please refer to [the official embaas API documentation](https://embaas.io/api-reference).

- [Prerequisites](#prerequisites)
- [Document Text Extraction API](#document-text-extraction-api)
