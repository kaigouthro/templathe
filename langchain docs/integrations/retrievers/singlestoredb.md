# SingleStoreDB

[SingleStoreDB](https://singlestore.com/) is a high-performance distributed SQL database that supports deployment both in the [cloud](https://www.singlestore.com/cloud/) and on-premises. It provides vector storage, and vector functions including [dot_product](https://docs.singlestore.com/managed-service/en/reference/sql-reference/vector-functions/dot_product.html) and [euclidean_distance](https://docs.singlestore.com/managed-service/en/reference/sql-reference/vector-functions/euclidean_distance.html), thereby supporting AI applications that require text similarity matching.

This notebook shows how to use a retriever that uses `SingleStoreDB`.

```bash
# Establishing a connection to the database is facilitated through the singlestoredb Python connector.  
# Please ensure that this connector is installed in your working environment.  
pip install singlestoredb  

```

## Create Retriever from vector store[​](#create-retriever-from-vector-store "Direct link to Create Retriever from vector store")

```python
import os  
import getpass  
  
# We want to use OpenAIEmbeddings so we have to get the OpenAI API Key.  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  
  
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import SingleStoreDB  
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  
  
# Setup connection url as environment variable  
os.environ["SINGLESTOREDB\_URL"] = "root:pass@localhost:3306/db"  
  
# Load documents to the store  
docsearch = SingleStoreDB.from\_documents(  
 docs,  
 embeddings,  
 table\_name="notebook", # use table with a custom name  
)  
  
# create retriever from the vector store  
retriever = docsearch.as\_retriever(search\_kwargs={"k": 2})  

```

## Search with retriever[​](#search-with-retriever "Direct link to Search with retriever")

```python
result = retriever.get\_relevant\_documents("What did the president say about Ketanji Brown Jackson")  
print(docs[0].page\_content)  

```

- [Create Retriever from vector store](#create-retriever-from-vector-store)
- [Search with retriever](#search-with-retriever)
