# Hugging Face Local Pipelines

Hugging Face models can be run locally through the `HuggingFacePipeline` class.

The [Hugging Face Model Hub](https://huggingface.co/models) hosts over 120k models, 20k datasets, and 50k demo apps (Spaces), all open source and publicly available, in an online platform where people can easily collaborate and build ML together.

These can be called from LangChain either through this local pipeline wrapper or by calling their hosted inference endpoints through the HuggingFaceHub class. For more information on the hosted pipelines, see the [HuggingFaceHub](/docs/integrations/llms/huggingface_hub.html) notebook.

To use, you should have the `transformers` python [package installed](https://pypi.org/project/transformers/), as well as [pytorch](https://pytorch.org/get-started/locally/). You can also install `xformer` for a more memory-efficient attention implementation.

```python
%pip install transformers --quiet  

```

### Load the model[​](#load-the-model "Direct link to Load the model")

```python
from langchain.llms import HuggingFacePipeline  
  
llm = HuggingFacePipeline.from\_model\_id(  
 model\_id="bigscience/bloom-1b7",  
 task="text-generation",  
 model\_kwargs={"temperature": 0, "max\_length": 64},  
)  

```

### Create Chain[​](#create-chain "Direct link to Create Chain")

With the model loaded into memory, you can compose it with a prompt to
form a chain.

```python
from langchain.prompts import PromptTemplate  
  
template = """Question: {question}  
  
Answer: Let's think step by step."""  
prompt = PromptTemplate.from\_template(template)  
  
chain = prompt | llm  
  
question = "What is electroencephalography?"  
  
print(chain.invoke({"question": question}))  

```

### Batch GPU Inference[​](#batch-gpu-inference "Direct link to Batch GPU Inference")

If running on a device with GPU, you can also run inference on the GPU in batch mode.

```python
gpu\_llm = HuggingFacePipeline.from\_model\_id(  
 model\_id="bigscience/bloom-1b7",  
 task="text-generation",  
 device=0, # -1 for CPU  
 batch\_size=2, # adjust as needed based on GPU map and model size.  
 model\_kwargs={"temperature": 0, "max\_length": 64},  
)  
  
gpu\_chain = prompt | gpu\_llm.bind(stop=["\n\n"])  
  
questions = []  
for i in range(4):  
 questions.append({"question": f"What is the number {i} in french?"})  
  
answers = gpu\_chain.batch(questions)  
for answer in answers:  
 print(answer)  

```

- [Load the model](#load-the-model)
- [Create Chain](#create-chain)
- [Batch GPU Inference](#batch-gpu-inference)
