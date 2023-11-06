# Memory in LLMChain

This notebook goes over how to use the Memory class with an `LLMChain`.

We will add the [ConversationBufferMemory](https://api.python.langchain.com/en/latest/memory/langchain.memory.buffer.ConversationBufferMemory.html#langchain.memory.buffer.ConversationBufferMemory) class, although this can be any memory class.

```python
from langchain.chains import LLMChain  
from langchain.llms import OpenAI  
from langchain.memory import ConversationBufferMemory  
from langchain.prompts import PromptTemplate  

```

The most important step is setting up the prompt correctly. In the below prompt, we have two input keys: one for the actual input, another for the input from the Memory class. Importantly, we make sure the keys in the `PromptTemplate` and the `ConversationBufferMemory` match up (`chat_history`).

```python
template = """You are a chatbot having a conversation with a human.  
  
{chat\_history}  
Human: {human\_input}  
Chatbot:"""  
  
prompt = PromptTemplate(  
 input\_variables=["chat\_history", "human\_input"], template=template  
)  
memory = ConversationBufferMemory(memory\_key="chat\_history")  

```

```python
llm = OpenAI()  
llm\_chain = LLMChain(  
 llm=llm,  
 prompt=prompt,  
 verbose=True,  
 memory=memory,  
)  

```

```python
llm\_chain.predict(human\_input="Hi there my friend")  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 You are a chatbot having a conversation with a human.  
   
   
 Human: Hi there my friend  
 Chatbot:  
   
 > Finished chain.  
  
  
  
  
  
 ' Hi there! How can I help you today?'  

```

```python
llm\_chain.predict(human\_input="Not too bad - how are you?")  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 You are a chatbot having a conversation with a human.  
   
 Human: Hi there my friend  
 AI: Hi there! How can I help you today?  
 Human: Not too bad - how are you?  
 Chatbot:  
   
 > Finished chain.  
  
  
  
  
  
 " I'm doing great, thanks for asking! How are you doing?"  

```

## Adding Memory to a chat model-based `LLMChain`[​](#adding-memory-to-a-chat-model-based-llmchain "Direct link to adding-memory-to-a-chat-model-based-llmchain")

The above works for completion-style `LLM`s, but if you are using a chat model, you will likely get better performance using structured chat messages. Below is an example.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.schema import SystemMessage  
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder  

```

We will use the [ChatPromptTemplate](https://api.python.langchain.com/en/latest/prompts/langchain.prompts.chat.ChatPromptTemplate.html) class to set up the chat prompt.

The [from_messages](https://api.python.langchain.com/en/latest/prompts/langchain.prompts.chat.ChatPromptTemplate.html#langchain.prompts.chat.ChatPromptTemplate.from_messages) method creates a `ChatPromptTemplate` from a list of messages (e.g., `SystemMessage`, `HumanMessage`, `AIMessage`, `ChatMessage`, etc.) or message templates, such as the [MessagesPlaceholder](https://api.python.langchain.com/en/latest/prompts/langchain.prompts.chat.MessagesPlaceholder.html#langchain.prompts.chat.MessagesPlaceholder) below.

The configuration below makes it so the memory will be injected to the middle of the chat prompt, in the `chat_history` key, and the user's inputs will be added in a human/user message to the end of the chat prompt.

```python
prompt = ChatPromptTemplate.from\_messages([  
 SystemMessage(content="You are a chatbot having a conversation with a human."), # The persistent system prompt  
 MessagesPlaceholder(variable\_name="chat\_history"), # Where the memory will be stored.  
 HumanMessagePromptTemplate.from\_template("{human\_input}"), # Where the human input will injected  
])  
   
memory = ConversationBufferMemory(memory\_key="chat\_history", return\_messages=True)  

```

```python
llm = ChatOpenAI()  
  
chat\_llm\_chain = LLMChain(  
 llm=llm,  
 prompt=prompt,  
 verbose=True,  
 memory=memory,  
)  

```

```python
chat\_llm\_chain.predict(human\_input="Hi there my friend")  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 System: You are a chatbot having a conversation with a human.  
 Human: Hi there my friend  
   
 > Finished chain.  
  
  
  
  
  
 'Hello! How can I assist you today, my friend?'  

```

```python
chat\_llm\_chain.predict(human\_input="Not too bad - how are you?")  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 System: You are a chatbot having a conversation with a human.  
 Human: Hi there my friend  
 AI: Hello! How can I assist you today, my friend?  
 Human: Not too bad - how are you?  
   
 > Finished chain.  
  
  
  
  
  
 "I'm an AI chatbot, so I don't have feelings, but I'm here to help and chat with you! Is there something specific you would like to talk about or any questions I can assist you with?"  

```

- [Adding Memory to a chat model-based `LLMChain`](#adding-memory-to-a-chat-model-based-llmchain)
