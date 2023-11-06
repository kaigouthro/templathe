# WebResearchRetriever

Given a query, this retriever will:

- Formulate a set of relate Google searches
- Search for each
- Load all the resulting URLs
- Then embed and perform similarity search with the query on the consolidate page content

```python
from langchain.retrievers.web\_research import WebResearchRetriever  

```

### Simple usage[​](#simple-usage "Direct link to Simple usage")

Specify the LLM to use for Google search query generation.

```python
import os  
from langchain.vectorstores import Chroma  
from langchain.embeddings import OpenAIEmbeddings  
from langchain.chat\_models.openai import ChatOpenAI  
from langchain.utilities import GoogleSearchAPIWrapper  
  
# Vectorstore  
vectorstore = Chroma(embedding\_function=OpenAIEmbeddings(),persist\_directory="./chroma\_db\_oai")  
  
# LLM  
llm = ChatOpenAI(temperature=0)  
  
# Search   
os.environ["GOOGLE\_CSE\_ID"] = "xxx"  
os.environ["GOOGLE\_API\_KEY"] = "xxx"  
search = GoogleSearchAPIWrapper()  

```

```python
# Initialize  
web\_research\_retriever = WebResearchRetriever.from\_llm(  
 vectorstore=vectorstore,  
 llm=llm,   
 search=search,   
)  

```

#### Run with citations[​](#run-with-citations "Direct link to Run with citations")

We can use `RetrievalQAWithSourcesChain` to retrieve docs and provide citations.

```python
from langchain.chains import RetrievalQAWithSourcesChain  
user\_input = "How do LLM Powered Autonomous Agents work?"  
qa\_chain = RetrievalQAWithSourcesChain.from\_chain\_type(llm,retriever=web\_research\_retriever)  
result = qa\_chain({"question": user\_input})  
result  

```

```text
 Fetching pages: 100%|###################################################################################################################################| 1/1 [00:00<00:00, 3.33it/s]  
  
  
  
  
  
 {'question': 'How do LLM Powered Autonomous Agents work?',  
 'answer': "LLM Powered Autonomous Agents work by using LLM (large language model) as the core controller of the agent's brain. It is complemented by several key components, including planning, memory, and tool use. The agent system is designed to be a powerful general problem solver. \n",  
 'sources': 'https://lilianweng.github.io/posts/2023-06-23-agent/'}  

```

#### Run with logging[​](#run-with-logging "Direct link to Run with logging")

Here, we use `get_relevant_documents` method to return docs.

```python
# Run  
import logging  
logging.basicConfig()  
logging.getLogger("langchain.retrievers.web\_research").setLevel(logging.INFO)  
user\_input = "What is Task Decomposition in LLM Powered Autonomous Agents?"  
docs = web\_research\_retriever.get\_relevant\_documents(user\_input)  

```

```text
 INFO:langchain.retrievers.web\_research:Generating questions for Google Search ...  
 INFO:langchain.retrievers.web\_research:Questions for Google Search (raw): {'question': 'What is Task Decomposition in LLM Powered Autonomous Agents?', 'text': LineList(lines=['1. How do LLM powered autonomous agents utilize task decomposition?\n', '2. Can you explain the concept of task decomposition in LLM powered autonomous agents?\n', '3. What role does task decomposition play in the functioning of LLM powered autonomous agents?\n', '4. Why is task decomposition important for LLM powered autonomous agents?\n'])}  
 INFO:langchain.retrievers.web\_research:Questions for Google Search: ['1. How do LLM powered autonomous agents utilize task decomposition?\n', '2. Can you explain the concept of task decomposition in LLM powered autonomous agents?\n', '3. What role does task decomposition play in the functioning of LLM powered autonomous agents?\n', '4. Why is task decomposition important for LLM powered autonomous agents?\n']  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Search results: [{'title': "LLM Powered Autonomous Agents | Lil'Log", 'link': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'snippet': 'Jun 23, 2023 ... Task decomposition can be done (1) by LLM with simple prompting like "Steps for XYZ.\\n1." , "What are the subgoals for achieving XYZ?'}]  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Search results: [{'title': "LLM Powered Autonomous Agents | Lil'Log", 'link': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'snippet': 'Jun 23, 2023 ... Task decomposition can be done (1) by LLM with simple prompting like "Steps for XYZ.\\n1." , "What are the subgoals for achieving XYZ?" , (2)\xa0...'}]  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Search results: [{'title': "LLM Powered Autonomous Agents | Lil'Log", 'link': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'snippet': 'Jun 23, 2023 ... In a LLM-powered autonomous agent system, LLM functions as the ... Task decomposition can be done (1) by LLM with simple prompting like\xa0...'}]  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Search results: [{'title': "LLM Powered Autonomous Agents | Lil'Log", 'link': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'snippet': 'Jun 23, 2023 ... Agent System Overview In a LLM-powered autonomous agent system, ... Task decomposition can be done (1) by LLM with simple prompting like\xa0...'}]  
 INFO:langchain.retrievers.web\_research:New URLs to load: []  

```

