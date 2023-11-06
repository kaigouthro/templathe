# Azure Cosmos DB

[Azure Cosmos DB for MongoDB vCore](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/) makes it easy to create a database with full native MongoDB support.
You can apply your MongoDB experience and continue to use your favorite MongoDB drivers, SDKs, and tools by pointing your application to the API for MongoDB vCore account's connection string.
Use vector search in Azure Cosmos DB for MongoDB vCore to seamlessly integrate your AI-based applications with your data that's stored in Azure Cosmos DB.

This notebook shows you how to leverage the [Vector Search](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/vector-search) capabilities within Azure Cosmos DB for Mongo vCore to store documents in collections, create indicies and perform vector search queries using approximate nearest neighbor algorithms such as COS (cosine distance), L2 (Euclidean distance), and IP (inner product) to locate documents close to the query vectors.

Azure Cosmos DB for MongoDB vCore provides developers with a fully managed MongoDB-compatible database service for building modern applications with a familiar architecture.

With Cosmos DB for MongoDB vCore, developers can enjoy the benefits of native Azure integrations, low total cost of ownership (TCO), and the familiar vCore architecture when migrating existing applications or building new ones.

[Sign Up](https://azure.microsoft.com/en-us/free/) for free to get started today.

```bash
pip install pymongo  

```

```text
 Requirement already satisfied: pymongo in /Users/iekpo/Langchain/langchain-python/.venv/lib/python3.10/site-packages (4.5.0)  
 Requirement already satisfied: dnspython<3.0.0,>=1.16.0 in /Users/iekpo/Langchain/langchain-python/.venv/lib/python3.10/site-packages (from pymongo) (2.4.2)  

```

```python
import os  
import getpass  
  
CONNECTION\_STRING = "AZURE COSMOS DB MONGO vCORE connection string"  
INDEX\_NAME = "izzy-test-index"  
NAMESPACE = "izzy\_test\_db.izzy\_test\_collection"  
DB\_NAME, COLLECTION\_NAME = NAMESPACE.split(".")  

```

We want to use `OpenAIEmbeddings` so we need to set up our Azure OpenAI API Key alongside other environment variables.

```python
# Set up the OpenAI Environment Variables  
os.environ["OPENAI\_API\_TYPE"] = "azure"  
os.environ["OPENAI\_API\_VERSION"] = "2023-05-15"  
os.environ["OPENAI\_API\_BASE"] = "YOUR\_OPEN\_AI\_ENDPOINT" # https://example.openai.azure.com/  
os.environ["OPENAI\_API\_KEY"] = "YOUR\_OPEN\_AI\_KEY"  
os.environ["OPENAI\_EMBEDDINGS\_DEPLOYMENT"] = "smart-agent-embedding-ada" # the deployment name for the embedding model  
os.environ["OPENAI\_EMBEDDINGS\_MODEL\_NAME"] = "text-embedding-ada-002" # the model name  

```

Now, we need to load the documents into the collection, create the index and then run our queries against the index to retrieve matches.

Please refer to the [documentation](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/vector-search) if you have questions about certain parameters

```python
from langchain.docstore.document import Document  
from langchain.embeddings import OpenAIEmbeddings  
from langchain.schema.embeddings import Embeddings  
from langchain.vectorstores.azure\_cosmos\_db\_vector\_search import AzureCosmosDBVectorSearch, CosmosDBSimilarityType  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.document\_loaders import TextLoader  
  
SOURCE\_FILE\_NAME = "../../modules/state\_of\_the\_union.txt"  
  
loader = TextLoader(SOURCE\_FILE\_NAME)  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
# OpenAI Settings  
model\_deployment = os.getenv("OPENAI\_EMBEDDINGS\_DEPLOYMENT", "smart-agent-embedding-ada")  
model\_name = os.getenv("OPENAI\_EMBEDDINGS\_MODEL\_NAME", "text-embedding-ada-002")  
  
  
openai\_embeddings: OpenAIEmbeddings = OpenAIEmbeddings(deployment=model\_deployment, model=model\_name, chunk\_size=1)  

```

```python
from pymongo import MongoClient  
  
INDEX\_NAME = "izzy-test-index-2"  
NAMESPACE = "izzy\_test\_db.izzy\_test\_collection"  
DB\_NAME, COLLECTION\_NAME = NAMESPACE.split(".")  
  
client: MongoClient = MongoClient(CONNECTION\_STRING)  
collection = client[DB\_NAME][COLLECTION\_NAME]  
  
model\_deployment = os.getenv("OPENAI\_EMBEDDINGS\_DEPLOYMENT", "smart-agent-embedding-ada")  
model\_name = os.getenv("OPENAI\_EMBEDDINGS\_MODEL\_NAME", "text-embedding-ada-002")  
  
vectorstore = AzureCosmosDBVectorSearch.from\_documents(  
 docs,  
 openai\_embeddings,  
 collection=collection,  
 index\_name=INDEX\_NAME,  
)  
  
num\_lists = 100  
dimensions = 1536  
similarity\_algorithm = CosmosDBSimilarityType.COS  
  
vectorstore.create\_index(num\_lists, dimensions, similarity\_algorithm)  

```

```text
 {'raw': {'defaultShard': {'numIndexesBefore': 2,  
 'numIndexesAfter': 3,  
 'createdCollectionAutomatically': False,  
 'ok': 1}},  
 'ok': 1}  

```

```python
# perform a similarity search between the embedding of the query and the embeddings of the documents  
query = "What did the president say about Ketanji Brown Jackson"  
docs = vectorstore.similarity\_search(query)  

```

```python
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

Once the documents have been loaded and the index has been created, you can now instantiate the vector store directly and run queries against the index

```python
vectorstore = AzureCosmosDBVectorSearch.from\_connection\_string(CONNECTION\_STRING, NAMESPACE, openai\_embeddings, index\_name=INDEX\_NAME)  
  
# perform a similarity search between a query and the ingested documents  
query = "What did the president say about Ketanji Brown Jackson"  
docs = vectorstore.similarity\_search(query)  
  
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

```python
vectorstore = AzureCosmosDBVectorSearch(collection, openai\_embeddings, index\_name=INDEX\_NAME)  
  
# perform a similarity search between a query and the ingested documents  
query = "What did the president say about Ketanji Brown Jackson"  
docs = vectorstore.similarity\_search(query)  
  
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```
