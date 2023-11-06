# AzureOpenAI

Let's load the OpenAI Embedding class with environment variables set to indicate to use Azure endpoints.

```python
# set the environment variables needed for openai package to know to reach out to azure  
import os  
  
os.environ["OPENAI\_API\_TYPE"] = "azure"  
os.environ["OPENAI\_API\_BASE"] = "https://<your-endpoint.openai.azure.com/"  
os.environ["OPENAI\_API\_KEY"] = "your AzureOpenAI key"  
os.environ["OPENAI\_API\_VERSION"] = "2023-05-15"  

```

```python
from langchain.embeddings import OpenAIEmbeddings  
  
embeddings = OpenAIEmbeddings(deployment="your-embeddings-deployment-name")  

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