#### Generate answer using retrieved docs[​](#generate-answer-using-retrieved-docs "Direct link to Generate answer using retrieved docs")

We can use `load_qa_chain` for QA using the retrieved docs.

```python
from langchain.chains.question\_answering import load\_qa\_chain  
chain = load\_qa\_chain(llm, chain\_type="stuff")  
output = chain({"input\_documents": docs, "question": user\_input},return\_only\_outputs=True)  
output['output\_text']  

```

```text
 'Task decomposition in LLM-powered autonomous agents refers to the process of breaking down a complex task into smaller, more manageable subgoals. This allows the agent to efficiently handle and execute the individual steps required to complete the overall task. By decomposing the task, the agent can prioritize and organize its actions, making it easier to plan and execute the necessary steps towards achieving the desired outcome.'  

```

### More flexibility[​](#more-flexibility "Direct link to More flexibility")

Pass an LLM chain with custom prompt and output parsing.

```python
import os  
import re  
from typing import List  
from langchain.chains import LLMChain  
from pydantic import BaseModel, Field  
from langchain.prompts import PromptTemplate  
from langchain.output\_parsers.pydantic import PydanticOutputParser  
  
# LLMChain  
search\_prompt = PromptTemplate(  
 input\_variables=["question"],  
 template="""You are an assistant tasked with improving Google search   
 results. Generate FIVE Google search queries that are similar to  
 this question. The output should be a numbered list of questions and each  
 should have a question mark at the end: {question}""",  
)  
  
class LineList(BaseModel):  
 """List of questions."""  
  
 lines: List[str] = Field(description="Questions")  
  
class QuestionListOutputParser(PydanticOutputParser):  
 """Output parser for a list of numbered questions."""  
  
 def \_\_init\_\_(self) -> None:  
 super().\_\_init\_\_(pydantic\_object=LineList)  
  
 def parse(self, text: str) -> LineList:  
 lines = re.findall(r"\d+\..\*?\n", text)  
 return LineList(lines=lines)  
   
llm\_chain = LLMChain(  
 llm=llm,  
 prompt=search\_prompt,  
 output\_parser=QuestionListOutputParser(),  
 )  

```

```python
# Initialize  
web\_research\_retriever\_llm\_chain = WebResearchRetriever(  
 vectorstore=vectorstore,  
 llm\_chain=llm\_chain,   
 search=search,   
)  
  
# Run  
docs = web\_research\_retriever\_llm\_chain.get\_relevant\_documents(user\_input)  

```

