# Runhouse

The [Runhouse](https://github.com/run-house/runhouse) allows remote compute and data across environments and users. See the [Runhouse docs](https://runhouse-docs.readthedocs-hosted.com/en/latest/).

This example goes over how to use LangChain and [Runhouse](https://github.com/run-house/runhouse) to interact with models hosted on your own GPU, or on-demand GPUs on AWS, GCP, AWS, or Lambda.

**Note**: Code uses `SelfHosted` name instead of the `Runhouse`.

```bash
pip install runhouse  

```

```python
from langchain.llms import SelfHostedPipeline, SelfHostedHuggingFaceLLM  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
import runhouse as rh  

```

```text
 INFO | 2023-04-17 16:47:36,173 | No auth token provided, so not using RNS API to save and load configs  

```

```python
# For an on-demand A100 with GCP, Azure, or Lambda  
gpu = rh.cluster(name="rh-a10x", instance\_type="A100:1", use\_spot=False)  
  
# For an on-demand A10G with AWS (no single A100s on AWS)  
# gpu = rh.cluster(name='rh-a10x', instance\_type='g5.2xlarge', provider='aws')  
  
# For an existing cluster  
# gpu = rh.cluster(ips=['<ip of the cluster>'],  
# ssh\_creds={'ssh\_user': '...', 'ssh\_private\_key':'<path\_to\_key>'},  
# name='rh-a10x')  

```

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

```python
llm = SelfHostedHuggingFaceLLM(  
 model\_id="gpt2", hardware=gpu, model\_reqs=["pip:./", "transformers", "torch"]  
)  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"  
  
llm\_chain.run(question)  

```

```text
 INFO | 2023-02-17 05:42:23,537 | Running \_generate\_text via gRPC  
 INFO | 2023-02-17 05:42:24,016 | Time to send message: 0.48 seconds  
  
  
  
  
  
 "\n\nLet's say we're talking sports teams who won the Super Bowl in the year Justin Beiber"  

```

You can also load more custom models through the SelfHostedHuggingFaceLLM interface:

```python
llm = SelfHostedHuggingFaceLLM(  
 model\_id="google/flan-t5-small",  
 task="text2text-generation",  
 hardware=gpu,  
)  

```

```python
llm("What is the capital of Germany?")  

```

```text
 INFO | 2023-02-17 05:54:21,681 | Running \_generate\_text via gRPC  
 INFO | 2023-02-17 05:54:21,937 | Time to send message: 0.25 seconds  
  
  
  
  
  
 'berlin'  

```

Using a custom load function, we can load a custom pipeline directly on the remote hardware:

```python
def load\_pipeline():  
 from transformers import (  
 AutoModelForCausalLM,  
 AutoTokenizer,  
 pipeline,  
 ) # Need to be inside the fn in notebooks  
  
 model\_id = "gpt2"  
 tokenizer = AutoTokenizer.from\_pretrained(model\_id)  
 model = AutoModelForCausalLM.from\_pretrained(model\_id)  
 pipe = pipeline(  
 "text-generation", model=model, tokenizer=tokenizer, max\_new\_tokens=10  
 )  
 return pipe  
  
  
def inference\_fn(pipeline, prompt, stop=None):  
 return pipeline(prompt)[0]["generated\_text"][len(prompt) :]  

```

```python
llm = SelfHostedHuggingFaceLLM(  
 model\_load\_fn=load\_pipeline, hardware=gpu, inference\_fn=inference\_fn  
)  

```

```python
llm("Who is the current US president?")  

```

```text
 INFO | 2023-02-17 05:42:59,219 | Running \_generate\_text via gRPC  
 INFO | 2023-02-17 05:42:59,522 | Time to send message: 0.3 seconds  
  
  
  
  
  
 'john w. bush'  

```

You can send your pipeline directly over the wire to your model, but this will only work for small models (\<2 Gb), and will be pretty slow:

```python
pipeline = load\_pipeline()  
llm = SelfHostedPipeline.from\_pipeline(  
 pipeline=pipeline, hardware=gpu, model\_reqs=model\_reqs  
)  

```

Instead, we can also send it to the hardware's filesystem, which will be much faster.

```python
rh.blob(pickle.dumps(pipeline), path="models/pipeline.pkl").save().to(  
 gpu, path="models"  
)  
  
llm = SelfHostedPipeline.from\_pipeline(pipeline="models/pipeline.pkl", hardware=gpu)  

```
