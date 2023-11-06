# Azure ML

[Azure ML](https://azure.microsoft.com/en-us/products/machine-learning/) is a platform used to build, train, and deploy machine learning models. Users can explore the types of models to deploy in the Model Catalog, which provides Azure Foundation Models and OpenAI Models. Azure Foundation Models include various open-source models and popular Hugging Face models. Users can also import models of their liking into AzureML.

This notebook goes over how to use an LLM hosted on an `AzureML online endpoint`

```python
from langchain.llms.azureml\_endpoint import AzureMLOnlineEndpoint  

```

## Set up[​](#set-up "Direct link to Set up")

To use the wrapper, you must [deploy a model on AzureML](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-foundation-models?view=azureml-api-2#deploying-foundation-models-to-endpoints-for-inferencing) and obtain the following parameters:

- `endpoint_api_key`: Required - The API key provided by the endpoint
- `endpoint_url`: Required - The REST endpoint url provided by the endpoint
- `deployment_name`: Not required - The deployment name of the model using the endpoint

## Content Formatter[​](#content-formatter "Direct link to Content Formatter")

The `content_formatter` parameter is a handler class for transforming the request and response of an AzureML endpoint to match with required schema. Since there are a wide range of models in the model catalog, each of which may process data differently from one another, a `ContentFormatterBase` class is provided to allow users to transform data to their liking. The following content formatters are provided:

- `GPT2ContentFormatter`: Formats request and response data for GPT2
- `DollyContentFormatter`: Formats request and response data for the Dolly-v2
- `HFContentFormatter`: Formats request and response data for text-generation Hugging Face models
- `LLamaContentFormatter`: Formats request and response data for LLaMa2

*Note: `OSSContentFormatter` is being deprecated and replaced with `GPT2ContentFormatter`. The logic is the same but `GPT2ContentFormatter` is a more suitable name. You can still continue to use `OSSContentFormatter` as the changes are backwards compatible.*

Below is an example using a summarization model from Hugging Face.

### Custom Content Formatter[​](#custom-content-formatter "Direct link to Custom Content Formatter")

```python
from typing import Dict  
  
from langchain.llms.azureml\_endpoint import AzureMLOnlineEndpoint, ContentFormatterBase  
import os  
import json  
  
  
class CustomFormatter(ContentFormatterBase):  
 content\_type = "application/json"  
 accepts = "application/json"  
  
 def format\_request\_payload(self, prompt: str, model\_kwargs: Dict) -> bytes:  
 input\_str = json.dumps(  
 {  
 "inputs": [prompt],  
 "parameters": model\_kwargs,  
 "options": {"use\_cache": False, "wait\_for\_model": True},  
 }  
 )  
 return str.encode(input\_str)  
  
 def format\_response\_payload(self, output: bytes) -> str:  
 response\_json = json.loads(output)  
 return response\_json[0]["summary\_text"]  
  
  
content\_formatter = CustomFormatter()  
  
llm = AzureMLOnlineEndpoint(  
 endpoint\_api\_key=os.getenv("BART\_ENDPOINT\_API\_KEY"),  
 endpoint\_url=os.getenv("BART\_ENDPOINT\_URL"),  
 model\_kwargs={"temperature": 0.8, "max\_new\_tokens": 400},  
 content\_formatter=content\_formatter,  
)  
large\_text = """On January 7, 2020, Blockberry Creative announced that HaSeul would not participate in the promotion for Loona's   
next album because of mental health concerns. She was said to be diagnosed with "intermittent anxiety symptoms" and would be   
taking time to focus on her health.[39] On February 5, 2020, Loona released their second EP titled [#] (read as hash), along   
with the title track "So What".[40] Although HaSeul did not appear in the title track, her vocals are featured on three other   
songs on the album, including "365". Once peaked at number 1 on the daily Gaon Retail Album Chart,[41] the EP then debuted at   
number 2 on the weekly Gaon Album Chart. On March 12, 2020, Loona won their first music show trophy with "So What" on Mnet's   
M Countdown.[42]  
  
On October 19, 2020, Loona released their third EP titled [12:00] (read as midnight),[43] accompanied by its first single   
"Why Not?". HaSeul was again not involved in the album, out of her own decision to focus on the recovery of her health.[44]   
The EP then became their first album to enter the Billboard 200, debuting at number 112.[45] On November 18, Loona released   
the music video for "Star", another song on [12:00].[46] Peaking at number 40, "Star" is Loona's first entry on the Billboard   
Mainstream Top 40, making them the second K-pop girl group to enter the chart.[47]  
  
On June 1, 2021, Loona announced that they would be having a comeback on June 28, with their fourth EP, [&] (read as and).  
[48] The following day, on June 2, a teaser was posted to Loona's official social media accounts showing twelve sets of eyes,   
confirming the return of member HaSeul who had been on hiatus since early 2020.[49] On June 12, group members YeoJin, Kim Lip,   
Choerry, and Go Won released the song "Yum-Yum" as a collaboration with Cocomong.[50] On September 8, they released another   
collaboration song named "Yummy-Yummy".[51] On June 27, 2021, Loona announced at the end of their special clip that they are   
making their Japanese debut on September 15 under Universal Music Japan sublabel EMI Records.[52] On August 27, it was announced   
that Loona will release the double A-side single, "Hula Hoop / Star Seed" on September 15, with a physical CD release on October   
20.[53] In December, Chuu filed an injunction to suspend her exclusive contract with Blockberry Creative.[54][55]  
"""  
summarized\_text = llm(large\_text)  
print(summarized\_text)  

```

```text
 HaSeul won her first music show trophy with "So What" on Mnet's M Countdown. Loona released their second EP titled [#] (read as hash] on February 5, 2020. HaSeul did not take part in the promotion of the album because of mental health issues. On October 19, 2020, they released their third EP called [12:00]. It was their first album to enter the Billboard 200, debuting at number 112. On June 2, 2021, the group released their fourth EP called Yummy-Yummy. On August 27, it was announced that they are making their Japanese debut on September 15 under Universal Music Japan sublabel EMI Records.  

```

### Dolly with LLMChain[​](#dolly-with-llmchain "Direct link to Dolly with LLMChain")

```python
from langchain.prompts import PromptTemplate  
from langchain.llms.azureml\_endpoint import DollyContentFormatter  
from langchain.chains import LLMChain  
  
formatter\_template = "Write a {word\_count} word essay about {topic}."  
  
prompt = PromptTemplate(  
 input\_variables=["word\_count", "topic"], template=formatter\_template  
)  
  
content\_formatter = DollyContentFormatter()  
  
llm = AzureMLOnlineEndpoint(  
 endpoint\_api\_key=os.getenv("DOLLY\_ENDPOINT\_API\_KEY"),  
 endpoint\_url=os.getenv("DOLLY\_ENDPOINT\_URL"),  
 model\_kwargs={"temperature": 0.8, "max\_tokens": 300},  
 content\_formatter=content\_formatter,  
)  
  
chain = LLMChain(llm=llm, prompt=prompt)  
print(chain.run({"word\_count": 100, "topic": "how to make friends"}))  

```

```text
 Many people are willing to talk about themselves; it's others who seem to be stuck up. Try to understand others where they're coming from. Like minded people can build a tribe together.  

```

### Serializing an LLM[​](#serializing-an-llm "Direct link to Serializing an LLM")

You can also save and load LLM configurations

```python
from langchain.llms.loading import load\_llm  
from langchain.llms.azureml\_endpoint import AzureMLEndpointClient  
  
save\_llm = AzureMLOnlineEndpoint(  
 deployment\_name="databricks-dolly-v2-12b-4",  
 model\_kwargs={  
 "temperature": 0.2,  
 "max\_tokens": 150,  
 "top\_p": 0.8,  
 "frequency\_penalty": 0.32,  
 "presence\_penalty": 72e-3,  
 },  
)  
save\_llm.save("azureml.json")  
loaded\_llm = load\_llm("azureml.json")  
  
print(loaded\_llm)  

```

```text
 AzureMLOnlineEndpoint  
 Params: {'deployment\_name': 'databricks-dolly-v2-12b-4', 'model\_kwargs': {'temperature': 0.2, 'max\_tokens': 150, 'top\_p': 0.8, 'frequency\_penalty': 0.32, 'presence\_penalty': 0.072}}  

```

- [Set up](#set-up)

- [Content Formatter](#content-formatter)

  - [Custom Content Formatter](#custom-content-formatter)
  - [Dolly with LLMChain](#dolly-with-llmchain)
  - [Serializing an LLM](#serializing-an-llm)

- [Custom Content Formatter](#custom-content-formatter)

- [Dolly with LLMChain](#dolly-with-llmchain)

- [Serializing an LLM](#serializing-an-llm)