```text
 INFO:langchain.retrievers.web\_research:Generating questions for Google Search ...  
 INFO:langchain.retrievers.web\_research:Questions for Google Search (raw): {'question': 'What is Task Decomposition in LLM Powered Autonomous Agents?', 'text': LineList(lines=['1. How do LLM powered autonomous agents use task decomposition?\n', '2. Why is task decomposition important for LLM powered autonomous agents?\n', '3. Can you explain the concept of task decomposition in LLM powered autonomous agents?\n', '4. What are the benefits of task decomposition in LLM powered autonomous agents?\n'])}  
 INFO:langchain.retrievers.web\_research:Questions for Google Search: ['1. How do LLM powered autonomous agents use task decomposition?\n', '2. Why is task decomposition important for LLM powered autonomous agents?\n', '3. Can you explain the concept of task decomposition in LLM powered autonomous agents?\n', '4. What are the benefits of task decomposition in LLM powered autonomous agents?\n']  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Search results: [{'title': "LLM Powered Autonomous Agents | Lil'Log", 'link': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'snippet': 'Jun 23, 2023 ... Task decomposition can be done (1) by LLM with simple prompting like "Steps for XYZ.\\n1." , "What are the subgoals for achieving XYZ?'}]  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Search results: [{'title': "LLM Powered Autonomous Agents | Lil'Log", 'link': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'snippet': 'Jun 23, 2023 ... Task decomposition can be done (1) by LLM with simple prompting like "Steps for XYZ.\\n1." , "What are the subgoals for achieving XYZ?" , (2)\xa0...'}]  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Search results: [{'title': "LLM Powered Autonomous Agents | Lil'Log", 'link': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'snippet': 'Jun 23, 2023 ... Task decomposition can be done (1) by LLM with simple prompting like "Steps for XYZ.\\n1." , "What are the subgoals for achieving XYZ?'}]  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Search results: [{'title': "LLM Powered Autonomous Agents | Lil'Log", 'link': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'snippet': 'Jun 23, 2023 ... Task decomposition can be done (1) by LLM with simple prompting like "Steps for XYZ.\\n1." , "What are the subgoals for achieving XYZ?'}]  
 INFO:langchain.retrievers.web\_research:New URLs to load: ['https://lilianweng.github.io/posts/2023-06-23-agent/']  
 INFO:langchain.retrievers.web\_research:Grabbing most relevant splits from urls ...  
 Fetching pages: 100%|###################################################################################################################################| 1/1 [00:00<00:00, 6.32it/s]  

```

```python
len(docs)  

```

```text
 1  

```

### Run locally[​](#run-locally "Direct link to Run locally")

Specify LLM and embeddings that will run locally (e.g., on your laptop).

```python
from langchain.llms import LlamaCpp  
from langchain.embeddings import GPT4AllEmbeddings  
from langchain.callbacks.manager import CallbackManager  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  
  
n\_gpu\_layers = 1 # Metal set to 1 is enough.  
n\_batch = 512 # Should be between 1 and n\_ctx, consider the amount of RAM of your Apple Silicon Chip.  
callback\_manager = CallbackManager([StreamingStdOutCallbackHandler()])  
llama = LlamaCpp(  
 model\_path="/Users/rlm/Desktop/Code/llama.cpp/llama-2-13b-chat.ggmlv3.q4\_0.bin",  
 n\_gpu\_layers=n\_gpu\_layers,  
 n\_batch=n\_batch,  
 n\_ctx=4096, # Context window  
 max\_tokens=1000, # Max tokens to generate  
 f16\_kv=True, # MUST set to True, otherwise you will run into problem after a couple of calls  
 callback\_manager=callback\_manager,  
 verbose=True,  
)  
  
vectorstore\_llama = Chroma(embedding\_function=GPT4AllEmbeddings(),persist\_directory="./chroma\_db\_llama")  

```

