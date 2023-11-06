# Fine-Tuning on LangSmith Chat Datasets

This notebook demonstrates an easy way to load a LangSmith chat dataset fine-tune a model on that data.
The process is simple and comprises 3 steps.

1. Create the chat dataset.
1. Use the LangSmithDatasetChatLoader to load examples.
1. Fine-tune your model.

Then you can use the fine-tuned model in your LangChain app.

Before diving in, let's install our prerequisites.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Ensure you've installed langchain >= 0.0.311 and have configured your environment with your LangSmith API key.

```python
%pip install -U langchain openai  

```

```python
import os  
import uuid  
uid = uuid.uuid4().hex[:6]  
os.environ["LANGCHAIN\_TRACING\_V2"] = "true"  
os.environ["LANGCHAIN\_API\_KEY"] = "YOUR API KEY"  

```

1. Select a dataset[​](#1-select-a-dataset "Direct link to 1. Select a dataset")

______________________________________________________________________

This notebook fine-tunes a model directly on selecting which runs to fine-tune on. You will often curate these from traced runs. You can learn more about LangSmith datasets in the docs [docs](https://docs.smith.langchain.com/evaluation/datasets).

For the sake of this tutorial, we will upload an existing dataset here that you can use.

```python
from langsmith.client import Client  
  
client = Client()  

```

```python
import requests  
url = "https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/docs/integrations/chat\_loaders/example\_data/langsmith\_chat\_dataset.json"  
response = requests.get(url)  
response.raise\_for\_status()  
data = response.json()  

```

```python
dataset\_name = f"Extraction Fine-tuning Dataset {uid}"  
ds = client.create\_dataset(dataset\_name=dataset\_name, data\_type="chat")  

```

```python
\_ = client.create\_examples(  
 inputs = [e['inputs'] for e in data],  
 outputs = [e['outputs'] for e in data],  
 dataset\_id=ds.id,  
)  

```

2. Prepare Data[​](#2-prepare-data "Direct link to 2. Prepare Data")

______________________________________________________________________

Now we can create an instance of LangSmithRunChatLoader and load the chat sessions using its lazy_load() method.

```python
from langchain.chat\_loaders.langsmith import LangSmithDatasetChatLoader  
  
loader = LangSmithDatasetChatLoader(dataset\_name=dataset\_name)  
  
chat\_sessions = loader.lazy\_load()  

```

#### With the chat sessions loaded, convert them into a format suitable for fine-tuning.[​](#with-the-chat-sessions-loaded-convert-them-into-a-format-suitable-for-fine-tuning "Direct link to With the chat sessions loaded, convert them into a format suitable for fine-tuning.")

```python
from langchain.adapters.openai import convert\_messages\_for\_finetuning  
  
training\_data = convert\_messages\_for\_finetuning(chat\_sessions)  

```

3. Fine-tune the Model[​](#3-fine-tune-the-model "Direct link to 3. Fine-tune the Model")

______________________________________________________________________

Now, initiate the fine-tuning process using the OpenAI library.

```python
import openai  
import time  
import json  
from io import BytesIO  
  
my\_file = BytesIO()  
for dialog in training\_data:  
 my\_file.write((json.dumps({"messages": dialog}) + "\n").encode('utf-8'))  
  
my\_file.seek(0)  
training\_file = openai.File.create(  
 file=my\_file,  
 purpose='fine-tune'  
)  
  
job = openai.FineTuningJob.create(  
 training\_file=training\_file.id,  
 model="gpt-3.5-turbo",  
)  
  
# Wait for the fine-tuning to complete (this may take some time)  
status = openai.FineTuningJob.retrieve(job.id).status  
start\_time = time.time()  
while status != "succeeded":  
 print(f"Status=[{status}]... {time.time() - start\_time:.2f}s", end="\r", flush=True)  
 time.sleep(5)  
 status = openai.FineTuningJob.retrieve(job.id).status  
  
# Now your model is fine-tuned!  

```

```text
 Status=[running]... 302.42s. 143.85s  

```

4. Use in LangChain[​](#4-use-in-langchain "Direct link to 4. Use in LangChain")

______________________________________________________________________

After fine-tuning, use the resulting model ID with the ChatOpenAI model class in your LangChain app.

```python
# Get the fine-tuned model ID  
job = openai.FineTuningJob.retrieve(job.id)  
model\_id = job.fine\_tuned\_model  
  
# Use the fine-tuned model in LangChain  
model = ChatOpenAI(  
 model=model\_id,  
 temperature=1,  
)  

```

```python
model.invoke("There were three ravens sat on a tree.")  

```

Now you have successfully fine-tuned a model using data from LangSmith LLM runs!

- [Prerequisites](#prerequisites)
- [1. Select a dataset](#1-select-a-dataset)
- [2. Prepare Data](#2-prepare-data)
- [3. Fine-tune the Model](#3-fine-tune-the-model)
- [4. Use in LangChain](#4-use-in-langchain)
