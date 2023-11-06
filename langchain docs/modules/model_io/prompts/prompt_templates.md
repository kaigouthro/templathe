# Prompt templates

Prompt templates are pre-defined recipes for generating prompts for language models.

A template may include instructions, few-shot examples, and specific context and
questions appropriate for a given task.

LangChain provides tooling to create and work with prompt templates.

LangChain strives to create model agnostic templates to make it easy to reuse
existing templates across different language models.

Typically, language models expect the prompt to either be a string or else a list of chat messages.

## `PromptTemplate`[​](#prompttemplate "Direct link to prompttemplate")

Use `PromptTemplate` to create a template for a string prompt.

By default, `PromptTemplate` uses [Python's str.format](https://docs.python.org/3/library/stdtypes.html#str.format)
syntax for templating.

```python
from langchain.prompts import PromptTemplate  
  
prompt\_template = PromptTemplate.from\_template(  
 "Tell me a {adjective} joke about {content}."  
)  
prompt\_template.format(adjective="funny", content="chickens")  

```

```text
 'Tell me a funny joke about chickens.'  

```

The template supports any number of variables, including no variables:n

```python
from langchain.prompts import PromptTemplate  
  
prompt\_template = PromptTemplate.from\_template(  
"Tell me a joke"  
)  
prompt\_template.format()  

```

```text
 'Tell me a joke'  

```

For additional validation, specify `input_variables` explicitly. These variables
will be compared against the variables present in the template string during instantiation, **raising an exception if
there is a mismatch**. For example:

```python
from langchain.prompts import PromptTemplate  
  
invalid\_prompt = PromptTemplate(  
 input\_variables=["adjective"],  
 template="Tell me a {adjective} joke about {content}."  
)  

```

```text
 ---------------------------------------------------------------------------  
  
 ValidationError Traceback (most recent call last)  
  
 Cell In[19], line 3  
 1 from langchain.prompts import PromptTemplate  
 ----> 3 invalid\_prompt = PromptTemplate(  
 4 input\_variables=["adjective"],  
 5 template="Tell me a {adjective} joke about {content}."  
 6 )  
  
  
 File ~/langchain/libs/langchain/langchain/load/serializable.py:97, in Serializable.\_\_init\_\_(self, \*\*kwargs)  
 96 def \_\_init\_\_(self, \*\*kwargs: Any) -> None:  
 ---> 97 super().\_\_init\_\_(\*\*kwargs)  
 98 self.\_lc\_kwargs = kwargs  
  
  
 File ~/langchain/.venv/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.\_\_init\_\_()  
  
  
 ValidationError: 1 validation error for PromptTemplate  
 \_\_root\_\_  
 Invalid prompt schema; check for mismatched or missing input parameters. 'content' (type=value\_error)  

```

You can create custom prompt templates that format the prompt in any way you want.
For more information, see [Custom Prompt Templates](/docs/modules/model_io/prompts/prompt_templates/custom_prompt_template.html).

## `ChatPromptTemplate`[​](#chatprompttemplate "Direct link to chatprompttemplate")

The prompt to [chat models](/docs/modules/model_io/prompts/models/chat) is a list of chat messages.

Each chat message is associated with content, and an additional parameter called `role`.
For example, in the OpenAI [Chat Completions API](https://platform.openai.com/docs/guides/chat/introduction), a chat message can be associated with an AI assistant, a human or a system role.

Create a chat prompt template like this:

```python
from langchain.prompts import ChatPromptTemplate  
  
chat\_template = ChatPromptTemplate.from\_messages([  
 ("system", "You are a helpful AI bot. Your name is {name}."),  
 ("human", "Hello, how are you doing?"),  
 ("ai", "I'm doing well, thanks!"),  
 ("human", "{user\_input}"),  
])  
  
messages = chat\_template.format\_messages(  
 name="Bob",  
 user\_input="What is your name?"  
)  

```

`ChatPromptTemplate.from_messages` accepts a variety of message representations.

For example, in addition to using the 2-tuple representation of (type, content) used
above, you could pass in an instance of `MessagePromptTemplate` or `BaseMessage`.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.prompts import HumanMessagePromptTemplate  
from langchain.schema.messages import SystemMessage  
  
chat\_template = ChatPromptTemplate.from\_messages(  
 [  
 SystemMessage(  
 content=(  
 "You are a helpful assistant that re-writes the user's text to "  
 "sound more upbeat."  
 )  
 ),  
 HumanMessagePromptTemplate.from\_template("{text}"),  
 ]  
)  
  
llm = ChatOpenAI()  
llm(chat\_template.format\_messages(text='i dont like eating tasty things.'))  

```

```text
 AIMessage(content='I absolutely love indulging in delicious treats!')  

```

This provides you with a lot of flexibility in how you construct your chat prompts.

## LCEL[​](#lcel "Direct link to LCEL")

`PromptTemplate` and `ChatPromptTemplate` implement the [Runnable interface](/docs/expression_language/interface), the basic building block of the [LangChain Expression Language (LCEL)](/docs/expression_language/). This means they support `invoke`, `ainvoke`, `stream`, `astream`, `batch`, `abatch`, `astream_log` calls.

`PromptTemplate` accepts a dictionary (of the prompt variables) and returns a `StringPromptValue`. A `ChatPromptTemplate` accepts a dictionary and returns a `ChatPromptValue`.

```python
prompt\_val = prompt\_template.invoke({"adjective": "funny", "content": "chickens"})  
prompt\_val  

```

```text
 StringPromptValue(text='Tell me a joke')  

```

```python
prompt\_val.to\_string()  

```

```text
 'Tell me a joke'  

```

```python
prompt\_val.to\_messages()  

```

```text
 [HumanMessage(content='Tell me a joke')]  

```

```python
chat\_val = chat\_template.invoke({"text": 'i dont like eating tasty things.'})  

```

```python
chat\_val.to\_messages()  

```

```text
 [SystemMessage(content="You are a helpful assistant that re-writes the user's text to sound more upbeat."),  
 HumanMessage(content='i dont like eating tasty things.')]  

```

```python
chat\_val.to\_string()  

```

```text
 "System: You are a helpful assistant that re-writes the user's text to sound more upbeat.\nHuman: i dont like eating tasty things."  

```

- [`PromptTemplate`](#prompttemplate)
- [`ChatPromptTemplate`](#chatprompttemplate)
- [LCEL](#lcel)
