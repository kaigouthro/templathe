# SageMaker Tracking

This notebook shows how LangChain Callback can be used to log and track prompts and other LLM hyperparameters into SageMaker Experiments. Here, we use different scenarios to showcase the capability:

- **Scenario 1**: *Single LLM* - A case where a single LLM model is used to generate output based on a given prompt.
- **Scenario 2**: *Sequential Chain* - A case where a sequential chain of two LLM models is used.
- **Scenario 3**: *Agent with Tools (Chain of Thought)* - A case where multiple tools (search and math) are used in addition to an LLM.

[Amazon SageMaker](https://aws.amazon.com/sagemaker/) is a fully managed service that is used to quickly and easily build, train and deploy machine learning (ML) models.

[Amazon SageMaker Experiments](https://docs.aws.amazon.com/sagemaker/latest/dg/experiments.html) is a capability of Amazon SageMaker that lets you organize, track, compare and evaluate ML experiments and model versions.

In this notebook, we will create a single experiment to log the prompts from each scenario.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

```bash
pip install sagemaker  
pip install openai  
pip install google-search-results  

```

First, setup the required API keys

- OpenAI: <https://platform.openai.com/account/api-keys> (For OpenAI LLM model)
- Google SERP API: <https://serpapi.com/manage-api-key> (For Google Search Tool)

```python
import os  
  
## Add your API keys below  
os.environ["OPENAI\_API\_KEY"] = "<ADD-KEY-HERE>"  
os.environ["SERPAPI\_API\_KEY"] = "<ADD-KEY-HERE>"  

```

```python
from langchain.llms import OpenAI  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain, SimpleSequentialChain  
from langchain.agents import initialize\_agent, load\_tools  
from langchain.agents import Tool  
from langchain.callbacks import SageMakerCallbackHandler  
  
from sagemaker.analytics import ExperimentAnalytics  
from sagemaker.session import Session  
from sagemaker.experiments.run import Run  

```

## LLM Prompt Tracking[​](#llm-prompt-tracking "Direct link to LLM Prompt Tracking")

```python
#LLM Hyperparameters  
HPARAMS = {  
 "temperature": 0.1,  
 "model\_name": "text-davinci-003",  
}  
  
#Bucket used to save prompt logs (Use `None` is used to save the default bucket or otherwise change it)  
BUCKET\_NAME = None  
  
#Experiment name  
EXPERIMENT\_NAME = "langchain-sagemaker-tracker"  
  
#Create SageMaker Session with the given bucket  
session = Session(default\_bucket=BUCKET\_NAME)  

```

### Scenario 1 - LLM[​](#scenario-1---llm "Direct link to Scenario 1 - LLM")

```python
RUN\_NAME = "run-scenario-1"  
PROMPT\_TEMPLATE = "tell me a joke about {topic}"  
INPUT\_VARIABLES = {"topic": "fish"}  

```

```python
with Run(experiment\_name=EXPERIMENT\_NAME, run\_name=RUN\_NAME, sagemaker\_session=session) as run:  
  
 # Create SageMaker Callback  
 sagemaker\_callback = SageMakerCallbackHandler(run)  
  
 # Define LLM model with callback  
 llm = OpenAI(callbacks=[sagemaker\_callback], \*\*HPARAMS)  
  
 # Create prompt template  
 prompt = PromptTemplate.from\_template(template=PROMPT\_TEMPLATE)  
  
 # Create LLM Chain  
 chain = LLMChain(llm=llm, prompt=prompt, callbacks=[sagemaker\_callback])  
  
 # Run chain  
 chain.run(\*\*INPUT\_VARIABLES)  
  
 # Reset the callback  
 sagemaker\_callback.flush\_tracker()  

```

### Scenario 2 - Sequential Chain[​](#scenario-2---sequential-chain "Direct link to Scenario 2 - Sequential Chain")

```python
RUN\_NAME = "run-scenario-2"  
  
PROMPT\_TEMPLATE\_1 = """You are a playwright. Given the title of play, it is your job to write a synopsis for that title.  
Title: {title}  
Playwright: This is a synopsis for the above play:"""  
PROMPT\_TEMPLATE\_2 = """You are a play critic from the New York Times. Given the synopsis of play, it is your job to write a review for that play.  
Play Synopsis: {synopsis}  
Review from a New York Times play critic of the above play:"""  
  
INPUT\_VARIABLES = {  
 "input": "documentary about good video games that push the boundary of game design"  
}  

```

```python
with Run(experiment\_name=EXPERIMENT\_NAME, run\_name=RUN\_NAME, sagemaker\_session=session) as run:  
  
 # Create SageMaker Callback  
 sagemaker\_callback = SageMakerCallbackHandler(run)  
  
 # Create prompt templates for the chain  
 prompt\_template1 = PromptTemplate.from\_template(template=PROMPT\_TEMPLATE\_1)  
 prompt\_template2 = PromptTemplate.from\_template(template=PROMPT\_TEMPLATE\_2)  
  
 # Define LLM model with callback  
 llm = OpenAI(callbacks=[sagemaker\_callback], \*\*HPARAMS)  
  
 # Create chain1  
 chain1 = LLMChain(llm=llm, prompt=prompt\_template1, callbacks=[sagemaker\_callback])  
  
 # Create chain2  
 chain2 = LLMChain(llm=llm, prompt=prompt\_template2, callbacks=[sagemaker\_callback])  
  
 # Create Sequential chain  
 overall\_chain = SimpleSequentialChain(chains=[chain1, chain2], callbacks=[sagemaker\_callback])  
  
 # Run overall sequential chain  
 overall\_chain.run(\*\*INPUT\_VARIABLES)  
  
 # Reset the callback  
 sagemaker\_callback.flush\_tracker()  

```

### Scenario 3 - Agent with Tools[​](#scenario-3---agent-with-tools "Direct link to Scenario 3 - Agent with Tools")

```python
RUN\_NAME = "run-scenario-3"  
PROMPT\_TEMPLATE = "Who is the oldest person alive? And what is their current age raised to the power of 1.51?"  

```

```python
with Run(experiment\_name=EXPERIMENT\_NAME, run\_name=RUN\_NAME, sagemaker\_session=session) as run:  
  
 # Create SageMaker Callback  
 sagemaker\_callback = SageMakerCallbackHandler(run)  
  
 # Define LLM model with callback  
 llm = OpenAI(callbacks=[sagemaker\_callback], \*\*HPARAMS)  
  
 # Define tools  
 tools = load\_tools(["serpapi", "llm-math"], llm=llm, callbacks=[sagemaker\_callback])  
  
 # Initialize agent with all the tools  
 agent = initialize\_agent(tools, llm, agent="zero-shot-react-description", callbacks=[sagemaker\_callback])  
  
 # Run agent  
 agent.run(input=PROMPT\_TEMPLATE)  
  
 # Reset the callback  
 sagemaker\_callback.flush\_tracker()  

```

## Load Log Data[​](#load-log-data "Direct link to Load Log Data")

Once the prompts are logged, we can easily load and convert them to Pandas DataFrame as follows.

```python
#Load  
logs = ExperimentAnalytics(experiment\_name=EXPERIMENT\_NAME)  
  
#Convert as pandas dataframe  
df = logs.dataframe(force\_refresh=True)  
  
print(df.shape)  
df.head()  

```

As can be seen above, there are three runs (rows) in the experiment corresponding to each scenario. Each run logs the prompts and related LLM settings/hyperparameters as json and are saved in s3 bucket. Feel free to load and explore the log data from each json path.

- [Installation and Setup](#installation-and-setup)

- [LLM Prompt Tracking](#llm-prompt-tracking)

  - [Scenario 1 - LLM](#scenario-1---llm)
  - [Scenario 2 - Sequential Chain](#scenario-2---sequential-chain)
  - [Scenario 3 - Agent with Tools](#scenario-3---agent-with-tools)

- [Load Log Data](#load-log-data)

- [Scenario 1 - LLM](#scenario-1---llm)

- [Scenario 2 - Sequential Chain](#scenario-2---sequential-chain)

- [Scenario 3 - Agent with Tools](#scenario-3---agent-with-tools)
