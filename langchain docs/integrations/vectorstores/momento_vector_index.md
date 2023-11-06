# Momento Vector Index (MVI)

[MVI](https://gomomento.com): the most productive, easiest to use, serverless vector index for your data. To get started with MVI, simply sign up for an account. There's no need to handle infrastructure, manage servers, or be concerned about scaling. MVI is a service that scales automatically to meet your needs.

To sign up and access MVI, visit the [Momento Console](https://console.gomomento.com).

# Setup

## Install prerequisites[​](#install-prerequisites "Direct link to Install prerequisites")

You will need:

- the [`momento`](https://pypi.org/project/momento/) package for interacting with MVI, and
- the openai package for interacting with the OpenAI API.
- the tiktoken package for tokenizing text.

```bash
pip install momento openai tiktoken  

```

## Enter API keys[​](#enter-api-keys "Direct link to Enter API keys")

```python
import os  
import getpass  

```

### Momento: for indexing data[​](#momento-for-indexing-data "Direct link to Momento: for indexing data")

Visit the [Momento Console](https://console.gomomento.com) to get your API key.

```python
os.environ["MOMENTO\_API\_KEY"] = getpass.getpass("Momento API Key:")  

```

### OpenAI: for text embeddings[​](#openai-for-text-embeddings "Direct link to OpenAI: for text embeddings")

```python
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

# Load your data

Here we use the example dataset from Langchain, the state of the union address.

First we load relevant modules:

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import MomentoVectorIndex  
from langchain.document\_loaders import TextLoader  

```

Then we load the data:

```python
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
len(documents)  

```

```text
 1  

```

Note the data is one large file, hence there is only one document:

```python
len(documents[0].page\_content)  

```

```text
 38539  

```

Because this is one large text file, we split it into chunks for question answering. That way, user questions will be answered from the most relevant chunk.

```python
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
len(docs)  

```

```text
 42  

```

# Index your data

Indexing your data is as simple as instantiating the `MomentoVectorIndex` object. Here we use the `from_documents` helper to both instantiate and index the data:

```python
vector\_db = MomentoVectorIndex.from\_documents(  
 docs,  
 OpenAIEmbeddings(),  
 index\_name="sotu"  
)  

```

This connects to the Momento Vector Index service using your API key and indexes the data. If the index did not exist before, this process creates it for you. The data is now searchable.

# Query your data

## Ask a question directly against the index[​](#ask-a-question-directly-against-the-index "Direct link to Ask a question directly against the index")

The most direct way to query the data is to search against the index. We can do that as follows using the `VectorStore` API:

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs = vector\_db.similarity\_search(query)  

```

```python
docs[0].page\_content  

```

```text
 'Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.'  

```

While this does contain relevant information about Ketanji Brown Jackson, we don't have a concise, human-readable answer. We'll tackle that in the next section.

## Use an LLM to generate fluent answers[​](#use-an-llm-to-generate-fluent-answers "Direct link to Use an LLM to generate fluent answers")

With the data indexed in MVI, we can integrate with any chain that leverages vector similarity search. Here we use the `RetrievalQA` chain to demonstrate how to answer questions from the indexed data.

First we load the relevant modules:

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.chains import RetrievalQA  

```

Then we instantiate the retrieval QA chain:

```python
llm = ChatOpenAI(model\_name="gpt-3.5-turbo", temperature=0)  
qa\_chain = RetrievalQA.from\_chain\_type(llm, retriever=vector\_db.as\_retriever())  

```

```python
qa\_chain({"query": "What did the president say about Ketanji Brown Jackson?"})  

```

```text
 {'query': 'What did the president say about Ketanji Brown Jackson?',  
 'result': "The President said that he nominated Circuit Court of Appeals Judge Ketanji Brown Jackson to serve on the United States Supreme Court. He described her as one of the nation's top legal minds and mentioned that she has received broad support from various groups, including the Fraternal Order of Police and former judges appointed by Democrats and Republicans."}  

```

# Next Steps

That's it! You've now indexed your data and can query it using the Momento Vector Index. You can use the same index to query your data from any chain that supports vector similarity search.

With Momento you can not only index your vector data, but also cache your API calls and store your chat message history. Check out the other Momento langchain integrations to learn more.

To learn more about the Momento Vector Index, visit the [Momento Documentation](https://docs.gomomento.com).

- [Install prerequisites](#install-prerequisites)

- [Enter API keys](#enter-api-keys)

  - [Momento: for indexing data](#momento-for-indexing-data)
  - [OpenAI: for text embeddings](#openai-for-text-embeddings)

- [Ask a question directly against the index](#ask-a-question-directly-against-the-index)

- [Use an LLM to generate fluent answers](#use-an-llm-to-generate-fluent-answers)

- [Momento: for indexing data](#momento-for-indexing-data)

- [OpenAI: for text embeddings](#openai-for-text-embeddings)
