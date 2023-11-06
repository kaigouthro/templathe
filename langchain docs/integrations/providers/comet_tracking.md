# Comet

![](https://user-images.githubusercontent.com/7529846/230328046-a8b18c51-12e3-4617-9b39-97614a571a2d.png)

![](https://user-images.githubusercontent.com/7529846/230328046-a8b18c51-12e3-4617-9b39-97614a571a2d.png)

In this guide we will demonstrate how to track your Langchain Experiments, Evaluation Metrics, and LLM Sessions with [Comet](https://www.comet.com/site/?utm_source=langchain&utm_medium=referral&utm_campaign=comet_notebook).

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

**Example Project:** [Comet with LangChain](https://www.comet.com/examples/comet-example-langchain/view/b5ZThK6OFdhKWVSP3fDfRtrNF/panels?utm_source=langchain&utm_medium=referral&utm_campaign=comet_notebook)

![](https://user-images.githubusercontent.com/7529846/230326720-a9711435-9c6f-4edb-a707-94b67271ab25.png)

![](https://user-images.githubusercontent.com/7529846/230326720-a9711435-9c6f-4edb-a707-94b67271ab25.png)

### Install Comet and Dependencies[​](#install-comet-and-dependencies "Direct link to Install Comet and Dependencies")

```bash
import sys  
{sys.executable} -m spacy download en\_core\_web\_sm  

```

### Initialize Comet and Set your Credentials[​](#initialize-comet-and-set-your-credentials "Direct link to Initialize Comet and Set your Credentials")

You can grab your [Comet API Key here](https://www.comet.com/signup?utm_source=langchain&utm_medium=referral&utm_campaign=comet_notebook) or click the link after initializing Comet

```python
import comet\_ml  
  
comet\_ml.init(project\_name="comet-example-langchain")  

```

### Set OpenAI and SerpAPI credentials[​](#set-openai-and-serpapi-credentials "Direct link to Set OpenAI and SerpAPI credentials")

You will need an [OpenAI API Key](https://platform.openai.com/account/api-keys) and a [SerpAPI API Key](https://serpapi.com/dashboard) to run the following examples

```python
import os  
  
os.environ["OPENAI\_API\_KEY"] = "..."  
# os.environ["OPENAI\_ORGANIZATION"] = "..."  
os.environ["SERPAPI\_API\_KEY"] = "..."  

```

### Scenario 1: Using just an LLM[​](#scenario-1-using-just-an-llm "Direct link to Scenario 1: Using just an LLM")

```python
from datetime import datetime  
  
from langchain.callbacks import CometCallbackHandler, StdOutCallbackHandler  
from langchain.llms import OpenAI  
  
comet\_callback = CometCallbackHandler(  
 project\_name="comet-example-langchain",  
 complexity\_metrics=True,  
 stream\_logs=True,  
 tags=["llm"],  
 visualizations=["dep"],  
)  
callbacks = [StdOutCallbackHandler(), comet\_callback]  
llm = OpenAI(temperature=0.9, callbacks=callbacks, verbose=True)  
  
llm\_result = llm.generate(["Tell me a joke", "Tell me a poem", "Tell me a fact"] \* 3)  
print("LLM result", llm\_result)  
comet\_callback.flush\_tracker(llm, finish=True)  

```

### Scenario 2: Using an LLM in a Chain[​](#scenario-2-using-an-llm-in-a-chain "Direct link to Scenario 2: Using an LLM in a Chain")

```python
from langchain.callbacks import CometCallbackHandler, StdOutCallbackHandler  
from langchain.chains import LLMChain  
from langchain.llms import OpenAI  
from langchain.prompts import PromptTemplate  
  
comet\_callback = CometCallbackHandler(  
 complexity\_metrics=True,  
 project\_name="comet-example-langchain",  
 stream\_logs=True,  
 tags=["synopsis-chain"],  
)  
callbacks = [StdOutCallbackHandler(), comet\_callback]  
llm = OpenAI(temperature=0.9, callbacks=callbacks)  
  
template = """You are a playwright. Given the title of play, it is your job to write a synopsis for that title.  
Title: {title}  
Playwright: This is a synopsis for the above play:"""  
prompt\_template = PromptTemplate(input\_variables=["title"], template=template)  
synopsis\_chain = LLMChain(llm=llm, prompt=prompt\_template, callbacks=callbacks)  
  
test\_prompts = [{"title": "Documentary about Bigfoot in Paris"}]  
print(synopsis\_chain.apply(test\_prompts))  
comet\_callback.flush\_tracker(synopsis\_chain, finish=True)  

```

### Scenario 3: Using An Agent with Tools[​](#scenario-3-using-an-agent-with-tools "Direct link to Scenario 3: Using An Agent with Tools")

```python
from langchain.agents import initialize\_agent, load\_tools  
from langchain.callbacks import CometCallbackHandler, StdOutCallbackHandler  
from langchain.llms import OpenAI  
  
comet\_callback = CometCallbackHandler(  
 project\_name="comet-example-langchain",  
 complexity\_metrics=True,  
 stream\_logs=True,  
 tags=["agent"],  
)  
callbacks = [StdOutCallbackHandler(), comet\_callback]  
llm = OpenAI(temperature=0.9, callbacks=callbacks)  
  
tools = load\_tools(["serpapi", "llm-math"], llm=llm, callbacks=callbacks)  
agent = initialize\_agent(  
 tools,  
 llm,  
 agent="zero-shot-react-description",  
 callbacks=callbacks,  
 verbose=True,  
)  
agent.run(  
 "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"  
)  
comet\_callback.flush\_tracker(agent, finish=True)  

```

### Scenario 4: Using Custom Evaluation Metrics[​](#scenario-4-using-custom-evaluation-metrics "Direct link to Scenario 4: Using Custom Evaluation Metrics")

The `CometCallbackManager` also allows you to define and use Custom Evaluation Metrics to assess generated outputs from your model. Let's take a look at how this works.

In the snippet below, we will use the [ROUGE](https://huggingface.co/spaces/evaluate-metric/rouge) metric to evaluate the quality of a generated summary of an input prompt.

```python
%pip install rouge-score  

```

```python
from rouge\_score import rouge\_scorer  
  
from langchain.callbacks import CometCallbackHandler, StdOutCallbackHandler  
from langchain.chains import LLMChain  
from langchain.llms import OpenAI  
from langchain.prompts import PromptTemplate  
  
  
class Rouge:  
 def \_\_init\_\_(self, reference):  
 self.reference = reference  
 self.scorer = rouge\_scorer.RougeScorer(["rougeLsum"], use\_stemmer=True)  
  
 def compute\_metric(self, generation, prompt\_idx, gen\_idx):  
 prediction = generation.text  
 results = self.scorer.score(target=self.reference, prediction=prediction)  
  
 return {  
 "rougeLsum\_score": results["rougeLsum"].fmeasure,  
 "reference": self.reference,  
 }  
  
  
reference = """  
The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building.  
It was the first structure to reach a height of 300 metres.  
  
It is now taller than the Chrysler Building in New York City by 5.2 metres (17 ft)  
Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France .  
"""  
rouge\_score = Rouge(reference=reference)  
  
template = """Given the following article, it is your job to write a summary.  
Article:  
{article}  
Summary: This is the summary for the above article:"""  
prompt\_template = PromptTemplate(input\_variables=["article"], template=template)  
  
comet\_callback = CometCallbackHandler(  
 project\_name="comet-example-langchain",  
 complexity\_metrics=False,  
 stream\_logs=True,  
 tags=["custom\_metrics"],  
 custom\_metrics=rouge\_score.compute\_metric,  
)  
callbacks = [StdOutCallbackHandler(), comet\_callback]  
llm = OpenAI(temperature=0.9)  
  
synopsis\_chain = LLMChain(llm=llm, prompt=prompt\_template)  
  
test\_prompts = [  
 {  
 "article": """  
 The tower is 324 metres (1,063 ft) tall, about the same height as  
 an 81-storey building, and the tallest structure in Paris. Its base is square,  
 measuring 125 metres (410 ft) on each side.  
 During its construction, the Eiffel Tower surpassed the  
 Washington Monument to become the tallest man-made structure in the world,  
 a title it held for 41 years until the Chrysler Building  
 in New York City was finished in 1930.  
  
 It was the first structure to reach a height of 300 metres.  
 Due to the addition of a broadcasting aerial at the top of the tower in 1957,  
 it is now taller than the Chrysler Building by 5.2 metres (17 ft).  
  
 Excluding transmitters, the Eiffel Tower is the second tallest  
 free-standing structure in France after the Millau Viaduct.  
 """  
 }  
]  
print(synopsis\_chain.apply(test\_prompts, callbacks=callbacks))  
comet\_callback.flush\_tracker(synopsis\_chain, finish=True)  

```

- [Install Comet and Dependencies](#install-comet-and-dependencies)
- [Initialize Comet and Set your Credentials](#initialize-comet-and-set-your-credentials)
- [Set OpenAI and SerpAPI credentials](#set-openai-and-serpapi-credentials)
- [Scenario 1: Using just an LLM](#scenario-1-using-just-an-llm)
- [Scenario 2: Using an LLM in a Chain](#scenario-2-using-an-llm-in-a-chain)
- [Scenario 3: Using An Agent with Tools](#scenario-3-using-an-agent-with-tools)
- [Scenario 4: Using Custom Evaluation Metrics](#scenario-4-using-custom-evaluation-metrics)
