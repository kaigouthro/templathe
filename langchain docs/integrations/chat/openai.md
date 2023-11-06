# OpenAI

This notebook covers how to get started with OpenAI chat models.

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
chat = ChatOpenAI(temperature=0)  

```

The above cell assumes that your OpenAI API key is set in your environment variables. If you would rather manually specify your API key and/or organization ID, use the following code:

```python
chat = ChatOpenAI(temperature=0, openai\_api\_key="YOUR\_API\_KEY", openai\_organization="YOUR\_ORGANIZATION\_ID")  

```

Remove the openai_organization parameter should it not apply to you.

```python
messages = [  
 SystemMessage(  
 content="You are a helpful assistant that translates English to French."  
 ),  
 HumanMessage(  
 content="Translate this sentence from English to French. I love programming."  
 ),  
]  
chat(messages)  

```

```text
 AIMessage(content="J'adore la programmation.", additional\_kwargs={}, example=False)  

```

You can make use of templating by using a `MessagePromptTemplate`. You can build a `ChatPromptTemplate` from one or more `MessagePromptTemplates`. You can use `ChatPromptTemplate`'s `format_prompt` -- this returns a `PromptValue`, which you can convert to a string or Message object, depending on whether you want to use the formatted value as input to an llm or chat model.

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
 input\_language="English", output\_language="French", text="I love programming."  
 ).to\_messages()  
)  

```

```text
 AIMessage(content="J'adore la programmation.", additional\_kwargs={}, example=False)  

```

## Fine-tuning[​](#fine-tuning "Direct link to Fine-tuning")

You can call fine-tuned OpenAI models by passing in your corresponding `modelName` parameter.

This generally takes the form of `ft:{OPENAI_MODEL_NAME}:{ORG_NAME}::{MODEL_ID}`. For example:

```python
fine\_tuned\_model = ChatOpenAI(temperature=0, model\_name="ft:gpt-3.5-turbo-0613:langchain::7qTVM5AR")  
  
fine\_tuned\_model(messages)  

```

```text
 AIMessage(content="J'adore la programmation.", additional\_kwargs={}, example=False)  

```

- [Fine-tuning](#fine-tuning)
