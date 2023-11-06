# Add fallbacks

There are many possible points of failure in an LLM application, whether that be issues with LLM API's, poor model outputs, issues with other integrations, etc. Fallbacks help you gracefully handle and isolate these issues.

Crucially, fallbacks can be applied not only on the LLM level but on the whole runnable level.

## Handling LLM API Errors[​](#handling-llm-api-errors "Direct link to Handling LLM API Errors")

This is maybe the most common use case for fallbacks. A request to an LLM API can fail for a variety of reasons - the API could be down, you could have hit rate limits, any number of things. Therefore, using fallbacks can help protect against these types of things.

IMPORTANT: By default, a lot of the LLM wrappers catch errors and retry. You will most likely want to turn those off when working with fallbacks. Otherwise the first wrapper will keep on retrying and not failing.

```python
from langchain.chat\_models import ChatOpenAI, ChatAnthropic  

```

First, let's mock out what happens if we hit a RateLimitError from OpenAI

```python
from unittest.mock import patch  
from openai.error import RateLimitError  

```

```python
# Note that we set max\_retries = 0 to avoid retrying on RateLimits, etc  
openai\_llm = ChatOpenAI(max\_retries=0)  
anthropic\_llm = ChatAnthropic()  
llm = openai\_llm.with\_fallbacks([anthropic\_llm])  

```

```python
# Let's use just the OpenAI LLm first, to show that we run into an error  
with patch('openai.ChatCompletion.create', side\_effect=RateLimitError()):  
 try:  
 print(openai\_llm.invoke("Why did the chicken cross the road?"))  
 except:  
 print("Hit error")  

```

```text
 Hit error  

```

```python
# Now let's try with fallbacks to Anthropic  
with patch('openai.ChatCompletion.create', side\_effect=RateLimitError()):  
 try:  
 print(llm.invoke("Why did the chicken cross the road?"))  
 except:  
 print("Hit error")  

```

```text
 content=' I don\'t actually know why the chicken crossed the road, but here are some possible humorous answers:\n\n- To get to the other side!\n\n- It was too chicken to just stand there. \n\n- It wanted a change of scenery.\n\n- It wanted to show the possum it could be done.\n\n- It was on its way to a poultry farmers\' convention.\n\nThe joke plays on the double meaning of "the other side" - literally crossing the road to the other side, or the "other side" meaning the afterlife. So it\'s an anti-joke, with a silly or unexpected pun as the answer.' additional\_kwargs={} example=False  

```

We can use our "LLM with Fallbacks" as we would a normal LLM.

```python
from langchain.prompts import ChatPromptTemplate  
  
prompt = ChatPromptTemplate.from\_messages(  
 [  
 ("system", "You're a nice assistant who always includes a compliment in your response"),  
 ("human", "Why did the {animal} cross the road"),  
 ]  
)  
chain = prompt | llm  
with patch('openai.ChatCompletion.create', side\_effect=RateLimitError()):  
 try:  
 print(chain.invoke({"animal": "kangaroo"}))  
 except:  
 print("Hit error")  

```

```text
 content=" I don't actually know why the kangaroo crossed the road, but I'm happy to take a guess! Maybe the kangaroo was trying to get to the other side to find some tasty grass to eat. Or maybe it was trying to get away from a predator or other danger. Kangaroos do need to cross roads and other open areas sometimes as part of their normal activities. Whatever the reason, I'm sure the kangaroo looked both ways before hopping across!" additional\_kwargs={} example=False  

```

### Specifying errors to handle[​](#specifying-errors-to-handle "Direct link to Specifying errors to handle")

We can also specify the errors to handle if we want to be more specific about when the fallback is invoked:

```python
llm = openai\_llm.with\_fallbacks([anthropic\_llm], exceptions\_to\_handle=(KeyboardInterrupt,))  
  
chain = prompt | llm  
with patch('openai.ChatCompletion.create', side\_effect=RateLimitError()):  
 try:  
 print(chain.invoke({"animal": "kangaroo"}))  
 except:  
 print("Hit error")  

```

```text
 Hit error  

```

## Fallbacks for Sequences[​](#fallbacks-for-sequences "Direct link to Fallbacks for Sequences")

We can also create fallbacks for sequences, that are sequences themselves. Here we do that with two different models: ChatOpenAI and then normal OpenAI (which does not use a chat model). Because OpenAI is NOT a chat model, you likely want a different prompt.

```python
# First let's create a chain with a ChatModel  
# We add in a string output parser here so the outputs between the two are the same type  
from langchain.schema.output\_parser import StrOutputParser  
  
chat\_prompt = ChatPromptTemplate.from\_messages(  
 [  
 ("system", "You're a nice assistant who always includes a compliment in your response"),  
 ("human", "Why did the {animal} cross the road"),  
 ]  
)  
# Here we're going to use a bad model name to easily create a chain that will error  
chat\_model = ChatOpenAI(model\_name="gpt-fake")  
bad\_chain = chat\_prompt | chat\_model | StrOutputParser()  

```

```python
# Now lets create a chain with the normal OpenAI model  
from langchain.llms import OpenAI  
from langchain.prompts import PromptTemplate  
  
prompt\_template = """Instructions: You should always include a compliment in your response.  
  
Question: Why did the {animal} cross the road?"""  
prompt = PromptTemplate.from\_template(prompt\_template)  
llm = OpenAI()  
good\_chain = prompt | llm  

```

```python
# We can now create a final chain which combines the two  
chain = bad\_chain.with\_fallbacks([good\_chain])  
chain.invoke({"animal": "turtle"})  

```

```text
 '\n\nAnswer: The turtle crossed the road to get to the other side, and I have to say he had some impressive determination.'  

```

- [Handling LLM API Errors](#handling-llm-api-errors)

  - [Specifying errors to handle](#specifying-errors-to-handle)

- [Fallbacks for Sequences](#fallbacks-for-sequences)

- [Specifying errors to handle](#specifying-errors-to-handle)