```text
 llama.cpp: loading model from /Users/rlm/Desktop/Code/llama.cpp/llama-2-13b-chat.ggmlv3.q4\_0.bin  
 llama\_model\_load\_internal: format = ggjt v3 (latest)  
 llama\_model\_load\_internal: n\_vocab = 32000  
 llama\_model\_load\_internal: n\_ctx = 4096  
 llama\_model\_load\_internal: n\_embd = 5120  
 llama\_model\_load\_internal: n\_mult = 256  
 llama\_model\_load\_internal: n\_head = 40  
 llama\_model\_load\_internal: n\_layer = 40  
 llama\_model\_load\_internal: n\_rot = 128  
 llama\_model\_load\_internal: freq\_base = 10000.0  
 llama\_model\_load\_internal: freq\_scale = 1  
 llama\_model\_load\_internal: ftype = 2 (mostly Q4\_0)  
 llama\_model\_load\_internal: n\_ff = 13824  
 llama\_model\_load\_internal: model size = 13B  
 llama\_model\_load\_internal: ggml ctx size = 0.09 MB  
 llama\_model\_load\_internal: mem required = 9132.71 MB (+ 1608.00 MB per state)  
 llama\_new\_context\_with\_model: kv self size = 3200.00 MB  
 ggml\_metal\_init: allocating  
  
  
 Found model file at /Users/rlm/.cache/gpt4all/ggml-all-MiniLM-L6-v2-f16.bin  
 llama\_new\_context\_with\_model: max tensor size = 87.89 MB  
  
  
 ggml\_metal\_init: using MPS  
 ggml\_metal\_init: loading '/Users/rlm/miniforge3/envs/llama/lib/python3.9/site-packages/llama\_cpp/ggml-metal.metal'  
 ggml\_metal\_init: loaded kernel\_add 0x110fbd600  
 ggml\_metal\_init: loaded kernel\_mul 0x110fbeb30  
 ggml\_metal\_init: loaded kernel\_mul\_row 0x110fbf350  
 ggml\_metal\_init: loaded kernel\_scale 0x110fbf9e0  
 ggml\_metal\_init: loaded kernel\_silu 0x110fc0150  
 ggml\_metal\_init: loaded kernel\_relu 0x110fbd950  
 ggml\_metal\_init: loaded kernel\_gelu 0x110fbdbb0  
 ggml\_metal\_init: loaded kernel\_soft\_max 0x110fc14d0  
 ggml\_metal\_init: loaded kernel\_diag\_mask\_inf 0x110fc1980  
 ggml\_metal\_init: loaded kernel\_get\_rows\_f16 0x110fc22a0  
 ggml\_metal\_init: loaded kernel\_get\_rows\_q4\_0 0x110fc2ad0  
 ggml\_metal\_init: loaded kernel\_get\_rows\_q4\_1 0x110fc3260  
 ggml\_metal\_init: loaded kernel\_get\_rows\_q2\_K 0x110fc3ad0  
 ggml\_metal\_init: loaded kernel\_get\_rows\_q3\_K 0x110fc41c0  
 ggml\_metal\_init: loaded kernel\_get\_rows\_q4\_K 0x110fc48c0  
 ggml\_metal\_init: loaded kernel\_get\_rows\_q5\_K 0x110fc4fa0  
 ggml\_metal\_init: loaded kernel\_get\_rows\_q6\_K 0x110fc56a0  
 ggml\_metal\_init: loaded kernel\_rms\_norm 0x110fc5da0  
 ggml\_metal\_init: loaded kernel\_norm 0x110fc64d0  
 ggml\_metal\_init: loaded kernel\_mul\_mat\_f16\_f32 0x2a5c19990  
 ggml\_metal\_init: loaded kernel\_mul\_mat\_q4\_0\_f32 0x2a5c1d4a0  
 ggml\_metal\_init: loaded kernel\_mul\_mat\_q4\_1\_f32 0x2a5c19fc0  
 ggml\_metal\_init: loaded kernel\_mul\_mat\_q2\_K\_f32 0x2a5c1dcc0  
 ggml\_metal\_init: loaded kernel\_mul\_mat\_q3\_K\_f32 0x2a5c1e420  
 ggml\_metal\_init: loaded kernel\_mul\_mat\_q4\_K\_f32 0x2a5c1edc0  
 ggml\_metal\_init: loaded kernel\_mul\_mat\_q5\_K\_f32 0x2a5c1fd90  
 ggml\_metal\_init: loaded kernel\_mul\_mat\_q6\_K\_f32 0x2a5c20540  
 ggml\_metal\_init: loaded kernel\_rope 0x2a5c20d40  
 ggml\_metal\_init: loaded kernel\_alibi\_f32 0x2a5c21730  
 ggml\_metal\_init: loaded kernel\_cpy\_f32\_f16 0x2a5c21ab0  
 ggml\_metal\_init: loaded kernel\_cpy\_f32\_f32 0x2a5c22080  
 ggml\_metal\_init: loaded kernel\_cpy\_f16\_f16 0x2a5c231d0  
 ggml\_metal\_init: recommendedMaxWorkingSetSize = 21845.34 MB  
 ggml\_metal\_init: hasUnifiedMemory = true  
 ggml\_metal\_init: maxTransferRate = built-in GPU  
 ggml\_metal\_add\_buffer: allocated 'data ' buffer, size = 6984.06 MB, ( 6984.52 / 21845.34)  
 ggml\_metal\_add\_buffer: allocated 'eval ' buffer, size = 1040.00 MB, ( 8024.52 / 21845.34)  
 ggml\_metal\_add\_buffer: allocated 'kv ' buffer, size = 3202.00 MB, (11226.52 / 21845.34)  
 ggml\_metal\_add\_buffer: allocated 'scr0 ' buffer, size = 597.00 MB, (11823.52 / 21845.34)  
 AVX = 0 | AVX2 = 0 | AVX512 = 0 | AVX512\_VBMI = 0 | AVX512\_VNNI = 0 | FMA = 0 | NEON = 1 | ARM\_FMA = 1 | F16C = 0 | FP16\_VA = 1 | WASM\_SIMD = 0 | BLAS = 1 | SSE3 = 0 | VSX = 0 |   
 ggml\_metal\_add\_buffer: allocated 'scr1 ' buffer, size = 512.00 MB, (12335.52 / 21845.34)  
 objc[33471]: Class GGMLMetalClass is implemented in both /Users/rlm/miniforge3/envs/llama/lib/python3.9/site-packages/llama\_cpp/libllama.dylib (0x2c7368208) and /Users/rlm/miniforge3/envs/llama/lib/python3.9/site-packages/gpt4all/llmodel\_DO\_NOT\_MODIFY/build/libreplit-mainline-metal.dylib (0x5ebf48208). One of the two will be used. Which one is undefined.  
 objc[33471]: Class GGMLMetalClass is implemented in both /Users/rlm/miniforge3/envs/llama/lib/python3.9/site-packages/llama\_cpp/libllama.dylib (0x2c7368208) and /Users/rlm/miniforge3/envs/llama/lib/python3.9/site-packages/gpt4all/llmodel\_DO\_NOT\_MODIFY/build/libllamamodel-mainline-metal.dylib (0x5ec374208). One of the two will be used. Which one is undefined.  

```

