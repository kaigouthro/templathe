# Infino

This example shows how one can track the following while calling OpenAI and ChatOpenAI models via `LangChain` and [Infino](https://github.com/infinohq/infino):

- prompt input,
- response from `ChatGPT` or any other `LangChain` model,
- latency,
- errors,
- number of tokens consumed

## Initializing[​](#initializing "Direct link to Initializing")

```bash
# Install necessary dependencies.  
pip install -q infinopy  
pip install -q matplotlib  
pip install -q tiktoken  

```

```python
import datetime as dt  
import json  
from langchain.llms import OpenAI  
import matplotlib.pyplot as plt  
import matplotlib.dates as md  
import os  
import time  
import sys  
  
from infinopy import InfinoClient  
from langchain.callbacks import InfinoCallbackHandler  

```

## Start Infino server, initialize the Infino client[​](#start-infino-server-initialize-the-infino-client "Direct link to Start Infino server, initialize the Infino client")

```bash
# Start server using the Infino docker image.  
docker run --rm --detach --name infino-example -p 3000:3000 infinohq/infino:latest  
  
# Create Infino client.  
client = InfinoClient()  

```

```text
 a1159e99c6bdb3101139157acee6aba7ae9319375e77ab6fbc79beff75abeca3  

```

## Read the questions dataset[​](#read-the-questions-dataset "Direct link to Read the questions dataset")

```python
# These are a subset of questions from Stanford's QA dataset -  
# https://rajpurkar.github.io/SQuAD-explorer/  
data = """In what country is Normandy located?  
When were the Normans in Normandy?  
From which countries did the Norse originate?  
Who was the Norse leader?  
What century did the Normans first gain their separate identity?  
Who gave their name to Normandy in the 1000's and 1100's  
What is France a region of?  
Who did King Charles III swear fealty to?  
When did the Frankish identity emerge?  
Who was the duke in the battle of Hastings?  
Who ruled the duchy of Normandy  
What religion were the Normans  
What type of major impact did the Norman dynasty have on modern Europe?  
Who was famed for their Christian spirit?  
Who assimilted the Roman language?  
Who ruled the country of Normandy?  
What principality did William the conquerer found?  
What is the original meaning of the word Norman?  
When was the Latin version of the word Norman first recorded?  
What name comes from the English words Normans/Normanz?"""  
  
questions = data.split("\n")  

```

## Example 1: LangChain OpenAI Q&A; Publish metrics and logs to Infino[​](#example-1-langchain-openai-qa-publish-metrics-and-logs-to-infino "Direct link to Example 1: LangChain OpenAI Q&A; Publish metrics and logs to Infino")

```python
# Set your key here.  
# os.environ["OPENAI\_API\_KEY"] = "YOUR\_API\_KEY"  
  
# Create callback handler. This logs latency, errors, token usage, prompts as well as prompt responses to Infino.  
handler = InfinoCallbackHandler(  
 model\_id="test\_openai", model\_version="0.1", verbose=False  
)  
  
# Create LLM.  
llm = OpenAI(temperature=0.1)  
  
# Number of questions to ask the OpenAI model. We limit to a short number here to save $$ while running this demo.  
num\_questions = 10  
  
questions = questions[0:num\_questions]  
for question in questions:  
 print(question)  
  
 # We send the question to OpenAI API, with Infino callback.  
 llm\_result = llm.generate([question], callbacks=[handler])  
 print(llm\_result)  

```

```text
 In what country is Normandy located?  
 generations=[[Generation(text='\n\nNormandy is located in France.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})]] llm\_output={'token\_usage': {'total\_tokens': 16, 'prompt\_tokens': 7, 'completion\_tokens': 9}, 'model\_name': 'text-davinci-003'} run=[RunInfo(run\_id=UUID('67a516e3-d48a-4e83-92ba-a139079bd3b1'))]  
 When were the Normans in Normandy?  
 generations=[[Generation(text='\n\nThe Normans first settled in Normandy in the late 9th century.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})]] llm\_output={'token\_usage': {'total\_tokens': 24, 'prompt\_tokens': 8, 'completion\_tokens': 16}, 'model\_name': 'text-davinci-003'} run=[RunInfo(run\_id=UUID('6417a773-c863-4942-9607-c8a0c5d486e7'))]  
 From which countries did the Norse originate?  
 generations=[[Generation(text='\n\nThe Norse originated from Scandinavia, which includes the modern-day countries of Norway, Sweden, and Denmark.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})]] llm\_output={'token\_usage': {'total\_tokens': 32, 'prompt\_tokens': 8, 'completion\_tokens': 24}, 'model\_name': 'text-davinci-003'} run=[RunInfo(run\_id=UUID('70547d72-7925-454e-97fb-5539f8788c3f'))]  
 Who was the Norse leader?  
 generations=[[Generation(text='\n\nThe most famous Norse leader was the legendary Viking king Ragnar Lodbrok. He was a legendary Viking hero and ruler who is said to have lived in the 9th century. He is known for his legendary exploits, including leading a Viking raid on Paris in 845.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})]] llm\_output={'token\_usage': {'total\_tokens': 62, 'prompt\_tokens': 6, 'completion\_tokens': 56}, 'model\_name': 'text-davinci-003'} run=[RunInfo(run\_id=UUID('04500e37-44ab-4e56-9017-76fe8c19e2ca'))]  
 What century did the Normans first gain their separate identity?  
 generations=[[Generation(text='\n\nThe Normans first gained their separate identity in the 11th century.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})]] llm\_output={'token\_usage': {'total\_tokens': 28, 'prompt\_tokens': 12, 'completion\_tokens': 16}, 'model\_name': 'text-davinci-003'} run=[RunInfo(run\_id=UUID('adf319b7-1022-40df-9afe-1d65f869d83d'))]  
 Who gave their name to Normandy in the 1000's and 1100's  
 generations=[[Generation(text='\n\nThe Normans, a people from northern France, gave their name to Normandy in the 1000s and 1100s. The Normans were descendants of Vikings who had settled in the region in the late 800s.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})]] llm\_output={'token\_usage': {'total\_tokens': 57, 'prompt\_tokens': 13, 'completion\_tokens': 44}, 'model\_name': 'text-davinci-003'} run=[RunInfo(run\_id=UUID('1a0503bc-d033-4b69-a5fa-5e1796566133'))]  
 What is France a region of?  
 generations=[[Generation(text='\n\nFrance is a region of Europe.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})]] llm\_output={'token\_usage': {'total\_tokens': 16, 'prompt\_tokens': 7, 'completion\_tokens': 9}, 'model\_name': 'text-davinci-003'} run=[RunInfo(run\_id=UUID('7485d954-1c14-4dff-988a-25a0aa0871cc'))]  
 Who did King Charles III swear fealty to?  
 generations=[[Generation(text='\n\nKing Charles III swore fealty to King Philip II of Spain.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})]] llm\_output={'token\_usage': {'total\_tokens': 25, 'prompt\_tokens': 10, 'completion\_tokens': 15}, 'model\_name': 'text-davinci-003'} run=[RunInfo(run\_id=UUID('292c7143-4a08-43cd-a1e1-42cb1f594f33'))]  
 When did the Frankish identity emerge?  
 generations=[[Generation(text='\n\nThe Frankish identity began to emerge in the late 5th century, when the Franks began to expand their power and influence in the region. The Franks were a Germanic tribe that had settled in the area of modern-day France and Germany. They eventually established the Merovingian dynasty, which ruled much of Western Europe from the mid-6th century until 751.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})]] llm\_output={'token\_usage': {'total\_tokens': 85, 'prompt\_tokens': 8, 'completion\_tokens': 77}, 'model\_name': 'text-davinci-003'} run=[RunInfo(run\_id=UUID('3d9475c2-931e-4217-8bc3-b3e970e7597c'))]  
 Who was the duke in the battle of Hastings?  
 generations=[[Generation(text='\n\nThe Duke of Normandy, William the Conqueror, was the leader of the Norman forces at the Battle of Hastings in 1066.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})]] llm\_output={'token\_usage': {'total\_tokens': 39, 'prompt\_tokens': 11, 'completion\_tokens': 28}, 'model\_name': 'text-davinci-003'} run=[RunInfo(run\_id=UUID('b8f84619-ea5f-4c18-b411-b62194f36fe0'))]  

```

## Create Metric Charts[​](#create-metric-charts "Direct link to Create Metric Charts")

We now use matplotlib to create graphs of latency, errors and tokens consumed.

```python
# Helper function to create a graph using matplotlib.  
def plot(data, title):  
 data = json.loads(data)  
  
 # Extract x and y values from the data  
 timestamps = [item["time"] for item in data]  
 dates = [dt.datetime.fromtimestamp(ts) for ts in timestamps]  
 y = [item["value"] for item in data]  
  
 plt.rcParams["figure.figsize"] = [6, 4]  
 plt.subplots\_adjust(bottom=0.2)  
 plt.xticks(rotation=25)  
 ax = plt.gca()  
 xfmt = md.DateFormatter("%Y-%m-%d %H:%M:%S")  
 ax.xaxis.set\_major\_formatter(xfmt)  
  
 # Create the plot  
 plt.plot(dates, y)  
  
 # Set labels and title  
 plt.xlabel("Time")  
 plt.ylabel("Value")  
 plt.title(title)  
  
 plt.show()  

```

```python
response = client.search\_ts("\_\_name\_\_", "latency", 0, int(time.time()))  
plot(response.text, "Latency")  
  
response = client.search\_ts("\_\_name\_\_", "error", 0, int(time.time()))  
plot(response.text, "Errors")  
  
response = client.search\_ts("\_\_name\_\_", "prompt\_tokens", 0, int(time.time()))  
plot(response.text, "Prompt Tokens")  
  
response = client.search\_ts("\_\_name\_\_", "completion\_tokens", 0, int(time.time()))  
plot(response.text, "Completion Tokens")  
  
response = client.search\_ts("\_\_name\_\_", "total\_tokens", 0, int(time.time()))  
plot(response.text, "Total Tokens")  

```

## Full text query on prompt or prompt outputs.[​](#full-text-query-on-prompt-or-prompt-outputs "Direct link to Full text query on prompt or prompt outputs.")

```python
# Search for a particular prompt text.  
query = "normandy"  
response = client.search\_log(query, 0, int(time.time()))  
print("Results for", query, ":", response.text)  
  
print("===")  
  
query = "king charles III"  
response = client.search\_log("king charles III", 0, int(time.time()))  
print("Results for", query, ":", response.text)  

```

```text
 Results for normandy : [{"time":1696947743,"fields":{"prompt\_response":"\n\nThe Normans, a people from northern France, gave their name to Normandy in the 1000s and 1100s. The Normans were descendants of Vikings who had settled in the region in the late 800s."},"text":"\n\nThe Normans, a people from northern France, gave their name to Normandy in the 1000s and 1100s. The Normans were descendants of Vikings who had settled in the region in the late 800s."},{"time":1696947740,"fields":{"prompt":"Who gave their name to Normandy in the 1000's and 1100's"},"text":"Who gave their name to Normandy in the 1000's and 1100's"},{"time":1696947733,"fields":{"prompt\_response":"\n\nThe Normans first settled in Normandy in the late 9th century."},"text":"\n\nThe Normans first settled in Normandy in the late 9th century."},{"time":1696947732,"fields":{"prompt\_response":"\n\nNormandy is located in France."},"text":"\n\nNormandy is located in France."},{"time":1696947731,"fields":{"prompt":"In what country is Normandy located?"},"text":"In what country is Normandy located?"}]  
 ===  
 Results for king charles III : [{"time":1696947745,"fields":{"prompt\_response":"\n\nKing Charles III swore fealty to King Philip II of Spain."},"text":"\n\nKing Charles III swore fealty to King Philip II of Spain."},{"time":1696947744,"fields":{"prompt":"Who did King Charles III swear fealty to?"},"text":"Who did King Charles III swear fealty to?"}]  

```

# Example 2: Summarize a piece of text using ChatOpenAI

```python
# Set your key here.  
# os.environ["OPENAI\_API\_KEY"] = "YOUR\_API\_KEY"  
  
from langchain.chat\_models import ChatOpenAI  
from langchain.document\_loaders import WebBaseLoader  
from langchain.chains.summarize import load\_summarize\_chain  
  
# Create callback handler. This logs latency, errors, token usage, prompts, as well as prompt responses to Infino.  
handler = InfinoCallbackHandler(  
 model\_id="test\_chatopenai", model\_version="0.1", verbose=False  
)  
  
urls = ["https://lilianweng.github.io/posts/2023-06-23-agent/",  
 "https://medium.com/lyft-engineering/lyftlearn-ml-model-training-infrastructure-built-on-kubernetes-aef8218842bb",  
 "https://blog.langchain.dev/week-of-10-2-langchain-release-notes/"]  
  
for url in urls:  
 loader = WebBaseLoader(url)  
 docs = loader.load()  
  
 llm = ChatOpenAI(temperature=0, model\_name="gpt-3.5-turbo-16k", callbacks=[handler])  
 chain = load\_summarize\_chain(llm, chain\_type="stuff", verbose=False)  
  
 chain.run(docs)  

```

## Create Metric Charts[​](#create-metric-charts-1 "Direct link to Create Metric Charts")

```python
response = client.search\_ts("\_\_name\_\_", "latency", 0, int(time.time()))  
plot(response.text, "Latency")  
  
response = client.search\_ts("\_\_name\_\_", "error", 0, int(time.time()))  
plot(response.text, "Errors")  
  
response = client.search\_ts("\_\_name\_\_", "prompt\_tokens", 0, int(time.time()))  
plot(response.text, "Prompt Tokens")  
  
response = client.search\_ts("\_\_name\_\_", "completion\_tokens", 0, int(time.time()))  
plot(response.text, "Completion Tokens")  

```

```python
## Full text query on prompt or prompt outputs  

```

```python
# Search for a particular prompt text.  
query = "machine learning"  
response = client.search\_log(query, 0, int(time.time()))  
  
# The output can be verbose - uncomment below if it needs to be printed.  
# print("Results for", query, ":", response.text)  
  
print("===")  

```

```text
 ===  

```

```python
## Stop Infino server  

```

```bash
docker rm -f infino-example  

```

```text
 infino-example  

```

- [Initializing](#initializing)
- [Start Infino server, initialize the Infino client](#start-infino-server-initialize-the-infino-client)
- [Read the questions dataset](#read-the-questions-dataset)
- [Example 1: LangChain OpenAI Q&A; Publish metrics and logs to Infino](#example-1-langchain-openai-qa-publish-metrics-and-logs-to-infino)
- [Create Metric Charts](#create-metric-charts)
- [Full text query on prompt or prompt outputs.](#full-text-query-on-prompt-or-prompt-outputs)
- [Create Metric Charts](#create-metric-charts-1)
