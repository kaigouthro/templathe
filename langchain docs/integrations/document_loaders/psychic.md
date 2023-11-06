# Psychic

This notebook covers how to load documents from `Psychic`. See [here](/docs/ecosystem/integrations/psychic.html) for more details.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

1. Follow the Quick Start section in [this document](/docs/ecosystem/integrations/psychic.html)
1. Log into the [Psychic dashboard](https://dashboard.psychic.dev/) and get your secret key
1. Install the frontend react library into your web app and have a user authenticate a connection. The connection will be created using the connection id that you specify.

## Loading documents[​](#loading-documents "Direct link to Loading documents")

Use the `PsychicLoader` class to load in documents from a connection. Each connection has a connector id (corresponding to the SaaS app that was connected) and a connection id (which you passed in to the frontend library).

```bash
# Uncomment this to install psychicapi if you don't already have it installed  
poetry run pip -q install psychicapi  

```

```text
   
 [notice] A new release of pip is available: 23.0.1 -> 23.1.2  
 [notice] To update, run: pip install --upgrade pip  

```

```python
from langchain.document\_loaders import PsychicLoader  
from psychicapi import ConnectorId  
  
# Create a document loader for google drive. We can also load from other connectors by setting the connector\_id to the appropriate value e.g. ConnectorId.notion.value  
# This loader uses our test credentials  
google\_drive\_loader = PsychicLoader(  
 api\_key="7ddb61c1-8b6a-4d31-a58e-30d1c9ea480e",  
 connector\_id=ConnectorId.gdrive.value,  
 connection\_id="google-test",  
)  
  
documents = google\_drive\_loader.load()  

```

## Converting the docs to embeddings[​](#converting-the-docs-to-embeddings "Direct link to Converting the docs to embeddings")

We can now convert these documents into embeddings and store them in a vector database like Chroma

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.vectorstores import Chroma  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.llms import OpenAI  
from langchain.chains import RetrievalQAWithSourcesChain  

```

```python
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
texts = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  
docsearch = Chroma.from\_documents(texts, embeddings)  
chain = RetrievalQAWithSourcesChain.from\_chain\_type(  
 OpenAI(temperature=0), chain\_type="stuff", retriever=docsearch.as\_retriever()  
)  
chain({"question": "what is psychic?"}, return\_only\_outputs=True)  

```

- [Prerequisites](#prerequisites)
- [Loading documents](#loading-documents)
- [Converting the docs to embeddings](#converting-the-docs-to-embeddings)
