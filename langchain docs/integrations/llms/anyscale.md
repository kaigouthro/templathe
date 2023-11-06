# Anyscale

[Anyscale](https://www.anyscale.com/) is a fully-managed [Ray](https://www.ray.io/) platform, on which you can build, deploy, and manage scalable AI and Python applications

This example goes over how to use LangChain to interact with [Anyscale Endpoint](https://app.endpoints.anyscale.com/).

```python
import os  
  
os.environ["ANYSCALE\_API\_BASE"] = ANYSCALE\_API\_BASE  
os.environ["ANYSCALE\_API\_KEY"] = ANYSCALE\_API\_KEY  

```

```python
from langchain.llms import Anyscale  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

```python
llm = Anyscale(model\_name=ANYSCALE\_MODEL\_NAME)  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
question = "When was George Washington president?"  
  
llm\_chain.run(question)  

```

With Ray, we can distribute the queries without asynchronized implementation. This not only applies to Anyscale LLM model, but to any other Langchain LLM models which do not have `_acall` or `_agenerate` implemented

```python
prompt\_list = [  
 "When was George Washington president?",  
 "Explain to me the difference between nuclear fission and fusion.",  
 "Give me a list of 5 science fiction books I should read next.",  
 "Explain the difference between Spark and Ray.",  
 "Suggest some fun holiday ideas.",  
 "Tell a joke.",  
 "What is 2+2?",  
 "Explain what is machine learning like I am five years old.",  
 "Explain what is artifical intelligence.",  
]  

```

```python
import ray  
  
@ray.remote(num\_cpus=0.1)  
def send\_query(llm, prompt):  
 resp = llm(prompt)  
 return resp  
  
futures = [send\_query.remote(llm, prompt) for prompt in prompt\_list]  
results = ray.get(futures)  

```
