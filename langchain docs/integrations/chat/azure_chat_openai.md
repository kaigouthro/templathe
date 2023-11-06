# Azure

This notebook goes over how to connect to an Azure hosted OpenAI endpoint

```python
from langchain.chat\_models import AzureChatOpenAI  
from langchain.schema import HumanMessage  

```

```python
BASE\_URL = "https://${TODO}.openai.azure.com"  
API\_KEY = "..."  
DEPLOYMENT\_NAME = "chat"  
model = AzureChatOpenAI(  
 openai\_api\_base=BASE\_URL,  
 openai\_api\_version="2023-05-15",  
 deployment\_name=DEPLOYMENT\_NAME,  
 openai\_api\_key=API\_KEY,  
 openai\_api\_type="azure",  
)  

```

```python
model(  
 [  
 HumanMessage(  
 content="Translate this sentence from English to French. I love programming."  
 )  
 ]  
)  

```

```text
 AIMessage(content="\n\nJ'aime programmer.", additional\_kwargs={})  

```

## Model Version[​](#model-version "Direct link to Model Version")

Azure OpenAI responses contain `model` property, which is name of the model used to generate the response. However unlike native OpenAI responses, it does not contain the version of the model, which is set on the deployment in Azure. This makes it tricky to know which version of the model was used to generate the response, which as result can lead to e.g. wrong total cost calculation with `OpenAICallbackHandler`.

To solve this problem, you can pass `model_version` parameter to `AzureChatOpenAI` class, which will be added to the model name in the llm output. This way you can easily distinguish between different versions of the model.

```python
from langchain.callbacks import get\_openai\_callback  

```

```python
BASE\_URL = "https://{endpoint}.openai.azure.com"  
API\_KEY = "..."  
DEPLOYMENT\_NAME = "gpt-35-turbo" # in Azure, this deployment has version 0613 - input and output tokens are counted separately  

```

```python
model = AzureChatOpenAI(  
 openai\_api\_base=BASE\_URL,  
 openai\_api\_version="2023-05-15",  
 deployment\_name=DEPLOYMENT\_NAME,  
 openai\_api\_key=API\_KEY,  
 openai\_api\_type="azure",  
)  
with get\_openai\_callback() as cb:  
 model(  
 [  
 HumanMessage(  
 content="Translate this sentence from English to French. I love programming."  
 )  
 ]  
 )  
 print(f"Total Cost (USD): ${format(cb.total\_cost, '.6f')}") # without specifying the model version, flat-rate 0.002 USD per 1k input and output tokens is used  

```

```text
 Total Cost (USD): $0.000054  

```

We can provide the model version to `AzureChatOpenAI` constructor. It will get appended to the model name returned by Azure OpenAI and cost will be counted correctly.

```python
model0613 = AzureChatOpenAI(  
 openai\_api\_base=BASE\_URL,  
 openai\_api\_version="2023-05-15",  
 deployment\_name=DEPLOYMENT\_NAME,  
 openai\_api\_key=API\_KEY,  
 openai\_api\_type="azure",  
 model\_version="0613"  
)  
with get\_openai\_callback() as cb:  
 model0613(  
 [  
 HumanMessage(  
 content="Translate this sentence from English to French. I love programming."  
 )  
 ]  
 )  
 print(f"Total Cost (USD): ${format(cb.total\_cost, '.6f')}")  

```

```text
 Total Cost (USD): $0.000044  

```

- [Model Version](#model-version)
