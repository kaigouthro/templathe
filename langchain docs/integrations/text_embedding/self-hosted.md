# Self Hosted

Let's load the `SelfHostedEmbeddings`, `SelfHostedHuggingFaceEmbeddings`, and `SelfHostedHuggingFaceInstructEmbeddings` classes.

```python
from langchain.embeddings import (  
 SelfHostedEmbeddings,  
 SelfHostedHuggingFaceEmbeddings,  
 SelfHostedHuggingFaceInstructEmbeddings,  
)  
import runhouse as rh  

```

```python
# For an on-demand A100 with GCP, Azure, or Lambda  
gpu = rh.cluster(name="rh-a10x", instance\_type="A100:1", use\_spot=False)  
  
# For an on-demand A10G with AWS (no single A100s on AWS)  
# gpu = rh.cluster(name='rh-a10x', instance\_type='g5.2xlarge', provider='aws')  
  
# For an existing cluster  
# gpu = rh.cluster(ips=['<ip of the cluster>'],  
# ssh\_creds={'ssh\_user': '...', 'ssh\_private\_key':'<path\_to\_key>'},  
# name='my-cluster')  

```

```python
embeddings = SelfHostedHuggingFaceEmbeddings(hardware=gpu)  

```

```python
text = "This is a test document."  

```

```python
query\_result = embeddings.embed\_query(text)  

```

And similarly for SelfHostedHuggingFaceInstructEmbeddings:

```python
embeddings = SelfHostedHuggingFaceInstructEmbeddings(hardware=gpu)  

```

Now let's load an embedding model with a custom load function:

```python
def get\_pipeline():  
 from transformers import (  
 AutoModelForCausalLM,  
 AutoTokenizer,  
 pipeline,  
 ) # Must be inside the function in notebooks  
  
 model\_id = "facebook/bart-base"  
 tokenizer = AutoTokenizer.from\_pretrained(model\_id)  
 model = AutoModelForCausalLM.from\_pretrained(model\_id)  
 return pipeline("feature-extraction", model=model, tokenizer=tokenizer)  
  
  
def inference\_fn(pipeline, prompt):  
 # Return last hidden state of the model  
 if isinstance(prompt, list):  
 return [emb[0][-1] for emb in pipeline(prompt)]  
 return pipeline(prompt)[0][-1]  

```

```python
embeddings = SelfHostedEmbeddings(  
 model\_load\_fn=get\_pipeline,  
 hardware=gpu,  
 model\_reqs=["./", "torch", "transformers"],  
 inference\_fn=inference\_fn,  
)  

```

```python
query\_result = embeddings.embed\_query(text)  

```
