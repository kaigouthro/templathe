# Serialization

This notebook covers how to serialize chains to and from disk. The serialization format we use is JSON or YAML. Currently, only some chains support this type of serialization. We will grow the number of supported chains over time.

## Saving a chain to disk[​](#saving-a-chain-to-disk "Direct link to Saving a chain to disk")

First, let's go over how to save a chain to disk. This can be done with the `.save` method, and specifying a file path with a `.json` or `.yaml` extension.

```python
from langchain.prompts import PromptTemplate  
from langchain.llms import OpenAI  
from langchain.chains import LLMChain  
  
template = """Question: {question}  
  
Answer: Let's think step by step."""  
prompt = PromptTemplate(template=template, input\_variables=["question"])  
llm\_chain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0), verbose=True)  

```

```python
llm\_chain.save("llm\_chain.json")  

```

Let's now take a look at what's inside this saved file:

```bash
cat llm\_chain.json  

```

```text
 {  
 "memory": null,  
 "verbose": true,  
 "prompt": {  
 "input\_variables": [  
 "question"  
 ],  
 "output\_parser": null,  
 "template": "Question: {question}\n\nAnswer: Let's think step by step.",  
 "template\_format": "f-string"  
 },  
 "llm": {  
 "model\_name": "text-davinci-003",  
 "temperature": 0.0,  
 "max\_tokens": 256,  
 "top\_p": 1,  
 "frequency\_penalty": 0,  
 "presence\_penalty": 0,  
 "n": 1,  
 "best\_of": 1,  
 "request\_timeout": null,  
 "logit\_bias": {},  
 "\_type": "openai"  
 },  
 "output\_key": "text",  
 "\_type": "llm\_chain"  
 }  

```

## Loading a chain from disk[​](#loading-a-chain-from-disk "Direct link to Loading a chain from disk")

We can load a chain from disk by using the `load_chain` method.

```python
from langchain.chains import load\_chain  

```

```python
chain = load\_chain("llm\_chain.json")  

```

```python
chain.run("whats 2 + 2")  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 Question: whats 2 + 2  
   
 Answer: Let's think step by step.  
   
 > Finished chain.  
  
  
  
  
  
 ' 2 + 2 = 4'  

```

## Saving components separately[​](#saving-components-separately "Direct link to Saving components separately")

In the above example, we can see that the prompt and LLM configuration information is saved in the same JSON as the overall chain. Alternatively, we can split them up and save them separately. This is often useful to make the saved components more modular. In order to do this, we just need to specify `llm_path` instead of the `llm` component, and `prompt_path` instead of the `prompt` component.

```python
llm\_chain.prompt.save("prompt.json")  

```

```bash
cat prompt.json  

```

```text
 {  
 "input\_variables": [  
 "question"  
 ],  
 "output\_parser": null,  
 "template": "Question: {question}\n\nAnswer: Let's think step by step.",  
 "template\_format": "f-string"  
 }  

```

```python
llm\_chain.llm.save("llm.json")  

```

```bash
cat llm.json  

```

```text
 {  
 "model\_name": "text-davinci-003",  
 "temperature": 0.0,  
 "max\_tokens": 256,  
 "top\_p": 1,  
 "frequency\_penalty": 0,  
 "presence\_penalty": 0,  
 "n": 1,  
 "best\_of": 1,  
 "request\_timeout": null,  
 "logit\_bias": {},  
 "\_type": "openai"  
 }  

```

```python
config = {  
 "memory": None,  
 "verbose": True,  
 "prompt\_path": "prompt.json",  
 "llm\_path": "llm.json",  
 "output\_key": "text",  
 "\_type": "llm\_chain",  
}  
import json  
  
with open("llm\_chain\_separate.json", "w") as f:  
 json.dump(config, f, indent=2)  

```

```bash
cat llm\_chain\_separate.json  

```

```text
 {  
 "memory": null,  
 "verbose": true,  
 "prompt\_path": "prompt.json",  
 "llm\_path": "llm.json",  
 "output\_key": "text",  
 "\_type": "llm\_chain"  
 }  

```

We can then load it in the same way:

```python
chain = load\_chain("llm\_chain\_separate.json")  

```

```python
chain.run("whats 2 + 2")  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 Question: whats 2 + 2  
   
 Answer: Let's think step by step.  
   
 > Finished chain.  
  
  
  
  
  
 ' 2 + 2 = 4'  

```

- [Saving a chain to disk](#saving-a-chain-to-disk)
- [Loading a chain from disk](#loading-a-chain-from-disk)
- [Saving components separately](#saving-components-separately)
