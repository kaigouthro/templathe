# Google Cloud Vertex AI

Note: This is separate from the Google PaLM integration. Google has chosen to offer an enterprise version of PaLM through GCP, and this supports the models made available through there.

By default, Google Cloud [does not use](https://cloud.google.com/vertex-ai/docs/generative-ai/data-governance#foundation_model_development) Customer Data to train its foundation models as part of Google Cloud\`s AI/ML Privacy Commitment. More details about how Google processes data can also be found in [Google's Customer Data Processing Addendum (CDPA)](https://cloud.google.com/terms/data-processing-addendum).

To use Vertex AI PaLM you must have the `google-cloud-aiplatform` Python package installed and either:

- Have credentials configured for your environment (gcloud, workload identity, etc...)
- Store the path to a service account JSON file as the GOOGLE_APPLICATION_CREDENTIALS environment variable

This codebase uses the `google.auth` library which first looks for the application credentials variable mentioned above, and then looks for system-level auth.

For more information, see:

- <https://cloud.google.com/docs/authentication/application-default-credentials#GAC>
- <https://googleapis.dev/python/google-auth/latest/reference/google.auth.html#module-google.auth>

```python
#!pip install langchain google-cloud-aiplatform  

```

```python
from langchain.chat\_models import ChatVertexAI  
from langchain.prompts import ChatPromptTemplate  

```

```python
chat = ChatVertexAI()  

```

```python
system = "You are a helpful assistant who translate English to French"  
human = "Translate this sentence from English to French. I love programming."  
prompt = ChatPromptTemplate.from\_messages(  
 [("system", system), ("human", human)]  
)  
messages = prompt.format\_messages()  

```

```python
chat(messages)  

```

```text
 AIMessage(content=" J'aime la programmation.", additional\_kwargs={}, example=False)  

```

If we want to construct a simple chain that takes user specified parameters:

```python
system = "You are a helpful assistant that translates {input\_language} to {output\_language}."  
human = "{text}"  
prompt = ChatPromptTemplate.from\_messages(  
 [("system", system), ("human", human)]  
)  

```

```python
chain = prompt | chat  
chain.invoke(  
 {"input\_language": "English", "output\_language": "Japanese", "text": "I love programming"}  
)  

```

```text
 AIMessage(content=' 私はプログラミングが大好きです。', additional\_kwargs={}, example=False)  

```

## Code generation chat models[​](#code-generation-chat-models "Direct link to Code generation chat models")

You can now leverage the Codey API for code chat within Vertex AI. The model name is:

- codechat-bison: for code assistance

```python
chat = ChatVertexAI(  
 model\_name="codechat-bison",  
 max\_output\_tokens=1000,  
 temperature=0.5  
)  

```

```python
# For simple string in string out usage, we can use the `predict` method:  
print(chat.predict("Write a Python function to identify all prime numbers"))  

```

````text
 ```python  
 def is\_prime(x):   
 if (x <= 1):   
 return False  
 for i in range(2, x):   
 if (x % i == 0):   
 return False  
 return True  
````

````


Asynchronous calls[​](#asynchronous-calls "Direct link to Asynchronous calls")
------------------------------------------------------------------------------



We can make asynchronous calls via the `agenerate` and `ainvoke` methods.




```python
import asyncio  
# import nest\_asyncio  
# nest\_asyncio.apply()  

````

```python
chat = ChatVertexAI(  
 model\_name="chat-bison",  
 max\_output\_tokens=1000,  
 temperature=0.7,  
 top\_p=0.95,  
 top\_k=40,  
)  
  
asyncio.run(chat.agenerate([messages]))  

```

```text
 LLMResult(generations=[[ChatGeneration(text=" J'aime la programmation.", generation\_info=None, message=AIMessage(content=" J'aime la programmation.", additional\_kwargs={}, example=False))]], llm\_output={}, run=[RunInfo(run\_id=UUID('223599ef-38f8-4c79-ac6d-a5013060eb9d'))])  

```

```python
asyncio.run(chain.ainvoke({"input\_language": "English", "output\_language": "Sanskrit", "text": "I love programming"}))  

```

```text
 AIMessage(content=' अहं प्रोग्रामिंग प्रेमामि', additional\_kwargs={}, example=False)  

```

## Streaming calls[​](#streaming-calls "Direct link to Streaming calls")

We can also stream outputs via the `stream` method:

```python
import sys  

```

```python
prompt = ChatPromptTemplate.from\_messages([("human", "List out the 15 most populous countries in the world")])  
messages = prompt.format\_messages()  
for chunk in chat.stream(messages):  
 sys.stdout.write(chunk.content)  
 sys.stdout.flush()  

```

```text
 1. China (1,444,216,107)  
 2. India (1,393,409,038)  
 3. United States (332,403,650)  
 4. Indonesia (273,523,615)  
 5. Pakistan (220,892,340)  
 6. Brazil (212,559,409)  
 7. Nigeria (206,139,589)  
 8. Bangladesh (164,689,383)  
 9. Russia (145,934,462)  
 10. Mexico (128,932,488)  
 11. Japan (126,476,461)  
 12. Ethiopia (115,063,982)  
 13. Philippines (109,581,078)  
 14. Egypt (102,334,404)  
 15. Vietnam (97,338,589)  

```

- [Code generation chat models](#code-generation-chat-models)
- [Asynchronous calls](#asynchronous-calls)
- [Streaming calls](#streaming-calls)
