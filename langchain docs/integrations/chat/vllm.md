# vLLM Chat

vLLM can be deployed as a server that mimics the OpenAI API protocol. This allows vLLM to be used as a drop-in replacement for applications using OpenAI API. This server can be queried in the same format as OpenAI API.

This notebook covers how to get started with vLLM chat models using langchain's `ChatOpenAI` **as it is**.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.prompts.chat import (  
 ChatPromptTemplate,  
 SystemMessagePromptTemplate,  
 AIMessagePromptTemplate,  
 HumanMessagePromptTemplate,  
)  
from langchain.schema import AIMessage, HumanMessage, SystemMessage  

```

```python
inference\_server\_url = "http://localhost:8000/v1"  
  
chat = ChatOpenAI(  
 model="mosaicml/mpt-7b",  
 openai\_api\_key="EMPTY",  
 openai\_api\_base=inference\_server\_url,  
 max\_tokens=5,  
 temperature=0,  
)  

```

```python
messages = [  
 SystemMessage(  
 content="You are a helpful assistant that translates English to Italian."  
 ),  
 HumanMessage(  
 content="Translate the following sentence from English to Italian: I love programming."  
 ),  
]  
chat(messages)  

```

```text
 AIMessage(content=' Io amo programmare', additional\_kwargs={}, example=False)  

```

You can make use of templating by using a `MessagePromptTemplate`. You can build a `ChatPromptTemplate` from one or more `MessagePromptTemplates`. You can use ChatPromptTemplate's format_prompt -- this returns a `PromptValue`, which you can convert to a string or `Message` object, depending on whether you want to use the formatted value as input to an llm or chat model.

For convenience, there is a `from_template` method exposed on the template. If you were to use this template, this is what it would look like:

```python
template = (  
 "You are a helpful assistant that translates {input\_language} to {output\_language}."  
)  
system\_message\_prompt = SystemMessagePromptTemplate.from\_template(template)  
human\_template = "{text}"  
human\_message\_prompt = HumanMessagePromptTemplate.from\_template(human\_template)  

```

```python
chat\_prompt = ChatPromptTemplate.from\_messages(  
 [system\_message\_prompt, human\_message\_prompt]  
)  
  
# get a chat completion from the formatted messages  
chat(  
 chat\_prompt.format\_prompt(  
 input\_language="English", output\_language="Italian", text="I love programming."  
 ).to\_messages()  
)  

```

```text
 AIMessage(content=' I love programming too.', additional\_kwargs={}, example=False)  

```
