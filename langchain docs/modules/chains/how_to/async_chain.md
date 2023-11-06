# Async API

LangChain provides async support for Chains by leveraging the [asyncio](https://docs.python.org/3/library/asyncio.html) library.

Async methods are currently supported in `LLMChain` (through `arun`, `apredict`, `acall`) and `LLMMathChain` (through `arun` and `acall`), `ChatVectorDBChain`, and [QA chains](/docs/use_cases/question_answering/question_answering). Async support for other chains is on the roadmap.

```python
import asyncio  
import time  
  
from langchain.llms import OpenAI  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
  
  
def generate\_serially():  
 llm = OpenAI(temperature=0.9)  
 prompt = PromptTemplate(  
 input\_variables=["product"],  
 template="What is a good name for a company that makes {product}?",  
 )  
 chain = LLMChain(llm=llm, prompt=prompt)  
 for \_ in range(5):  
 resp = chain.run(product="toothpaste")  
 print(resp)  
  
  
async def async\_generate(chain):  
 resp = await chain.arun(product="toothpaste")  
 print(resp)  
  
  
async def generate\_concurrently():  
 llm = OpenAI(temperature=0.9)  
 prompt = PromptTemplate(  
 input\_variables=["product"],  
 template="What is a good name for a company that makes {product}?",  
 )  
 chain = LLMChain(llm=llm, prompt=prompt)  
 tasks = [async\_generate(chain) for \_ in range(5)]  
 await asyncio.gather(\*tasks)  
  
  
s = time.perf\_counter()  
# If running this outside of Jupyter, use asyncio.run(generate\_concurrently())  
await generate\_concurrently()  
elapsed = time.perf\_counter() - s  
print("\033[1m" + f"Concurrent executed in {elapsed:0.2f} seconds." + "\033[0m")  
  
s = time.perf\_counter()  
generate\_serially()  
elapsed = time.perf\_counter() - s  
print("\033[1m" + f"Serial executed in {elapsed:0.2f} seconds." + "\033[0m")  

```

```text
   
   
 BrightSmile Toothpaste Company  
   
   
 BrightSmile Toothpaste Co.  
   
   
 BrightSmile Toothpaste  
   
   
 Gleaming Smile Inc.  
   
   
 SparkleSmile Toothpaste  
 Concurrent executed in 1.54 seconds.  
   
   
 BrightSmile Toothpaste Co.  
   
   
 MintyFresh Toothpaste Co.  
   
   
 SparkleSmile Toothpaste.  
   
   
 Pearly Whites Toothpaste Co.  
   
   
 BrightSmile Toothpaste.  
 Serial executed in 6.38 seconds.  

```
