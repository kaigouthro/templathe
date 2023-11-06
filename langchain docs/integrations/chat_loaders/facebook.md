# Facebook Messenger

This notebook shows how to load data from Facebook in a format you can fine-tune on. The overall steps are:

1. Download your messenger data to disk.
1. Create the Chat Loader and call `loader.load()` (or `loader.lazy_load()`) to perform the conversion.
1. Optionally use `merge_chat_runs` to combine message from the same sender in sequence, and/or `map_ai_messages` to convert messages from the specified sender to the "AIMessage" class. Once you've done this, call `convert_messages_for_finetuning` to prepare your data for fine-tuning.

Once this has been done, you can fine-tune your model. To do so you would complete the following steps:

4. Upload your messages to OpenAI and run a fine-tuning job.
1. Use the resulting model in your LangChain app!

Let's begin.

1. Download Data[​](#1-download-data "Direct link to 1. Download Data")

______________________________________________________________________

To download your own messenger data, following instructions [here](https://www.zapptales.com/en/download-facebook-messenger-chat-history-how-to/). IMPORTANT - make sure to download them in JSON format (not HTML).

We are hosting an example dump at [this google drive link](https://drive.google.com/file/d/1rh1s1o2i7B-Sk1v9o8KNgivLVGwJ-osV/view?usp=sharing) that we will use in this walkthrough.

```python
# This uses some example data  
import requests  
import zipfile  
  
def download\_and\_unzip(url: str, output\_path: str = 'file.zip') -> None:  
 file\_id = url.split('/')[-2]  
 download\_url = f'https://drive.google.com/uc?export=download&id={file\_id}'  
  
 response = requests.get(download\_url)  
 if response.status\_code != 200:  
 print('Failed to download the file.')  
 return  
  
 with open(output\_path, 'wb') as file:  
 file.write(response.content)  
 print(f'File {output\_path} downloaded.')  
  
 with zipfile.ZipFile(output\_path, 'r') as zip\_ref:  
 zip\_ref.extractall()  
 print(f'File {output\_path} has been unzipped.')  
  
# URL of the file to download  
url = 'https://drive.google.com/file/d/1rh1s1o2i7B-Sk1v9o8KNgivLVGwJ-osV/view?usp=sharing'  
  
# Download and unzip  
download\_and\_unzip(url)  

```

```text
 File file.zip downloaded.  
 File file.zip has been unzipped.  

```

2. Create Chat Loader[​](#2-create-chat-loader "Direct link to 2. Create Chat Loader")

______________________________________________________________________

We have 2 different `FacebookMessengerChatLoader` classes, one for an entire directory of chats, and one to load individual files. We

```python
directory\_path = "./hogwarts"  

```

```python
from langchain.chat\_loaders.facebook\_messenger import (  
 SingleFileFacebookMessengerChatLoader,  
 FolderFacebookMessengerChatLoader,  
)  

```

```python
loader = SingleFileFacebookMessengerChatLoader(  
 path="./hogwarts/inbox/HermioneGranger/messages\_Hermione\_Granger.json",  
)  

```

```python
chat\_session = loader.load()[0]  
chat\_session["messages"][:3]  

```

```text
 [HumanMessage(content="Hi Hermione! How's your summer going so far?", additional\_kwargs={'sender': 'Harry Potter'}, example=False),  
 HumanMessage(content="Harry! Lovely to hear from you. My summer is going well, though I do miss everyone. I'm spending most of my time going through my books and researching fascinating new topics. How about you?", additional\_kwargs={'sender': 'Hermione Granger'}, example=False),  
 HumanMessage(content="I miss you all too. The Dursleys are being their usual unpleasant selves but I'm getting by. At least I can practice some spells in my room without them knowing. Let me know if you find anything good in your researching!", additional\_kwargs={'sender': 'Harry Potter'}, example=False)]  

```

```python
loader = FolderFacebookMessengerChatLoader(  
 path="./hogwarts",  
)  

```

```python
chat\_sessions = loader.load()  
len(chat\_sessions)  

```

```text
 9  

```

3. Prepare for fine-tuning[​](#3-prepare-for-fine-tuning "Direct link to 3. Prepare for fine-tuning")

______________________________________________________________________

Calling `load()` returns all the chat messages we could extract as human messages. When conversing with chat bots, conversations typically follow a more strict alternating dialogue pattern relative to real conversations.

You can choose to merge message "runs" (consecutive messages from the same sender) and select a sender to represent the "AI". The fine-tuned LLM will learn to generate these AI messages.

```python
from langchain.chat\_loaders.utils import (  
 merge\_chat\_runs,  
 map\_ai\_messages,  
)  

```

```python
merged\_sessions = merge\_chat\_runs(chat\_sessions)  
alternating\_sessions = list(map\_ai\_messages(merged\_sessions, "Harry Potter"))  

```

```python
# Now all of Harry Potter's messages will take the AI message class  
# which maps to the 'assistant' role in OpenAI's training format  
alternating\_sessions[0]['messages'][:3]  

```

```text
 [AIMessage(content="Professor Snape, I was hoping I could speak with you for a moment about something that's been concerning me lately.", additional\_kwargs={'sender': 'Harry Potter'}, example=False),  
 HumanMessage(content="What is it, Potter? I'm quite busy at the moment.", additional\_kwargs={'sender': 'Severus Snape'}, example=False),  
 AIMessage(content="I apologize for the interruption, sir. I'll be brief. I've noticed some strange activity around the school grounds at night. I saw a cloaked figure lurking near the Forbidden Forest last night. I'm worried someone may be plotting something sinister.", additional\_kwargs={'sender': 'Harry Potter'}, example=False)]  

```

#### Now we can convert to OpenAI format dictionaries[​](#now-we-can-convert-to-openai-format-dictionaries "Direct link to Now we can convert to OpenAI format dictionaries")

```python
from langchain.adapters.openai import convert\_messages\_for\_finetuning  

```

```python
training\_data = convert\_messages\_for\_finetuning(alternating\_sessions)  
print(f"Prepared {len(training\_data)} dialogues for training")  

```

```text
 Prepared 9 dialogues for training  

```

```python
training\_data[0][:3]  

```

```text
 [{'role': 'assistant',  
 'content': "Professor Snape, I was hoping I could speak with you for a moment about something that's been concerning me lately."},  
 {'role': 'user',  
 'content': "What is it, Potter? I'm quite busy at the moment."},  
 {'role': 'assistant',  
 'content': "I apologize for the interruption, sir. I'll be brief. I've noticed some strange activity around the school grounds at night. I saw a cloaked figure lurking near the Forbidden Forest last night. I'm worried someone may be plotting something sinister."}]  

```

OpenAI currently requires at least 10 training examples for a fine-tuning job, though they recommend between 50-100 for most tasks. Since we only have 9 chat sessions, we can subdivide them (optionally with some overlap) so that each training example is comprised of a portion of a whole conversation.

Facebook chat sessions (1 per person) often span multiple days and conversations,
so the long-range dependencies may not be that important to model anyhow.

```python
# Our chat is alternating, we will make each datapoint a group of 8 messages,  
# with 2 messages overlapping  
chunk\_size = 8  
overlap = 2  
  
training\_examples = [  
 conversation\_messages[i: i + chunk\_size]   
 for conversation\_messages in training\_data  
 for i in range(  
 0, len(conversation\_messages) - chunk\_size + 1,   
 chunk\_size - overlap)  
]  
  
len(training\_examples)  

```

```text
 100  

```

4. Fine-tune the model[​](#4-fine-tune-the-model "Direct link to 4. Fine-tune the model")

______________________________________________________________________

It's time to fine-tune the model. Make sure you have `openai` installed
and have set your `OPENAI_API_KEY` appropriately

```python
# %pip install -U openai --quiet  

```

```python
import json  
from io import BytesIO  
import time  
  
import openai  
  
# We will write the jsonl file in memory  
my\_file = BytesIO()  
for m in training\_examples:  
 my\_file.write((json.dumps({"messages": m}) + "\n").encode('utf-8'))  
  
my\_file.seek(0)  
training\_file = openai.File.create(  
 file=my\_file,  
 purpose='fine-tune'  
)  
  
# OpenAI audits each training file for compliance reasons.  
# This make take a few minutes  
status = openai.File.retrieve(training\_file.id).status  
start\_time = time.time()  
while status != "processed":  
 print(f"Status=[{status}]... {time.time() - start\_time:.2f}s", end="\r", flush=True)  
 time.sleep(5)  
 status = openai.File.retrieve(training\_file.id).status  
print(f"File {training\_file.id} ready after {time.time() - start\_time:.2f} seconds.")  

```

```text
 File file-zCyNBeg4snpbBL7VkvsuhCz8 ready afer 30.55 seconds.  

```

With the file ready, it's time to kick off a training job.

```python
job = openai.FineTuningJob.create(  
 training\_file=training\_file.id,  
 model="gpt-3.5-turbo",  
)  

```

Grab a cup of tea while your model is being prepared. This may take some time!

```python
status = openai.FineTuningJob.retrieve(job.id).status  
start\_time = time.time()  
while status != "succeeded":  
 print(f"Status=[{status}]... {time.time() - start\_time:.2f}s", end="\r", flush=True)  
 time.sleep(5)  
 job = openai.FineTuningJob.retrieve(job.id)  
 status = job.status  

```

```text
 Status=[running]... 908.87s  

```

```python
print(job.fine\_tuned\_model)  

```

```text
 ft:gpt-3.5-turbo-0613:personal::7rDwkaOq  

```

5. Use in LangChain[​](#5-use-in-langchain "Direct link to 5. Use in LangChain")

______________________________________________________________________

You can use the resulting model ID directly the `ChatOpenAI` model class.

```python
from langchain.chat\_models import ChatOpenAI  
  
model = ChatOpenAI(  
 model=job.fine\_tuned\_model,  
 temperature=1,  
)  

```

```python
from langchain.prompts import ChatPromptTemplate  
from langchain.schema.output\_parser import StrOutputParser  
  
prompt = ChatPromptTemplate.from\_messages(  
 [  
 ("human", "{input}"),  
 ]  
)  
  
chain = prompt | model | StrOutputParser()  

```

```python
for tok in chain.stream({"input": "What classes are you taking?"}):  
 print(tok, end="", flush=True)  

```

```text
 The usual - Potions, Transfiguration, Defense Against the Dark Arts. What about you?  

```

- [1. Download Data](#1-download-data)
- [2. Create Chat Loader](#2-create-chat-loader)
- [3. Prepare for fine-tuning](#3-prepare-for-fine-tuning)
- [4. Fine-tune the model](#4-fine-tune-the-model)
- [5. Use in LangChain](#5-use-in-langchain)
