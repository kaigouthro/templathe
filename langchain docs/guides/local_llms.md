# Run LLMs locally

## Use case[​](#use-case "Direct link to Use case")

The popularity of projects like [PrivateGPT](https://github.com/imartinez/privateGPT), [llama.cpp](https://github.com/ggerganov/llama.cpp), and [GPT4All](https://github.com/nomic-ai/gpt4all) underscore the demand to run LLMs locally (on your own device).

This has at least two important benefits:

1. `Privacy`: Your data is not sent to a third party, and it is not subject to the terms of service of a commercial service
1. `Cost`: There is no inference fee, which is important for token-intensive applications (e.g., [long-running simulations](https://twitter.com/RLanceMartin/status/1691097659262820352?s=20), summarization)

## Overview[​](#overview "Direct link to Overview")

Running an LLM locally requires a few things:

1. `Open-source LLM`: An open-source LLM that can be freely modified and shared
1. `Inference`: Ability to run this LLM on your device w/ acceptable latency

### Open-source LLMs[​](#open-source-llms "Direct link to Open-source LLMs")

Users can now gain access to a rapidly growing set of [open-source LLMs](https://cameronrwolfe.substack.com/p/the-history-of-open-source-llms-better).

These LLMs can be assessed across at least two dimensions (see figure):

1. `Base model`: What is the base-model and how was it trained?
1. `Fine-tuning approach`: Was the base-model fine-tuned and, if so, what [set of instructions](https://cameronrwolfe.substack.com/p/beyond-llama-the-power-of-open-llms#%C2%A7alpaca-an-instruction-following-llama-model) was used?

![Image description](/assets/images/OSS_LLM_overview-b0a96cc35216ec43c3ccde7ed1140854.png)

![Image description](/assets/images/OSS_LLM_overview-b0a96cc35216ec43c3ccde7ed1140854.png)

The relative performance of these models can be assessed using several leaderboards, including:

1. [LmSys](https://chat.lmsys.org/?arena)
1. [GPT4All](https://gpt4all.io/index.html)
1. [HuggingFace](https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard)

### Inference[​](#inference "Direct link to Inference")

A few frameworks for this have emerged to support inference of open-source LLMs on various devices:

1. [`llama.cpp`](https://github.com/ggerganov/llama.cpp): C++ implementation of llama inference code with [weight optimization / quantization](https://finbarr.ca/how-is-llama-cpp-possible/)
1. [`gpt4all`](https://docs.gpt4all.io/index.html): Optimized C backend for inference
1. [`Ollama`](https://ollama.ai/): Bundles model weights and environment into an app that runs on device and serves the LLM

In general, these frameworks will do a few things:

1. `Quantization`: Reduce the memory footprint of the raw model weights
1. `Efficient implementation for inference`: Support inference on consumer hardware (e.g., CPU or laptop GPU)

In particular, see [this excellent post](https://finbarr.ca/how-is-llama-cpp-possible/) on the importance of quantization.

![Image description](/assets/images/llama-memory-weights-aaccef5df087e993b0f46277500039b6.png)

![Image description](/assets/images/llama-memory-weights-aaccef5df087e993b0f46277500039b6.png)

With less precision, we radically decrease the memory needed to store the LLM in memory.

In addition, we can see the importance of GPU memory bandwidth [sheet](https://docs.google.com/spreadsheets/d/1OehfHHNSn66BP2h3Bxp2NJTVX97icU0GmCXF6pK23H8/edit#gid=0)!

A Mac M2 Max is 5-6x faster than a M1 for inference due to the larger GPU memory bandwidth.

![Image description](/assets/images/llama_t_put-c6f0ea201a6dd508999170325cd6804a.png)

![Image description](/assets/images/llama_t_put-c6f0ea201a6dd508999170325cd6804a.png)

## Quickstart[​](#quickstart "Direct link to Quickstart")

[`Ollama`](https://ollama.ai/) is one way to easily run inference on macOS.

The instructions [here](/docs/guides/docs/integrations/llms/ollama) provide details, which we summarize:

- [Download and run](https://ollama.ai/download) the app
- From command line, fetch a model from this [list of options](https://github.com/jmorganca/ollama): e.g., `ollama pull llama2`
- When the app is running, all models are automatically served on `localhost:11434`

```python
from langchain.llms import Ollama  
llm = Ollama(model="llama2")  
llm("The first man on the moon was ...")  

```

```text
 ' The first man on the moon was Neil Armstrong, who landed on the moon on July 20, 1969 as part of the Apollo 11 mission. obviously.'  

```

Stream tokens as they are being generated.

```python
from langchain.callbacks.manager import CallbackManager  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler   
llm = Ollama(model="llama2",   
 callback\_manager = CallbackManager([StreamingStdOutCallbackHandler()]))  
llm("The first man on the moon was ...")  

```

```text
 The first man to walk on the moon was Neil Armstrong, an American astronaut who was part of the Apollo 11 mission in 1969. февруари 20, 1969, Armstrong stepped out of the lunar module Eagle and onto the moon's surface, famously declaring "That's one small step for man, one giant leap for mankind" as he took his first steps. He was followed by fellow astronaut Edwin "Buzz" Aldrin, who also walked on the moon during the mission.  
  
  
  
  
 ' The first man to walk on the moon was Neil Armstrong, an American astronaut who was part of the Apollo 11 mission in 1969. февруари 20, 1969, Armstrong stepped out of the lunar module Eagle and onto the moon\'s surface, famously declaring "That\'s one small step for man, one giant leap for mankind" as he took his first steps. He was followed by fellow astronaut Edwin "Buzz" Aldrin, who also walked on the moon during the mission.'  

```

## Environment[​](#environment "Direct link to Environment")

Inference speed is a challenge when running models locally (see above).

To minimize latency, it is desirable to run models locally on GPU, which ships with many consumer laptops [e.g., Apple devices](https://www.apple.com/newsroom/2022/06/apple-unveils-m2-with-breakthrough-performance-and-capabilities/).

And even with GPU, the available GPU memory bandwidth (as noted above) is important.

### Running Apple silicon GPU[​](#running-apple-silicon-gpu "Direct link to Running Apple silicon GPU")

`Ollama` will automatically utilize the GPU on Apple devices.

Other frameworks require the user to set up the environment to utilize the Apple GPU.

For example, `llama.cpp` python bindings can be configured to use the GPU via [Metal](https://developer.apple.com/metal/).

Metal is a graphics and compute API created by Apple providing near-direct access to the GPU.

See the [`llama.cpp`](/docs/guides/docs/integrations/llms/llamacpp) setup [here](https://github.com/abetlen/llama-cpp-python/blob/main/docs/install/macos.md) to enable this.

In particular, ensure that conda is using the correct virtual environment that you created (`miniforge3`).

E.g., for me:

```text
conda activate /Users/rlm/miniforge3/envs/llama  

```

With the above confirmed, then:

```text
CMAKE\_ARGS="-DLLAMA\_METAL=on" FORCE\_CMAKE=1 pip install -U llama-cpp-python --no-cache-dir  

```

## LLMs[​](#llms "Direct link to LLMs")

There are various ways to gain access to quantized model weights.

1. [`HuggingFace`](https://huggingface.co/TheBloke) - Many quantized model are available for download and can be run with framework such as [`llama.cpp`](https://github.com/ggerganov/llama.cpp)
1. [`gpt4all`](https://gpt4all.io/index.html) - The model explorer offers a leaderboard of metrics and associated quantized models available for download
1. [`Ollama`](https://github.com/jmorganca/ollama) - Several models can be accessed directly via `pull`

### Ollama[​](#ollama "Direct link to Ollama")

With [Ollama](/docs/guides/docs/integrations/llms/ollama), fetch a model via `ollama pull <model family>:<tag>`:

- E.g., for Llama-7b: `ollama pull llama2` will download the most basic version of the model (e.g., smallest # parameters and 4 bit quantization)
- We can also specify a particular version from the [model list](https://github.com/jmorganca/ollama), e.g., `ollama pull llama2:13b`
- See the full set of parameters on the [API reference page](https://api.python.langchain.com/en/latest/llms/langchain.llms.ollama.Ollama.html)

```python
from langchain.llms import Ollama  
llm = Ollama(model="llama2:13b")  
llm("The first man on the moon was ... think step by step")  

```

```text
 ' Sure! Here\'s the answer, broken down step by step:\n\nThe first man on the moon was... Neil Armstrong.\n\nHere\'s how I arrived at that answer:\n\n1. The first manned mission to land on the moon was Apollo 11.\n2. The mission included three astronauts: Neil Armstrong, Edwin "Buzz" Aldrin, and Michael Collins.\n3. Neil Armstrong was the mission commander and the first person to set foot on the moon.\n4. On July 20, 1969, Armstrong stepped out of the lunar module Eagle and onto the moon\'s surface, famously declaring "That\'s one small step for man, one giant leap for mankind."\n\nSo, the first man on the moon was Neil Armstrong!'  

```

### Llama.cpp[​](#llamacpp "Direct link to Llama.cpp")

Llama.cpp is compatible with a [broad set of models](https://github.com/ggerganov/llama.cpp).

For example, below we run inference on `llama2-13b` with 4 bit quantization downloaded from [HuggingFace](https://huggingface.co/TheBloke/Llama-2-13B-GGML/tree/main).

As noted above, see the [API reference](https://api.python.langchain.com/en/latest/llms/langchain.llms.llamacpp.LlamaCpp.html?highlight=llamacpp#langchain.llms.llamacpp.LlamaCpp) for the full set of parameters.

From the [llama.cpp docs](https://python.langchain.com/docs/integrations/llms/llamacpp), a few are worth commenting on:

`n_gpu_layers`: number of layers to be loaded into GPU memory

- Value: 1
- Meaning: Only one layer of the model will be loaded into GPU memory (1 is often sufficient).

`n_batch`: number of tokens the model should process in parallel

- Value: n_batch
- Meaning: It's recommended to choose a value between 1 and n_ctx (which in this case is set to 2048)

`n_ctx`: Token context window .

- Value: 2048
- Meaning: The model will consider a window of 2048 tokens at a time

`f16_kv`: whether the model should use half-precision for the key/value cache

- Value: True
- Meaning: The model will use half-precision, which can be more memory efficient; Metal only supports True.

```python
CMAKE\_ARGS="-DLLAMA\_METAL=on" FORCE\_CMAKE=1 pip install -U llama-cpp-python --no-cache-dirclear  

```

```python
from langchain.llms import LlamaCpp  
llm = LlamaCpp(  
 model\_path="/Users/rlm/Desktop/Code/llama.cpp/models/openorca-platypus2-13b.gguf.q4\_0.bin",  
 n\_gpu\_layers=1,  
 n\_batch=512,  
 n\_ctx=2048,  
 f16\_kv=True,   
 callback\_manager=CallbackManager([StreamingStdOutCallbackHandler()]),  
 verbose=True,  
)  

```

The console log will show the below to indicate Metal was enabled properly from steps above:

```text
ggml\_metal\_init: allocating  
ggml\_metal\_init: using MPS  

```

```python
llm("The first man on the moon was ... Let's think step by step")  

```

```text
 Llama.generate: prefix-match hit  
  
  
 and use logical reasoning to figure out who the first man on the moon was.  
   
 Here are some clues:  
   
 1. The first man on the moon was an American.  
 2. He was part of the Apollo 11 mission.  
 3. He stepped out of the lunar module and became the first person to set foot on the moon's surface.  
 4. His last name is Armstrong.  
   
 Now, let's use our reasoning skills to figure out who the first man on the moon was. Based on clue #1, we know that the first man on the moon was an American. Clue #2 tells us that he was part of the Apollo 11 mission. Clue #3 reveals that he was the first person to set foot on the moon's surface. And finally, clue #4 gives us his last name: Armstrong.  
 Therefore, the first man on the moon was Neil Armstrong!  
  
   
 llama\_print\_timings: load time = 9623.21 ms  
 llama\_print\_timings: sample time = 143.77 ms / 203 runs ( 0.71 ms per token, 1412.01 tokens per second)  
 llama\_print\_timings: prompt eval time = 485.94 ms / 7 tokens ( 69.42 ms per token, 14.40 tokens per second)  
 llama\_print\_timings: eval time = 6385.16 ms / 202 runs ( 31.61 ms per token, 31.64 tokens per second)  
 llama\_print\_timings: total time = 7279.28 ms  
  
  
  
  
  
 " and use logical reasoning to figure out who the first man on the moon was.\n\nHere are some clues:\n\n1. The first man on the moon was an American.\n2. He was part of the Apollo 11 mission.\n3. He stepped out of the lunar module and became the first person to set foot on the moon's surface.\n4. His last name is Armstrong.\n\nNow, let's use our reasoning skills to figure out who the first man on the moon was. Based on clue #1, we know that the first man on the moon was an American. Clue #2 tells us that he was part of the Apollo 11 mission. Clue #3 reveals that he was the first person to set foot on the moon's surface. And finally, clue #4 gives us his last name: Armstrong.\nTherefore, the first man on the moon was Neil Armstrong!"  

```

### GPT4All[​](#gpt4all "Direct link to GPT4All")

We can use model weights downloaded from [GPT4All](https://python.langchain.com/docs/integrations/llms/gpt4all) model explorer.

Similar to what is shown above, we can run inference and use [the API reference](https://api.python.langchain.com/en/latest/llms/langchain.llms.gpt4all.GPT4All.html?highlight=gpt4all#langchain.llms.gpt4all.GPT4All) to set parameters of interest.

```python
pip install gpt4all  

```

```python
from langchain.llms import GPT4All  
llm = GPT4All(model="/Users/rlm/Desktop/Code/gpt4all/models/nous-hermes-13b.ggmlv3.q4\_0.bin")  

```

```python
llm("The first man on the moon was ... Let's think step by step")  

```

```text
 ".\n1) The United States decides to send a manned mission to the moon.2) They choose their best astronauts and train them for this specific mission.3) They build a spacecraft that can take humans to the moon, called the Lunar Module (LM).4) They also create a larger spacecraft, called the Saturn V rocket, which will launch both the LM and the Command Service Module (CSM), which will carry the astronauts into orbit.5) The mission is planned down to the smallest detail: from the trajectory of the rockets to the exact movements of the astronauts during their moon landing.6) On July 16, 1969, the Saturn V rocket launches from Kennedy Space Center in Florida, carrying the Apollo 11 mission crew into space.7) After one and a half orbits around the Earth, the LM separates from the CSM and begins its descent to the moon's surface.8) On July 20, 1969, at 2:56 pm EDT (GMT-4), Neil Armstrong becomes the first man on the moon. He speaks these"  

```

## Prompts[​](#prompts "Direct link to Prompts")

Some LLMs will benefit from specific prompts.

For example, LLaMA will use [special tokens](https://twitter.com/RLanceMartin/status/1681879318493003776?s=20).

We can use `ConditionalPromptSelector` to set prompt based on the model type.

```python
# Set our LLM  
llm = LlamaCpp(  
 model\_path="/Users/rlm/Desktop/Code/llama.cpp/models/openorca-platypus2-13b.gguf.q4\_0.bin",  
 n\_gpu\_layers=1,  
 n\_batch=512,  
 n\_ctx=2048,  
 f16\_kv=True,   
 callback\_manager=CallbackManager([StreamingStdOutCallbackHandler()]),  
 verbose=True,  
)  

```

Set the associated prompt based upon the model version.

```python
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
from langchain.chains.prompt\_selector import ConditionalPromptSelector  
  
DEFAULT\_LLAMA\_SEARCH\_PROMPT = PromptTemplate(  
 input\_variables=["question"],  
 template="""<<SYS>> \n You are an assistant tasked with improving Google search \  
results. \n <</SYS>> \n\n [INST] Generate THREE Google search queries that \  
are similar to this question. The output should be a numbered list of questions \  
and each should have a question mark at the end: \n\n {question} [/INST]""",  
)  
  
DEFAULT\_SEARCH\_PROMPT = PromptTemplate(  
 input\_variables=["question"],  
 template="""You are an assistant tasked with improving Google search \  
results. Generate THREE Google search queries that are similar to \  
this question. The output should be a numbered list of questions and each \  
should have a question mark at the end: {question}""",  
)  
  
QUESTION\_PROMPT\_SELECTOR = ConditionalPromptSelector(  
 default\_prompt=DEFAULT\_SEARCH\_PROMPT,  
 conditionals=[  
 (lambda llm: isinstance(llm, LlamaCpp), DEFAULT\_LLAMA\_SEARCH\_PROMPT)  
 ],  
 )  
  
prompt = QUESTION\_PROMPT\_SELECTOR.get\_prompt(llm)  
prompt  

```

```text
 PromptTemplate(input\_variables=['question'], output\_parser=None, partial\_variables={}, template='<<SYS>> \n You are an assistant tasked with improving Google search results. \n <</SYS>> \n\n [INST] Generate THREE Google search queries that are similar to this question. The output should be a numbered list of questions and each should have a question mark at the end: \n\n {question} [/INST]', template\_format='f-string', validate\_template=True)  

```

```python
# Chain  
llm\_chain = LLMChain(prompt=prompt,llm=llm)  
question = "What NFL team won the Super Bowl in the year that Justin Bieber was born?"  
llm\_chain.run({"question":question})  

```

```text
 Sure! Here are three similar search queries with a question mark at the end:  
   
 1. Which NBA team did LeBron James lead to a championship in the year he was drafted?  
 2. Who won the Grammy Awards for Best New Artist and Best Female Pop Vocal Performance in the same year that Lady Gaga was born?  
 3. What MLB team did Babe Ruth play for when he hit 60 home runs in a single season?  
  
   
 llama\_print\_timings: load time = 14943.19 ms  
 llama\_print\_timings: sample time = 72.93 ms / 101 runs ( 0.72 ms per token, 1384.87 tokens per second)  
 llama\_print\_timings: prompt eval time = 14942.95 ms / 93 tokens ( 160.68 ms per token, 6.22 tokens per second)  
 llama\_print\_timings: eval time = 3430.85 ms / 100 runs ( 34.31 ms per token, 29.15 tokens per second)  
 llama\_print\_timings: total time = 18578.26 ms  
  
  
  
  
  
 ' Sure! Here are three similar search queries with a question mark at the end:\n\n1. Which NBA team did LeBron James lead to a championship in the year he was drafted?\n2. Who won the Grammy Awards for Best New Artist and Best Female Pop Vocal Performance in the same year that Lady Gaga was born?\n3. What MLB team did Babe Ruth play for when he hit 60 home runs in a single season?'  

```

We also can use the LangChain Prompt Hub to fetch and / or store prompts that are model specific.

This will work with your [LangSmith API key](https://docs.smith.langchain.com/).

For example, [here](https://smith.langchain.com/hub/rlm/rag-prompt-llama) is a prompt for RAG with LLaMA-specific tokens.

## Use cases[​](#use-cases "Direct link to Use cases")

Given an `llm` created from one of the models above, you can use it for [many use cases](/docs/guides/docs/use_cases).

For example, here is a guide to [RAG](/docs/guides/docs/use_cases/question_answering/local_retrieval_qa) with local LLMs.

In general, use cases for local LLMs can be driven by at least two factors:

- `Privacy`: private data (e.g., journals, etc) that a user does not want to share
- `Cost`: text preprocessing (extraction/tagging), summarization, and agent simulations are token-use-intensive tasks

In addition, [here](https://blog.langchain.dev/using-langsmith-to-support-fine-tuning-of-open-source-llms/) is an overview on fine-tuning, which can utilize open-source LLMs.

- [Use case](#use-case)

- [Overview](#overview)

  - [Open-source LLMs](#open-source-llms)
  - [Inference](#inference)

- [Quickstart](#quickstart)

- [Environment](#environment)

  - [Running Apple silicon GPU](#running-apple-silicon-gpu)

- [LLMs](#llms)

  - [Ollama](#ollama)
  - [Llama.cpp](#llamacpp)
  - [GPT4All](#gpt4all)

- [Prompts](#prompts)

- [Use cases](#use-cases)

- [Open-source LLMs](#open-source-llms)

- [Inference](#inference)

- [Running Apple silicon GPU](#running-apple-silicon-gpu)

- [Ollama](#ollama)

- [Llama.cpp](#llamacpp)

- [GPT4All](#gpt4all)
