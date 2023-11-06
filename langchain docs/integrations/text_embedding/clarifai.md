# Clarifai

[Clarifai](https://www.clarifai.com/) is an AI Platform that provides the full AI lifecycle ranging from data exploration, data labeling, model training, evaluation, and inference.

This example goes over how to use LangChain to interact with `Clarifai` [models](https://clarifai.com/explore/models). Text embedding models in particular can be found [here](https://clarifai.com/explore/models?page=1&perPage=24&filterData=%5B%7B%22field%22%3A%22model_type_id%22%2C%22value%22%3A%5B%22text-embedder%22%5D%7D%5D).

To use Clarifai, you must have an account and a Personal Access Token (PAT) key.
[Check here](https://clarifai.com/settings/security) to get or create a PAT.

# Dependencies

```bash
# Install required dependencies  
pip install clarifai  

```

# Imports

Here we will be setting the personal access token. You can find your PAT under [settings/security](https://clarifai.com/settings/security) in your Clarifai account.

```python
# Please login and get your API key from https://clarifai.com/settings/security  
from getpass import getpass  
  
CLARIFAI\_PAT = getpass()  

```

```text
 ········  

```

```python
# Import the required modules  
from langchain.embeddings import ClarifaiEmbeddings  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

# Input

Create a prompt template to be used with the LLM Chain:

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

# Setup

Set the user id and app id to the application in which the model resides. You can find a list of public models on <https://clarifai.com/explore/models>

You will have to also initialize the model id and if needed, the model version id. Some models have many versions, you can choose the one appropriate for your task.

```python
USER\_ID = "salesforce"  
APP\_ID = "blip"  
MODEL\_ID = "multimodal-embedder-blip-2"  
  
# You can provide a specific model version as the model\_version\_id arg.  
# MODEL\_VERSION\_ID = "MODEL\_VERSION\_ID"  

```

```python
# Initialize a Clarifai embedding model  
embeddings = ClarifaiEmbeddings(  
 pat=CLARIFAI\_PAT, user\_id=USER\_ID, app\_id=APP\_ID, model\_id=MODEL\_ID  
)  

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
