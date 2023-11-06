# Configuration

Oftentimes you may want to experiment with, or even expose to the end user, multiple different ways of doing things.
In order to make this experience as easy as possible, we have defined two methods.

First, a `configurable_fields` method.
This lets you configure particular fields of a runnable.

Second, a `configurable_alternatives` method.
With this method, you can list out alternatives for any particular runnable that can be set during runtime.

## Configuration Fields[​](#configuration-fields "Direct link to Configuration Fields")

### With LLMs[​](#with-llms "Direct link to With LLMs")

With LLMs we can configure things like temperature

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.prompts import PromptTemplate  
  
model = ChatOpenAI(temperature=0).configurable\_fields(  
 temperature=ConfigurableField(  
 id="llm\_temperature",  
 name="LLM Temperature",  
 description="The temperature of the LLM",  
 )  
)  

```

```python
model.invoke("pick a random number")  

```

```text
 AIMessage(content='7')  

```

```python
model.with\_config(configurable={"llm\_temperature": .9}).invoke("pick a random number")  

```

```text
 AIMessage(content='34')  

```

We can also do this when its used as part of a chain

```python
prompt = PromptTemplate.from\_template("Pick a random number above {x}")  
chain = prompt | model  

```

```python
chain.invoke({"x": 0})  

```

```text
 AIMessage(content='57')  

```

```python
chain.with\_config(configurable={"llm\_temperature": .9}).invoke({"x": 0})  

```

```text
 AIMessage(content='6')  

```

### With HubRunnables[​](#with-hubrunnables "Direct link to With HubRunnables")

This is useful to allow for switching of prompts

```python
from langchain.runnables.hub import HubRunnable  

```

```python
prompt = HubRunnable("rlm/rag-prompt").configurable\_fields(  
 owner\_repo\_commit=ConfigurableField(  
 id="hub\_commit",  
 name="Hub Commit",  
 description="The Hub commit to pull from",  
 )  
)  

```

```python
prompt.invoke({"question": "foo", "context": "bar"})  

```

```text
 ChatPromptValue(messages=[HumanMessage(content="You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\nQuestion: foo \nContext: bar \nAnswer:")])  

```

```python
prompt.with\_config(configurable={"hub\_commit": "rlm/rag-prompt-llama"}).invoke({"question": "foo", "context": "bar"})  

```

```text
 ChatPromptValue(messages=[HumanMessage(content="[INST]<<SYS>> You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.<</SYS>> \nQuestion: foo \nContext: bar \nAnswer: [/INST]")])  

```

## Configurable Alternatives[​](#configurable-alternatives "Direct link to Configurable Alternatives")

### With LLMs[​](#with-llms-1 "Direct link to With LLMs")

Let's take a look at doing this with LLMs

```python
from langchain.chat\_models import ChatOpenAI, ChatAnthropic  
from langchain.schema.runnable import ConfigurableField  
from langchain.prompts import PromptTemplate  

```

```python
llm = ChatAnthropic(temperature=0).configurable\_alternatives(  
 # This gives this field an id  
 # When configuring the end runnable, we can then use this id to configure this field  
 ConfigurableField(id="llm"),  
 # This sets a default\_key.  
 # If we specify this key, the default LLM (ChatAnthropic initialized above) will be used  
 default\_key="anthropic",  
 # This adds a new option, with name `openai` that is equal to `ChatOpenAI()`  
 openai=ChatOpenAI(),  
 # This adds a new option, with name `gpt4` that is equal to `ChatOpenAI(model="gpt-4")`  
 gpt4=ChatOpenAI(model="gpt-4"),  
 # You can add more configuration options here  
)  
prompt = PromptTemplate.from\_template("Tell me a joke about {topic}")  
chain = prompt | llm  

```

```python
# By default it will call Anthropic  
chain.invoke({"topic": "bears"})  

```

```text
 AIMessage(content=" Here's a silly joke about bears:\n\nWhat do you call a bear with no teeth?\nA gummy bear!")  

```

```python
# We can use `.with\_config(configurable={"llm": "openai"})` to specify an llm to use  
chain.with\_config(configurable={"llm": "openai"}).invoke({"topic": "bears"})  

```

```text
 AIMessage(content="Sure, here's a bear joke for you:\n\nWhy don't bears wear shoes?\n\nBecause they already have bear feet!")  

```

```python
# If we use the `default\_key` then it uses the default  
chain.with\_config(configurable={"llm": "anthropic"}).invoke({"topic": "bears"})  

```

```text
 AIMessage(content=" Here's a silly joke about bears:\n\nWhat do you call a bear with no teeth?\nA gummy bear!")  

```

### With Prompts[​](#with-prompts "Direct link to With Prompts")

We can do a similar thing, but alternate between prompts

```python
llm = ChatAnthropic(temperature=0)  
prompt = PromptTemplate.from\_template("Tell me a joke about {topic}").configurable\_alternatives(  
 # This gives this field an id  
 # When configuring the end runnable, we can then use this id to configure this field  
 ConfigurableField(id="prompt"),  
 # This sets a default\_key.  
 # If we specify this key, the default LLM (ChatAnthropic initialized above) will be used  
 default\_key="joke",  
 # This adds a new option, with name `poem`  
 poem=PromptTemplate.from\_template("Write a short poem about {topic}"),  
 # You can add more configuration options here  
)  
chain = prompt | llm  

