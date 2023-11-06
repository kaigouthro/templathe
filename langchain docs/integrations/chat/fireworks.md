# Fireworks

[Fireworks](https://app.fireworks.ai/) accelerates product development on generative AI by creating an innovative AI experiment and production platform.

This example goes over how to use LangChain to interact with `ChatFireworks` models.

```python
from langchain.chat\_models.fireworks import ChatFireworks  
from langchain.schema import SystemMessage, HumanMessage  
import os  

```

# Setup

1. Make sure the `fireworks-ai` package is installed in your environment.
1. Sign in to [Fireworks AI](http://fireworks.ai) for the an API Key to access our models, and make sure it is set as the `FIREWORKS_API_KEY` environment variable.
1. Set up your model using a model id. If the model is not set, the default model is fireworks-llama-v2-7b-chat. See the full, most up-to-date model list on [app.fireworks.ai](https://app.fireworks.ai).

```python
import os  
import getpass  
  
if "FIREWORKS\_API\_KEY" not in os.environ:  
 os.environ["FIREWORKS\_API\_KEY"] = getpass.getpass("Fireworks API Key:")  
  
# Initialize a Fireworks chat model  
chat = ChatFireworks(model="accounts/fireworks/models/llama-v2-13b-chat")  

```

# Calling the Model Directly

You can call the model directly with a system and human message to get answers.

```python
# ChatFireworks Wrapper  
system\_message = SystemMessage(content="You are to chat with the user.")  
human\_message = HumanMessage(content="Who are you?")  
  
chat([system\_message, human\_message])  

```

```text
 AIMessage(content="Hello! My name is LLaMA, I'm a large language model trained by a team of researcher at Meta AI. My primary function is to assist and converse with users like you, answering questions and engaging in discussion to the best of my ability. I'm here to help and provide information on a wide range of topics, so feel free to ask me anything!", additional\_kwargs={}, example=False)  

```

```python
# Setting additional parameters: temperature, max\_tokens, top\_p  
chat = ChatFireworks(model="accounts/fireworks/models/llama-v2-13b-chat", model\_kwargs={"temperature":1, "max\_tokens": 20, "top\_p": 1})  
system\_message = SystemMessage(content="You are to chat with the user.")  
human\_message = HumanMessage(content="How's the weather today?")  
chat([system\_message, human\_message])  

```

```text
 AIMessage(content="Oh hello there! \*giggle\* It's such a beautiful day today, isn", additional\_kwargs={}, example=False)  

```

# Simple Chat Chain

You can use chat models on fireworks, with system prompts and memory.

```python
from langchain.chat\_models import ChatFireworks  
from langchain.memory import ConversationBufferMemory  
from langchain.schema.runnable import RunnablePassthrough  
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder  
  
llm = ChatFireworks(model="accounts/fireworks/models/llama-v2-13b-chat", model\_kwargs={"temperature":0, "max\_tokens":64, "top\_p":1.0})  
prompt = ChatPromptTemplate.from\_messages([  
 ("system", "You are a helpful chatbot that speaks like a pirate."),  
 MessagesPlaceholder(variable\_name="history"),  
 ("human", "{input}")  
])  

```

Initially, there is no chat memory

```python
memory = ConversationBufferMemory(return\_messages=True)  
memory.load\_memory\_variables({})  

```

```text
 {'history': []}  

```

Create a simple chain with memory

```python
chain = RunnablePassthrough.assign(  
 history=memory.load\_memory\_variables | (lambda x: x["history"])  
) | prompt | llm.bind(stop=["\n\n"])  

```

Run the chain with a simple question, expecting an answer aligned with the system message provided.

```python
inputs = {"input": "hi im bob"}  
response = chain.invoke(inputs)  
response  

```

```text
 AIMessage(content="Ahoy there, me hearty! Yer a fine lookin' swashbuckler, I can see that! \*adjusts eye patch\* What be bringin' ye to these waters? Are ye here to plunder some booty or just to enjoy the sea breeze?", additional\_kwargs={}, example=False)  

```

Save the memory context, then read it back to inspect contents

```python
memory.save\_context(inputs, {"output": response.content})  
memory.load\_memory\_variables({})  

```

```text
 {'history': [HumanMessage(content='hi im bob', additional\_kwargs={}, example=False),  
 AIMessage(content="Ahoy there, me hearty! Yer a fine lookin' swashbuckler, I can see that! \*adjusts eye patch\* What be bringin' ye to these waters? Are ye here to plunder some booty or just to enjoy the sea breeze?", additional\_kwargs={}, example=False)]}  

```

Now as another question that requires use of the memory.

```python
inputs = {"input": "whats my name"}  
chain.invoke(inputs)  

```

```text
 AIMessage(content="Arrrr, ye be askin' about yer name, eh? Well, me matey, I be knowin' ye as Bob, the scurvy dog! \*winks\* But if ye want me to call ye somethin' else, just let me know, and I", additional\_kwargs={}, example=False)  

```
