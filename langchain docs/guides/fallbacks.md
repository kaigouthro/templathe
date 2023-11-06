# Fallbacks

When working with language models, you may often encounter issues from the underlying APIs, whether these be rate limiting or downtime. Therefore, as you go to move your LLM applications into production it becomes more and more important to safeguard against these. That's why we've introduced the concept of fallbacks.

A **fallback** is an alternative plan that may be used in an emergency.

Crucially, fallbacks can be applied not only on the LLM level but on the whole runnable level. This is important because often times different models require different prompts. So if your call to OpenAI fails, you don't just want to send the same prompt to Anthropic - you probably want to use a different prompt template and send a different version there.

## Fallback for LLM API Errors[​](#fallback-for-llm-api-errors "Direct link to Fallback for LLM API Errors")

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
 content=" I don't actually know why the kangaroo crossed the road, but I can take a guess! Here are some possible reasons:\n\n- To get to the other side (the classic joke answer!)\n\n- It was trying to find some food or water \n\n- It was trying to find a mate during mating season\n\n- It was fleeing from a predator or perceived threat\n\n- It was disoriented and crossed accidentally \n\n- It was following a herd of other kangaroos who were crossing\n\n- It wanted a change of scenery or environment \n\n- It was trying to reach a new habitat or territory\n\nThe real reason is unknown without more context, but hopefully one of those potential explanations does the joke justice! Let me know if you have any other animal jokes I can try to decipher." additional\_kwargs={} example=False  

```

## Fallback for Sequences[​](#fallback-for-sequences "Direct link to Fallback for Sequences")

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

## Fallback for Long Inputs[​](#fallback-for-long-inputs "Direct link to Fallback for Long Inputs")

One of the big limiting factors of LLMs is their context window. Usually, you can count and track the length of prompts before sending them to an LLM, but in situations where that is hard/complicated, you can fallback to a model with a longer context length.

```python
short\_llm = ChatOpenAI()  
long\_llm = ChatOpenAI(model="gpt-3.5-turbo-16k")  
llm = short\_llm.with\_fallbacks([long\_llm])  

```

```python
inputs = "What is the next number: " + ", ".join(["one", "two"] \* 3000)  

```

```python
try:  
 print(short\_llm.invoke(inputs))  
except Exception as e:  
 print(e)  

```

```text
 This model's maximum context length is 4097 tokens. However, your messages resulted in 12012 tokens. Please reduce the length of the messages.  

```

```python
try:  
 print(llm.invoke(inputs))  
except Exception as e:  
 print(e)  

```

```text
 content='The next number in the sequence is two.' additional\_kwargs={} example=False  

```

## Fallback to Better Model[​](#fallback-to-better-model "Direct link to Fallback to Better Model")

Often times we ask models to output format in a specific format (like JSON). Models like GPT-3.5 can do this okay, but sometimes struggle. This naturally points to fallbacks - we can try with GPT-3.5 (faster, cheaper), but then if parsing fails we can use GPT-4.

```python
from langchain.output\_parsers import DatetimeOutputParser  

```

```python
prompt = ChatPromptTemplate.from\_template(  
 "what time was {event} (in %Y-%m-%dT%H:%M:%S.%fZ format - only return this value)"  
)  

```

```python
# In this case we are going to do the fallbacks on the LLM + output parser level  
# Because the error will get raised in the OutputParser  
openai\_35 = ChatOpenAI() | DatetimeOutputParser()  
openai\_4 = ChatOpenAI(model="gpt-4")| DatetimeOutputParser()  

```

```python
only\_35 = prompt | openai\_35   
fallback\_4 = prompt | openai\_35.with\_fallbacks([openai\_4])  

```

```python
try:  
 print(only\_35.invoke({"event": "the superbowl in 1994"}))  
except Exception as e:  
 print(f"Error: {e}")  

```

```text
 Error: Could not parse datetime string: The Super Bowl in 1994 took place on January 30th at 3:30 PM local time. Converting this to the specified format (%Y-%m-%dT%H:%M:%S.%fZ) results in: 1994-01-30T15:30:00.000Z  

```

```python
try:  
 print(fallback\_4.invoke({"event": "the superbowl in 1994"}))  
except Exception as e:  
 print(f"Error: {e}")  

```

```text
 1994-01-30 15:30:00  

```

- [Fallback for LLM API Errors](#fallback-for-llm-api-errors)
- [Fallback for Sequences](#fallback-for-sequences)
- [Fallback for Long Inputs](#fallback-for-long-inputs)
- [Fallback to Better Model](#fallback-to-better-model)