```

```python
# By default it will write a joke  
chain.invoke({"topic": "bears"})  

```

```text
 AIMessage(content=" Here's a silly joke about bears:\n\nWhat do you call a bear with no teeth?\nA gummy bear!")  

```

```python
# We can configure it write a poem  
chain.with\_config(configurable={"prompt": "poem"}).invoke({"topic": "bears"})  

```

```text
 AIMessage(content=' Here is a short poem about bears:\n\nThe bears awaken from their sleep\nAnd lumber out into the deep\nForests filled with trees so tall\nForaging for food before nightfall \nTheir furry coats and claws so sharp\nSniffing for berries and fish to nab\nLumbering about without a care\nThe mighty grizzly and black bear\nProud creatures, wild and free\nRuling their domain majestically\nWandering the woods they call their own\nBefore returning to their dens alone')  

```

### With Prompts and LLMs[​](#with-prompts-and-llms "Direct link to With Prompts and LLMs")

We can also have multiple things configurable!
Here's an example doing that with both prompts and LLMs.

```python
llm = ChatAnthropic(temperature=0).configurable\_alternatives(  
 # This gives this field an id  
 # When configuring the end runnable, we can then use this id to configure this field  
 ConfigurableField(id="llm"),  
 # This sets a default\_key.  
 # If we specify this key, the default LLM (ChatAnthropic initialized above) will be used  
 default\_key="anthropic",  
 # This adds a new option, with name `openai` that is equal to `ChatOpenAI()`  
 openai=ChatOpenAI(),  
 # This adds a new option, with name `gpt4` that is equal to `ChatOpenAI(model="gpt-4")`  
 gpt4=ChatOpenAI(model="gpt-4"),  
 # You can add more configuration options here  
)  
prompt = PromptTemplate.from\_template("Tell me a joke about {topic}").configurable\_alternatives(  
 # This gives this field an id  
 # When configuring the end runnable, we can then use this id to configure this field  
 ConfigurableField(id="prompt"),  
 # This sets a default\_key.  
 # If we specify this key, the default LLM (ChatAnthropic initialized above) will be used  
 default\_key="joke",  
 # This adds a new option, with name `poem`  
 poem=PromptTemplate.from\_template("Write a short poem about {topic}"),  
 # You can add more configuration options here  
)  
chain = prompt | llm  

```

```python
# We can configure it write a poem with OpenAI  
chain.with\_config(configurable={"prompt": "poem", "llm": "openai"}).invoke({"topic": "bears"})  

```

```text
 AIMessage(content="In the forest, where tall trees sway,\nA creature roams, both fierce and gray.\nWith mighty paws and piercing eyes,\nThe bear, a symbol of strength, defies.\n\nThrough snow-kissed mountains, it does roam,\nA guardian of its woodland home.\nWith fur so thick, a shield of might,\nIt braves the coldest winter night.\n\nA gentle giant, yet wild and free,\nThe bear commands respect, you see.\nWith every step, it leaves a trace,\nOf untamed power and ancient grace.\n\nFrom honeyed feast to salmon's leap,\nIt takes its place, in nature's keep.\nA symbol of untamed delight,\nThe bear, a wonder, day and night.\n\nSo let us honor this noble beast,\nIn forests where its soul finds peace.\nFor in its presence, we come to know,\nThe untamed spirit that in us also flows.")  

```

```python
# We can always just configure only one if we want  
chain.with\_config(configurable={"llm": "openai"}).invoke({"topic": "bears"})  

```

```text
 AIMessage(content="Sure, here's a bear joke for you:\n\nWhy don't bears wear shoes?\n\nBecause they have bear feet!")  

```

### Saving configurations[​](#saving-configurations "Direct link to Saving configurations")

We can also easily save configured chains as their own objects

```python
openai\_poem = chain.with\_config(configurable={"llm": "openai"})  

```

```python
openai\_poem.invoke({"topic": "bears"})  

```

```text
 AIMessage(content="Why don't bears wear shoes?\n\nBecause they have bear feet!")  

```

- [Configuration Fields](#configuration-fields)

  - [With LLMs](#with-llms)
  - [With HubRunnables](#with-hubrunnables)

- [Configurable Alternatives](#configurable-alternatives)

  - [With LLMs](#with-llms-1)
  - [With Prompts](#with-prompts)
  - [With Prompts and LLMs](#with-prompts-and-llms)
  - [Saving configurations](#saving-configurations)

- [With LLMs](#with-llms)

- [With HubRunnables](#with-hubrunnables)

- [With LLMs](#with-llms-1)

- [With Prompts](#with-prompts)

- [With Prompts and LLMs](#with-prompts-and-llms)

- [Saving configurations](#saving-configurations)
