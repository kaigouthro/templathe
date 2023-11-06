# Motörhead

[Motörhead](https://github.com/getmetal/motorhead) is a memory server implemented in Rust. It automatically handles incremental summarization in the background and allows for stateless applications.

## Setup[​](#setup "Direct link to Setup")

See instructions at [Motörhead](https://github.com/getmetal/motorhead) for running the server locally.

```python
from langchain.memory.motorhead\_memory import MotorheadMemory  

```

## Example[​](#example "Direct link to Example")

```python
from langchain.llms import OpenAI  
from langchain.chains import LLMChain  
from langchain.prompts import PromptTemplate  
  
template = """You are a chatbot having a conversation with a human.  
  
{chat\_history}  
Human: {human\_input}  
AI:"""  
  
prompt = PromptTemplate(  
 input\_variables=["chat\_history", "human\_input"], template=template  
)  
memory = MotorheadMemory(  
 session\_id="testing-1", url="http://localhost:8080", memory\_key="chat\_history"  
)  
  
await memory.init()  
# loads previous state from Motörhead 🤘  
  
llm\_chain = LLMChain(  
 llm=OpenAI(),  
 prompt=prompt,  
 verbose=True,  
 memory=memory,  
)  

```

```python
llm\_chain.run("hi im bob")  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 You are a chatbot having a conversation with a human.  
   
   
 Human: hi im bob  
 AI:  
   
 > Finished chain.  
  
  
  
  
  
 ' Hi Bob, nice to meet you! How are you doing today?'  

```

```python
llm\_chain.run("whats my name?")  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 You are a chatbot having a conversation with a human.  
   
 Human: hi im bob  
 AI: Hi Bob, nice to meet you! How are you doing today?  
 Human: whats my name?  
 AI:  
   
 > Finished chain.  
  
  
  
  
  
 ' You said your name is Bob. Is that correct?'  

```

```python
llm\_chain.run("whats for dinner?")  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 You are a chatbot having a conversation with a human.  
   
 Human: hi im bob  
 AI: Hi Bob, nice to meet you! How are you doing today?  
 Human: whats my name?  
 AI: You said your name is Bob. Is that correct?  
 Human: whats for dinner?  
 AI:  
   
 > Finished chain.  
  
  
  
  
  
 " I'm sorry, I'm not sure what you're asking. Could you please rephrase your question?"  

```

- [Setup](#setup)
- [Example](#example)
