# Replicate

[Replicate](https://replicate.com/blog/machine-learning-needs-better-tools) runs machine learning models in the cloud. We have a library of open-source models that you can run with a few lines of code. If you're building your own machine learning models, Replicate makes it easy to deploy them at scale.

This example goes over how to use LangChain to interact with `Replicate` [models](https://replicate.com/explore)

## Setup[​](#setup "Direct link to Setup")

```python
# magics to auto-reload external modules in case you are making changes to langchain while working on this notebook  
%autoreload 2  

```

To run this notebook, you'll need to create a [replicate](https://replicate.com) account and install the [replicate python client](https://github.com/replicate/replicate-python).

```bash
poetry run pip install replicate  

```

```text
 Collecting replicate  
 Using cached replicate-0.9.0-py3-none-any.whl (21 kB)  
 Requirement already satisfied: packaging in /root/Source/github/docugami.langchain/libs/langchain/.venv/lib/python3.9/site-packages (from replicate) (23.1)  
 Requirement already satisfied: pydantic>1 in /root/Source/github/docugami.langchain/libs/langchain/.venv/lib/python3.9/site-packages (from replicate) (1.10.9)  
 Requirement already satisfied: requests>2 in /root/Source/github/docugami.langchain/libs/langchain/.venv/lib/python3.9/site-packages (from replicate) (2.28.2)  
 Requirement already satisfied: typing-extensions>=4.2.0 in /root/Source/github/docugami.langchain/libs/langchain/.venv/lib/python3.9/site-packages (from pydantic>1->replicate) (4.5.0)  
 Requirement already satisfied: charset-normalizer<4,>=2 in /root/Source/github/docugami.langchain/libs/langchain/.venv/lib/python3.9/site-packages (from requests>2->replicate) (3.1.0)  
 Requirement already satisfied: idna<4,>=2.5 in /root/Source/github/docugami.langchain/libs/langchain/.venv/lib/python3.9/site-packages (from requests>2->replicate) (3.4)  
 Requirement already satisfied: urllib3<1.27,>=1.21.1 in /root/Source/github/docugami.langchain/libs/langchain/.venv/lib/python3.9/site-packages (from requests>2->replicate) (1.26.16)  
 Requirement already satisfied: certifi>=2017.4.17 in /root/Source/github/docugami.langchain/libs/langchain/.venv/lib/python3.9/site-packages (from requests>2->replicate) (2023.5.7)  
 Installing collected packages: replicate  
 Successfully installed replicate-0.9.0  

```

```python
# get a token: https://replicate.com/account  
  
from getpass import getpass  
  
REPLICATE\_API\_TOKEN = getpass()  

```

```python
import os  
  
os.environ["REPLICATE\_API\_TOKEN"] = REPLICATE\_API\_TOKEN  

```

```python
from langchain.llms import Replicate  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

## Calling a model[​](#calling-a-model "Direct link to Calling a model")

Find a model on the [replicate explore page](https://replicate.com/explore), and then paste in the model name and version in this format: model_name/version.

For example, here is [`LLama-V2`](https://replicate.com/a16z-infra/llama13b-v2-chat).

```python
llm = Replicate(  
 model="a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5",  
 model\_kwargs={"temperature": 0.75, "max\_length": 500, "top\_p": 1},  
)  
prompt = """  
User: Answer the following yes/no question by reasoning step by step. Can a dog drive a car?  
Assistant:  
"""  
llm(prompt)  

```

```text
 '1. Dogs do not have the ability to operate complex machinery like cars.\n2. Dogs do not have human-like intelligence or cognitive abilities to understand the concept of driving.\n3. Dogs do not have the physical ability to use their paws to press pedals or turn a steering wheel.\n4. Therefore, a dog cannot drive a car.'  

```

As another example, for this [dolly model](https://replicate.com/replicate/dolly-v2-12b), click on the API tab. The model name/version would be: `replicate/dolly-v2-12b:ef0e1aefc61f8e096ebe4db6b2bacc297daf2ef6899f0f7e001ec445893500e5`

Only the `model` param is required, but we can add other model params when initializing.

For example, if we were running stable diffusion and wanted to change the image dimensions:

```text
Replicate(model="stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf", input={'image\_dimensions': '512x512'})  

```

*Note that only the first output of a model will be returned.*

```python
llm = Replicate(  
 model="replicate/dolly-v2-12b:ef0e1aefc61f8e096ebe4db6b2bacc297daf2ef6899f0f7e001ec445893500e5"  
)  

```

```python
prompt = """  
Answer the following yes/no question by reasoning step by step.   
Can a dog drive a car?  
"""  
llm(prompt)  

```

```text
 'No, dogs lack some of the brain functions required to operate a motor vehicle. They cannot focus and react in time to accelerate or brake correctly. Additionally, they do not have enough muscle control to properly operate a steering wheel.\n\n'  

```

We can call any replicate model using this syntax. For example, we can call stable diffusion.

```python
text2image = Replicate(  
 model="stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",  
 model\_kwargs={"image\_dimensions": "512x512"},  
)  

```

```python
image\_output = text2image("A cat riding a motorcycle by Picasso")  
image\_output  

```

```text
 'https://pbxt.replicate.delivery/bqQq4KtzwrrYL9Bub9e7NvMTDeEMm5E9VZueTXkLE7kWumIjA/out-0.png'  

```

The model spits out a URL. Let's render it.

```bash
poetry run pip install Pillow  

```

```text
 Requirement already satisfied: Pillow in /Users/bagatur/langchain/.venv/lib/python3.9/site-packages (9.5.0)  
   
 [notice] A new release of pip is available: 23.2 -> 23.2.1  
 [notice] To update, run: pip install --upgrade pip  

```

```python
from PIL import Image  
import requests  
from io import BytesIO  
  
response = requests.get(image\_output)  
img = Image.open(BytesIO(response.content))  
  
img  

```

## Streaming Response[​](#streaming-response "Direct link to Streaming Response")

You can optionally stream the response as it is produced, which is helpful to show interactivity to users for time-consuming generations. See detailed docs on [Streaming](https://python.langchain.com/docs/modules/model_io/models/llms/how_to/streaming_llm) for more information.

```python
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  
  
llm = Replicate(  
 streaming=True,  
 callbacks=[StreamingStdOutCallbackHandler()],  
 model="a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5",  
 model\_kwargs={"temperature": 0.75, "max\_length": 500, "top\_p": 1},  
)  
prompt = """  
User: Answer the following yes/no question by reasoning step by step. Can a dog drive a car?  
Assistant:  
"""  
\_ = llm(prompt)  

```

```text
 1. Dogs do not have the physical ability to operate a vehicle.  

```

# Stop Sequences

You can also specify stop sequences. If you have a definite stop sequence for the generation that you are going to parse with anyway, it is better (cheaper and faster!) to just cancel the generation once one or more stop sequences are reached, rather than letting the model ramble on till the specified `max_length`. Stop sequences work regardless of whether you are in streaming mode or not, and Replicate only charges you for the generation up until the stop sequence.

```python
import time  
  
llm = Replicate(  
 model="a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5",  
 model\_kwargs={"temperature": 0.01, "max\_length": 500, "top\_p": 1},  
)  
  
prompt = """  
User: What is the best way to learn python?  
Assistant:  
"""  
start\_time = time.perf\_counter()  
raw\_output = llm(prompt) # raw output, no stop  
end\_time = time.perf\_counter()  
print(f"Raw output:\n {raw\_output}")  
print(f"Raw output runtime: {end\_time - start\_time} seconds")  
  
start\_time = time.perf\_counter()  
stopped\_output = llm(prompt, stop=["\n\n"]) # stop on double newlines  
end\_time = time.perf\_counter()  
print(f"Stopped output:\n {stopped\_output}")  
print(f"Stopped output runtime: {end\_time - start\_time} seconds")  

```

```text
 Raw output:  
 There are several ways to learn Python, and the best method for you will depend on your learning style and goals. Here are a few suggestions:  
   
 1. Online tutorials and courses: Websites such as Codecademy, Coursera, and edX offer interactive coding lessons and courses that can help you get started with Python. These courses are often designed for beginners and cover the basics of Python programming.  
 2. Books: There are many books available that can teach you Python, ranging from introductory texts to more advanced manuals. Some popular options include "Python Crash Course" by Eric Matthes, "Automate the Boring Stuff with Python" by Al Sweigart, and "Python for Data Analysis" by Wes McKinney.  
 3. Videos: YouTube and other video platforms have a wealth of tutorials and lectures on Python programming. Many of these videos are created by experienced programmers and can provide detailed explanations and examples of Python concepts.  
 4. Practice: One of the best ways to learn Python is to practice writing code. Start with simple programs and gradually work your way up to more complex projects. As you gain experience, you'll become more comfortable with the language and develop a better understanding of its capabilities.  
 5. Join a community: There are many online communities and forums dedicated to Python programming, such as Reddit's r/learnpython community. These communities can provide support, resources, and feedback as you learn.  
 6. Take online courses: Many universities and organizations offer online courses on Python programming. These courses can provide a structured learning experience and often include exercises and assignments to help you practice your skills.  
 7. Use a Python IDE: An Integrated Development Environment (IDE) is a software application that provides an interface for writing, debugging, and testing code. Popular Python IDEs include PyCharm, Visual Studio Code, and Spyder. These tools can help you write more efficient code and provide features such as code completion, debugging, and project management.  
   
   
 Which of the above options do you think is the best way to learn Python?  
 Raw output runtime: 25.27470933299992 seconds  
 Stopped output:  
 There are several ways to learn Python, and the best method for you will depend on your learning style and goals. Here are some suggestions:  
 Stopped output runtime: 25.77039254200008 seconds  

```

## Chaining Calls[​](#chaining-calls "Direct link to Chaining Calls")

The whole point of langchain is to... chain! Here's an example of how do that.

```python
from langchain.chains import SimpleSequentialChain  

```

First, let's define the LLM for this model as a flan-5, and text2image as a stable diffusion model.

```python
dolly\_llm = Replicate(  
 model="replicate/dolly-v2-12b:ef0e1aefc61f8e096ebe4db6b2bacc297daf2ef6899f0f7e001ec445893500e5"  
)  
text2image = Replicate(  
 model="stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf"  
)  

```

First prompt in the chain

```python
prompt = PromptTemplate(  
 input\_variables=["product"],  
 template="What is a good name for a company that makes {product}?",  
)  
  
chain = LLMChain(llm=dolly\_llm, prompt=prompt)  

```

Second prompt to get the logo for company description

```python
second\_prompt = PromptTemplate(  
 input\_variables=["company\_name"],  
 template="Write a description of a logo for this company: {company\_name}",  
)  
chain\_two = LLMChain(llm=dolly\_llm, prompt=second\_prompt)  

```

Third prompt, let's create the image based on the description output from prompt 2

```python
third\_prompt = PromptTemplate(  
 input\_variables=["company\_logo\_description"],  
 template="{company\_logo\_description}",  
)  
chain\_three = LLMChain(llm=text2image, prompt=third\_prompt)  

```

Now let's run it!

```python
# Run the chain specifying only the input variable for the first chain.  
overall\_chain = SimpleSequentialChain(  
 chains=[chain, chain\_two, chain\_three], verbose=True  
)  
catchphrase = overall\_chain.run("colorful socks")  
print(catchphrase)  

```

```text
   
   
 > Entering new SimpleSequentialChain chain...  
 Colorful socks could be named after a song by The Beatles or a color (yellow, blue, pink). A good combination of letters and digits would be 6399. Apple also owns the domain 6399.com so this could be reserved for the Company.  
   
   
 A colorful sock with the numbers 3, 9, and 99 screen printed in yellow, blue, and pink, respectively.  
   
   
 https://pbxt.replicate.delivery/P8Oy3pZ7DyaAC1nbJTxNw95D1A3gCPfi2arqlPGlfG9WYTkRA/out-0.png  
   
 > Finished chain.  
 https://pbxt.replicate.delivery/P8Oy3pZ7DyaAC1nbJTxNw95D1A3gCPfi2arqlPGlfG9WYTkRA/out-0.png  

```

```python
response = requests.get(  
 "https://replicate.delivery/pbxt/682XgeUlFela7kmZgPOf39dDdGDDkwjsCIJ0aQ0AO5bTbbkiA/out-0.png"  
)  
img = Image.open(BytesIO(response.content))  
img  

```

- [Setup](#setup)
- [Calling a model](#calling-a-model)
- [Streaming Response](#streaming-response)
- [Chaining Calls](#chaining-calls)
