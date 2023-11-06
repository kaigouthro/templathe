# RELLM

[RELLM](https://github.com/r2d4/rellm) is a library that wraps local Hugging Face pipeline models for structured decoding.

It works by generating tokens one at a time. At each step, it masks tokens that don't conform to the provided partial regular expression.

**Warning - this module is still experimental**

```bash
pip install rellm > /dev/null  

```

### Hugging Face Baseline[​](#hugging-face-baseline "Direct link to Hugging Face Baseline")

First, let's establish a qualitative baseline by checking the output of the model without structured decoding.

```python
import logging  
  
logging.basicConfig(level=logging.ERROR)  
prompt = """Human: "What's the capital of the United States?"  
AI Assistant:{  
 "action": "Final Answer",  
 "action\_input": "The capital of the United States is Washington D.C."  
}  
Human: "What's the capital of Pennsylvania?"  
AI Assistant:{  
 "action": "Final Answer",  
 "action\_input": "The capital of Pennsylvania is Harrisburg."  
}  
Human: "What 2 + 5?"  
AI Assistant:{  
 "action": "Final Answer",  
 "action\_input": "2 + 5 = 7."  
}  
Human: 'What's the capital of Maryland?'  
AI Assistant:"""  

```

```python
from transformers import pipeline  
from langchain.llms import HuggingFacePipeline  
  
hf\_model = pipeline(  
 "text-generation", model="cerebras/Cerebras-GPT-590M", max\_new\_tokens=200  
)  
  
original\_model = HuggingFacePipeline(pipeline=hf\_model)  
  
generated = original\_model.generate([prompt], stop=["Human:"])  
print(generated)  

```

```text
 Setting `pad\_token\_id` to `eos\_token\_id`:50256 for open-end generation.  
  
  
 generations=[[Generation(text=' "What\'s the capital of Maryland?"\n', generation\_info=None)]] llm\_output=None  

```

***That's not so impressive, is it? It didn't answer the question and it didn't follow the JSON format at all! Let's try with the structured decoder.***

## RELLM LLM Wrapper[​](#rellm-llm-wrapper "Direct link to RELLM LLM Wrapper")

Let's try that again, now providing a regex to match the JSON structured format.

```python
import regex # Note this is the regex library NOT python's re stdlib module  
  
# We'll choose a regex that matches to a structured json string that looks like:  
# {  
# "action": "Final Answer",  
# "action\_input": string or dict  
# }  
pattern = regex.compile(  
 r'\{\s\*"action":\s\*"Final Answer",\s\*"action\_input":\s\*(\{.\*\}|"[^"]\*")\s\*\}\nHuman:'  
)  

```

```python
from langchain\_experimental.llms import RELLM  
  
model = RELLM(pipeline=hf\_model, regex=pattern, max\_new\_tokens=200)  
  
generated = model.predict(prompt, stop=["Human:"])  
print(generated)  

```

```text
 {"action": "Final Answer",  
 "action\_input": "The capital of Maryland is Baltimore."  
 }  
   

```

**Voila! Free of parsing errors.**

- [Hugging Face Baseline](#hugging-face-baseline)
- [RELLM LLM Wrapper](#rellm-llm-wrapper)
