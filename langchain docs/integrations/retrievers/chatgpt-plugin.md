# ChatGPT Plugin

[OpenAI plugins](https://platform.openai.com/docs/plugins/introduction) connect ChatGPT to third-party applications. These plugins enable ChatGPT to interact with APIs defined by developers, enhancing ChatGPT's capabilities and allowing it to perform a wide range of actions.

Plugins can allow ChatGPT to do things like:

- Retrieve real-time information; e.g., sports scores, stock prices, the latest news, etc.
- Retrieve knowledge-base information; e.g., company docs, personal notes, etc.
- Perform actions on behalf of the user; e.g., booking a flight, ordering food, etc.

This notebook shows how to use the ChatGPT Retriever Plugin within LangChain.

```python
# STEP 1: Load  
  
# Load documents using LangChain's DocumentLoaders  
# This is from https://langchain.readthedocs.io/en/latest/modules/document\_loaders/examples/csv.html  
  
from langchain.document\_loaders.csv\_loader import CSVLoader  
  
loader = CSVLoader(  
 file\_path="../../document\_loaders/examples/example\_data/mlb\_teams\_2012.csv"  
)  
data = loader.load()  
  
  
# STEP 2: Convert  
  
# Convert Document to format expected by https://github.com/openai/chatgpt-retrieval-plugin  
from typing import List  
from langchain.docstore.document import Document  
import json  
  
  
def write\_json(path: str, documents: List[Document]) -> None:  
 results = [{"text": doc.page\_content} for doc in documents]  
 with open(path, "w") as f:  
 json.dump(results, f, indent=2)  
  
  
write\_json("foo.json", data)  
  
# STEP 3: Use  
  
# Ingest this as you would any other json file in https://github.com/openai/chatgpt-retrieval-plugin/tree/main/scripts/process\_json  

```

## Using the ChatGPT Retriever Plugin[​](#using-the-chatgpt-retriever-plugin "Direct link to Using the ChatGPT Retriever Plugin")

Okay, so we've created the ChatGPT Retriever Plugin, but how do we actually use it?

The below code walks through how to do that.

We want to use `ChatGPTPluginRetriever` so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```text
 OpenAI API Key: ········  

```

```python
from langchain.retrievers import ChatGPTPluginRetriever  

```

```python
retriever = ChatGPTPluginRetriever(url="http://0.0.0.0:8000", bearer\_token="foo")  

```

```python
retriever.get\_relevant\_documents("alice's phone number")  

```

```text
 [Document(page\_content="This is Alice's phone number: 123-456-7890", lookup\_str='', metadata={'id': '456\_0', 'metadata': {'source': 'email', 'source\_id': '567', 'url': None, 'created\_at': '1609592400.0', 'author': 'Alice', 'document\_id': '456'}, 'embedding': None, 'score': 0.925571561}, lookup\_index=0),  
 Document(page\_content='This is a document about something', lookup\_str='', metadata={'id': '123\_0', 'metadata': {'source': 'file', 'source\_id': 'https://example.com/doc1', 'url': 'https://example.com/doc1', 'created\_at': '1609502400.0', 'author': 'Alice', 'document\_id': '123'}, 'embedding': None, 'score': 0.6987589}, lookup\_index=0),  
 Document(page\_content='Team: Angels "Payroll (millions)": 154.49 "Wins": 89', lookup\_str='', metadata={'id': '59c2c0c1-ae3f-4272-a1da-f44a723ea631\_0', 'metadata': {'source': None, 'source\_id': None, 'url': None, 'created\_at': None, 'author': None, 'document\_id': '59c2c0c1-ae3f-4272-a1da-f44a723ea631'}, 'embedding': None, 'score': 0.697888613}, lookup\_index=0)]  

```

- [Using the ChatGPT Retriever Plugin](#using-the-chatgpt-retriever-plugin)
