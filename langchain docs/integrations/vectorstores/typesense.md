# Typesense

[Typesense](https://typesense.org) is an open-source, in-memory search engine, that you can either [self-host](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting) or run on [Typesense Cloud](https://cloud.typesense.org/).

Typesense focuses on performance by storing the entire index in RAM (with a backup on disk) and also focuses on providing an out-of-the-box developer experience by simplifying available options and setting good defaults.

It also lets you combine attribute-based filtering together with vector queries, to fetch the most relevant documents.

This notebook shows you how to use Typesense as your VectorStore.

Let's first install our dependencies:

```bash
pip install typesense openapi-schema-pydantic openai tiktoken  

```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Typesense  
from langchain.document\_loaders import TextLoader  

```

Let's import our test dataset:

```python
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

```python
docsearch = Typesense.from\_documents(  
 docs,  
 embeddings,  
 typesense\_client\_params={  
 "host": "localhost", # Use xxx.a1.typesense.net for Typesense Cloud  
 "port": "8108", # Use 443 for Typesense Cloud  
 "protocol": "http", # Use https for Typesense Cloud  
 "typesense\_api\_key": "xyz",  
 "typesense\_collection\_name": "lang-chain",  
 },  
)  

```

## Similarity Search[​](#similarity-search "Direct link to Similarity Search")

```python
query = "What did the president say about Ketanji Brown Jackson"  
found\_docs = docsearch.similarity\_search(query)  

```

```python
print(found\_docs[0].page\_content)  

```

## Typesense as a Retriever[​](#typesense-as-a-retriever "Direct link to Typesense as a Retriever")

Typesense, as all the other vector stores, is a LangChain Retriever, by using cosine similarity.

```python
retriever = docsearch.as\_retriever()  
retriever  

```

```python
query = "What did the president say about Ketanji Brown Jackson"  
retriever.get\_relevant\_documents(query)[0]  

```

- [Similarity Search](#similarity-search)
- [Typesense as a Retriever](#typesense-as-a-retriever)
