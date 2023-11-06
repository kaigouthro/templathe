# Google Cloud Vertex AI

**Note:** This is separate from the `Google PaLM` integration, it exposes [Vertex AI PaLM API](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/overview) on `Google Cloud`.

## Setting up[​](#setting-up "Direct link to Setting up")

By default, Google Cloud [does not use](https://cloud.google.com/vertex-ai/docs/generative-ai/data-governance#foundation_model_development) customer data to train its foundation models as part of Google Cloud's AI/ML Privacy Commitment. More details about how Google processes data can also be found in [Google's Customer Data Processing Addendum (CDPA)](https://cloud.google.com/terms/data-processing-addendum).

To use `Vertex AI PaLM` you must have the `google-cloud-aiplatform` Python package installed and either:

- Have credentials configured for your environment (gcloud, workload identity, etc...)
- Store the path to a service account JSON file as the GOOGLE_APPLICATION_CREDENTIALS environment variable

This codebase uses the `google.auth` library which first looks for the application credentials variable mentioned above, and then looks for system-level auth.

For more information, see:

- <https://cloud.google.com/docs/authentication/application-default-credentials#GAC>
- <https://googleapis.dev/python/google-auth/latest/reference/google.auth.html#module-google.auth>

```python
#!pip install langchain google-cloud-aiplatform  

```

```python
from langchain.llms import VertexAI  

```

```python
llm = VertexAI()  
print(llm("What are some of the pros and cons of Python as a programming language?"))  

```

```text
 Python is a widely used, interpreted, object-oriented, and high-level programming language with dynamic semantics, used for general-purpose programming. It is known for its readability, simplicity, and versatility. Here are some of the pros and cons of Python:  
   
 \*\*Pros:\*\*  
   
 - \*\*Easy to learn:\*\* Python is known for its simple and intuitive syntax, making it easy for beginners to learn. It has a relatively shallow learning curve compared to other programming languages.  
   
 - \*\*Versatile:\*\* Python is a general-purpose programming language, meaning it can be used for a wide variety of tasks, including web development, data science, machine  

```

## Using in a chain[​](#using-in-a-chain "Direct link to Using in a chain")

```python
from langchain.prompts import PromptTemplate  

```

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
prompt = PromptTemplate.from\_template(template)  

```

```python
chain = prompt | llm  

```

```python
question = "Who was the president in the year Justin Beiber was born?"  
print(chain.invoke({"question": question}))  

```

```text
 Justin Bieber was born on March 1, 1994. Bill Clinton was the president of the United States from January 20, 1993, to January 20, 2001.  
 The final answer is Bill Clinton  

```

## Code generation example[​](#code-generation-example "Direct link to Code generation example")

You can now leverage the `Codey API` for code generation within `Vertex AI`.

The model names are:

- `code-bison`: for code suggestion
- `code-gecko`: for code completion

```python
llm = VertexAI(model\_name="code-bison", max\_output\_tokens=1000, temperature=0.3)  

```

```python
question = "Write a python function that checks if a string is a valid email address"  

```

```python
print(llm(question))  

```

````text
 ```python  
 import re  
   
 def is\_valid\_email(email):  
 pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")  
 return pattern.match(email)  
````

````


Full generation info[​](#full-generation-info "Direct link to Full generation info")
------------------------------------------------------------------------------------



We can use the `generate` method to get back extra metadata like [safety attributes](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/responsible-ai#safety_attribute_confidence_scoring) and not just text completions




```python
result = llm.generate([question])  
result.generations  

````

````text
 [[GenerationChunk(text='```python\nimport re\n\ndef is\_valid\_email(email):\n pattern = re.compile(r"[^@]+@[^@]+\\.[^@]+")\n return pattern.match(email)\n```', generation\_info={'is\_blocked': False, 'safety\_attributes': {'Health': 0.1}})]]  

````

## Asynchronous calls[​](#asynchronous-calls "Direct link to Asynchronous calls")

With `agenerate` we can make asynchronous calls

```python
# If running in a Jupyter notebook you'll need to install nest\_asyncio  
  
# !pip install nest\_asyncio  

```

```python
import asyncio  
# import nest\_asyncio  
# nest\_asyncio.apply()  

```

```python
asyncio.run(llm.agenerate([question]))  

```

````text
 LLMResult(generations=[[GenerationChunk(text='```python\nimport re\n\ndef is\_valid\_email(email):\n pattern = re.compile(r"[^@]+@[^@]+\\.[^@]+")\n return pattern.match(email)\n```', generation\_info={'is\_blocked': False, 'safety\_attributes': {'Health': 0.1}})]], llm\_output=None, run=[RunInfo(run\_id=UUID('caf74e91-aefb-48ac-8031-0c505fcbbcc6'))])  

````

## Streaming calls[​](#streaming-calls "Direct link to Streaming calls")

With `stream` we can stream results from the model

```python
import sys  

```

```python
for chunk in llm.stream(question):  
 sys.stdout.write(chunk)  
 sys.stdout.flush()  

```

````text
 ```python  
 import re  
   
 def is\_valid\_email(email):  
 """  
 Checks if a string is a valid email address.  
   
 Args:  
 email: The string to check.  
   
 Returns:  
 True if the string is a valid email address, False otherwise.  
 """  
   
 # Check for a valid email address format.  
 if not re.match(r"^[A-Za-z0-9\.\+\_-]+@[A-Za-z0-9\.\_-]+\.[a-zA-Z]\*$", email):  
 return False  
   
 # Check if the domain name exists.  
 try:  
 domain = email.split("@")[1]  
 socket.gethostbyname(domain)  
 except socket.gaierror:  
 return False  
   
 return True  
````

````


Vertex Model Garden[​](#vertex-model-garden "Direct link to Vertex Model Garden")
---------------------------------------------------------------------------------



Vertex Model Garden [exposes](https://cloud.google.com/vertex-ai/docs/start/explore-models) open-sourced models that can be deployed and served on Vertex AI. If you have successfully deployed a model from Vertex Model Garden, you can find a corresponding Vertex AI [endpoint](https://cloud.google.com/vertex-ai/docs/general/deployment#what_happens_when_you_deploy_a_model) in the console or via API.




```python
from langchain.llms import VertexAIModelGarden  

````

```python
llm = VertexAIModelGarden(  
 project="YOUR PROJECT",  
 endpoint\_id="YOUR ENDPOINT\_ID"  
)  

```

```python
print(llm("What is the meaning of life?"))  

```

Like all LLMs, we can then compose it with other components:

```python
prompt = PromptTemplate.from\_template("What is the meaning of {thing}?")  

```

```python
chian = prompt | llm  
print(chain.invoke({"thing": "life"}))  

```

- [Setting up](#setting-up)
- [Using in a chain](#using-in-a-chain)
- [Code generation example](#code-generation-example)
- [Full generation info](#full-generation-info)
- [Asynchronous calls](#asynchronous-calls)
- [Streaming calls](#streaming-calls)
- [Vertex Model Garden](#vertex-model-garden)
