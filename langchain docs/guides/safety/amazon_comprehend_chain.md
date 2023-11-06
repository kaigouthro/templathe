# Amazon Comprehend Moderation Chain

This notebook shows how to use [Amazon Comprehend](https://aws.amazon.com/comprehend/) to detect and handle `Personally Identifiable Information` (`PII`) and toxicity.

## Setting up[​](#setting-up "Direct link to Setting up")

```python
%pip install boto3 nltk  

```

```python
import boto3  
  
comprehend\_client = boto3.client('comprehend', region\_name='us-east-1')  

```

```python
from langchain\_experimental.comprehend\_moderation import AmazonComprehendModerationChain  
  
comprehend\_moderation = AmazonComprehendModerationChain(  
 client=comprehend\_client, #optional  
 verbose=True  
)  

```

## Using AmazonComprehendModerationChain with LLM chain[​](#using-amazoncomprehendmoderationchain-with-llm-chain "Direct link to Using AmazonComprehendModerationChain with LLM chain")

**Note**: The example below uses the *Fake LLM* from LangChain, but the same concept could be applied to other LLMs.

```python
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
from langchain.llms.fake import FakeListLLM  
from langchain\_experimental.comprehend\_moderation.base\_moderation\_exceptions import ModerationPiiError  
  
template = """Question: {question}  
  
Answer:"""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  
  
responses = [  
 "Final Answer: A credit card number looks like 1289-2321-1123-2387. A fake SSN number looks like 323-22-9980. John Doe's phone number is (999)253-9876.",   
 "Final Answer: This is a really shitty way of constructing a birdhouse. This is fucking insane to think that any birds would actually create their motherfucking nests here."  
]  
llm = FakeListLLM(responses=responses)  
  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
  
chain = (  
 prompt   
 | comprehend\_moderation   
 | {llm\_chain.input\_keys[0]: lambda x: x['output'] }   
 | llm\_chain   
 | { "input": lambda x: x['text'] }   
 | comprehend\_moderation   
)  
  
try:  
 response = chain.invoke({"question": "A sample SSN number looks like this 123-456-7890. Can you give me some more samples?"})  
except ModerationPiiError as e:  
 print(e.message)  
else:  
 print(response['output'])  

```

## Using `moderation_config` to customize your moderation[​](#using-moderation_config-to-customize-your-moderation "Direct link to using-moderation_config-to-customize-your-moderation")

Use Amazon Comprehend Moderation with a configuration to control what moderations you wish to perform and what actions should be taken for each of them. There are three different moderations that happen when no configuration is passed as demonstrated above. These moderations are:

- PII (Personally Identifiable Information) checks
- Toxicity content detection
- Intention detection

Here is an example of a moderation config.

```python
from langchain\_experimental.comprehend\_moderation import BaseModerationActions, BaseModerationFilters  
  
moderation\_config = {   
 "filters":[   
 BaseModerationFilters.PII,   
 BaseModerationFilters.TOXICITY,  
 BaseModerationFilters.INTENT  
 ],  
 "pii":{   
 "action": BaseModerationActions.ALLOW,   
 "threshold":0.5,   
 "labels":["SSN"],  
 "mask\_character": "X"  
 },  
 "toxicity":{   
 "action": BaseModerationActions.STOP,   
 "threshold":0.5  
 },  
 "intent":{   
 "action": BaseModerationActions.STOP,   
 "threshold":0.5  
 }  
}  

```

At the core of the configuration you have three filters specified in the `filters` key:

1. `BaseModerationFilters.PII`
1. `BaseModerationFilters.TOXICITY`
1. `BaseModerationFilters.INTENT`

And an `action` key that defines two possible actions for each moderation function:

1. `BaseModerationActions.ALLOW` - `allows` the prompt to pass through but masks detected PII in case of PII check. The default behavior is to run and redact all PII entities. If there is an entity specified in the `labels` field, then only those entities will go through the PII check and masked.
1. `BaseModerationActions.STOP` - `stops` the prompt from passing through to the next step in case any PII, Toxicity, or incorrect Intent is detected. The action of `BaseModerationActions.STOP` will raise a Python `Exception` essentially stopping the chain in progress.

Using the configuration in the previous cell will perform PII checks and will allow the prompt to pass through however it will mask any SSN numbers present in either the prompt or the LLM output.

```python
comp\_moderation\_with\_config = AmazonComprehendModerationChain(  
 moderation\_config=moderation\_config, #specify the configuration  
 client=comprehend\_client, #optionally pass the Boto3 Client  
 verbose=True  
)  
  
template = """Question: {question}  
  
Answer:"""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  
  
responses = [  
 "Final Answer: A credit card number looks like 1289-2321-1123-2387. A fake SSN number looks like 323-22-9980. John Doe's phone number is (999)253-9876.",   
 "Final Answer: This is a really shitty way of constructing a birdhouse. This is fucking insane to think that any birds would actually create their motherfucking nests here."  
]  
llm = FakeListLLM(responses=responses)  
  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
  
chain = (   
 prompt   
 | comp\_moderation\_with\_config   
 | {llm\_chain.input\_keys[0]: lambda x: x['output'] }   
 | llm\_chain   
 | { "input": lambda x: x['text'] }   
 | comp\_moderation\_with\_config   
)  
  
try:  
 response = chain.invoke({"question": "A sample SSN number looks like this 123-456-7890. Can you give me some more samples?"})  
except Exception as e:  
 print(str(e))  
else:  
 print(response['output'])  

```

## Unique ID, and Moderation Callbacks[​](#unique-id-and-moderation-callbacks "Direct link to Unique ID, and Moderation Callbacks")

When Amazon Comprehend moderation action is specified as `STOP`, the chain will raise one of the following exceptions-

```text
- `ModerationPiiError`, for PII checks  
- `ModerationToxicityError`, for Toxicity checks   
- `ModerationIntentionError` for Intent checks  

```

In addition to the moderation configuration, the `AmazonComprehendModerationChain` can also be initialized with the following parameters

- `unique_id` \[Optional\] a string parameter. This parameter can be used to pass any string value or ID. For example, in a chat application, you may want to keep track of abusive users, in this case, you can pass the user's username/email ID etc. This defaults to `None`.

- `moderation_callback` \[Optional\] the `BaseModerationCallbackHandler` will be called asynchronously (non-blocking to the chain). Callback functions are useful when you want to perform additional actions when the moderation functions are executed, for example logging into a database, or writing a log file. You can override three functions by subclassing `BaseModerationCallbackHandler` - `on_after_pii()`, `on_after_toxicity()`, and `on_after_intent()`. Note that all three functions must be `async` functions. These callback functions receive two arguments:

  - `moderation_beacon` is a dictionary that will contain information about the moderation function, the full response from the Amazon Comprehend model, a unique chain id, the moderation status, and the input string which was validated. The dictionary is of the following schema-

  ```text
  {   
   'moderation\_chain\_id': 'xxx-xxx-xxx', # Unique chain ID  
   'moderation\_type': 'Toxicity' | 'PII' | 'Intent',   
   'moderation\_status': 'LABELS\_FOUND' | 'LABELS\_NOT\_FOUND',  
   'moderation\_input': 'A sample SSN number looks like this 123-456-7890. Can you give me some more samples?',  
   'moderation\_output': {...} #Full Amazon Comprehend PII, Toxicity, or Intent Model Output  
  }  

  ```

  - `unique_id` if passed to the `AmazonComprehendModerationChain`

`unique_id` \[Optional\] a string parameter. This parameter can be used to pass any string value or ID. For example, in a chat application, you may want to keep track of abusive users, in this case, you can pass the user's username/email ID etc. This defaults to `None`.

`moderation_callback` \[Optional\] the `BaseModerationCallbackHandler` will be called asynchronously (non-blocking to the chain). Callback functions are useful when you want to perform additional actions when the moderation functions are executed, for example logging into a database, or writing a log file. You can override three functions by subclassing `BaseModerationCallbackHandler` - `on_after_pii()`, `on_after_toxicity()`, and `on_after_intent()`. Note that all three functions must be `async` functions. These callback functions receive two arguments:

- `moderation_beacon` is a dictionary that will contain information about the moderation function, the full response from the Amazon Comprehend model, a unique chain id, the moderation status, and the input string which was validated. The dictionary is of the following schema-

```text
{   
 'moderation\_chain\_id': 'xxx-xxx-xxx', # Unique chain ID  
 'moderation\_type': 'Toxicity' | 'PII' | 'Intent',   
 'moderation\_status': 'LABELS\_FOUND' | 'LABELS\_NOT\_FOUND',  
 'moderation\_input': 'A sample SSN number looks like this 123-456-7890. Can you give me some more samples?',  
 'moderation\_output': {...} #Full Amazon Comprehend PII, Toxicity, or Intent Model Output  
}  

```

- `unique_id` if passed to the `AmazonComprehendModerationChain`

`moderation_beacon` is a dictionary that will contain information about the moderation function, the full response from the Amazon Comprehend model, a unique chain id, the moderation status, and the input string which was validated. The dictionary is of the following schema-

```text
{   
 'moderation\_chain\_id': 'xxx-xxx-xxx', # Unique chain ID  
 'moderation\_type': 'Toxicity' | 'PII' | 'Intent',   
 'moderation\_status': 'LABELS\_FOUND' | 'LABELS\_NOT\_FOUND',  
 'moderation\_input': 'A sample SSN number looks like this 123-456-7890. Can you give me some more samples?',  
 'moderation\_output': {...} #Full Amazon Comprehend PII, Toxicity, or Intent Model Output  
}  

```

`unique_id` if passed to the `AmazonComprehendModerationChain`

```text
from langchain.callbacks.stdout import StdOutCallbackHandler comp\_moderation\_with\_config = AmazonComprehendModerationChain(verbose=True, callbacks=[StdOutCallbackHandler()])  

```

```python
from langchain\_experimental.comprehend\_moderation import BaseModerationCallbackHandler  

```

```python
# Define callback handlers by subclassing BaseModerationCallbackHandler  
  
class MyModCallback(BaseModerationCallbackHandler):  
   
 async def on\_after\_pii(self, output\_beacon, unique\_id):  
 import json  
 moderation\_type = output\_beacon['moderation\_type']  
 chain\_id = output\_beacon['moderation\_chain\_id']  
 with open(f'output-{moderation\_type}-{chain\_id}.json', 'w') as file:  
 data = { 'beacon\_data': output\_beacon, 'unique\_id': unique\_id }  
 json.dump(data, file)  
   
 '''  
 async def on\_after\_toxicity(self, output\_beacon, unique\_id):  
 pass  
   
 async def on\_after\_intent(self, output\_beacon, unique\_id):  
 pass  
 '''  
   
  
my\_callback = MyModCallback()  

```

```python
moderation\_config = {   
 "filters": [   
 BaseModerationFilters.PII,   
 BaseModerationFilters.TOXICITY  
 ],  
 "pii":{   
 "action": BaseModerationActions.STOP,   
 "threshold":0.5,   
 "labels":["SSN"],   
 "mask\_character": "X"   
 },  
 "toxicity":{   
 "action": BaseModerationActions.STOP,   
 "threshold":0.5   
 }  
}  
  
comp\_moderation\_with\_config = AmazonComprehendModerationChain(  
 moderation\_config=moderation\_config, # specify the configuration  
 client=comprehend\_client, # optionally pass the Boto3 Client  
 unique\_id='john.doe@email.com', # A unique ID  
 moderation\_callback=my\_callback, # BaseModerationCallbackHandler  
 verbose=True  
)  

```

```python
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
from langchain.llms.fake import FakeListLLM  
  
template = """Question: {question}  
  
Answer:"""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  
  
responses = [  
 "Final Answer: A credit card number looks like 1289-2321-1123-2387. A fake SSN number looks like 323-22-9980. John Doe's phone number is (999)253-9876.",   
 "Final Answer: This is a really shitty way of constructing a birdhouse. This is fucking insane to think that any birds would actually create their motherfucking nests here."  
]  
  
llm = FakeListLLM(responses=responses)  
  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
  
chain = (  
 prompt   
 | comp\_moderation\_with\_config   
 | {llm\_chain.input\_keys[0]: lambda x: x['output'] }   
 | llm\_chain   
 | { "input": lambda x: x['text'] }   
 | comp\_moderation\_with\_config   
)   
  
try:  
 response = chain.invoke({"question": "A sample SSN number looks like this 123-456-7890. Can you give me some more samples?"})  
except Exception as e:  
 print(str(e))  
else:  
 print(response['output'])  

```

## `moderation_config` and moderation execution order[​](#moderation_config-and-moderation-execution-order "Direct link to moderation_config-and-moderation-execution-order")

If `AmazonComprehendModerationChain` is not initialized with any `moderation_config` then the default action is `STOP` and the default order of moderation check is as follows.

```text
AmazonComprehendModerationChain  
│  
└──Check PII with Stop Action  
 ├── Callback (if available)  
 ├── Label Found ⟶ [Error Stop]  
 └── No Label Found   
 └──Check Toxicity with Stop Action  
 ├── Callback (if available)  
 ├── Label Found ⟶ [Error Stop]  
 └── No Label Found  
 └──Check Intent with Stop Action  
 ├── Callback (if available)  
 ├── Label Found ⟶ [Error Stop]  
 └── No Label Found  
 └── Return Prompt  

```

If any of the checks raises an exception then the subsequent checks will not be performed. If a `callback` is provided in this case, then it will be called for each of the checks that have been performed. For example, in the case above, if the Chain fails due to the presence of PII then the Toxicity and Intent checks will not be performed.

You can override the execution order by passing `moderation_config` and simply specifying the desired order in the `filters` key of the configuration. In case you use `moderation_config` then the order of the checks as specified in the `filters` key will be maintained. For example, in the configuration below, first Toxicity check will be performed, then PII, and finally Intent validation will be performed. In this case, `AmazonComprehendModerationChain` will perform the desired checks in the specified order with default values of each model `kwargs`.

```python
moderation\_config = {   
 "filters":[ BaseModerationFilters.TOXICITY,   
 BaseModerationFilters.PII,   
 BaseModerationFilters.INTENT]  
 }  

```

Model `kwargs` are specified by the `pii`, `toxicity`, and `intent` keys within the `moderation_config` dictionary. For example, in the `moderation_config` below, the default order of moderation is overriden and the `pii` & `toxicity` model `kwargs` have been overriden. For `intent` the chain's default `kwargs` will be used.

```python
 moderation\_config = {   
 "filters":[ BaseModerationFilters.TOXICITY,   
 BaseModerationFilters.PII,   
 BaseModerationFilters.INTENT],  
 "pii":{ "action": BaseModerationActions.ALLOW,   
 "threshold":0.5,   
 "labels":["SSN"],   
 "mask\_character": "X" },  
 "toxicity":{ "action": BaseModerationActions.STOP,   
 "threshold":0.5 }  
 }  

```

1. For a list of PII labels see Amazon Comprehend Universal PII entity types - <https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html#how-pii-types>
1. Following are the list of available Toxicity labels-
   - `HATE_SPEECH`: Speech that criticizes, insults, denounces or dehumanizes a person or a group on the basis of an identity, be it race, ethnicity, gender identity, religion, sexual orientation, ability, national origin, or another identity-group.
   - `GRAPHIC`: Speech that uses visually descriptive, detailed and unpleasantly vivid imagery is considered as graphic. Such language is often made verbose so as to amplify an insult, discomfort or harm to the recipient.
   - `HARASSMENT_OR_ABUSE`: Speech that imposes disruptive power dynamics between the speaker and hearer, regardless of intent, seeks to affect the psychological well-being of the recipient, or objectifies a person should be classified as Harassment.
   - `SEXUAL`: Speech that indicates sexual interest, activity or arousal by using direct or indirect references to body parts or physical traits or sex is considered as toxic with toxicityType "sexual".
   - `VIOLENCE_OR_THREAT`: Speech that includes threats which seek to inflict pain, injury or hostility towards a person or group.
   - `INSULT`: Speech that includes demeaning, humiliating, mocking, insulting, or belittling language.
   - `PROFANITY`: Speech that contains words, phrases or acronyms that are impolite, vulgar, or offensive is considered as profane.
1. For a list of Intent labels refer to documentation \[link here\]

- `HATE_SPEECH`: Speech that criticizes, insults, denounces or dehumanizes a person or a group on the basis of an identity, be it race, ethnicity, gender identity, religion, sexual orientation, ability, national origin, or another identity-group.
- `GRAPHIC`: Speech that uses visually descriptive, detailed and unpleasantly vivid imagery is considered as graphic. Such language is often made verbose so as to amplify an insult, discomfort or harm to the recipient.
- `HARASSMENT_OR_ABUSE`: Speech that imposes disruptive power dynamics between the speaker and hearer, regardless of intent, seeks to affect the psychological well-being of the recipient, or objectifies a person should be classified as Harassment.
- `SEXUAL`: Speech that indicates sexual interest, activity or arousal by using direct or indirect references to body parts or physical traits or sex is considered as toxic with toxicityType "sexual".
- `VIOLENCE_OR_THREAT`: Speech that includes threats which seek to inflict pain, injury or hostility towards a person or group.
- `INSULT`: Speech that includes demeaning, humiliating, mocking, insulting, or belittling language.
- `PROFANITY`: Speech that contains words, phrases or acronyms that are impolite, vulgar, or offensive is considered as profane.

## Examples[​](#examples "Direct link to Examples")

### With Hugging Face Hub Models[​](#with-hugging-face-hub-models "Direct link to With Hugging Face Hub Models")

Get your [API Key from Hugging Face hub](https://huggingface.co/docs/api-inference/quicktour#get-your-api-token)

```python
%pip install huggingface\_hub  

```

```python
%env HUGGINGFACEHUB\_API\_TOKEN="<HUGGINGFACEHUB\_API\_TOKEN>"  

```

```python
# See https://huggingface.co/models?pipeline\_tag=text-generation&sort=downloads for some other options  
repo\_id = "google/flan-t5-xxl"  

```

```python
from langchain.llms import HuggingFaceHub  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
  
template = """Question: {question}  
  
Answer:"""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  
  
llm = HuggingFaceHub(  
 repo\_id=repo\_id, model\_kwargs={"temperature": 0.5, "max\_length": 256}  
)  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

Create a configuration and initialize an Amazon Comprehend Moderation chain

```python
moderation\_config = {   
 "filters":[ BaseModerationFilters.PII, BaseModerationFilters.TOXICITY, BaseModerationFilters.INTENT ],  
 "pii":{"action": BaseModerationActions.ALLOW, "threshold":0.5, "labels":["SSN","CREDIT\_DEBIT\_NUMBER"], "mask\_character": "X"},  
 "toxicity":{"action": BaseModerationActions.STOP, "threshold":0.5},  
 "intent":{"action": BaseModerationActions.ALLOW, "threshold":0.5,},  
 }  
  
# without any callback  
amazon\_comp\_moderation = AmazonComprehendModerationChain(moderation\_config=moderation\_config,   
 client=comprehend\_client,  
 verbose=True)  
  
# with callback  
amazon\_comp\_moderation\_out = AmazonComprehendModerationChain(moderation\_config=moderation\_config,   
 client=comprehend\_client,  
 moderation\_callback=my\_callback,  
 verbose=True)  

```

The `moderation_config` will now prevent any inputs and model outputs containing obscene words or sentences, bad intent, or PII with entities other than SSN with score above threshold or 0.5 or 50%. If it finds Pii entities - SSN - it will redact them before allowing the call to proceed.

```python
chain = (  
 prompt   
 | amazon\_comp\_moderation   
 | {llm\_chain.input\_keys[0]: lambda x: x['output'] }   
 | llm\_chain   
 | { "input": lambda x: x['text'] }   
 | amazon\_comp\_moderation\_out  
)  
  
try:  
 response = chain.invoke({"question": "My AnyCompany Financial Services, LLC credit card account 1111-0000-1111-0008 has 24$ due by July 31st. Can you give me some more credit car number samples?"})  
except Exception as e:  
 print(str(e))  
else:  
 print(response['output'])  

```

### With Amazon SageMaker Jumpstart[​](#with-amazon-sagemaker-jumpstart "Direct link to With Amazon SageMaker Jumpstart")

The example below shows how to use the `Amazon Comprehend Moderation chain` with an Amazon SageMaker Jumpstart hosted LLM. You should have an `Amazon SageMaker Jumpstart` hosted LLM endpoint within your AWS Account.

```python
endpoint\_name = "<SAGEMAKER\_ENDPOINT\_NAME>" # replace with your SageMaker Endpoint name  

```

```python
from langchain.llms import SagemakerEndpoint  
from langchain.llms.sagemaker\_endpoint import LLMContentHandler  
from langchain.chains import LLMChain  
from langchain.prompts import load\_prompt, PromptTemplate  
import json  
  
class ContentHandler(LLMContentHandler):  
 content\_type = "application/json"  
 accepts = "application/json"  
  
 def transform\_input(self, prompt: str, model\_kwargs: dict) -> bytes:  
 input\_str = json.dumps({"text\_inputs": prompt, \*\*model\_kwargs})  
 return input\_str.encode('utf-8')  
   
 def transform\_output(self, output: bytes) -> str:  
 response\_json = json.loads(output.read().decode("utf-8"))  
 return response\_json['generated\_texts'][0]  
  
content\_handler = ContentHandler()  
  
#prompt template for input text  
llm\_prompt = PromptTemplate(input\_variables=["input\_text"], template="{input\_text}")  
  
llm\_chain = LLMChain(  
 llm=SagemakerEndpoint(  
 endpoint\_name=endpoint\_name,   
 region\_name='us-east-1',  
 model\_kwargs={"temperature":0.97,  
 "max\_length": 200,  
 "num\_return\_sequences": 3,  
 "top\_k": 50,  
 "top\_p": 0.95,  
 "do\_sample": True},  
 content\_handler=content\_handler  
 ),  
 prompt=llm\_prompt  
)  

```

Create a configuration and initialize an Amazon Comprehend Moderation chain

```python
moderation\_config = {   
 "filters":[ BaseModerationFilters.PII, BaseModerationFilters.TOXICITY ],  
 "pii":{"action": BaseModerationActions.ALLOW, "threshold":0.5, "labels":["SSN"], "mask\_character": "X"},  
 "toxicity":{"action": BaseModerationActions.STOP, "threshold":0.5},  
 "intent":{"action": BaseModerationActions.ALLOW, "threshold":0.5,},  
 }  
  
amazon\_comp\_moderation = AmazonComprehendModerationChain(moderation\_config=moderation\_config,   
 client=comprehend\_client ,  
 verbose=True)  

```

The `moderation_config` will now prevent any inputs and model outputs containing obscene words or sentences, bad intent, or Pii with entities other than SSN with score above threshold or 0.5 or 50%. If it finds Pii entities - SSN - it will redact them before allowing the call to proceed.

```python
chain = (  
 prompt   
 | amazon\_comp\_moderation   
 | {llm\_chain.input\_keys[0]: lambda x: x['output'] }   
 | llm\_chain   
 | { "input": lambda x: x['text'] }   
 | amazon\_comp\_moderation   
)  
  
try:  
 response = chain.invoke({"question": "My AnyCompany Financial Services, LLC credit card account 1111-0000-1111-0008 has 24$ due by July 31st. Can you give me some more samples?"})  
except Exception as e:  
 print(str(e))  
else:  
 print(response['output'])  

```

- [Setting up](#setting-up)

- [Using AmazonComprehendModerationChain with LLM chain](#using-amazoncomprehendmoderationchain-with-llm-chain)

- [Using `moderation_config` to customize your moderation](#using-moderation_config-to-customize-your-moderation)

- [Unique ID, and Moderation Callbacks](#unique-id-and-moderation-callbacks)

- [`moderation_config` and moderation execution order](#moderation_config-and-moderation-execution-order)

- [Examples](#examples)

  - [With Hugging Face Hub Models](#with-hugging-face-hub-models)
  - [With Amazon SageMaker Jumpstart](#with-amazon-sagemaker-jumpstart)

- [With Hugging Face Hub Models](#with-hugging-face-hub-models)

- [With Amazon SageMaker Jumpstart](#with-amazon-sagemaker-jumpstart)
