# iMessage

This notebook shows how to use the iMessage chat loader. This class helps convert iMessage conversations to LangChain chat messages.

On MacOS, iMessage stores conversations in a sqlite database at `~/Library/Messages/chat.db` (at least for macOS Ventura 13.4).
The `IMessageChatLoader` loads from this database file.

1. Create the `IMessageChatLoader` with the file path pointed to `chat.db` database you'd like to process.

1. Call `loader.load()` (or `loader.lazy_load()`) to perform the conversion. Optionally use `merge_chat_runs` to combine message from the same sender in sequence, and/or `map_ai_messages` to convert messages from the specified sender to the "AIMessage" class.

1. Access Chat DB[​](#1-access-chat-db "Direct link to 1. Access Chat DB")

______________________________________________________________________

It's likely that your terminal is denied access to `~/Library/Messages`. To use this class, you can copy the DB to an accessible directory (e.g., Documents) and load from there. Alternatively (and not recommended), you can grant full disk access for your terminal emulator in System Settings > Security and Privacy > Full Disk Access.

We have created an example database you can use at [this linked drive file](https://drive.google.com/file/d/1NebNKqTA2NXApCmeH6mu0unJD2tANZzo/view?usp=sharing).

```python
# This uses some example data  
import requests  
  
def download\_drive\_file(url: str, output\_path: str = 'chat.db') -> None:  
 file\_id = url.split('/')[-2]  
 download\_url = f'https://drive.google.com/uc?export=download&id={file\_id}'  
  
 response = requests.get(download\_url)  
 if response.status\_code != 200:  
 print('Failed to download the file.')  
 return  
  
 with open(output\_path, 'wb') as file:  
 file.write(response.content)  
 print(f'File {output\_path} downloaded.')  
  
url = 'https://drive.google.com/file/d/1NebNKqTA2NXApCmeH6mu0unJD2tANZzo/view?usp=sharing'  
  
# Download file to chat.db  
download\_drive\_file(url)  

```

```text
 File chat.db downloaded.  

```

2. Create the Chat Loader[​](#2-create-the-chat-loader "Direct link to 2. Create the Chat Loader")

______________________________________________________________________

Provide the loader with the file path to the zip directory. You can optionally specify the user id that maps to an ai message as well an configure whether to merge message runs.

```python
from langchain.chat\_loaders.imessage import IMessageChatLoader  

```

```python
loader = IMessageChatLoader(  
 path="./chat.db",  
)  

```

3. Load messages[​](#3-load-messages "Direct link to 3. Load messages")

______________________________________________________________________

The `load()` (or `lazy_load`) methods return a list of "ChatSessions" that currently just contain a list of messages per loaded conversation. All messages are mapped to "HumanMessage" objects to start.

You can optionally choose to merge message "runs" (consecutive messages from the same sender) and select a sender to represent the "AI". The fine-tuned LLM will learn to generate these AI messages.

```python
from typing import List  
from langchain.chat\_loaders.base import ChatSession  
from langchain.chat\_loaders.utils import (  
 map\_ai\_messages,  
 merge\_chat\_runs,  
)  
  
raw\_messages = loader.lazy\_load()  
# Merge consecutive messages from the same sender into a single message  
merged\_messages = merge\_chat\_runs(raw\_messages)  
# Convert messages from "Tortoise" to AI messages. Do you have a guess who these conversations are between?  
chat\_sessions: List[ChatSession] = list(map\_ai\_messages(merged\_messages, sender="Tortoise"))  

```

```python
# Now all of the Tortoise's messages will take the AI message class  
# which maps to the 'assistant' role in OpenAI's training format  
alternating\_sessions[0]['messages'][:3]  

```

```text
 [AIMessage(content="Slow and steady, that's my motto.", additional\_kwargs={'message\_time': 1693182723, 'sender': 'Tortoise'}, example=False),  
 HumanMessage(content='Speed is key!', additional\_kwargs={'message\_time': 1693182753, 'sender': 'Hare'}, example=False),  
 AIMessage(content='A balanced approach is more reliable.', additional\_kwargs={'message\_time': 1693182783, 'sender': 'Tortoise'}, example=False)]  

```

3. Prepare for fine-tuning[​](#3-prepare-for-fine-tuning "Direct link to 3. Prepare for fine-tuning")

______________________________________________________________________

Now it's time to convert our chat messages to OpenAI dictionaries. We can use the `convert_messages_for_finetuning` utility to do so.

```python
from langchain.adapters.openai import convert\_messages\_for\_finetuning  

```

```python
training\_data = convert\_messages\_for\_finetuning(alternating\_sessions)  
print(f"Prepared {len(training\_data)} dialogues for training")  

```

```text
 Prepared 10 dialogues for training  

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
for m in training\_data:  
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
 File file-zHIgf4r8LltZG3RFpkGd4Sjf ready after 10.19 seconds.  

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
 Status=[running]... 524.95s  

```

```python
print(job.fine\_tuned\_model)  

```

```text
 ft:gpt-3.5-turbo-0613:personal::7sKoRdlz  

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
 ("system", "You are speaking to hare."),  
 ("human", "{input}"),  
 ]  
)  
  
chain = prompt | model | StrOutputParser()  

```

```python
for tok in chain.stream({"input": "What's the golden thread?"}):  
 print(tok, end="", flush=True)  

```

```text
 A symbol of interconnectedness.  

```

- [1. Access Chat DB](#1-access-chat-db)
- [2. Create the Chat Loader](#2-create-the-chat-loader)
- [3. Load messages](#3-load-messages)
- [3. Prepare for fine-tuning](#3-prepare-for-fine-tuning)
- [4. Fine-tune the model](#4-fine-tune-the-model)
- [5. Use in LangChain](#5-use-in-langchain)
