# EDEN AI

Eden AI is revolutionizing the AI landscape by uniting the best AI providers, empowering users to unlock limitless possibilities and tap into the true potential of artificial intelligence. With an all-in-one comprehensive and hassle-free platform, it allows users to deploy AI features to production lightning fast, enabling effortless access to the full breadth of AI capabilities via a single API. (website: <https://edenai.co/>)

This example goes over how to use LangChain to interact with Eden AI embedding models

Accessing the EDENAI's API requires an API key,

which you can get by creating an account <https://app.edenai.run/user/register> and heading here <https://app.edenai.run/admin/account/settings>

Once we have a key we'll want to set it as an environment variable by running:

```python
export EDENAI\_API\_KEY="..."  

```

If you'd prefer not to set an environment variable you can pass the key in directly via the edenai_api_key named parameter

when initiating the EdenAI embedding class:

```python
from langchain.embeddings.edenai import EdenAiEmbeddings  

```

```python
embeddings = EdenAiEmbeddings(edenai\_api\_key="...",provider="...")  

```

## Calling a model[​](#calling-a-model "Direct link to Calling a model")

The EdenAI API brings together various providers.

To access a specific model, you can simply use the "provider" when calling.

```python
embeddings = EdenAiEmbeddings(provider="openai")  

```

```python
docs = ["It's raining right now", "cats are cute"]  
document\_result = embeddings.embed\_documents(docs)  

```

```python
query = "my umbrella is broken"  
query\_result = embeddings.embed\_query(query)  

```

```python
import numpy as np  
  
query\_numpy = np.array(query\_result)  
for doc\_res, doc in zip(document\_result, docs):  
 document\_numpy = np.array(doc\_res)  
 similarity = np.dot(query\_numpy, document\_numpy) / (  
 np.linalg.norm(query\_numpy) \* np.linalg.norm(document\_numpy)  
 )  
 print(f'Cosine similarity between "{doc}" and query: {similarity}')  

```

```text
 Cosine similarity between "It's raining right now" and query: 0.849261496107252  
 Cosine similarity between "cats are cute" and query: 0.7525900655705218  

```

- [Calling a model](#calling-a-model)
