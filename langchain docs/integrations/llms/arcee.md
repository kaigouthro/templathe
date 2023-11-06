# Arcee

This notebook demonstrates how to use the `Arcee` class for generating text using Arcee's Domain Adapted Language Models (DALMs).

### Setup[​](#setup "Direct link to Setup")

Before using Arcee, make sure the Arcee API key is set as `ARCEE_API_KEY` environment variable. You can also pass the api key as a named parameter.

```python
from langchain.llms import Arcee  
  
# Create an instance of the Arcee class  
arcee = Arcee(  
 model="DALM-PubMed",  
 # arcee\_api\_key="ARCEE-API-KEY" # if not already set in the environment  
)  

```

### Additional Configuration[​](#additional-configuration "Direct link to Additional Configuration")

You can also configure Arcee's parameters such as `arcee_api_url`, `arcee_app_url`, and `model_kwargs` as needed.
Setting the `model_kwargs` at the object initialization uses the parameters as default for all the subsequent calls to the generate response.

```python
arcee = Arcee(  
 model="DALM-Patent",  
 # arcee\_api\_key="ARCEE-API-KEY", # if not already set in the environment  
 arcee\_api\_url="https://custom-api.arcee.ai", # default is https://api.arcee.ai  
 arcee\_app\_url="https://custom-app.arcee.ai", # default is https://app.arcee.ai  
 model\_kwargs={  
 "size": 5,  
 "filters": [  
 {  
 "field\_name": "document",  
 "filter\_type": "fuzzy\_search",  
 "value": "Einstein"  
 }  
 ]  
 }  
)  

```

### Generating Text[​](#generating-text "Direct link to Generating Text")

You can generate text from Arcee by providing a prompt. Here's an example:

```python
# Generate text  
prompt = "Can AI-driven music therapy contribute to the rehabilitation of patients with disorders of consciousness?"  
response = arcee(prompt)  

```

### Additional parameters[​](#additional-parameters "Direct link to Additional parameters")

Arcee allows you to apply `filters` and set the `size` (in terms of count) of retrieved document(s) to aid text generation. Filters help narrow down the results. Here's how to use these parameters:

```python
# Define filters  
filters = [  
 {  
 "field\_name": "document",  
 "filter\_type": "fuzzy\_search",  
 "value": "Einstein"  
 },  
 {  
 "field\_name": "year",  
 "filter\_type": "strict\_search",  
 "value": "1905"  
 }  
]  
  
# Generate text with filters and size params  
response = arcee(prompt, size=5, filters=filters)  

```

- [Setup](#setup)
- [Additional Configuration](#additional-configuration)
- [Generating Text](#generating-text)
- [Additional parameters](#additional-parameters)
