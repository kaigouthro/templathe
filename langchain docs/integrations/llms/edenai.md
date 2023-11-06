# Eden AI

Eden AI is revolutionizing the AI landscape by uniting the best AI providers, empowering users to unlock limitless possibilities and tap into the true potential of artificial intelligence. With an all-in-one comprehensive and hassle-free platform, it allows users to deploy AI features to production lightning fast, enabling effortless access to the full breadth of AI capabilities via a single API. (website: <https://edenai.co/>)

This example goes over how to use LangChain to interact with Eden AI models

Accessing the EDENAI's API requires an API key,

which you can get by creating an account <https://app.edenai.run/user/register> and heading here <https://app.edenai.run/admin/account/settings>

Once we have a key we'll want to set it as an environment variable by running:

```python
export EDENAI\_API\_KEY="..."  

```

If you'd prefer not to set an environment variable you can pass the key in directly via the edenai_api_key named parameter

when initiating the EdenAI LLM class:

```python
from langchain.llms import EdenAI  

```

```python
llm = EdenAI(edenai\_api\_key="...",provider="openai", temperature=0.2, max\_tokens=250)  

```

## Calling a model[​](#calling-a-model "Direct link to Calling a model")

The EdenAI API brings together various providers, each offering multiple models.

To access a specific model, you can simply add 'model' during instantiation.

For instance, let's explore the models provided by OpenAI, such as GPT3.5

### text generation[​](#text-generation "Direct link to text generation")

```python
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
llm=EdenAI(feature="text",provider="openai",model="text-davinci-003",temperature=0.2, max\_tokens=250)  
  
prompt = """  
User: Answer the following yes/no question by reasoning step by step. Can a dog drive a car?  
Assistant:  
"""  
  
llm(prompt)  

```

### image generation[​](#image-generation "Direct link to image generation")

```python
import base64  
from io import BytesIO  
from PIL import Image  
import json  
def print\_base64\_image(base64\_string):  
 # Decode the base64 string into binary data  
 decoded\_data = base64.b64decode(base64\_string)  
  
 # Create an in-memory stream to read the binary data  
 image\_stream = BytesIO(decoded\_data)  
  
 # Open the image using PIL  
 image = Image.open(image\_stream)  
  
 # Display the image  
 image.show()  

```

```python
text2image = EdenAI(  
 feature="image" ,  
 provider= "openai",  
 resolution="512x512"  
)  

```

```python
image\_output = text2image("A cat riding a motorcycle by Picasso")  

```

```python
print\_base64\_image(image\_output)  

```

### text generation with callback[​](#text-generation-with-callback "Direct link to text generation with callback")

```python
from langchain.llms import EdenAI  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  
  
llm = EdenAI(  
 callbacks=[StreamingStdOutCallbackHandler()],  
 feature="text",provider="openai", temperature=0.2,max\_tokens=250  
)  
prompt = """  
User: Answer the following yes/no question by reasoning step by step. Can a dog drive a car?  
Assistant:  
"""  
print(llm(prompt))  

```

## Chaining Calls[​](#chaining-calls "Direct link to Chaining Calls")

```python
from langchain.chains import SimpleSequentialChain  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
llm = EdenAI(  
feature="text", provider="openai", temperature=0.2, max\_tokens=250  
)  
text2image = EdenAI(  
feature="image", provider="openai", resolution="512x512"  
)  

```

```python
prompt = PromptTemplate(  
 input\_variables=["product"],  
 template="What is a good name for a company that makes {product}?",  
)  
  
chain = LLMChain(llm=llm, prompt=prompt)  

```

```python
second\_prompt = PromptTemplate(  
 input\_variables=["company\_name"],  
 template="Write a description of a logo for this company: {company\_name}, the logo should not contain text at all ",  
)  
chain\_two = LLMChain(llm=llm, prompt=second\_prompt)  

```

```python
third\_prompt = PromptTemplate(  
 input\_variables=["company\_logo\_description"],  
 template="{company\_logo\_description}",  
)  
chain\_three = LLMChain(llm=text2image, prompt=third\_prompt)  

```

```python
# Run the chain specifying only the input variable for the first chain.  
overall\_chain = SimpleSequentialChain(  
 chains=[chain, chain\_two, chain\_three],verbose=True  
)  
output = overall\_chain.run("hats")  

```

```python
#print the image  
print\_base64\_image(output)  

```

- [Calling a model](#calling-a-model)

  - [text generation](#text-generation)
  - [image generation](#image-generation)
  - [text generation with callback](#text-generation-with-callback)

- [Chaining Calls](#chaining-calls)

- [text generation](#text-generation)

- [image generation](#image-generation)

- [text generation with callback](#text-generation-with-callback)
