# Ollama

[Ollama](https://ollama.ai/) allows you to run open-source large language models, such as Llama 2, locally.

Ollama bundles model weights, configuration, and data into a single package, defined by a Modelfile.

It optimizes setup and configuration details, including GPU usage.

For a complete list of supported models and model variants, see the [Ollama model library](https://github.com/jmorganca/ollama#model-library).

## Setup[​](#setup "Direct link to Setup")

First, follow [these instructions](https://github.com/jmorganca/ollama) to set up and run a local Ollama instance:

- [Download](https://ollama.ai/download)
- Fetch a model via `ollama pull <model family>`
- e.g., for `Llama-7b`: `ollama pull llama2` (see full list [here](https://github.com/jmorganca/ollama))
- This will download the most basic version of the model typically (e.g., smallest # parameters and `q4_0`)
- On Mac, it will download to

`~/.ollama/models/manifests/registry.ollama.ai/library/<model family>/latest`

- And we specify a particular version, e.g., for `ollama pull vicuna:13b-v1.5-16k-q4_0`
- The file is here with the model version in place of `latest`

`~/.ollama/models/manifests/registry.ollama.ai/library/vicuna/13b-v1.5-16k-q4_0`

You can easily access models in a few ways:

1/ if the app is running:

- All of your local models are automatically served on `localhost:11434`
- Select your model when setting `llm = Ollama(..., model="<model family>:<version>")`
- If you set `llm = Ollama(..., model="<model family")` withoout a version it will simply look for `latest`

2/ if building from source or just running the binary:

- Then you must run `ollama serve`
- All of your local models are automatically served on `localhost:11434`
- Then, select as shown above

## Usage[​](#usage "Direct link to Usage")

You can see a full list of supported parameters on the [API reference page](https://api.python.langchain.com/en/latest/llms/langchain.llms.ollama.Ollama.html).

```python
from langchain.llms import Ollama  
from langchain.callbacks.manager import CallbackManager  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler   
llm = Ollama(model="llama2",   
 callback\_manager = CallbackManager([StreamingStdOutCallbackHandler()]))  

```

With `StreamingStdOutCallbackHandler`, you will see tokens streamed.

```python
llm("Tell me about the history of AI")  

```

Ollama supports embeddings via `OllamaEmbeddings`:

```python
from langchain.embeddings import OllamaEmbeddings  
oembed = OllamaEmbeddings(base\_url="http://localhost:11434", model="llama2")  
oembed.embed\_query("Llamas are social animals and live with others as a herd.")  

```

## RAG[​](#rag "Direct link to RAG")

We can use Olama with RAG, [just as shown here](https://python.langchain.com/docs/use_cases/question_answering/local_retrieval_qa).

Let's use the 13b model:

```text
ollama pull llama2:13b  

```

Let's also use local embeddings from `OllamaEmbeddings` and `Chroma`.

```bash
pip install chromadb  

```

```python
# Load web page  
from langchain.document\_loaders import WebBaseLoader  
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")  
data = loader.load()  

```

```python
# Split into chunks   
from langchain.text\_splitter import RecursiveCharacterTextSplitter  
text\_splitter = RecursiveCharacterTextSplitter(chunk\_size=1500, chunk\_overlap=100)  
all\_splits = text\_splitter.split\_documents(data)  

```

```python
# Embed and store  
from langchain.vectorstores import Chroma  
from langchain.embeddings import GPT4AllEmbeddings  
from langchain.embeddings import OllamaEmbeddings # We can also try Ollama embeddings  
vectorstore = Chroma.from\_documents(documents=all\_splits,  
 embedding=GPT4AllEmbeddings())  

```

```text
 Found model file at /Users/rlm/.cache/gpt4all/ggml-all-MiniLM-L6-v2-f16.bin  
  
  
 objc[77472]: Class GGMLMetalClass is implemented in both /Users/rlm/miniforge3/envs/llama2/lib/python3.9/site-packages/gpt4all/llmodel\_DO\_NOT\_MODIFY/build/libreplit-mainline-metal.dylib (0x17f754208) and /Users/rlm/miniforge3/envs/llama2/lib/python3.9/site-packages/gpt4all/llmodel\_DO\_NOT\_MODIFY/build/libllamamodel-mainline-metal.dylib (0x17fb80208). One of the two will be used. Which one is undefined.  

```

```python
# Retrieve  
question = "How can Task Decomposition be done?"  
docs = vectorstore.similarity\_search(question)  
len(docs)  

```

```text
 4  

```

```python
# RAG prompt  
from langchain import hub  
QA\_CHAIN\_PROMPT = hub.pull("rlm/rag-prompt-llama")  

```

```python
# LLM  
from langchain.llms import Ollama  
from langchain.callbacks.manager import CallbackManager  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  
llm = Ollama(model="llama2",  
 verbose=True,  
 callback\_manager=CallbackManager([StreamingStdOutCallbackHandler()]))  

```

```python
# QA chain  
from langchain.chains import RetrievalQA  
qa\_chain = RetrievalQA.from\_chain\_type(  
 llm,  
 retriever=vectorstore.as\_retriever(),  
 chain\_type\_kwargs={"prompt": QA\_CHAIN\_PROMPT},  
)  

```

```python
question = "What are the various approaches to Task Decomposition for AI Agents?"  
result = qa\_chain({"query": question})  

```

```text
 There are several approaches to task decomposition for AI agents, including:  
   
 1. Chain of thought (CoT): This involves instructing the model to "think step by step" and use more test-time computation to decompose hard tasks into smaller and simpler steps.  
 2. Tree of thoughts (ToT): This extends CoT by exploring multiple reasoning possibilities at each step, creating a tree structure. The search process can be BFS or DFS with each state evaluated by a classifier or majority vote.  
 3. Using task-specific instructions: For example, "Write a story outline." for writing a novel.  
 4. Human inputs: The agent can receive input from a human operator to perform tasks that require creativity and domain expertise.  
   
 These approaches allow the agent to break down complex tasks into manageable subgoals, enabling efficient handling of tasks and improving the quality of final results through self-reflection and refinement.  

```

You can also get logging for tokens.

```python
from langchain.schema import LLMResult  
from langchain.callbacks.base import BaseCallbackHandler  
  
class GenerationStatisticsCallback(BaseCallbackHandler):  
 def on\_llm\_end(self, response: LLMResult, \*\*kwargs) -> None:  
 print(response.generations[0][0].generation\_info)  
   
callback\_manager = CallbackManager([StreamingStdOutCallbackHandler(), GenerationStatisticsCallback()])  
  
llm = Ollama(base\_url="http://localhost:11434",  
 model="llama2",  
 verbose=True,  
 callback\_manager=callback\_manager)  
  
qa\_chain = RetrievalQA.from\_chain\_type(  
 llm,  
 retriever=vectorstore.as\_retriever(),  
 chain\_type\_kwargs={"prompt": QA\_CHAIN\_PROMPT},  
)  
  
question = "What are the approaches to Task Decomposition?"  
result = qa\_chain({"query": question})  

```

`eval_count` / (`eval_duration`/10e9) gets `tok / s`

```python
62 / (1313002000/1000/1000/1000)  

```

```text
 47.22003469910937  

```

## Using the Hub for prompt management[​](#using-the-hub-for-prompt-management "Direct link to Using the Hub for prompt management")

Open-source models often benefit from specific prompts.

For example, [Mistral 7b](https://mistral.ai/news/announcing-mistral-7b/) was fine-tuned for chat using the prompt format shown [here](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1).

Get the model: `ollama pull mistral:7b-instruct`

```python
# LLM  
from langchain.llms import Ollama  
from langchain.callbacks.manager import CallbackManager  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  
llm = Ollama(model="mistral:7b-instruct",  
 verbose=True,  
 callback\_manager=CallbackManager([StreamingStdOutCallbackHandler()]))  

```

```python
from langchain import hub  
QA\_CHAIN\_PROMPT = hub.pull("rlm/rag-prompt-mistral")  
  
# QA chain  
from langchain.chains import RetrievalQA  
qa\_chain = RetrievalQA.from\_chain\_type(  
 llm,  
 retriever=vectorstore.as\_retriever(),  
 chain\_type\_kwargs={"prompt": QA\_CHAIN\_PROMPT},  
)  

```

```python
question = "What are the various approaches to Task Decomposition for AI Agents?"  
result = qa\_chain({"query": question})  

```

```text
   
 There are different approaches to Task Decomposition for AI Agents such as Chain of thought (CoT) and Tree of Thoughts (ToT). CoT breaks down big tasks into multiple manageable tasks and generates multiple thoughts per step, while ToT explores multiple reasoning possibilities at each step. Task decomposition can be done by LLM with simple prompting or using task-specific instructions or human inputs.  

```

- [Setup](#setup)
- [Usage](#usage)
- [RAG](#rag)
- [Using the Hub for prompt management](#using-the-hub-for-prompt-management)
