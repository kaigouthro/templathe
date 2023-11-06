# Bittensor

[Bittensor](https://bittensor.com/) is a mining network, similar to Bitcoin, that includes built-in incentives designed to encourage miners to contribute compute + knowledge.

`NIBittensorLLM` is developed by [Neural Internet](https://neuralinternet.ai/), powered by `Bittensor`.

This LLM showcases true potential of decentralized AI by giving you the best response(s) from the `Bittensor protocol`, which consist of various AI models such as `OpenAI`, `LLaMA2` etc.

Users can view their logs, requests, and API keys on the [Validator Endpoint Frontend](https://api.neuralinternet.ai/). However, changes to the configuration are currently prohibited; otherwise, the user's queries will be blocked.

If you encounter any difficulties or have any questions, please feel free to reach out to our developer on [GitHub](https://github.com/Kunj-2206), [Discord](https://discordapp.com/users/683542109248159777) or join our discord server for latest update and queries [Neural Internet](https://discord.gg/neuralinternet).

## Different Parameter and response handling for NIBittensorLLM[​](#different-parameter-and-response-handling-for-nibittensorllm "Direct link to Different Parameter and response handling for NIBittensorLLM")

```python
from langchain.llms import NIBittensorLLM  
import json  
from pprint import pprint  
  
from langchain.globals import set\_debug  
  
set\_debug(True)  
  
# System parameter in NIBittensorLLM is optional but you can set whatever you want to perform with model  
llm\_sys = NIBittensorLLM(  
 system\_prompt="Your task is to determine response based on user prompt.Explain me like I am technical lead of a project"  
)  
sys\_resp = llm\_sys(  
 "What is bittensor and What are the potential benefits of decentralized AI?"  
)  
print(f"Response provided by LLM with system prompt set is : {sys\_resp}")  
  
# The top\_responses parameter can give multiple responses based on its parameter value  
# This below code retrive top 10 miner's response all the response are in format of json  
  
# Json response structure is  
""" {  
 "choices": [  
 {"index": Bittensor's Metagraph index number,  
 "uid": Unique Identifier of a miner,  
 "responder\_hotkey": Hotkey of a miner,  
 "message":{"role":"assistant","content": Contains actual response},  
 "response\_ms": Time in millisecond required to fetch response from a miner}   
 ]  
 } """  
  
multi\_response\_llm = NIBittensorLLM(top\_responses=10)  
multi\_resp = multi\_response\_llm("What is Neural Network Feeding Mechanism?")  
json\_multi\_resp = json.loads(multi\_resp)  
pprint(json\_multi\_resp)  

```

## Using NIBittensorLLM with LLMChain and PromptTemplate[​](#using-nibittensorllm-with-llmchain-and-prompttemplate "Direct link to Using NIBittensorLLM with LLMChain and PromptTemplate")

```python
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
from langchain.llms import NIBittensorLLM  
  
from langchain.globals import set\_debug  
  
set\_debug(True)  
  
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  
  
# System parameter in NIBittensorLLM is optional but you can set whatever you want to perform with model  
llm = NIBittensorLLM(system\_prompt="Your task is to determine response based on user prompt.")  
  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
question = "What is bittensor?"  
  
llm\_chain.run(question)  

```

## Using NIBittensorLLM with Conversational Agent and Google Search Tool[​](#using-nibittensorllm-with-conversational-agent-and-google-search-tool "Direct link to Using NIBittensorLLM with Conversational Agent and Google Search Tool")

```python
from langchain.agents import (  
 AgentType,  
 initialize\_agent,  
 load\_tools,  
 ZeroShotAgent,  
 Tool,  
 AgentExecutor,  
)  
from langchain.memory import ConversationBufferMemory  
from langchain.chains import LLMChain  
from langchain.prompts import PromptTemplate  
from langchain.utilities import GoogleSearchAPIWrapper, SerpAPIWrapper  
from langchain.llms import NIBittensorLLM  
  
memory = ConversationBufferMemory(memory\_key="chat\_history")  
  
  
prefix = """Answer prompt based on LLM if there is need to search something then use internet and observe internet result and give accurate reply of user questions also try to use authenticated sources"""  
suffix = """Begin!  
 {chat\_history}  
 Question: {input}  
 {agent\_scratchpad}"""  
  
prompt = ZeroShotAgent.create\_prompt(  
 tools,  
 prefix=prefix,  
 suffix=suffix,  
 input\_variables=["input", "chat\_history", "agent\_scratchpad"],  
)  
  
llm = NIBittensorLLM(system\_prompt="Your task is to determine response based on user prompt")  
  
llm\_chain = LLMChain(llm=llm, prompt=prompt)  
  
memory = ConversationBufferMemory(memory\_key="chat\_history")  
  
agent = ZeroShotAgent(llm\_chain=llm\_chain, tools=tools, verbose=True)  
agent\_chain = AgentExecutor.from\_agent\_and\_tools(  
 agent=agent, tools=tools, verbose=True, memory=memory  
)  
  
response = agent\_chain.run(input=prompt)  

```

- [Different Parameter and response handling for NIBittensorLLM](#different-parameter-and-response-handling-for-nibittensorllm)
- [Using NIBittensorLLM with LLMChain and PromptTemplate](#using-nibittensorllm-with-llmchain-and-prompttemplate)
- [Using NIBittensorLLM with Conversational Agent and Google Search Tool](#using-nibittensorllm-with-conversational-agent-and-google-search-tool)
