# Tigris

[Tigris](htttps://tigrisdata.com) is an open-source Serverless NoSQL Database and Search Platform designed to simplify building high-performance vector search applications.
`Tigris` eliminates the infrastructure complexity of managing, operating, and synchronizing multiple tools, allowing you to focus on building great applications instead.

This notebook guides you how to use Tigris as your VectorStore

**Pre requisites**

1. An OpenAI account. You can sign up for an account [here](https://platform.openai.com/)
1. [Sign up for a free Tigris account](https://console.preview.tigrisdata.cloud). Once you have signed up for the Tigris account, create a new project called `vectordemo`. Next, make a note of the *Uri* for the region you've created your project in, the **clientId** and **clientSecret**. You can get all this information from the **Application Keys** section of the project.

Let's first install our dependencies:

```bash
pip install tigrisdb openapi-schema-pydantic openai tiktoken  

```

We will load the `OpenAI` api key and `Tigris` credentials in our environment

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  
os.environ["TIGRIS\_PROJECT"] = getpass.getpass("Tigris Project Name:")  
os.environ["TIGRIS\_CLIENT\_ID"] = getpass.getpass("Tigris Client Id:")  
os.environ["TIGRIS\_CLIENT\_SECRET"] = getpass.getpass("Tigris Client Secret:")  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Tigris  
from langchain.document\_loaders import TextLoader  

```

### Initialize Tigris vector store[​](#initialize-tigris-vector-store "Direct link to Initialize Tigris vector store")

Let's import our test dataset:

```python
loader = TextLoader("../../../state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

```python
vector\_store = Tigris.from\_documents(docs, embeddings, index\_name="my\_embeddings")  

```

### Similarity Search[​](#similarity-search "Direct link to Similarity Search")

```python
query = "What did the president say about Ketanji Brown Jackson"  
found\_docs = vector\_store.similarity\_search(query)  
print(found\_docs)  

```

### Similarity Search with score (vector distance)[​](#similarity-search-with-score-vector-distance "Direct link to Similarity Search with score (vector distance)")

```python
query = "What did the president say about Ketanji Brown Jackson"  
result = vector\_store.similarity\_search\_with\_score(query)  
for doc, score in result:  
 print(f"document={doc}, score={score}")  

```

- [Initialize Tigris vector store](#initialize-tigris-vector-store)
- [Similarity Search](#similarity-search)
- [Similarity Search with score (vector distance)](#similarity-search-with-score-vector-distance)
