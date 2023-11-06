# OpenAI Adapter

A lot of people get started with OpenAI but want to explore other models. LangChain's integrations with many model providers make this easy to do so. While LangChain has it's own message and model APIs, we've also made it as easy as possible to explore other models by exposing an adapter to adapt LangChain models to the OpenAI api.

At the moment this only deals with output and does not return other information (token counts, stop reasons, etc).

```python
import openai  
from langchain.adapters import openai as lc\_openai  

```

## ChatCompletion.create[​](#chatcompletioncreate "Direct link to ChatCompletion.create")

```python
messages = [{"role": "user", "content": "hi"}]  

```

Original OpenAI call

```python
result = openai.ChatCompletion.create(  
 messages=messages,   
 model="gpt-3.5-turbo",   
 temperature=0  
)  

```

```python
result["choices"][0]['message'].to\_dict\_recursive()  

```

```text
 {'role': 'assistant', 'content': 'Hello! How can I assist you today?'}  

```

LangChain OpenAI wrapper call

```python
lc\_result = lc\_openai.ChatCompletion.create(  
 messages=messages,   
 model="gpt-3.5-turbo",   
 temperature=0  
)  

```

```python
lc\_result["choices"][0]['message']  

```

```text
 {'role': 'assistant', 'content': 'Hello! How can I assist you today?'}  

```

Swapping out model providers

```python
lc\_result = lc\_openai.ChatCompletion.create(  
 messages=messages,   
 model="claude-2",   
 temperature=0,   
 provider="ChatAnthropic"  
)  

```

```python
lc\_result["choices"][0]['message']  

```

```text
 {'role': 'assistant', 'content': ' Hello!'}  

```

## ChatCompletion.stream[​](#chatcompletionstream "Direct link to ChatCompletion.stream")

Original OpenAI call

```python
for c in openai.ChatCompletion.create(  
 messages = messages,  
 model="gpt-3.5-turbo",   
 temperature=0,  
 stream=True  
):  
 print(c["choices"][0]['delta'].to\_dict\_recursive())  

```

```text
 {'role': 'assistant', 'content': ''}  
 {'content': 'Hello'}  
 {'content': '!'}  
 {'content': ' How'}  
 {'content': ' can'}  
 {'content': ' I'}  
 {'content': ' assist'}  
 {'content': ' you'}  
 {'content': ' today'}  
 {'content': '?'}  
 {}  

```

LangChain OpenAI wrapper call

```python
for c in lc\_openai.ChatCompletion.create(  
 messages = messages,  
 model="gpt-3.5-turbo",   
 temperature=0,  
 stream=True  
):  
 print(c["choices"][0]['delta'])  

```

```text
 {'role': 'assistant', 'content': ''}  
 {'content': 'Hello'}  
 {'content': '!'}  
 {'content': ' How'}  
 {'content': ' can'}  
 {'content': ' I'}  
 {'content': ' assist'}  
 {'content': ' you'}  
 {'content': ' today'}  
 {'content': '?'}  
 {}  

```

Swapping out model providers

```python
for c in lc\_openai.ChatCompletion.create(  
 messages = messages,  
 model="claude-2",   
 temperature=0,  
 stream=True,  
 provider="ChatAnthropic",  
):  
 print(c["choices"][0]['delta'])  

```

```text
 {'role': 'assistant', 'content': ' Hello'}  
 {'content': '!'}  
 {}  

```

- [ChatCompletion.create](#chatcompletioncreate)
- [ChatCompletion.stream](#chatcompletionstream)
