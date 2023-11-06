# Prompts

Prompts for chat models are built around messages, instead of just plain text.

You can make use of templating by using a `MessagePromptTemplate`. You can build a `ChatPromptTemplate` from one or more `MessagePromptTemplates`. You can use `ChatPromptTemplate`'s `format_prompt` -- this returns a `PromptValue`, which you can convert to a string or Message object, depending on whether you want to use the formatted value as input to an llm or chat model.

For convenience, there is a `from_template` method defined on the template. If you were to use this template, this is what it would look like:

```python
from langchain.prompts import PromptTemplate  
from langchain.prompts.chat import (  
 ChatPromptTemplate,  
 SystemMessagePromptTemplate,  
 AIMessagePromptTemplate,  
 HumanMessagePromptTemplate,  
)  
  
template="You are a helpful assistant that translates {input\_language} to {output\_language}."  
system\_message\_prompt = SystemMessagePromptTemplate.from\_template(template)  
human\_template="{text}"  
human\_message\_prompt = HumanMessagePromptTemplate.from\_template(human\_template)  

```

```python
chat\_prompt = ChatPromptTemplate.from\_messages([system\_message\_prompt, human\_message\_prompt])  
  
# get a chat completion from the formatted messages  
chat(chat\_prompt.format\_prompt(input\_language="English", output\_language="French", text="I love programming.").to\_messages())  

```

```text
 AIMessage(content="J'adore la programmation.", additional\_kwargs={})  

```

If you wanted to construct the MessagePromptTemplate more directly, you could create a PromptTemplate outside and then pass it in, e.g.:

```python
prompt=PromptTemplate(  
 template="You are a helpful assistant that translates {input\_language} to {output\_language}.",  
 input\_variables=["input\_language", "output\_language"],  
)  
system\_message\_prompt = SystemMessagePromptTemplate(prompt=prompt)  

```
