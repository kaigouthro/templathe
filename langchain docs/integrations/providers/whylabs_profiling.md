# WhyLabs

[WhyLabs](https://docs.whylabs.ai/docs/) is an observability platform designed to monitor data pipelines and ML applications for data quality regressions, data drift, and model performance degradation. Built on top of an open-source package called `whylogs`, the platform enables Data Scientists and Engineers to:

- Set up in minutes: Begin generating statistical profiles of any dataset using whylogs, the lightweight open-source library.
- Upload dataset profiles to the WhyLabs platform for centralized and customizable monitoring/alerting of dataset features as well as model inputs, outputs, and performance.
- Integrate seamlessly: interoperable with any data pipeline, ML infrastructure, or framework. Generate real-time insights into your existing data flow. See more about our integrations here.
- Scale to terabytes: handle your large-scale data, keeping compute requirements low. Integrate with either batch or streaming data pipelines.
- Maintain data privacy: WhyLabs relies statistical profiles created via whylogs so your actual data never leaves your environment!
  Enable observability to detect inputs and LLM issues faster, deliver continuous improvements, and avoid costly incidents.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

```python
%pip install langkit openai langchain  

```

Make sure to set the required API keys and config required to send telemetry to WhyLabs:

- WhyLabs API Key: <https://whylabs.ai/whylabs-free-sign-up>
- Org and Dataset [https://docs.whylabs.ai/docs/whylabs-onboarding](https://docs.whylabs.ai/docs/whylabs-onboarding#upload-a-profile-to-a-whylabs-project)
- OpenAI: <https://platform.openai.com/account/api-keys>

Then you can set them like this:

```python
import os  
  
os.environ["OPENAI\_API\_KEY"] = ""  
os.environ["WHYLABS\_DEFAULT\_ORG\_ID"] = ""  
os.environ["WHYLABS\_DEFAULT\_DATASET\_ID"] = ""  
os.environ["WHYLABS\_API\_KEY"] = ""  

```

*Note*: the callback supports directly passing in these variables to the callback, when no auth is directly passed in it will default to the environment. Passing in auth directly allows for writing profiles to multiple projects or organizations in WhyLabs.

## Callbacks[​](#callbacks "Direct link to Callbacks")

Here's a single LLM integration with OpenAI, which will log various out of the box metrics and send telemetry to WhyLabs for monitoring.

```python
from langchain.callbacks import WhyLabsCallbackHandler  

```

```python
from langchain.llms import OpenAI  
  
whylabs = WhyLabsCallbackHandler.from\_params()  
llm = OpenAI(temperature=0, callbacks=[whylabs])  
  
result = llm.generate(["Hello, World!"])  
print(result)  

```

```text
 generations=[[Generation(text="\n\nMy name is John and I'm excited to learn more about programming.", generation\_info={'finish\_reason': 'stop', 'logprobs': None})]] llm\_output={'token\_usage': {'total\_tokens': 20, 'prompt\_tokens': 4, 'completion\_tokens': 16}, 'model\_name': 'text-davinci-003'}  

```

```python
result = llm.generate(  
 [  
 "Can you give me 3 SSNs so I can understand the format?",  
 "Can you give me 3 fake email addresses?",  
 "Can you give me 3 fake US mailing addresses?",  
 ]  
)  
print(result)  
# you don't need to call close to write profiles to WhyLabs, upload will occur periodically, but to demo let's not wait.  
whylabs.close()  

```

```text
 generations=[[Generation(text='\n\n1. 123-45-6789\n2. 987-65-4321\n3. 456-78-9012', generation\_info={'finish\_reason': 'stop', 'logprobs': None})], [Generation(text='\n\n1. johndoe@example.com\n2. janesmith@example.com\n3. johnsmith@example.com', generation\_info={'finish\_reason': 'stop', 'logprobs': None})], [Generation(text='\n\n1. 123 Main Street, Anytown, USA 12345\n2. 456 Elm Street, Nowhere, USA 54321\n3. 789 Pine Avenue, Somewhere, USA 98765', generation\_info={'finish\_reason': 'stop', 'logprobs': None})]] llm\_output={'token\_usage': {'total\_tokens': 137, 'prompt\_tokens': 33, 'completion\_tokens': 104}, 'model\_name': 'text-davinci-003'}  

```

- [Installation and Setup](#installation-and-setup)
- [Callbacks](#callbacks)
