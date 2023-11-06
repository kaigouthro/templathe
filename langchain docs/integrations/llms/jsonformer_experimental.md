# JSONFormer

[JSONFormer](https://github.com/1rgs/jsonformer) is a library that wraps local Hugging Face pipeline models for structured decoding of a subset of the JSON Schema.

It works by filling in the structure tokens and then sampling the content tokens from the model.

**Warning - this module is still experimental**

```bash
pip install --upgrade jsonformer > /dev/null  

```

### Hugging Face Baseline[​](#hugging-face-baseline "Direct link to Hugging Face Baseline")

First, let's establish a qualitative baseline by checking the output of the model without structured decoding.

```python
import logging  
  
logging.basicConfig(level=logging.ERROR)  

```

```python
from typing import Optional  
from langchain.tools import tool  
import os  
import json  
import requests  
  
HF\_TOKEN = os.environ.get("HUGGINGFACE\_API\_KEY")  
  
  
@tool  
def ask\_star\_coder(query: str, temperature: float = 1.0, max\_new\_tokens: float = 250):  
 """Query the BigCode StarCoder model about coding questions."""  
 url = "https://api-inference.huggingface.co/models/bigcode/starcoder"  
 headers = {  
 "Authorization": f"Bearer {HF\_TOKEN}",  
 "content-type": "application/json",  
 }  
 payload = {  
 "inputs": f"{query}\n\nAnswer:",  
 "temperature": temperature,  
 "max\_new\_tokens": int(max\_new\_tokens),  
 }  
 response = requests.post(url, headers=headers, data=json.dumps(payload))  
 response.raise\_for\_status()  
 return json.loads(response.content.decode("utf-8"))  

```

```python
prompt = """You must respond using JSON format, with a single action and single action input.  
You may 'ask\_star\_coder' for help on coding problems.  
  
{arg\_schema}  
  
EXAMPLES  
----  
Human: "So what's all this about a GIL?"  
AI Assistant:{{  
 "action": "ask\_star\_coder",  
 "action\_input": {{"query": "What is a GIL?", "temperature": 0.0, "max\_new\_tokens": 100}}"  
}}  
Observation: "The GIL is python's Global Interpreter Lock"  
Human: "Could you please write a calculator program in LISP?"  
AI Assistant:{{  
 "action": "ask\_star\_coder",  
 "action\_input": {{"query": "Write a calculator program in LISP", "temperature": 0.0, "max\_new\_tokens": 250}}  
}}  
Observation: "(defun add (x y) (+ x y))\n(defun sub (x y) (- x y ))"  
Human: "What's the difference between an SVM and an LLM?"  
AI Assistant:{{  
 "action": "ask\_star\_coder",  
 "action\_input": {{"query": "What's the difference between SGD and an SVM?", "temperature": 1.0, "max\_new\_tokens": 250}}  
}}  
Observation: "SGD stands for stochastic gradient descent, while an SVM is a Support Vector Machine."  
  
BEGIN! Answer the Human's question as best as you are able.  
------  
Human: 'What's the difference between an iterator and an iterable?'  
AI Assistant:""".format(  
 arg\_schema=ask\_star\_coder.args  
)  

```

```python
from transformers import pipeline  
from langchain.llms import HuggingFacePipeline  
  
hf\_model = pipeline(  
 "text-generation", model="cerebras/Cerebras-GPT-590M", max\_new\_tokens=200  
)  
  
original\_model = HuggingFacePipeline(pipeline=hf\_model)  
  
generated = original\_model.predict(prompt, stop=["Observation:", "Human:"])  
print(generated)  

```

```text
 Setting `pad\_token\_id` to `eos\_token\_id`:50256 for open-end generation.  
  
  
 'What's the difference between an iterator and an iterable?'  
   

```

***That's not so impressive, is it? It didn't follow the JSON format at all! Let's try with the structured decoder.***

## JSONFormer LLM Wrapper[​](#jsonformer-llm-wrapper "Direct link to JSONFormer LLM Wrapper")

Let's try that again, now providing a the Action input's JSON Schema to the model.

```python
decoder\_schema = {  
 "title": "Decoding Schema",  
 "type": "object",  
 "properties": {  
 "action": {"type": "string", "default": ask\_star\_coder.name},  
 "action\_input": {  
 "type": "object",  
 "properties": ask\_star\_coder.args,  
 },  
 },  
}  

```

```python
from langchain\_experimental.llms import JsonFormer  
  
json\_former = JsonFormer(json\_schema=decoder\_schema, pipeline=hf\_model)  

```

```python
results = json\_former.predict(prompt, stop=["Observation:", "Human:"])  
print(results)  

```

```text
 {"action": "ask\_star\_coder", "action\_input": {"query": "What's the difference between an iterator and an iter", "temperature": 0.0, "max\_new\_tokens": 50.0}}  

```

**Voila! Free of parsing errors.**

- [Hugging Face Baseline](#hugging-face-baseline)
- [JSONFormer LLM Wrapper](#jsonformer-llm-wrapper)
