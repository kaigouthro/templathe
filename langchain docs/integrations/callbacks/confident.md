# Confident

[DeepEval](https://confident-ai.com) package for unit testing LLMs.
Using Confident, everyone can build robust language models through faster iterations
using both unit testing and integration testing. We provide support for each step in the iteration
from synthetic data creation to testing.

In this guide we will demonstrate how to test and measure LLMs in performance. We show how you can use our callback to measure performance and how you can define your own metric and log them into our dashboard.

DeepEval also offers:

- How to generate synthetic data
- How to measure performance
- A dashboard to monitor and review results over time

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

```bash
pip install deepeval --upgrade  

```

### Getting API Credentials[​](#getting-api-credentials "Direct link to Getting API Credentials")

To get the DeepEval API credentials, follow the next steps:

1. Go to <https://app.confident-ai.com>
1. Click on "Organization"
1. Copy the API Key.

When you log in, you will also be asked to set the `implementation` name. The implementation name is required to describe the type of implementation. (Think of what you want to call your project. We recommend making it descriptive.)

```bash
deepeval login  

```

### Setup DeepEval[​](#setup-deepeval "Direct link to Setup DeepEval")

You can, by default, use the `DeepEvalCallbackHandler` to set up the metrics you want to track. However, this has limited support for metrics at the moment (more to be added soon). It currently supports:

- [Answer Relevancy](https://docs.confident-ai.com/docs/measuring_llm_performance/answer_relevancy)
- [Bias](https://docs.confident-ai.com/docs/measuring_llm_performance/debias)
- [Toxicness](https://docs.confident-ai.com/docs/measuring_llm_performance/non_toxic)

```python
from deepeval.metrics.answer\_relevancy import AnswerRelevancy  
  
# Here we want to make sure the answer is minimally relevant  
answer\_relevancy\_metric = AnswerRelevancy(minimum\_score=0.5)  

```

## Get Started[​](#get-started "Direct link to Get Started")

To use the `DeepEvalCallbackHandler`, we need the `implementation_name`.

```python
import os  
from langchain.callbacks.confident\_callback import DeepEvalCallbackHandler  
  
deepeval\_callback = DeepEvalCallbackHandler(  
 implementation\_name="langchainQuickstart",  
 metrics=[answer\_relevancy\_metric]  
)  

```

### Scenario 1: Feeding into LLM[​](#scenario-1-feeding-into-llm "Direct link to Scenario 1: Feeding into LLM")

You can then feed it into your LLM with OpenAI.

```python
from langchain.llms import OpenAI  
llm = OpenAI(  
 temperature=0,  
 callbacks=[deepeval\_callback],  
 verbose=True,  
 openai\_api\_key="<YOUR\_API\_KEY>",  
)  
output = llm.generate(  
 [  
 "What is the best evaluation tool out there? (no bias at all)",  
 ]  
)  

```

```text
 LLMResult(generations=[[Generation(text='\n\nQ: What did the fish say when he hit the wall? \nA: Dam.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})], [Generation(text='\n\nThe Moon \n\nThe moon is high in the midnight sky,\nSparkling like a star above.\nThe night so peaceful, so serene,\nFilling up the air with love.\n\nEver changing and renewing,\nA never-ending light of grace.\nThe moon remains a constant view,\nA reminder of life’s gentle pace.\n\nThrough time and space it guides us on,\nA never-fading beacon of hope.\nThe moon shines down on us all,\nAs it continues to rise and elope.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})], [Generation(text='\n\nQ. What did one magnet say to the other magnet?\nA. "I find you very attractive!"', generation\_info={'finish\_reason': 'stop', 'logprobs': None})], [Generation(text="\n\nThe world is charged with the grandeur of God.\nIt will flame out, like shining from shook foil;\nIt gathers to a greatness, like the ooze of oil\nCrushed. Why do men then now not reck his rod?\n\nGenerations have trod, have trod, have trod;\nAnd all is seared with trade; bleared, smeared with toil;\nAnd wears man's smudge and shares man's smell: the soil\nIs bare now, nor can foot feel, being shod.\n\nAnd for all this, nature is never spent;\nThere lives the dearest freshness deep down things;\nAnd though the last lights off the black West went\nOh, morning, at the brown brink eastward, springs —\n\nBecause the Holy Ghost over the bent\nWorld broods with warm breast and with ah! bright wings.\n\n~Gerard Manley Hopkins", generation\_info={'finish\_reason': 'stop', 'logprobs': None})], [Generation(text='\n\nQ: What did one ocean say to the other ocean?\nA: Nothing, they just waved.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})], [Generation(text="\n\nA poem for you\n\nOn a field of green\n\nThe sky so blue\n\nA gentle breeze, the sun above\n\nA beautiful world, for us to love\n\nLife is a journey, full of surprise\n\nFull of joy and full of surprise\n\nBe brave and take small steps\n\nThe future will be revealed with depth\n\nIn the morning, when dawn arrives\n\nA fresh start, no reason to hide\n\nSomewhere down the road, there's a heart that beats\n\nBelieve in yourself, you'll always succeed.", generation\_info={'finish\_reason': 'stop', 'logprobs': None})]], llm\_output={'token\_usage': {'completion\_tokens': 504, 'total\_tokens': 528, 'prompt\_tokens': 24}, 'model\_name': 'text-davinci-003'})  

```

You can then check the metric if it was successful by calling the `is_successful()` method.

```python
answer\_relevancy\_metric.is\_successful()  
# returns True/False  

```

Once you have ran that, you should be able to see our dashboard below.

![Dashboard](https://docs.confident-ai.com/assets/images/dashboard-screenshot-b02db73008213a211b1158ff052d969e.png)

![Dashboard](https://docs.confident-ai.com/assets/images/dashboard-screenshot-b02db73008213a211b1158ff052d969e.png)

### Scenario 2: Tracking an LLM in a chain without callbacks[​](#scenario-2-tracking-an-llm-in-a-chain-without-callbacks "Direct link to Scenario 2: Tracking an LLM in a chain without callbacks")

To track an LLM in a chain without callbacks, you can plug into it at the end.

We can start by defining a simple chain as shown below.

```python
import requests  
from langchain.chains import RetrievalQA  
from langchain.document\_loaders import TextLoader  
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.llms import OpenAI  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Chroma  
  
text\_file\_url = "https://raw.githubusercontent.com/hwchase17/chat-your-data/master/state\_of\_the\_union.txt"  
  
openai\_api\_key = "sk-XXX"  
  
with open("state\_of\_the\_union.txt", "w") as f:  
 response = requests.get(text\_file\_url)  
 f.write(response.text)  
  
loader = TextLoader("state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
texts = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings(openai\_api\_key=openai\_api\_key)  
docsearch = Chroma.from\_documents(texts, embeddings)  
  
qa = RetrievalQA.from\_chain\_type(  
 llm=OpenAI(openai\_api\_key=openai\_api\_key), chain\_type="stuff",  
 retriever=docsearch.as\_retriever()  
)  
  
# Providing a new question-answering pipeline  
query = "Who is the president?"  
result = qa.run(query)  

```

After defining a chain, you can then manually check for answer similarity.

```python
answer\_relevancy\_metric.measure(result, query)  
answer\_relevancy\_metric.is\_successful()  

```

### What's next?[​](#whats-next "Direct link to What's next?")

You can create your own custom metrics [here](https://docs.confident-ai.com/docs/quickstart/custom-metrics).

DeepEval also offers other features such as being able to [automatically create unit tests](https://docs.confident-ai.com/docs/quickstart/synthetic-data-creation), [tests for hallucination](https://docs.confident-ai.com/docs/measuring_llm_performance/factual_consistency).

If you are interested, check out our Github repository here <https://github.com/confident-ai/deepeval>. We welcome any PRs and discussions on how to improve LLM performance.

- [Installation and Setup](#installation-and-setup)

  - [Getting API Credentials](#getting-api-credentials)
  - [Setup DeepEval](#setup-deepeval)

- [Get Started](#get-started)

  - [Scenario 1: Feeding into LLM](#scenario-1-feeding-into-llm)
  - [Scenario 2: Tracking an LLM in a chain without callbacks](#scenario-2-tracking-an-llm-in-a-chain-without-callbacks)
  - [What's next?](#whats-next)

- [Getting API Credentials](#getting-api-credentials)

- [Setup DeepEval](#setup-deepeval)

- [Scenario 1: Feeding into LLM](#scenario-1-feeding-into-llm)

- [Scenario 2: Tracking an LLM in a chain without callbacks](#scenario-2-tracking-an-llm-in-a-chain-without-callbacks)

- [What's next?](#whats-next)
