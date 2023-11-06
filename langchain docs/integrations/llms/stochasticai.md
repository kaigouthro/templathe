# StochasticAI

[Stochastic Acceleration Platform](https://docs.stochastic.ai/docs/introduction/) aims to simplify the life cycle of a Deep Learning model. From uploading and versioning the model, through training, compression and acceleration to putting it into production.

This example goes over how to use LangChain to interact with `StochasticAI` models.

You have to get the API_KEY and the API_URL [here](https://app.stochastic.ai/workspace/profile/settings?tab=profile).

```python
from getpass import getpass  
  
STOCHASTICAI\_API\_KEY = getpass()  

```

```text
 ········  

```

```python
import os  
  
os.environ["STOCHASTICAI\_API\_KEY"] = STOCHASTICAI\_API\_KEY  

```

```python
YOUR\_API\_URL = getpass()  

```

```text
 ········  

```

```python
from langchain.llms import StochasticAI  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

```python
llm = StochasticAI(api\_url=YOUR\_API\_URL)  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"  
  
llm\_chain.run(question)  

```

```text
 "\n\nStep 1: In 1999, the St. Louis Rams won the Super Bowl.\n\nStep 2: In 1999, Beiber was born.\n\nStep 3: The Rams were in Los Angeles at the time.\n\nStep 4: So they didn't play in the Super Bowl that year.\n"  

```
