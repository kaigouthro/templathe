# LangSmith Walkthrough

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/guides/langsmith/walkthrough.ipynb)

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

LangChain makes it easy to prototype LLM applications and Agents. However, delivering LLM applications to production can be deceptively difficult. You will likely have to heavily customize and iterate on your prompts, chains, and other components to create a high-quality product.

To aid in this process, we've launched LangSmith, a unified platform for debugging, testing, and monitoring your LLM applications.

When might this come in handy? You may find it useful when you want to:

- Quickly debug a new chain, agent, or set of tools
- Visualize how components (chains, llms, retrievers, etc.) relate and are used
- Evaluate different prompts and LLMs for a single component
- Run a given chain several times over a dataset to ensure it consistently meets a quality bar
- Capture usage traces and using LLMs or analytics pipelines to generate insights

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

**[Create a LangSmith account](https://smith.langchain.com/) and create an API key (see bottom left corner). Familiarize yourself with the platform by looking through the [docs](https://docs.smith.langchain.com/)**

Note LangSmith is in closed beta; we're in the process of rolling it out to more users. However, you can fill out the form on the website for expedited access.

Now, let's get started!

## Log runs to LangSmith[​](#log-runs-to-langsmith "Direct link to Log runs to LangSmith")

First, configure your environment variables to tell LangChain to log traces. This is done by setting the `LANGCHAIN_TRACING_V2` environment variable to true.
You can tell LangChain which project to log to by setting the `LANGCHAIN_PROJECT` environment variable (if this isn't set, runs will be logged to the `default` project). This will automatically create the project for you if it doesn't exist. You must also set the `LANGCHAIN_ENDPOINT` and `LANGCHAIN_API_KEY` environment variables.

For more information on other ways to set up tracing, please reference the [LangSmith documentation](https://docs.smith.langchain.com/docs/).

**NOTE:** You must also set your `OPENAI_API_KEY` environment variables in order to run the following tutorial.

**NOTE:** You can only access an API key when you first create it. Keep it somewhere safe.

**NOTE:** You can also use a context manager in python to log traces using

```python
from langchain.callbacks.manager import tracing\_v2\_enabled  
  
with tracing\_v2\_enabled(project\_name="My Project"):  
 agent.run("How many people live in canada as of 2023?")  

```

However, in this example, we will use environment variables.

```python
%pip install openai tiktoken pandas duckduckgo-search --quiet  

```

```python
import os  
from uuid import uuid4  
  
unique\_id = uuid4().hex[0:8]  
os.environ["LANGCHAIN\_TRACING\_V2"] = "true"  
os.environ["LANGCHAIN\_PROJECT"] = f"Tracing Walkthrough - {unique\_id}"  
os.environ["LANGCHAIN\_ENDPOINT"] = "https://api.smith.langchain.com"  
os.environ["LANGCHAIN\_API\_KEY"] = "<YOUR-API-KEY>" # Update to your API key  
  
# Used by the agent in this tutorial  
os.environ["OPENAI\_API\_KEY"] = "<YOUR-OPENAI-API-KEY>"  

```

Create the langsmith client to interact with the API

```python
from langsmith import Client  
  
client = Client()  

```

Create a LangChain component and log runs to the platform. In this example, we will create a ReAct-style agent with access to a general search tool (DuckDuckGo). The agent's prompt can be viewed in the [Hub here](https://smith.langchain.com/hub/wfh/langsmith-agent-prompt).

```python
from langchain import hub  
from langchain.agents import AgentExecutor  
from langchain.agents.format\_scratchpad import format\_to\_openai\_functions  
from langchain.agents.output\_parsers import OpenAIFunctionsAgentOutputParser  
from langchain.chat\_models import ChatOpenAI  
from langchain.tools import DuckDuckGoSearchResults  
from langchain.tools.render import format\_tool\_to\_openai\_function  
  
# Fetches the latest version of this prompt  
prompt = hub.pull("wfh/langsmith-agent-prompt:latest")  
  
llm = ChatOpenAI(  
 model="gpt-3.5-turbo-16k",  
 temperature=0,  
)  
  
tools = [  
 DuckDuckGoSearchResults(  
 name="duck\_duck\_go"  
 ), # General internet search using DuckDuckGo  
]  
  
llm\_with\_tools = llm.bind(functions=[format\_tool\_to\_openai\_function(t) for t in tools])  
  
runnable\_agent = (  
 {  
 "input": lambda x: x["input"],  
 "agent\_scratchpad": lambda x: format\_to\_openai\_functions(  
 x["intermediate\_steps"]  
 ),  
 }  
 | prompt  
 | llm\_with\_tools  
 | OpenAIFunctionsAgentOutputParser()  
)  
  
agent\_executor = AgentExecutor(  
 agent=runnable\_agent, tools=tools, handle\_parsing\_errors=True  
)  

```

We are running the agent concurrently on multiple inputs to reduce latency. Runs get logged to LangSmith in the background so execution latency is unaffected.

```python
inputs = [  
 "What is LangChain?",  
 "What's LangSmith?",  
 "When was Llama-v2 released?",  
 "Who trained Llama-v2?",  
 "What is the langsmith cookbook?",  
 "When did langchain first announce the hub?",  
]  
  
results = agent\_executor.batch([{"input": x} for x in inputs], return\_exceptions=True)  

```

```python
results[:2]  

```

```text
 [{'input': 'What is LangChain?',  
 'output': 'I\'m sorry, but I couldn\'t find any information about "LangChain". Could you please provide more context or clarify your question?'},  
 {'input': "What's LangSmith?",  
 'output': 'I\'m sorry, but I couldn\'t find any information about "LangSmith". It could be a specific term or a company that is not widely known. Can you provide more context or clarify what you are referring to?'}]  

```

Assuming you've successfully set up your environment, your agent traces should show up in the `Projects` section in the [app](https://smith.langchain.com/). Congrats!

![Initial Runs](/assets/images/log_traces-edd14f0c4d5c320263362395793babdc.png)

![Initial Runs](/assets/images/log_traces-edd14f0c4d5c320263362395793babdc.png)

It looks like the agent isn't effectively using the tools though. Let's evaluate this so we have a baseline.

## Evaluate Agent[​](#evaluate-agent "Direct link to Evaluate Agent")

In addition to logging runs, LangSmith also allows you to test and evaluate your LLM applications.

In this section, you will leverage LangSmith to create a benchmark dataset and run AI-assisted evaluators on an agent. You will do so in a few steps:

1. Create a dataset
1. Initialize a new agent to benchmark
1. Configure evaluators to grade an agent's output
1. Run the agent over the dataset and evaluate the results

### 1. Create a LangSmith dataset[​](#1-create-a-langsmith-dataset "Direct link to 1. Create a LangSmith dataset")

Below, we use the LangSmith client to create a dataset from the input questions from above and a list labels. You will use these later to measure performance for a new agent. A dataset is a collection of examples, which are nothing more than input-output pairs you can use as test cases to your application.

For more information on datasets, including how to create them from CSVs or other files or how to create them in the platform, please refer to the [LangSmith documentation](https://docs.smith.langchain.com/).

```python
outputs = [  
 "LangChain is an open-source framework for building applications using large language models. It is also the name of the company building LangSmith.",  
 "LangSmith is a unified platform for debugging, testing, and monitoring language model applications and agents powered by LangChain",  
 "July 18, 2023",  
 "The langsmith cookbook is a github repository containing detailed examples of how to use LangSmith to debug, evaluate, and monitor large language model-powered applications.",  
 "September 5, 2023",  
]  

```

```python
dataset\_name = f"agent-qa-{unique\_id}"  
  
dataset = client.create\_dataset(  
 dataset\_name, description="An example dataset of questions over the LangSmith documentation."  
)  
  
for query, answer in zip(inputs, outputs):  
 client.create\_example(inputs={"input": query}, outputs={"output": answer}, dataset\_id=dataset.id)  

```

### 2. Initialize a new agent to benchmark[​](#2-initialize-a-new-agent-to-benchmark "Direct link to 2. Initialize a new agent to benchmark")

LangSmith lets you evaluate any LLM, chain, agent, or even a custom function. Conversational agents are stateful (they have memory); to ensure that this state isn't shared between dataset runs, we will pass in a `chain_factory` (aka a `constructor`) function to initialize for each call.

In this case, we will test an agent that uses OpenAI's function calling endpoints.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.agents import AgentType, initialize\_agent, load\_tools, AgentExecutor  
from langchain.agents.format\_scratchpad import format\_to\_openai\_functions  
from langchain.agents.output\_parsers import OpenAIFunctionsAgentOutputParser  
from langchain.tools.render import format\_tool\_to\_openai\_function  
from langchain import hub  
  
  
# Since chains can be stateful (e.g. they can have memory), we provide  
# a way to initialize a new chain for each row in the dataset. This is done  
# by passing in a factory function that returns a new chain for each row.  
def agent\_factory(prompt):   
 llm\_with\_tools = llm.bind(  
 functions=[format\_tool\_to\_openai\_function(t) for t in tools]  
 )  
 runnable\_agent = (  
 {  
 "input": lambda x: x["input"],  
 "agent\_scratchpad": lambda x: format\_to\_openai\_functions(x['intermediate\_steps'])  
 }   
 | prompt   
 | llm\_with\_tools   
 | OpenAIFunctionsAgentOutputParser()  
 )  
 return AgentExecutor(agent=runnable\_agent, tools=tools, handle\_parsing\_errors=True)  

```

### 3. Configure evaluation[​](#3-configure-evaluation "Direct link to 3. Configure evaluation")

Manually comparing the results of chains in the UI is effective, but it can be time consuming.
It can be helpful to use automated metrics and AI-assisted feedback to evaluate your component's performance.

Below, we will create some pre-implemented run evaluators that do the following:

- Compare results against ground truth labels.
- Measure semantic (dis)similarity using embedding distance
- Evaluate 'aspects' of the agent's response in a reference-free manner using custom criteria

For a longer discussion of how to select an appropriate evaluator for your use case and how to create your own
custom evaluators, please refer to the [LangSmith documentation](https://docs.smith.langchain.com/).

```python
from langchain.evaluation import EvaluatorType  
from langchain.smith import RunEvalConfig  
  
evaluation\_config = RunEvalConfig(  
 # Evaluators can either be an evaluator type (e.g., "qa", "criteria", "embedding\_distance", etc.) or a configuration for that evaluator  
 evaluators=[  
 # Measures whether a QA response is "Correct", based on a reference answer  
 # You can also select via the raw string "qa"  
 EvaluatorType.QA,  
 # Measure the embedding distance between the output and the reference answer  
 # Equivalent to: EvalConfig.EmbeddingDistance(embeddings=OpenAIEmbeddings())  
 EvaluatorType.EMBEDDING\_DISTANCE,  
 # Grade whether the output satisfies the stated criteria.  
 # You can select a default one such as "helpfulness" or provide your own.  
 RunEvalConfig.LabeledCriteria("helpfulness"),  
 # The LabeledScoreString evaluator outputs a score on a scale from 1-10.  
 # You can use default criteria or write our own rubric  
 RunEvalConfig.LabeledScoreString(  
 {  
 "accuracy": """  
Score 1: The answer is completely unrelated to the reference.  
Score 3: The answer has minor relevance but does not align with the reference.  
Score 5: The answer has moderate relevance but contains inaccuracies.  
Score 7: The answer aligns with the reference but has minor errors or omissions.  
Score 10: The answer is completely accurate and aligns perfectly with the reference."""  
 },  
 normalize\_by=10,  
 ),  
 ],  
 # You can add custom StringEvaluator or RunEvaluator objects here as well, which will automatically be  
 # applied to each prediction. Check out the docs for examples.  
 custom\_evaluators=[],  
)  

```

### 4. Run the agent and evaluators[​](#4-run-the-agent-and-evaluators "Direct link to 4. Run the agent and evaluators")

Use the [run_on_dataset](https://api.python.langchain.com/en/latest/smith/langchain.smith.evaluation.runner_utils.run_on_dataset.html#langchain.smith.evaluation.runner_utils.run_on_dataset) (or asynchronous [arun_on_dataset](https://api.python.langchain.com/en/latest/smith/langchain.smith.evaluation.runner_utils.arun_on_dataset.html#langchain.smith.evaluation.runner_utils.arun_on_dataset)) function to evaluate your model. This will:

1. Fetch example rows from the specified dataset.
1. Run your agent (or any custom function) on each example.
1. Apply evaluators to the resulting run traces and corresponding reference examples to generate automated feedback.

The results will be visible in the LangSmith app.

```python
from langchain import hub  
  
# We will test this version of the prompt  
prompt = hub.pull("wfh/langsmith-agent-prompt:798e7324")  

```

```python
import functools  
from langchain.smith import (  
 arun\_on\_dataset,  
 run\_on\_dataset,   
)  
  
chain\_results = run\_on\_dataset(  
 dataset\_name=dataset\_name,  
 llm\_or\_chain\_factory=functools.partial(agent\_factory, prompt=prompt),  
 evaluation=evaluation\_config,  
 verbose=True,  
 client=client,  
 project\_name=f"runnable-agent-test-5d466cbc-{unique\_id}",  
 tags=["testing-notebook", "prompt:5d466cbc"], # Optional, adds a tag to the resulting chain runs  
)  
  
# Sometimes, the agent will error due to parsing issues, incompatible tool inputs, etc.  
# These are logged as warnings here and captured as errors in the tracing UI.  

```

```text
 View the evaluation results for project 'runnable-agent-test-5d466cbc-bf2162aa' at:  
 https://smith.langchain.com/o/ebbaf2eb-769b-4505-aca2-d11de10372a4/projects/p/0c3d22fa-f8b0-4608-b086-2187c18361a5  
 [> ] 0/5  
  
 Chain failed for example 54b4fce8-4492-409d-94af-708f51698b39 with inputs {'input': 'Who trained Llama-v2?'}  
 Error Type: TypeError, Message: DuckDuckGoSearchResults.\_run() got an unexpected keyword argument 'arg1'  
  
  
 [------------------------------------------------->] 5/5  
 Eval quantiles:  
 0.25 0.5 0.75 mean mode  
 embedding\_cosine\_distance 0.086614 0.118841 0.183672 0.151444 0.050158  
 correctness 0.000000 0.500000 1.000000 0.500000 0.000000  
 score\_string:accuracy 0.775000 1.000000 1.000000 0.775000 1.000000  
 helpfulness 0.750000 1.000000 1.000000 0.750000 1.000000  

```

### Review the test results[​](#review-the-test-results "Direct link to Review the test results")

You can review the test results tracing UI below by clicking the URL in the output above or navigating to the "Testing & Datasets" page in LangSmith **"agent-qa-{unique_id}"** dataset.

![test results](/assets/images/test_results-15649f0f4500fd64ef2209229951a6c1.png)

![test results](/assets/images/test_results-15649f0f4500fd64ef2209229951a6c1.png)

This will show the new runs and the feedback logged from the selected evaluators. You can also explore a summary of the results in tabular format below.

```python
chain\_results.to\_dataframe()  

```

```html
<div>  
<style scoped>  
 .dataframe tbody tr th:only-of-type {  
 vertical-align: middle;  
 }  
  
 .dataframe tbody tr th {  
 vertical-align: top;  
 }  
  
 .dataframe thead th {  
 text-align: right;  
 }  
</style>  
<table border="1" class="dataframe">  
 <thead>  
 <tr style="text-align: right;">  
 <th></th>  
 <th>embedding\_cosine\_distance</th>  
 <th>correctness</th>  
 <th>score\_string:accuracy</th>  
 <th>helpfulness</th>  
 <th>input</th>  
 <th>output</th>  
 <th>reference</th>  
 </tr>  
 </thead>  
 <tbody>  
 <tr>  
 <th>42b639a2-17c4-4031-88a9-0ce2c45781ce</th>  
 <td>0.317938</td>  
 <td>0.0</td>  
 <td>1.0</td>  
 <td>1.0</td>  
 <td>{'input': 'What is the langsmith cookbook?'}</td>  
 <td>{'input': 'What is the langsmith cookbook?', '...</td>  
 <td>{'output': 'September 5, 2023'}</td>  
 </tr>  
 <tr>  
 <th>54b4fce8-4492-409d-94af-708f51698b39</th>  
 <td>NaN</td>  
 <td>NaN</td>  
 <td>NaN</td>  
 <td>NaN</td>  
 <td>{'input': 'Who trained Llama-v2?'}</td>  
 <td>{'Error': 'TypeError("DuckDuckGoSearchResults....</td>  
 <td>{'output': 'The langsmith cookbook is a github...</td>  
 </tr>  
 <tr>  
 <th>8ae5104e-bbb4-42cc-a84e-f9b8cfc92b8e</th>  
 <td>0.138916</td>  
 <td>1.0</td>  
 <td>1.0</td>  
 <td>1.0</td>  
 <td>{'input': 'When was Llama-v2 released?'}</td>  
 <td>{'input': 'When was Llama-v2 released?', 'outp...</td>  
 <td>{'output': 'July 18, 2023'}</td>  
 </tr>  
 <tr>  
 <th>678c0363-3ed1-410a-811f-ebadef2e783a</th>  
 <td>0.050158</td>  
 <td>1.0</td>  
 <td>1.0</td>  
 <td>1.0</td>  
 <td>{'input': 'What's LangSmith?'}</td>  
 <td>{'input': 'What's LangSmith?', 'output': 'Lang...</td>  
 <td>{'output': 'LangSmith is a unified platform fo...</td>  
 </tr>  
 <tr>  
 <th>762a616c-7aab-419c-9001-b43ab6200d26</th>  
 <td>0.098766</td>  
 <td>0.0</td>  
 <td>0.1</td>  
 <td>0.0</td>  
 <td>{'input': 'What is LangChain?'}</td>  
 <td>{'input': 'What is LangChain?', 'output': 'Lan...</td>  
 <td>{'output': 'LangChain is an open-source framew...</td>  
 </tr>  
 </tbody>  
</table>  
</div>  

```

### (Optional) Compare to another prompt[​](#optional-compare-to-another-prompt "Direct link to (Optional) Compare to another prompt")

Now that we have our test run results, we can make changes to our agent and benchmark them. Let's try this again with a different prompt and see the results.

```python
candidate\_prompt = hub.pull("wfh/langsmith-agent-prompt:39f3bbd0")  
  
chain\_results = run\_on\_dataset(  
 dataset\_name=dataset\_name,  
 llm\_or\_chain\_factory=functools.partial(agent\_factory, prompt=candidate\_prompt),  
 evaluation=evaluation\_config,  
 verbose=True,  
 client=client,  
 project\_name=f"runnable-agent-test-39f3bbd0-{unique\_id}",  
 tags=["testing-notebook", "prompt:39f3bbd0"], # Optional, adds a tag to the resulting chain runs  
)  

```

```text
 View the evaluation results for project 'runnable-agent-test-39f3bbd0-bf2162aa' at:  
 https://smith.langchain.com/o/ebbaf2eb-769b-4505-aca2-d11de10372a4/projects/p/fa721ccc-dd0f-41c9-bf80-22215c44efd4  
 [------------------------------------------------->] 5/5  
 Eval quantiles:  
 0.25 0.5 0.75 mean mode  
 embedding\_cosine\_distance 0.059506 0.155538 0.212864 0.157915 0.043119  
 correctness 0.000000 0.000000 1.000000 0.400000 0.000000  
 score\_string:accuracy 0.700000 1.000000 1.000000 0.880000 1.000000  
 helpfulness 1.000000 1.000000 1.000000 0.800000 1.000000  

```

## Exporting datasets and runs[​](#exporting-datasets-and-runs "Direct link to Exporting datasets and runs")

LangSmith lets you export data to common formats such as CSV or JSONL directly in the web app. You can also use the client to fetch runs for further analysis, to store in your own database, or to share with others. Let's fetch the run traces from the evaluation run.

**Note: It may be a few moments before all the runs are accessible.**

```python
runs = client.list\_runs(project\_name=chain\_results["project\_name"], execution\_order=1)  

```

```python
# After some time, these will be populated.  
client.read\_project(project\_name=chain\_results["project\_name"]).feedback\_stats  

```

## Conclusion[​](#conclusion "Direct link to Conclusion")

Congratulations! You have successfully traced and evaluated an agent using LangSmith!

This was a quick guide to get started, but there are many more ways to use LangSmith to speed up your developer flow and produce better results.

For more information on how you can get the most out of LangSmith, check out [LangSmith documentation](https://docs.smith.langchain.com/), and please reach out with questions, feature requests, or feedback at [support@langchain.dev](mailto:support@langchain.dev).

- [Prerequisites](#prerequisites)

- [Log runs to LangSmith](#log-runs-to-langsmith)

- [Evaluate Agent](#evaluate-agent)

  - [1. Create a LangSmith dataset](#1-create-a-langsmith-dataset)
  - [2. Initialize a new agent to benchmark](#2-initialize-a-new-agent-to-benchmark)
  - [3. Configure evaluation](#3-configure-evaluation)
  - [4. Run the agent and evaluators](#4-run-the-agent-and-evaluators)
  - [Review the test results](#review-the-test-results)
  - [(Optional) Compare to another prompt](#optional-compare-to-another-prompt)

- [Exporting datasets and runs](#exporting-datasets-and-runs)

- [Conclusion](#conclusion)

- [1. Create a LangSmith dataset](#1-create-a-langsmith-dataset)

- [2. Initialize a new agent to benchmark](#2-initialize-a-new-agent-to-benchmark)

- [3. Configure evaluation](#3-configure-evaluation)

- [4. Run the agent and evaluators](#4-run-the-agent-and-evaluators)

- [Review the test results](#review-the-test-results)

- [(Optional) Compare to another prompt](#optional-compare-to-another-prompt)
