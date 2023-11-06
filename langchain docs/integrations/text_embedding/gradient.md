# Gradient

`Gradient` allows to create `Embeddings` as well fine tune and get completions on LLMs with a simple web API.

This notebook goes over how to use Langchain with Embeddings of [Gradient](https://gradient.ai/).

## Imports[​](#imports "Direct link to Imports")

```python
from langchain.embeddings import GradientEmbeddings  

```

## Set the Environment API Key[​](#set-the-environment-api-key "Direct link to Set the Environment API Key")

Make sure to get your API key from Gradient AI. You are given $10 in free credits to test and fine-tune different models.

```python
from getpass import getpass  
import os  
  
if not os.environ.get("GRADIENT\_ACCESS\_TOKEN",None):  
 # Access token under https://auth.gradient.ai/select-workspace  
 os.environ["GRADIENT\_ACCESS\_TOKEN"] = getpass("gradient.ai access token:")  
if not os.environ.get("GRADIENT\_WORKSPACE\_ID",None):  
 # `ID` listed in `$ gradient workspace list`  
 # also displayed after login at at https://auth.gradient.ai/select-workspace  
 os.environ["GRADIENT\_WORKSPACE\_ID"] = getpass("gradient.ai workspace id:")  

```

Optional: Validate your environment variables `GRADIENT_ACCESS_TOKEN` and `GRADIENT_WORKSPACE_ID` to get currently deployed models. Using the `gradientai` Python package.

```bash
pip install gradientai  

```

## Create the Gradient instance[​](#create-the-gradient-instance "Direct link to Create the Gradient instance")

```python
documents = ["Pizza is a dish.","Paris is the capital of France", "numpy is a lib for linear algebra"]  
query = "Where is Paris?"  

```

```python
embeddings = GradientEmbeddings(  
 model="bge-large"  
)  
  
documents\_embedded = embeddings.embed\_documents(documents)  
query\_result = embeddings.embed\_query(query)  

```

```python
# (demo) compute similarity  
import numpy as np  
  
scores = np.array(documents\_embedded) @ np.array(query\_result).T  
dict(zip(documents, scores))  

```

- [Imports](#imports)
- [Set the Environment API Key](#set-the-environment-api-key)
- [Create the Gradient instance](#create-the-gradient-instance)