We supplied `StreamingStdOutCallbackHandler()`, so model outputs (e.g., generated questions) are streamed.

We also have logging on, so we seem them there too.

```python
from langchain.chains import RetrievalQAWithSourcesChain  
# Initialize  
web\_research\_retriever = WebResearchRetriever.from\_llm(  
 vectorstore=vectorstore\_llama,  
 llm=llama,   
 search=search,   
)  
  
# Run  
user\_input = "What is Task Decomposition in LLM Powered Autonomous Agents?"  
qa\_chain = RetrievalQAWithSourcesChain.from\_chain\_type(llama,retriever=web\_research\_retriever)  
result = qa\_chain({"question": user\_input})  
result  

```

```text
 INFO:langchain.retrievers.web\_research:Generating questions for Google Search ...  
  
  
 Sure, here are five Google search queries that are similar to "What is Task Decomposition in LLM Powered Autonomous Agents?":  
   
 1. How does Task Decomposition work in LLM Powered Autonomous Agents?   
 2. What are the benefits of using Task Decomposition in LLM Powered Autonomous Agents?   
 3. Can you provide examples of Task Decomposition in LLM Powered Autonomous Agents?   
 4. How does Task Decomposition improve the performance of LLM Powered Autonomous Agents?   
 5. What are some common challenges or limitations of using Task Decomposition in LLM Powered Autonomous Agents, and how can they be addressed?  
  
   
 llama\_print\_timings: load time = 8585.01 ms  
 llama\_print\_timings: sample time = 124.24 ms / 164 runs ( 0.76 ms per token, 1320.04 tokens per second)  
 llama\_print\_timings: prompt eval time = 8584.83 ms / 101 tokens ( 85.00 ms per token, 11.76 tokens per second)  
 llama\_print\_timings: eval time = 7268.55 ms / 163 runs ( 44.59 ms per token, 22.43 tokens per second)  
 llama\_print\_timings: total time = 16236.13 ms  
 INFO:langchain.retrievers.web\_research:Questions for Google Search (raw): {'question': 'What is Task Decomposition in LLM Powered Autonomous Agents?', 'text': LineList(lines=['1. How does Task Decomposition work in LLM Powered Autonomous Agents? \n', '2. What are the benefits of using Task Decomposition in LLM Powered Autonomous Agents? \n', '3. Can you provide examples of Task Decomposition in LLM Powered Autonomous Agents? \n', '4. How does Task Decomposition improve the performance of LLM Powered Autonomous Agents? \n'])}  
 INFO:langchain.retrievers.web\_research:Questions for Google Search: ['1. How does Task Decomposition work in LLM Powered Autonomous Agents? \n', '2. What are the benefits of using Task Decomposition in LLM Powered Autonomous Agents? \n', '3. Can you provide examples of Task Decomposition in LLM Powered Autonomous Agents? \n', '4. How does Task Decomposition improve the performance of LLM Powered Autonomous Agents? \n']  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Search results: [{'title': "LLM Powered Autonomous Agents | Lil'Log", 'link': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'snippet': 'Jun 23, 2023 ... Task decomposition can be done (1) by LLM with simple prompting like "Steps for XYZ.\\n1." , "What are the subgoals for achieving XYZ?'}]  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Search results: [{'title': "LLM Powered Autonomous Agents | Lil'Log", 'link': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'snippet': 'Jun 23, 2023 ... Task decomposition can be done (1) by LLM with simple prompting like "Steps for XYZ.\\n1." , "What are the subgoals for achieving XYZ?" , (2)\xa0...'}]  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Search results: [{'title': "LLM Powered Autonomous Agents | Lil'Log", 'link': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'snippet': 'Jun 23, 2023 ... A complicated task usually involves many steps. An agent needs to know what they are and plan ahead. Task Decomposition#. Chain of thought (CoT;\xa0...'}]  
 INFO:langchain.retrievers.web\_research:Searching for relevant urls ...  
 INFO:langchain.retrievers.web\_research:Search results: [{'title': "LLM Powered Autonomous Agents | Lil'Log", 'link': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'snippet': 'Jun 23, 2023 ... Agent System Overview In a LLM-powered autonomous agent system, ... Task decomposition can be done (1) by LLM with simple prompting like\xa0...'}]  
 INFO:langchain.retrievers.web\_research:New URLs to load: ['https://lilianweng.github.io/posts/2023-06-23-agent/']  
 INFO:langchain.retrievers.web\_research:Grabbing most relevant splits from urls ...  
 Fetching pages: 100%|###################################################################################################################################| 1/1 [00:00<00:00, 10.49it/s]  
 Llama.generate: prefix-match hit  
  
  
 The content discusses Task Decomposition in LLM Powered Autonomous Agents, which involves breaking down large tasks into smaller, manageable subgoals for efficient handling of complex tasks.  
 SOURCES:  
 https://lilianweng.github.io/posts/2023-06-23-agent/  
  
   
 llama\_print\_timings: load time = 8585.01 ms  
 llama\_print\_timings: sample time = 52.88 ms / 72 runs ( 0.73 ms per token, 1361.55 tokens per second)  
 llama\_print\_timings: prompt eval time = 125925.13 ms / 2358 tokens ( 53.40 ms per token, 18.73 tokens per second)  
 llama\_print\_timings: eval time = 3504.16 ms / 71 runs ( 49.35 ms per token, 20.26 tokens per second)  
 llama\_print\_timings: total time = 129584.60 ms  
  
  
  
  
  
 {'question': 'What is Task Decomposition in LLM Powered Autonomous Agents?',  
 'answer': ' The content discusses Task Decomposition in LLM Powered Autonomous Agents, which involves breaking down large tasks into smaller, manageable subgoals for efficient handling of complex tasks.\n',  
 'sources': 'https://lilianweng.github.io/posts/2023-06-23-agent/'}  

```

- [Simple usage](#simple-usage)
- [More flexibility](#more-flexibility)
- [Run locally](#run-locally)
