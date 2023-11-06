# Comparing Chain Outputs

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/guides/evaluation/examples/comparisons.ipynb)

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

Suppose you have two different prompts (or LLMs). How do you know which will generate "better" results?

One automated way to predict the preferred configuration is to use a `PairwiseStringEvaluator` like the `PairwiseStringEvalChain`[\[1\]](#cite_note-1). This chain prompts an LLM to select which output is preferred, given a specific input.

For this evaluation, we will need 3 things:

1. An evaluator
1. A dataset of inputs
1. 2 (or more) LLMs, Chains, or Agents to compare

Then we will aggregate the results to determine the preferred model.

### Step 1. Create the Evaluator[​](#step-1-create-the-evaluator "Direct link to Step 1. Create the Evaluator")

In this example, you will use gpt-4 to select which output is preferred.

```python
from langchain.evaluation import load\_evaluator  
  
eval\_chain = load\_evaluator("pairwise\_string")  

```

### Step 2. Select Dataset[​](#step-2-select-dataset "Direct link to Step 2. Select Dataset")

If you already have real usage data for your LLM, you can use a representative sample. More examples
provide more reliable results. We will use some example queries someone might have about how to use langchain here.

```python
from langchain.evaluation.loading import load\_dataset  
  
dataset = load\_dataset("langchain-howto-queries")  

```

```text
 Found cached dataset parquet (/Users/wfh/.cache/huggingface/datasets/LangChainDatasets\_\_\_parquet/LangChainDatasets--langchain-howto-queries-bbb748bbee7e77aa/0.0.0/14a00e99c0d15a23649d0db8944380ac81082d4b021f398733dd84f3a6c569a7)  
  
  
  
 0%| | 0/1 [00:00<?, ?it/s]  

```

### Step 3. Define Models to Compare[​](#step-3-define-models-to-compare "Direct link to Step 3. Define Models to Compare")

We will be comparing two agents in this case.

```python
from langchain.utilities import SerpAPIWrapper  
from langchain.agents import initialize\_agent, Tool  
from langchain.agents import AgentType  
from langchain.chat\_models import ChatOpenAI  
  
  
# Initialize the language model  
# You can add your own OpenAI API key by adding openai\_api\_key="<your\_api\_key>"  
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")  
  
# Initialize the SerpAPIWrapper for search functionality  
# Replace <your\_api\_key> in openai\_api\_key="<your\_api\_key>" with your actual SerpAPI key.  
search = SerpAPIWrapper()  
  
# Define a list of tools offered by the agent  
tools = [  
 Tool(  
 name="Search",  
 func=search.run,  
 coroutine=search.arun,  
 description="Useful when you need to answer questions about current events. You should ask targeted questions.",  
 ),  
]  

```

```python
functions\_agent = initialize\_agent(  
 tools, llm, agent=AgentType.OPENAI\_MULTI\_FUNCTIONS, verbose=False  
)  
conversations\_agent = initialize\_agent(  
 tools, llm, agent=AgentType.CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=False  
)  

```

### Step 4. Generate Responses[​](#step-4-generate-responses "Direct link to Step 4. Generate Responses")

We will generate outputs for each of the models before evaluating them.

```python
from tqdm.notebook import tqdm  
import asyncio  
  
results = []  
agents = [functions\_agent, conversations\_agent]  
concurrency\_level = 6 # How many concurrent agents to run. May need to decrease if OpenAI is rate limiting.  
  
# We will only run the first 20 examples of this dataset to speed things up  
# This will lead to larger confidence intervals downstream.  
batch = []  
for example in tqdm(dataset[:20]):  
 batch.extend([agent.acall(example["inputs"]) for agent in agents])  
 if len(batch) >= concurrency\_level:  
 batch\_results = await asyncio.gather(\*batch, return\_exceptions=True)  
 results.extend(list(zip(\*[iter(batch\_results)] \* 2)))  
 batch = []  
if batch:  
 batch\_results = await asyncio.gather(\*batch, return\_exceptions=True)  
 results.extend(list(zip(\*[iter(batch\_results)] \* 2)))  

```

```text
 0%| | 0/20 [00:00<?, ?it/s]  

```

## Step 5. Evaluate Pairs[​](#step-5-evaluate-pairs "Direct link to Step 5. Evaluate Pairs")

Now it's time to evaluate the results. For each agent response, run the evaluation chain to select which output is preferred (or return a tie).

Randomly select the input order to reduce the likelihood that one model will be preferred just because it is presented first.

```python
import random  
  
  
def predict\_preferences(dataset, results) -> list:  
 preferences = []  
  
 for example, (res\_a, res\_b) in zip(dataset, results):  
 input\_ = example["inputs"]  
 # Flip a coin to reduce persistent position bias  
 if random.random() < 0.5:  
 pred\_a, pred\_b = res\_a, res\_b  
 a, b = "a", "b"  
 else:  
 pred\_a, pred\_b = res\_b, res\_a  
 a, b = "b", "a"  
 eval\_res = eval\_chain.evaluate\_string\_pairs(  
 prediction=pred\_a["output"] if isinstance(pred\_a, dict) else str(pred\_a),  
 prediction\_b=pred\_b["output"] if isinstance(pred\_b, dict) else str(pred\_b),  
 input=input\_,  
 )  
 if eval\_res["value"] == "A":  
 preferences.append(a)  
 elif eval\_res["value"] == "B":  
 preferences.append(b)  
 else:  
 preferences.append(None) # No preference  
 return preferences  

```

```python
preferences = predict\_preferences(dataset, results)  

```

**Print out the ratio of preferences.**

```python
from collections import Counter  
  
name\_map = {  
 "a": "OpenAI Functions Agent",  
 "b": "Structured Chat Agent",  
}  
counts = Counter(preferences)  
pref\_ratios = {k: v / len(preferences) for k, v in counts.items()}  
for k, v in pref\_ratios.items():  
 print(f"{name\_map.get(k)}: {v:.2%}")  

```

```text
 OpenAI Functions Agent: 95.00%  
 None: 5.00%  

```

### Estimate Confidence Intervals[​](#estimate-confidence-intervals "Direct link to Estimate Confidence Intervals")

The results seem pretty clear, but if you want to have a better sense of how confident we are, that model "A" (the OpenAI Functions Agent) is the preferred model, we can calculate confidence intervals.

Below, use the Wilson score to estimate the confidence interval.

```python
from math import sqrt  
  
  
def wilson\_score\_interval(  
 preferences: list, which: str = "a", z: float = 1.96  
) -> tuple:  
 """Estimate the confidence interval using the Wilson score.  
  
 See: https://en.wikipedia.org/wiki/Binomial\_proportion\_confidence\_interval#Wilson\_score\_interval  
 for more details, including when to use it and when it should not be used.  
 """  
 total\_preferences = preferences.count("a") + preferences.count("b")  
 n\_s = preferences.count(which)  
  
 if total\_preferences == 0:  
 return (0, 0)  
  
 p\_hat = n\_s / total\_preferences  
  
 denominator = 1 + (z\*\*2) / total\_preferences  
 adjustment = (z / denominator) \* sqrt(  
 p\_hat \* (1 - p\_hat) / total\_preferences  
 + (z\*\*2) / (4 \* total\_preferences \* total\_preferences)  
 )  
 center = (p\_hat + (z\*\*2) / (2 \* total\_preferences)) / denominator  
 lower\_bound = min(max(center - adjustment, 0.0), 1.0)  
 upper\_bound = min(max(center + adjustment, 0.0), 1.0)  
  
 return (lower\_bound, upper\_bound)  

```

```python
for which\_, name in name\_map.items():  
 low, high = wilson\_score\_interval(preferences, which=which\_)  
 print(  
 f'The "{name}" would be preferred between {low:.2%} and {high:.2%} percent of the time (with 95% confidence).'  
 )  

```

```text
 The "OpenAI Functions Agent" would be preferred between 83.18% and 100.00% percent of the time (with 95% confidence).  
 The "Structured Chat Agent" would be preferred between 0.00% and 16.82% percent of the time (with 95% confidence).  

```

**Print out the p-value.**

```python
from scipy import stats  
  
preferred\_model = max(pref\_ratios, key=pref\_ratios.get)  
successes = preferences.count(preferred\_model)  
n = len(preferences) - preferences.count(None)  
p\_value = stats.binom\_test(successes, n, p=0.5, alternative="two-sided")  
print(  
 f"""The p-value is {p\_value:.5f}. If the null hypothesis is true (i.e., if the selected eval chain actually has no preference between the models),  
then there is a {p\_value:.5%} chance of observing the {name\_map.get(preferred\_model)} be preferred at least {successes}  
times out of {n} trials."""  
)  

```

```text
 The p-value is 0.00000. If the null hypothesis is true (i.e., if the selected eval chain actually has no preference between the models),  
 then there is a 0.00038% chance of observing the OpenAI Functions Agent be preferred at least 19  
 times out of 19 trials.  
  
  
 /var/folders/gf/6rnp\_mbx5914kx7qmmh7xzmw0000gn/T/ipykernel\_15978/384907688.py:6: DeprecationWarning: 'binom\_test' is deprecated in favour of 'binomtest' from version 1.7.0 and will be removed in Scipy 1.12.0.  
 p\_value = stats.binom\_test(successes, n, p=0.5, alternative="two-sided")  

```

- [Step 1. Create the Evaluator](#step-1-create-the-evaluator)

- [Step 2. Select Dataset](#step-2-select-dataset)

- [Step 3. Define Models to Compare](#step-3-define-models-to-compare)

- [Step 4. Generate Responses](#step-4-generate-responses)

- [Step 5. Evaluate Pairs](#step-5-evaluate-pairs)

  - [Estimate Confidence Intervals](#estimate-confidence-intervals)

- [Estimate Confidence Intervals](#estimate-confidence-intervals)
