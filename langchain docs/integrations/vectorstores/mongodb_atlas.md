# MongoDB Atlas

[MongoDB Atlas](https://www.mongodb.com/docs/atlas/) is a fully-managed cloud database available in AWS, Azure, and GCP. It now has support for native Vector Search on your MongoDB document data.

This notebook shows how to use `MongoDB Atlas Vector Search` to store your embeddings in MongoDB documents, create a vector search index, and perform KNN search with an approximate nearest neighbor algorithm.

It uses the [knnBeta Operator](https://www.mongodb.com/docs/atlas/atlas-search/knn-beta) available in MongoDB Atlas Search. This feature is in Public Preview and available for evaluation purposes, to validate functionality, and to gather feedback from public preview users. It is not recommended for production deployments as we may introduce breaking changes.

To use MongoDB Atlas, you must first deploy a cluster. We have a Forever-Free tier of clusters available.
To get started head over to Atlas here: [quick start](https://www.mongodb.com/docs/atlas/getting-started/).

```bash
pip install pymongo  

```

```python
import os  
import getpass  
  
MONGODB\_ATLAS\_CLUSTER\_URI = getpass.getpass("MongoDB Atlas Cluster URI:")  

```

We want to use `OpenAIEmbeddings` so we need to set up our OpenAI API Key.

```python
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

Now, let's create a vector search index on your cluster. In the below example, `embedding` is the name of the field that contains the embedding vector. Please refer to the [documentation](https://www.mongodb.com/docs/atlas/atlas-search/define-field-mappings-for-vector-search) to get more details on how to define an Atlas Vector Search index.
You can name the index `langchain_demo` and create the index on the namespace `lanchain_db.langchain_col`. Finally, write the following definition in the JSON editor on MongoDB Atlas:

```json
{  
 "mappings": {  
 "dynamic": true,  
 "fields": {  
 "embedding": {  
 "dimensions": 1536,  
 "similarity": "cosine",  
 "type": "knnVector"  
 }  
 }  
 }  
}  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import MongoDBAtlasVectorSearch  
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

```python
from pymongo import MongoClient  
  
# initialize MongoDB python client  
client = MongoClient(MONGODB\_ATLAS\_CLUSTER\_URI)  
  
db\_name = "langchain\_db"  
collection\_name = "langchain\_col"  
collection = client[db\_name][collection\_name]  
index\_name = "langchain\_demo"  
  
# insert the documents in MongoDB Atlas with their embedding  
docsearch = MongoDBAtlasVectorSearch.from\_documents(  
 docs, embeddings, collection=collection, index\_name=index\_name  
)  
  
# perform a similarity search between the embedding of the query and the embeddings of the documents  
query = "What did the president say about Ketanji Brown Jackson"  
docs = docsearch.similarity\_search(query)  

```

```python
print(docs[0].page\_content)  

```

You can also instantiate the vector store directly and execute a query as follows:

```python
# initialize vector store  
vectorstore = MongoDBAtlasVectorSearch(  
 collection, OpenAIEmbeddings(), index\_name=index\_name  
)  
  
# perform a similarity search between a query and the ingested documents  
query = "What did the president say about Ketanji Brown Jackson"  
docs = vectorstore.similarity\_search(query)  
  
print(docs[0].page\_content)  

```
