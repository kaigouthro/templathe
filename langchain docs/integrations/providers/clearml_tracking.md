# ClearML

[ClearML](https://github.com/allegroai/clearml) is a ML/DL development and production suite, it contains 5 main modules:

- `Experiment Manager` - Automagical experiment tracking, environments and results
- `MLOps` - Orchestration, Automation & Pipelines solution for ML/DL jobs (K8s / Cloud / bare-metal)
- `Data-Management` - Fully differentiable data management & version control solution on top of object-storage (S3 / GS / Azure / NAS)
- `Model-Serving` - cloud-ready Scalable model serving solution!
  Deploy new model endpoints in under 5 minutes
  Includes optimized GPU serving support backed by Nvidia-Triton
  with out-of-the-box Model Monitoring
- `Fire Reports` - Create and share rich MarkDown documents supporting embeddable online content

In order to properly keep track of your langchain experiments and their results, you can enable the `ClearML` integration. We use the `ClearML Experiment Manager` that neatly tracks and organizes all your experiment runs.

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

```bash
pip install clearml  
pip install pandas  
pip install textstat  
pip install spacy  
python -m spacy download en\_core\_web\_sm  

```

### Getting API Credentials[​](#getting-api-credentials "Direct link to Getting API Credentials")

We'll be using quite some APIs in this notebook, here is a list and where to get them:

- ClearML: <https://app.clear.ml/settings/workspace-configuration>
- OpenAI: <https://platform.openai.com/account/api-keys>
- SerpAPI (google search): <https://serpapi.com/dashboard>

```python
import os  
  
os.environ["CLEARML\_API\_ACCESS\_KEY"] = ""  
os.environ["CLEARML\_API\_SECRET\_KEY"] = ""  
  
os.environ["OPENAI\_API\_KEY"] = ""  
os.environ["SERPAPI\_API\_KEY"] = ""  

```

## Callbacks[​](#callbacks "Direct link to Callbacks")

```python
from langchain.callbacks import ClearMLCallbackHandler  

```

```python
from datetime import datetime  
from langchain.callbacks import StdOutCallbackHandler  
from langchain.llms import OpenAI  
  
# Setup and use the ClearML Callback  
clearml\_callback = ClearMLCallbackHandler(  
 task\_type="inference",  
 project\_name="langchain\_callback\_demo",  
 task\_name="llm",  
 tags=["test"],  
 # Change the following parameters based on the amount of detail you want tracked  
 visualize=True,  
 complexity\_metrics=True,  
 stream\_logs=True,  
)  
callbacks = [StdOutCallbackHandler(), clearml\_callback]  
# Get the OpenAI model ready to go  
llm = OpenAI(temperature=0, callbacks=callbacks)  

```

```text
 The clearml callback is currently in beta and is subject to change based on updates to `langchain`. Please report any issues to https://github.com/allegroai/clearml/issues with the tag `langchain`.  

```

### Scenario 1: Just an LLM[​](#scenario-1-just-an-llm "Direct link to Scenario 1: Just an LLM")

First, let's just run a single LLM a few times and capture the resulting prompt-answer conversation in ClearML

```python
# SCENARIO 1 - LLM  
llm\_result = llm.generate(["Tell me a joke", "Tell me a poem"] \* 3)  
# After every generation run, use flush to make sure all the metrics  
# prompts and other output are properly saved separately  
clearml\_callback.flush\_tracker(langchain\_asset=llm, name="simple\_sequential")  

```

```text
 {'action': 'on\_llm\_start', 'name': 'OpenAI', 'step': 3, 'starts': 2, 'ends': 1, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 0, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 1, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'prompts': 'Tell me a joke'}  
 {'action': 'on\_llm\_start', 'name': 'OpenAI', 'step': 3, 'starts': 2, 'ends': 1, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 0, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 1, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'prompts': 'Tell me a poem'}  
 {'action': 'on\_llm\_start', 'name': 'OpenAI', 'step': 3, 'starts': 2, 'ends': 1, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 0, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 1, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'prompts': 'Tell me a joke'}  
 {'action': 'on\_llm\_start', 'name': 'OpenAI', 'step': 3, 'starts': 2, 'ends': 1, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 0, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 1, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'prompts': 'Tell me a poem'}  
 {'action': 'on\_llm\_start', 'name': 'OpenAI', 'step': 3, 'starts': 2, 'ends': 1, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 0, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 1, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'prompts': 'Tell me a joke'}  
 {'action': 'on\_llm\_start', 'name': 'OpenAI', 'step': 3, 'starts': 2, 'ends': 1, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 0, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 1, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'prompts': 'Tell me a poem'}  
 {'action': 'on\_llm\_end', 'token\_usage\_prompt\_tokens': 24, 'token\_usage\_completion\_tokens': 138, 'token\_usage\_total\_tokens': 162, 'model\_name': 'text-davinci-003', 'step': 4, 'starts': 2, 'ends': 2, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 0, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 2, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'text': '\n\nQ: What did the fish say when it hit the wall?\nA: Dam!', 'generation\_info\_finish\_reason': 'stop', 'generation\_info\_logprobs': None, 'flesch\_reading\_ease': 109.04, 'flesch\_kincaid\_grade': 1.3, 'smog\_index': 0.0, 'coleman\_liau\_index': -1.24, 'automated\_readability\_index': 0.3, 'dale\_chall\_readability\_score': 5.5, 'difficult\_words': 0, 'linsear\_write\_formula': 5.5, 'gunning\_fog': 5.2, 'text\_standard': '5th and 6th grade', 'fernandez\_huerta': 133.58, 'szigriszt\_pazos': 131.54, 'gutierrez\_polini': 62.3, 'crawford': -0.2, 'gulpease\_index': 79.8, 'osman': 116.91}  
 {'action': 'on\_llm\_end', 'token\_usage\_prompt\_tokens': 24, 'token\_usage\_completion\_tokens': 138, 'token\_usage\_total\_tokens': 162, 'model\_name': 'text-davinci-003', 'step': 4, 'starts': 2, 'ends': 2, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 0, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 2, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'text': '\n\nRoses are red,\nViolets are blue,\nSugar is sweet,\nAnd so are you.', 'generation\_info\_finish\_reason': 'stop', 'generation\_info\_logprobs': None, 'flesch\_reading\_ease': 83.66, 'flesch\_kincaid\_grade': 4.8, 'smog\_index': 0.0, 'coleman\_liau\_index': 3.23, 'automated\_readability\_index': 3.9, 'dale\_chall\_readability\_score': 6.71, 'difficult\_words': 2, 'linsear\_write\_formula': 6.5, 'gunning\_fog': 8.28, 'text\_standard': '6th and 7th grade', 'fernandez\_huerta': 115.58, 'szigriszt\_pazos': 112.37, 'gutierrez\_polini': 54.83, 'crawford': 1.4, 'gulpease\_index': 72.1, 'osman': 100.17}  
 {'action': 'on\_llm\_end', 'token\_usage\_prompt\_tokens': 24, 'token\_usage\_completion\_tokens': 138, 'token\_usage\_total\_tokens': 162, 'model\_name': 'text-davinci-003', 'step': 4, 'starts': 2, 'ends': 2, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 0, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 2, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'text': '\n\nQ: What did the fish say when it hit the wall?\nA: Dam!', 'generation\_info\_finish\_reason': 'stop', 'generation\_info\_logprobs': None, 'flesch\_reading\_ease': 109.04, 'flesch\_kincaid\_grade': 1.3, 'smog\_index': 0.0, 'coleman\_liau\_index': -1.24, 'automated\_readability\_index': 0.3, 'dale\_chall\_readability\_score': 5.5, 'difficult\_words': 0, 'linsear\_write\_formula': 5.5, 'gunning\_fog': 5.2, 'text\_standard': '5th and 6th grade', 'fernandez\_huerta': 133.58, 'szigriszt\_pazos': 131.54, 'gutierrez\_polini': 62.3, 'crawford': -0.2, 'gulpease\_index': 79.8, 'osman': 116.91}  
 {'action': 'on\_llm\_end', 'token\_usage\_prompt\_tokens': 24, 'token\_usage\_completion\_tokens': 138, 'token\_usage\_total\_tokens': 162, 'model\_name': 'text-davinci-003', 'step': 4, 'starts': 2, 'ends': 2, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 0, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 2, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'text': '\n\nRoses are red,\nViolets are blue,\nSugar is sweet,\nAnd so are you.', 'generation\_info\_finish\_reason': 'stop', 'generation\_info\_logprobs': None, 'flesch\_reading\_ease': 83.66, 'flesch\_kincaid\_grade': 4.8, 'smog\_index': 0.0, 'coleman\_liau\_index': 3.23, 'automated\_readability\_index': 3.9, 'dale\_chall\_readability\_score': 6.71, 'difficult\_words': 2, 'linsear\_write\_formula': 6.5, 'gunning\_fog': 8.28, 'text\_standard': '6th and 7th grade', 'fernandez\_huerta': 115.58, 'szigriszt\_pazos': 112.37, 'gutierrez\_polini': 54.83, 'crawford': 1.4, 'gulpease\_index': 72.1, 'osman': 100.17}  
 {'action': 'on\_llm\_end', 'token\_usage\_prompt\_tokens': 24, 'token\_usage\_completion\_tokens': 138, 'token\_usage\_total\_tokens': 162, 'model\_name': 'text-davinci-003', 'step': 4, 'starts': 2, 'ends': 2, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 0, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 2, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'text': '\n\nQ: What did the fish say when it hit the wall?\nA: Dam!', 'generation\_info\_finish\_reason': 'stop', 'generation\_info\_logprobs': None, 'flesch\_reading\_ease': 109.04, 'flesch\_kincaid\_grade': 1.3, 'smog\_index': 0.0, 'coleman\_liau\_index': -1.24, 'automated\_readability\_index': 0.3, 'dale\_chall\_readability\_score': 5.5, 'difficult\_words': 0, 'linsear\_write\_formula': 5.5, 'gunning\_fog': 5.2, 'text\_standard': '5th and 6th grade', 'fernandez\_huerta': 133.58, 'szigriszt\_pazos': 131.54, 'gutierrez\_polini': 62.3, 'crawford': -0.2, 'gulpease\_index': 79.8, 'osman': 116.91}  
 {'action': 'on\_llm\_end', 'token\_usage\_prompt\_tokens': 24, 'token\_usage\_completion\_tokens': 138, 'token\_usage\_total\_tokens': 162, 'model\_name': 'text-davinci-003', 'step': 4, 'starts': 2, 'ends': 2, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 0, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 2, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'text': '\n\nRoses are red,\nViolets are blue,\nSugar is sweet,\nAnd so are you.', 'generation\_info\_finish\_reason': 'stop', 'generation\_info\_logprobs': None, 'flesch\_reading\_ease': 83.66, 'flesch\_kincaid\_grade': 4.8, 'smog\_index': 0.0, 'coleman\_liau\_index': 3.23, 'automated\_readability\_index': 3.9, 'dale\_chall\_readability\_score': 6.71, 'difficult\_words': 2, 'linsear\_write\_formula': 6.5, 'gunning\_fog': 8.28, 'text\_standard': '6th and 7th grade', 'fernandez\_huerta': 115.58, 'szigriszt\_pazos': 112.37, 'gutierrez\_polini': 54.83, 'crawford': 1.4, 'gulpease\_index': 72.1, 'osman': 100.17}  
 {'action\_records': action name step starts ends errors text\_ctr chain\_starts \  
 0 on\_llm\_start OpenAI 1 1 0 0 0 0   
 1 on\_llm\_start OpenAI 1 1 0 0 0 0   
 2 on\_llm\_start OpenAI 1 1 0 0 0 0   
 3 on\_llm\_start OpenAI 1 1 0 0 0 0   
 4 on\_llm\_start OpenAI 1 1 0 0 0 0   
 5 on\_llm\_start OpenAI 1 1 0 0 0 0   
 6 on\_llm\_end NaN 2 1 1 0 0 0   
 7 on\_llm\_end NaN 2 1 1 0 0 0   
 8 on\_llm\_end NaN 2 1 1 0 0 0   
 9 on\_llm\_end NaN 2 1 1 0 0 0   
 10 on\_llm\_end NaN 2 1 1 0 0 0   
 11 on\_llm\_end NaN 2 1 1 0 0 0   
 12 on\_llm\_start OpenAI 3 2 1 0 0 0   
 13 on\_llm\_start OpenAI 3 2 1 0 0 0   
 14 on\_llm\_start OpenAI 3 2 1 0 0 0   
 15 on\_llm\_start OpenAI 3 2 1 0 0 0   
 16 on\_llm\_start OpenAI 3 2 1 0 0 0   
 17 on\_llm\_start OpenAI 3 2 1 0 0 0   
 18 on\_llm\_end NaN 4 2 2 0 0 0   
 19 on\_llm\_end NaN 4 2 2 0 0 0   
 20 on\_llm\_end NaN 4 2 2 0 0 0   
 21 on\_llm\_end NaN 4 2 2 0 0 0   
 22 on\_llm\_end NaN 4 2 2 0 0 0   
 23 on\_llm\_end NaN 4 2 2 0 0 0   
   
 chain\_ends llm\_starts ... difficult\_words linsear\_write\_formula \  
 0 0 1 ... NaN NaN   
 1 0 1 ... NaN NaN   
 2 0 1 ... NaN NaN   
 3 0 1 ... NaN NaN   
 4 0 1 ... NaN NaN   
 5 0 1 ... NaN NaN   
 6 0 1 ... 0.0 5.5   
 7 0 1 ... 2.0 6.5   
 8 0 1 ... 0.0 5.5   
 9 0 1 ... 2.0 6.5   
 10 0 1 ... 0.0 5.5   
 11 0 1 ... 2.0 6.5   
 12 0 2 ... NaN NaN   
 13 0 2 ... NaN NaN   
 14 0 2 ... NaN NaN   
 15 0 2 ... NaN NaN   
 16 0 2 ... NaN NaN   
 17 0 2 ... NaN NaN   
 18 0 2 ... 0.0 5.5   
 19 0 2 ... 2.0 6.5   
 20 0 2 ... 0.0 5.5   
 21 0 2 ... 2.0 6.5   
 22 0 2 ... 0.0 5.5   
 23 0 2 ... 2.0 6.5   
   
 gunning\_fog text\_standard fernandez\_huerta szigriszt\_pazos \  
 0 NaN NaN NaN NaN   
 1 NaN NaN NaN NaN   
 2 NaN NaN NaN NaN   
 3 NaN NaN NaN NaN   
 4 NaN NaN NaN NaN   
 5 NaN NaN NaN NaN   
 6 5.20 5th and 6th grade 133.58 131.54   
 7 8.28 6th and 7th grade 115.58 112.37   
 8 5.20 5th and 6th grade 133.58 131.54   
 9 8.28 6th and 7th grade 115.58 112.37   
 10 5.20 5th and 6th grade 133.58 131.54   
 11 8.28 6th and 7th grade 115.58 112.37   
 12 NaN NaN NaN NaN   
 13 NaN NaN NaN NaN   
 14 NaN NaN NaN NaN   
 15 NaN NaN NaN NaN   
 16 NaN NaN NaN NaN   
 17 NaN NaN NaN NaN   
 18 5.20 5th and 6th grade 133.58 131.54   
 19 8.28 6th and 7th grade 115.58 112.37   
 20 5.20 5th and 6th grade 133.58 131.54   
 21 8.28 6th and 7th grade 115.58 112.37   
 22 5.20 5th and 6th grade 133.58 131.54   
 23 8.28 6th and 7th grade 115.58 112.37   
   
 gutierrez\_polini crawford gulpease\_index osman   
 0 NaN NaN NaN NaN   
 1 NaN NaN NaN NaN   
 2 NaN NaN NaN NaN   
 3 NaN NaN NaN NaN   
 4 NaN NaN NaN NaN   
 5 NaN NaN NaN NaN   
 6 62.30 -0.2 79.8 116.91   
 7 54.83 1.4 72.1 100.17   
 8 62.30 -0.2 79.8 116.91   
 9 54.83 1.4 72.1 100.17   
 10 62.30 -0.2 79.8 116.91   
 11 54.83 1.4 72.1 100.17   
 12 NaN NaN NaN NaN   
 13 NaN NaN NaN NaN   
 14 NaN NaN NaN NaN   
 15 NaN NaN NaN NaN   
 16 NaN NaN NaN NaN   
 17 NaN NaN NaN NaN   
 18 62.30 -0.2 79.8 116.91   
 19 54.83 1.4 72.1 100.17   
 20 62.30 -0.2 79.8 116.91   
 21 54.83 1.4 72.1 100.17   
 22 62.30 -0.2 79.8 116.91   
 23 54.83 1.4 72.1 100.17   
   
 [24 rows x 39 columns], 'session\_analysis': prompt\_step prompts name output\_step \  
 0 1 Tell me a joke OpenAI 2   
 1 1 Tell me a poem OpenAI 2   
 2 1 Tell me a joke OpenAI 2   
 3 1 Tell me a poem OpenAI 2   
 4 1 Tell me a joke OpenAI 2   
 5 1 Tell me a poem OpenAI 2   
 6 3 Tell me a joke OpenAI 4   
 7 3 Tell me a poem OpenAI 4   
 8 3 Tell me a joke OpenAI 4   
 9 3 Tell me a poem OpenAI 4   
 10 3 Tell me a joke OpenAI 4   
 11 3 Tell me a poem OpenAI 4   
   
 output \  
 0 \n\nQ: What did the fish say when it hit the w...   
 1 \n\nRoses are red,\nViolets are blue,\nSugar i...   
 2 \n\nQ: What did the fish say when it hit the w...   
 3 \n\nRoses are red,\nViolets are blue,\nSugar i...   
 4 \n\nQ: What did the fish say when it hit the w...   
 5 \n\nRoses are red,\nViolets are blue,\nSugar i...   
 6 \n\nQ: What did the fish say when it hit the w...   
 7 \n\nRoses are red,\nViolets are blue,\nSugar i...   
 8 \n\nQ: What did the fish say when it hit the w...   
 9 \n\nRoses are red,\nViolets are blue,\nSugar i...   
 10 \n\nQ: What did the fish say when it hit the w...   
 11 \n\nRoses are red,\nViolets are blue,\nSugar i...   
   
 token\_usage\_total\_tokens token\_usage\_prompt\_tokens \  
 0 162 24   
 1 162 24   
 2 162 24   
 3 162 24   
 4 162 24   
 5 162 24   
 6 162 24   
 7 162 24   
 8 162 24   
 9 162 24   
 10 162 24   
 11 162 24   
   
 token\_usage\_completion\_tokens flesch\_reading\_ease flesch\_kincaid\_grade \  
 0 138 109.04 1.3   
 1 138 83.66 4.8   
 2 138 109.04 1.3   
 3 138 83.66 4.8   
 4 138 109.04 1.3   
 5 138 83.66 4.8   
 6 138 109.04 1.3   
 7 138 83.66 4.8   
 8 138 109.04 1.3   
 9 138 83.66 4.8   
 10 138 109.04 1.3   
 11 138 83.66 4.8   
   
 ... difficult\_words linsear\_write\_formula gunning\_fog \  
 0 ... 0 5.5 5.20   
 1 ... 2 6.5 8.28   
 2 ... 0 5.5 5.20   
 3 ... 2 6.5 8.28   
 4 ... 0 5.5 5.20   
 5 ... 2 6.5 8.28   
 6 ... 0 5.5 5.20   
 7 ... 2 6.5 8.28   
 8 ... 0 5.5 5.20   
 9 ... 2 6.5 8.28   
 10 ... 0 5.5 5.20   
 11 ... 2 6.5 8.28   
   
 text\_standard fernandez\_huerta szigriszt\_pazos gutierrez\_polini \  
 0 5th and 6th grade 133.58 131.54 62.30   
 1 6th and 7th grade 115.58 112.37 54.83   
 2 5th and 6th grade 133.58 131.54 62.30   
 3 6th and 7th grade 115.58 112.37 54.83   
 4 5th and 6th grade 133.58 131.54 62.30   
 5 6th and 7th grade 115.58 112.37 54.83   
 6 5th and 6th grade 133.58 131.54 62.30   
 7 6th and 7th grade 115.58 112.37 54.83   
 8 5th and 6th grade 133.58 131.54 62.30   
 9 6th and 7th grade 115.58 112.37 54.83   
 10 5th and 6th grade 133.58 131.54 62.30   
 11 6th and 7th grade 115.58 112.37 54.83   
   
 crawford gulpease\_index osman   
 0 -0.2 79.8 116.91   
 1 1.4 72.1 100.17   
 2 -0.2 79.8 116.91   
 3 1.4 72.1 100.17   
 4 -0.2 79.8 116.91   
 5 1.4 72.1 100.17   
 6 -0.2 79.8 116.91   
 7 1.4 72.1 100.17   
 8 -0.2 79.8 116.91   
 9 1.4 72.1 100.17   
 10 -0.2 79.8 116.91   
 11 1.4 72.1 100.17   
   
 [12 rows x 24 columns]}  
 2023-03-29 14:00:25,948 - clearml.Task - INFO - Completed model upload to https://files.clear.ml/langchain\_callback\_demo/llm.988bd727b0e94a29a3ac0ee526813545/models/simple\_sequential  

```

At this point you can already go to <https://app.clear.ml> and take a look at the resulting ClearML Task that was created.

Among others, you should see that this notebook is saved along with any git information. The model JSON that contains the used parameters is saved as an artifact, there are also console logs and under the plots section, you'll find tables that represent the flow of the chain.

Finally, if you enabled visualizations, these are stored as HTML files under debug samples.

### Scenario 2: Creating an agent with tools[​](#scenario-2-creating-an-agent-with-tools "Direct link to Scenario 2: Creating an agent with tools")

To show a more advanced workflow, let's create an agent with access to tools. The way ClearML tracks the results is not different though, only the table will look slightly different as there are other types of actions taken when compared to the earlier, simpler example.

You can now also see the use of the `finish=True` keyword, which will fully close the ClearML Task, instead of just resetting the parameters and prompts for a new conversation.

```python
from langchain.agents import initialize\_agent, load\_tools  
from langchain.agents import AgentType  
  
# SCENARIO 2 - Agent with Tools  
tools = load\_tools(["serpapi", "llm-math"], llm=llm, callbacks=callbacks)  
agent = initialize\_agent(  
 tools,  
 llm,  
 agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION,  
 callbacks=callbacks,  
)  
agent.run("Who is the wife of the person who sang summer of 69?")  
clearml\_callback.flush\_tracker(  
 langchain\_asset=agent, name="Agent with Tools", finish=True  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 {'action': 'on\_chain\_start', 'name': 'AgentExecutor', 'step': 1, 'starts': 1, 'ends': 0, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 0, 'llm\_ends': 0, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'input': 'Who is the wife of the person who sang summer of 69?'}  
 {'action': 'on\_llm\_start', 'name': 'OpenAI', 'step': 2, 'starts': 2, 'ends': 0, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 1, 'llm\_ends': 0, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'prompts': 'Answer the following questions as best you can. You have access to the following tools:\n\nSearch: A search engine. Useful for when you need to answer questions about current events. Input should be a search query.\nCalculator: Useful for when you need to answer questions about math.\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [Search, Calculator]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\n\nQuestion: Who is the wife of the person who sang summer of 69?\nThought:'}  
 {'action': 'on\_llm\_end', 'token\_usage\_prompt\_tokens': 189, 'token\_usage\_completion\_tokens': 34, 'token\_usage\_total\_tokens': 223, 'model\_name': 'text-davinci-003', 'step': 3, 'starts': 2, 'ends': 1, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 1, 'llm\_ends': 1, 'llm\_streams': 0, 'tool\_starts': 0, 'tool\_ends': 0, 'agent\_ends': 0, 'text': ' I need to find out who sang summer of 69 and then find out who their wife is.\nAction: Search\nAction Input: "Who sang summer of 69"', 'generation\_info\_finish\_reason': 'stop', 'generation\_info\_logprobs': None, 'flesch\_reading\_ease': 91.61, 'flesch\_kincaid\_grade': 3.8, 'smog\_index': 0.0, 'coleman\_liau\_index': 3.41, 'automated\_readability\_index': 3.5, 'dale\_chall\_readability\_score': 6.06, 'difficult\_words': 2, 'linsear\_write\_formula': 5.75, 'gunning\_fog': 5.4, 'text\_standard': '3rd and 4th grade', 'fernandez\_huerta': 121.07, 'szigriszt\_pazos': 119.5, 'gutierrez\_polini': 54.91, 'crawford': 0.9, 'gulpease\_index': 72.7, 'osman': 92.16}  
 I need to find out who sang summer of 69 and then find out who their wife is.  
 Action: Search  
 Action Input: "Who sang summer of 69"{'action': 'on\_agent\_action', 'tool': 'Search', 'tool\_input': 'Who sang summer of 69', 'log': ' I need to find out who sang summer of 69 and then find out who their wife is.\nAction: Search\nAction Input: "Who sang summer of 69"', 'step': 4, 'starts': 3, 'ends': 1, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 1, 'llm\_ends': 1, 'llm\_streams': 0, 'tool\_starts': 1, 'tool\_ends': 0, 'agent\_ends': 0}  
 {'action': 'on\_tool\_start', 'input\_str': 'Who sang summer of 69', 'name': 'Search', 'description': 'A search engine. Useful for when you need to answer questions about current events. Input should be a search query.', 'step': 5, 'starts': 4, 'ends': 1, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 1, 'llm\_ends': 1, 'llm\_streams': 0, 'tool\_starts': 2, 'tool\_ends': 0, 'agent\_ends': 0}  
   
 Observation: Bryan Adams - Summer Of 69 (Official Music Video).  
 Thought:{'action': 'on\_tool\_end', 'output': 'Bryan Adams - Summer Of 69 (Official Music Video).', 'step': 6, 'starts': 4, 'ends': 2, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 1, 'llm\_ends': 1, 'llm\_streams': 0, 'tool\_starts': 2, 'tool\_ends': 1, 'agent\_ends': 0}  
 {'action': 'on\_llm\_start', 'name': 'OpenAI', 'step': 7, 'starts': 5, 'ends': 2, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 1, 'llm\_streams': 0, 'tool\_starts': 2, 'tool\_ends': 1, 'agent\_ends': 0, 'prompts': 'Answer the following questions as best you can. You have access to the following tools:\n\nSearch: A search engine. Useful for when you need to answer questions about current events. Input should be a search query.\nCalculator: Useful for when you need to answer questions about math.\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [Search, Calculator]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\n\nQuestion: Who is the wife of the person who sang summer of 69?\nThought: I need to find out who sang summer of 69 and then find out who their wife is.\nAction: Search\nAction Input: "Who sang summer of 69"\nObservation: Bryan Adams - Summer Of 69 (Official Music Video).\nThought:'}  
 {'action': 'on\_llm\_end', 'token\_usage\_prompt\_tokens': 242, 'token\_usage\_completion\_tokens': 28, 'token\_usage\_total\_tokens': 270, 'model\_name': 'text-davinci-003', 'step': 8, 'starts': 5, 'ends': 3, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 2, 'llm\_streams': 0, 'tool\_starts': 2, 'tool\_ends': 1, 'agent\_ends': 0, 'text': ' I need to find out who Bryan Adams is married to.\nAction: Search\nAction Input: "Who is Bryan Adams married to"', 'generation\_info\_finish\_reason': 'stop', 'generation\_info\_logprobs': None, 'flesch\_reading\_ease': 94.66, 'flesch\_kincaid\_grade': 2.7, 'smog\_index': 0.0, 'coleman\_liau\_index': 4.73, 'automated\_readability\_index': 4.0, 'dale\_chall\_readability\_score': 7.16, 'difficult\_words': 2, 'linsear\_write\_formula': 4.25, 'gunning\_fog': 4.2, 'text\_standard': '4th and 5th grade', 'fernandez\_huerta': 124.13, 'szigriszt\_pazos': 119.2, 'gutierrez\_polini': 52.26, 'crawford': 0.7, 'gulpease\_index': 74.7, 'osman': 84.2}  
 I need to find out who Bryan Adams is married to.  
 Action: Search  
 Action Input: "Who is Bryan Adams married to"{'action': 'on\_agent\_action', 'tool': 'Search', 'tool\_input': 'Who is Bryan Adams married to', 'log': ' I need to find out who Bryan Adams is married to.\nAction: Search\nAction Input: "Who is Bryan Adams married to"', 'step': 9, 'starts': 6, 'ends': 3, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 2, 'llm\_streams': 0, 'tool\_starts': 3, 'tool\_ends': 1, 'agent\_ends': 0}  
 {'action': 'on\_tool\_start', 'input\_str': 'Who is Bryan Adams married to', 'name': 'Search', 'description': 'A search engine. Useful for when you need to answer questions about current events. Input should be a search query.', 'step': 10, 'starts': 7, 'ends': 3, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 2, 'llm\_streams': 0, 'tool\_starts': 4, 'tool\_ends': 1, 'agent\_ends': 0}  
   
 Observation: Bryan Adams has never married. In the 1990s, he was in a relationship with Danish model Cecilie Thomsen. In 2011, Bryan and Alicia Grimaldi, his ...  
 Thought:{'action': 'on\_tool\_end', 'output': 'Bryan Adams has never married. In the 1990s, he was in a relationship with Danish model Cecilie Thomsen. In 2011, Bryan and Alicia Grimaldi, his ...', 'step': 11, 'starts': 7, 'ends': 4, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 2, 'llm\_ends': 2, 'llm\_streams': 0, 'tool\_starts': 4, 'tool\_ends': 2, 'agent\_ends': 0}  
 {'action': 'on\_llm\_start', 'name': 'OpenAI', 'step': 12, 'starts': 8, 'ends': 4, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 3, 'llm\_ends': 2, 'llm\_streams': 0, 'tool\_starts': 4, 'tool\_ends': 2, 'agent\_ends': 0, 'prompts': 'Answer the following questions as best you can. You have access to the following tools:\n\nSearch: A search engine. Useful for when you need to answer questions about current events. Input should be a search query.\nCalculator: Useful for when you need to answer questions about math.\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [Search, Calculator]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\n\nQuestion: Who is the wife of the person who sang summer of 69?\nThought: I need to find out who sang summer of 69 and then find out who their wife is.\nAction: Search\nAction Input: "Who sang summer of 69"\nObservation: Bryan Adams - Summer Of 69 (Official Music Video).\nThought: I need to find out who Bryan Adams is married to.\nAction: Search\nAction Input: "Who is Bryan Adams married to"\nObservation: Bryan Adams has never married. In the 1990s, he was in a relationship with Danish model Cecilie Thomsen. In 2011, Bryan and Alicia Grimaldi, his ...\nThought:'}  
 {'action': 'on\_llm\_end', 'token\_usage\_prompt\_tokens': 314, 'token\_usage\_completion\_tokens': 18, 'token\_usage\_total\_tokens': 332, 'model\_name': 'text-davinci-003', 'step': 13, 'starts': 8, 'ends': 5, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 3, 'llm\_ends': 3, 'llm\_streams': 0, 'tool\_starts': 4, 'tool\_ends': 2, 'agent\_ends': 0, 'text': ' I now know the final answer.\nFinal Answer: Bryan Adams has never been married.', 'generation\_info\_finish\_reason': 'stop', 'generation\_info\_logprobs': None, 'flesch\_reading\_ease': 81.29, 'flesch\_kincaid\_grade': 3.7, 'smog\_index': 0.0, 'coleman\_liau\_index': 5.75, 'automated\_readability\_index': 3.9, 'dale\_chall\_readability\_score': 7.37, 'difficult\_words': 1, 'linsear\_write\_formula': 2.5, 'gunning\_fog': 2.8, 'text\_standard': '3rd and 4th grade', 'fernandez\_huerta': 115.7, 'szigriszt\_pazos': 110.84, 'gutierrez\_polini': 49.79, 'crawford': 0.7, 'gulpease\_index': 85.4, 'osman': 83.14}  
 I now know the final answer.  
 Final Answer: Bryan Adams has never been married.  
 {'action': 'on\_agent\_finish', 'output': 'Bryan Adams has never been married.', 'log': ' I now know the final answer.\nFinal Answer: Bryan Adams has never been married.', 'step': 14, 'starts': 8, 'ends': 6, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 0, 'llm\_starts': 3, 'llm\_ends': 3, 'llm\_streams': 0, 'tool\_starts': 4, 'tool\_ends': 2, 'agent\_ends': 1}  
   
 > Finished chain.  
 {'action': 'on\_chain\_end', 'outputs': 'Bryan Adams has never been married.', 'step': 15, 'starts': 8, 'ends': 7, 'errors': 0, 'text\_ctr': 0, 'chain\_starts': 1, 'chain\_ends': 1, 'llm\_starts': 3, 'llm\_ends': 3, 'llm\_streams': 0, 'tool\_starts': 4, 'tool\_ends': 2, 'agent\_ends': 1}  
 {'action\_records': action name step starts ends errors text\_ctr \  
 0 on\_llm\_start OpenAI 1 1 0 0 0   
 1 on\_llm\_start OpenAI 1 1 0 0 0   
 2 on\_llm\_start OpenAI 1 1 0 0 0   
 3 on\_llm\_start OpenAI 1 1 0 0 0   
 4 on\_llm\_start OpenAI 1 1 0 0 0   
 .. ... ... ... ... ... ... ...   
 66 on\_tool\_end NaN 11 7 4 0 0   
 67 on\_llm\_start OpenAI 12 8 4 0 0   
 68 on\_llm\_end NaN 13 8 5 0 0   
 69 on\_agent\_finish NaN 14 8 6 0 0   
 70 on\_chain\_end NaN 15 8 7 0 0   
   
 chain\_starts chain\_ends llm\_starts ... gulpease\_index osman input \  
 0 0 0 1 ... NaN NaN NaN   
 1 0 0 1 ... NaN NaN NaN   
 2 0 0 1 ... NaN NaN NaN   
 3 0 0 1 ... NaN NaN NaN   
 4 0 0 1 ... NaN NaN NaN   
 .. ... ... ... ... ... ... ...   
 66 1 0 2 ... NaN NaN NaN   
 67 1 0 3 ... NaN NaN NaN   
 68 1 0 3 ... 85.4 83.14 NaN   
 69 1 0 3 ... NaN NaN NaN   
 70 1 1 3 ... NaN NaN NaN   
   
 tool tool\_input log \  
 0 NaN NaN NaN   
 1 NaN NaN NaN   
 2 NaN NaN NaN   
 3 NaN NaN NaN   
 4 NaN NaN NaN   
 .. ... ... ...   
 66 NaN NaN NaN   
 67 NaN NaN NaN   
 68 NaN NaN NaN   
 69 NaN NaN I now know the final answer.\nFinal Answer: B...   
 70 NaN NaN NaN   
   
 input\_str description output \  
 0 NaN NaN NaN   
 1 NaN NaN NaN   
 2 NaN NaN NaN   
 3 NaN NaN NaN   
 4 NaN NaN NaN   
 .. ... ... ...   
 66 NaN NaN Bryan Adams has never married. In the 1990s, h...   
 67 NaN NaN NaN   
 68 NaN NaN NaN   
 69 NaN NaN Bryan Adams has never been married.   
 70 NaN NaN NaN   
   
 outputs   
 0 NaN   
 1 NaN   
 2 NaN   
 3 NaN   
 4 NaN   
 .. ...   
 66 NaN   
 67 NaN   
 68 NaN   
 69 NaN   
 70 Bryan Adams has never been married.   
   
 [71 rows x 47 columns], 'session\_analysis': prompt\_step prompts name \  
 0 2 Answer the following questions as best you can... OpenAI   
 1 7 Answer the following questions as best you can... OpenAI   
 2 12 Answer the following questions as best you can... OpenAI   
   
 output\_step output \  
 0 3 I need to find out who sang summer of 69 and ...   
 1 8 I need to find out who Bryan Adams is married...   
 2 13 I now know the final answer.\nFinal Answer: B...   
   
 token\_usage\_total\_tokens token\_usage\_prompt\_tokens \  
 0 223 189   
 1 270 242   
 2 332 314   
   
 token\_usage\_completion\_tokens flesch\_reading\_ease flesch\_kincaid\_grade \  
 0 34 91.61 3.8   
 1 28 94.66 2.7   
 2 18 81.29 3.7   
   
 ... difficult\_words linsear\_write\_formula gunning\_fog \  
 0 ... 2 5.75 5.4   
 1 ... 2 4.25 4.2   
 2 ... 1 2.50 2.8   
   
 text\_standard fernandez\_huerta szigriszt\_pazos gutierrez\_polini \  
 0 3rd and 4th grade 121.07 119.50 54.91   
 1 4th and 5th grade 124.13 119.20 52.26   
 2 3rd and 4th grade 115.70 110.84 49.79   
   
 crawford gulpease\_index osman   
 0 0.9 72.7 92.16   
 1 0.7 74.7 84.20   
 2 0.7 85.4 83.14   
   
 [3 rows x 24 columns]}  
  
  
 Could not update last created model in Task 988bd727b0e94a29a3ac0ee526813545, Task status 'completed' cannot be updated  

```

### Tips and Next Steps[​](#tips-and-next-steps "Direct link to Tips and Next Steps")

- Make sure you always use a unique `name` argument for the `clearml_callback.flush_tracker` function. If not, the model parameters used for a run will override the previous run!
- If you close the ClearML Callback using `clearml_callback.flush_tracker(..., finish=True)` the Callback cannot be used anymore. Make a new one if you want to keep logging.
- Check out the rest of the open-source ClearML ecosystem, there is a data version manager, a remote execution agent, automated pipelines and much more!

Make sure you always use a unique `name` argument for the `clearml_callback.flush_tracker` function. If not, the model parameters used for a run will override the previous run!

If you close the ClearML Callback using `clearml_callback.flush_tracker(..., finish=True)` the Callback cannot be used anymore. Make a new one if you want to keep logging.

Check out the rest of the open-source ClearML ecosystem, there is a data version manager, a remote execution agent, automated pipelines and much more!

- [Installation and Setup](#installation-and-setup)

  - [Getting API Credentials](#getting-api-credentials)

- [Callbacks](#callbacks)

  - [Scenario 1: Just an LLM](#scenario-1-just-an-llm)
  - [Scenario 2: Creating an agent with tools](#scenario-2-creating-an-agent-with-tools)
  - [Tips and Next Steps](#tips-and-next-steps)

- [Getting API Credentials](#getting-api-credentials)

- [Scenario 1: Just an LLM](#scenario-1-just-an-llm)

- [Scenario 2: Creating an agent with tools](#scenario-2-creating-an-agent-with-tools)

- [Tips and Next Steps](#tips-and-next-steps)
