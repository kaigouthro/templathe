# vLLM

[vLLM](https://vllm.readthedocs.io/en/latest/index.html) is a fast and easy-to-use library for LLM inference and serving, offering:

- State-of-the-art serving throughput
- Efficient management of attention key and value memory with PagedAttention
- Continuous batching of incoming requests
- Optimized CUDA kernels

This notebooks goes over how to use a LLM with langchain and vLLM.

To use, you should have the `vllm` python package installed.

```python
#!pip install vllm -q  

```

```python
from langchain.llms import VLLM  
  
llm = VLLM(model="mosaicml/mpt-7b",  
 trust\_remote\_code=True, # mandatory for hf models  
 max\_new\_tokens=128,  
 top\_k=10,  
 top\_p=0.95,  
 temperature=0.8,  
)  
  
print(llm("What is the capital of France ?"))  

```

```text
 INFO 08-06 11:37:33 llm\_engine.py:70] Initializing an LLM engine with config: model='mosaicml/mpt-7b', tokenizer='mosaicml/mpt-7b', tokenizer\_mode=auto, trust\_remote\_code=True, dtype=torch.bfloat16, use\_dummy\_weights=False, download\_dir=None, use\_np\_weights=False, tensor\_parallel\_size=1, seed=0)  
 INFO 08-06 11:37:41 llm\_engine.py:196] # GPU blocks: 861, # CPU blocks: 512  
  
  
 Processed prompts: 100%|██████████| 1/1 [00:00<00:00, 2.00it/s]  
  
   
 What is the capital of France ? The capital of France is Paris.  
  
  
   

```

## Integrate the model in an LLMChain[​](#integrate-the-model-in-an-llmchain "Direct link to Integrate the model in an LLMChain")

```python
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
  
template = """Question: {question}  
  
Answer: Let's think step by step."""  
prompt = PromptTemplate(template=template, input\_variables=["question"])  
  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
  
question = "Who was the US president in the year the first Pokemon game was released?"  
  
print(llm\_chain.run(question))  

```

```text
 Processed prompts: 100%|██████████| 1/1 [00:01<00:00, 1.34s/it]  
  
   
   
 1. The first Pokemon game was released in 1996.  
 2. The president was Bill Clinton.  
 3. Clinton was president from 1993 to 2001.  
 4. The answer is Clinton.  
   
  
  
   

```

## Distributed Inference[​](#distributed-inference "Direct link to Distributed Inference")

vLLM supports distributed tensor-parallel inference and serving.

To run multi-GPU inference with the LLM class, set the `tensor_parallel_size` argument to the number of GPUs you want to use. For example, to run inference on 4 GPUs

```python
from langchain.llms import VLLM  
  
llm = VLLM(model="mosaicml/mpt-30b",  
 tensor\_parallel\_size=4,  
 trust\_remote\_code=True, # mandatory for hf models  
)  
  
llm("What is the future of AI?")  

```

## OpenAI-Compatible Server[​](#openai-compatible-server "Direct link to OpenAI-Compatible Server")

vLLM can be deployed as a server that mimics the OpenAI API protocol. This allows vLLM to be used as a drop-in replacement for applications using OpenAI API.

This server can be queried in the same format as OpenAI API.

### OpenAI-Compatible Completion[​](#openai-compatible-completion "Direct link to OpenAI-Compatible Completion")

```python
from langchain.llms import VLLMOpenAI  
  
  
llm = VLLMOpenAI(  
 openai\_api\_key="EMPTY",  
 openai\_api\_base="http://localhost:8000/v1",  
 model\_name="tiiuae/falcon-7b",  
 model\_kwargs={"stop": ["."]}  
)  
print(llm("Rome is"))  

```

```text
 a city that is filled with history, ancient buildings, and art around every corner  

```

- [Integrate the model in an LLMChain](#integrate-the-model-in-an-llmchain)

- [Distributed Inference](#distributed-inference)

- [OpenAI-Compatible Server](#openai-compatible-server)

  - [OpenAI-Compatible Completion](#openai-compatible-completion)

- [OpenAI-Compatible Completion](#openai-compatible-completion)
