# Hugging Face

Let's load the Hugging Face Embedding class.

```bash
pip install langchain sentence\_transformers  

```

```python
from langchain.embeddings import HuggingFaceEmbeddings  

```

```python
embeddings = HuggingFaceEmbeddings()  

```

```python
text = "This is a test document."  

```

```python
query\_result = embeddings.embed\_query(text)  

```

```python
query\_result[:3]  

```

```text
 [-0.04895168915390968, -0.03986193612217903, -0.021562768146395683]  

```

```python
doc\_result = embeddings.embed\_documents([text])  

```

## Hugging Face Inference API[​](#hugging-face-inference-api "Direct link to Hugging Face Inference API")

We can also access embedding models via the Hugging Face Inference API, which does not require us to install `sentence_transformers` and download models locally.

```python
import getpass  
  
inference\_api\_key = getpass.getpass("Enter your HF Inference API Key:\n\n")  

```

```text
 Enter your HF Inference API Key:  
   
 ········  

```

```python
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings  
  
embeddings = HuggingFaceInferenceAPIEmbeddings(  
 api\_key=inference\_api\_key,  
 model\_name="sentence-transformers/all-MiniLM-l6-v2"  
)  
  
query\_result = embeddings.embed\_query(text)  
query\_result[:3]  

```

```text
 [-0.038338541984558105, 0.1234646737575531, -0.028642963618040085]  

```

- [Hugging Face Inference API](#hugging-face-inference-api)
