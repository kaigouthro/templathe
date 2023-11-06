# Azure Cognitive Search

[Azure Cognitive Search](https://learn.microsoft.com/azure/search/search-what-is-azure-search) (formerly known as `Azure Search`) is a cloud search service that gives developers infrastructure, APIs, and tools for building a rich search experience over private, heterogeneous content in web, mobile, and enterprise applications.

Vector search is currently in public preview. It's available through the Azure portal, preview REST API and beta client libraries. [More info](https://learn.microsoft.com/en-us/azure/search/vector-search-overview) Beta client libraries are subject to potential breaking changes, please be sure to use the SDK package version identified below. azure-search-documents==11.4.0b8

# Install Azure Cognitive Search SDK

```bash
pip install azure-search-documents==11.4.0b8  
pip install azure-identity  

```

## Import required libraries[​](#import-required-libraries "Direct link to Import required libraries")

```python
import openai  
import os  
from langchain.embeddings import OpenAIEmbeddings  
from langchain.vectorstores.azuresearch import AzureSearch  

```

## Configure OpenAI settings[​](#configure-openai-settings "Direct link to Configure OpenAI settings")

Configure the OpenAI settings to use Azure OpenAI or OpenAI

```python
os.environ["OPENAI\_API\_TYPE"] = "azure"  
os.environ["OPENAI\_API\_BASE"] = "YOUR\_OPENAI\_ENDPOINT"  
os.environ["OPENAI\_API\_KEY"] = "YOUR\_OPENAI\_API\_KEY"  
os.environ["OPENAI\_API\_VERSION"] = "2023-05-15"  
model: str = "text-embedding-ada-002"  

```

## Configure vector store settings[​](#configure-vector-store-settings "Direct link to Configure vector store settings")

Set up the vector store settings using environment variables:

```python
vector\_store\_address: str = "YOUR\_AZURE\_SEARCH\_ENDPOINT"  
vector\_store\_password: str = "YOUR\_AZURE\_SEARCH\_ADMIN\_KEY"  

```

## Create embeddings and vector store instances[​](#create-embeddings-and-vector-store-instances "Direct link to Create embeddings and vector store instances")

Create instances of the OpenAIEmbeddings and AzureSearch classes:

```python
embeddings: OpenAIEmbeddings = OpenAIEmbeddings(deployment=model, chunk\_size=1)  
index\_name: str = "langchain-vector-demo"  
vector\_store: AzureSearch = AzureSearch(  
 azure\_search\_endpoint=vector\_store\_address,  
 azure\_search\_key=vector\_store\_password,  
 index\_name=index\_name,  
 embedding\_function=embeddings.embed\_query,  
)  

```

## Insert text and embeddings into vector store[​](#insert-text-and-embeddings-into-vector-store "Direct link to Insert text and embeddings into vector store")

Add texts and metadata from the JSON data to the vector store:

```python
from langchain.document\_loaders import TextLoader  
from langchain.text\_splitter import CharacterTextSplitter  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt", encoding="utf-8")  
  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
vector\_store.add\_documents(documents=docs)  

```

## Perform a vector similarity search[​](#perform-a-vector-similarity-search "Direct link to Perform a vector similarity search")

Execute a pure vector similarity search using the similarity_search() method:

```python
# Perform a similarity search  
docs = vector\_store.similarity\_search(  
 query="What did the president say about Ketanji Brown Jackson",  
 k=3,  
 search\_type="similarity",  
)  
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

## Perform a vector similarity search with relevance scores[​](#perform-a-vector-similarity-search-with-relevance-scores "Direct link to Perform a vector similarity search with relevance scores")

Execute a pure vector similarity search using the similarity_search_with_relevance_scores() method:

```python
docs\_and\_scores = vector\_store.similarity\_search\_with\_relevance\_scores(query="What did the president say about Ketanji Brown Jackson", k=4, score\_threshold=0.80)  
from pprint import pprint  
pprint(docs\_and\_scores)  

```

```text
 [(Document(page\_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': 'C:\\repos\\langchain-fruocco-acs\\langchain\\docs\\extras\\modules\\state\_of\_the\_union.txt'}),  
 0.8441472),  
 (Document(page\_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': 'C:\\repos\\langchain-fruocco-acs\\langchain\\docs\\extras\\modules\\state\_of\_the\_union.txt'}),  
 0.8441472),  
 (Document(page\_content='A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling. \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers. \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', metadata={'source': 'C:\\repos\\langchain-fruocco-acs\\langchain\\docs\\extras\\modules\\state\_of\_the\_union.txt'}),  
 0.82153815),  
 (Document(page\_content='A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling. \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers. \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', metadata={'source': 'C:\\repos\\langchain-fruocco-acs\\langchain\\docs\\extras\\modules\\state\_of\_the\_union.txt'}),  
 0.82153815)]  

```

## Perform a Hybrid Search[​](#perform-a-hybrid-search "Direct link to Perform a Hybrid Search")

Execute hybrid search using the search_type or hybrid_search() method:

```python
# Perform a hybrid search  
docs = vector\_store.similarity\_search(  
 query="What did the president say about Ketanji Brown Jackson",  
 k=3,   
 search\_type="hybrid"  
)  
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

```python
# Perform a hybrid search  
docs = vector\_store.hybrid\_search(  
 query="What did the president say about Ketanji Brown Jackson",   
 k=3  
)  
print(docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

# Create a new index with custom filterable fields

```python
from azure.search.documents.indexes.models import (  
 SearchableField,  
 SearchField,  
 SearchFieldDataType,  
 SimpleField,  
 ScoringProfile,  
 TextWeights,  
)  
  
embeddings: OpenAIEmbeddings = OpenAIEmbeddings(deployment=model, chunk\_size=1)  
embedding\_function = embeddings.embed\_query  
  
fields = [  
 SimpleField(  
 name="id",  
 type=SearchFieldDataType.String,  
 key=True,  
 filterable=True,  
 ),  
 SearchableField(  
 name="content",  
 type=SearchFieldDataType.String,  
 searchable=True,  
 ),  
 SearchField(  
 name="content\_vector",  
 type=SearchFieldDataType.Collection(SearchFieldDataType.Single),  
 searchable=True,  
 vector\_search\_dimensions=len(embedding\_function("Text")),  
 vector\_search\_configuration="default",  
 ),  
 SearchableField(  
 name="metadata",  
 type=SearchFieldDataType.String,  
 searchable=True,  
 ),  
 # Additional field to store the title  
 SearchableField(  
 name="title",  
 type=SearchFieldDataType.String,  
 searchable=True,  
 ),  
 # Additional field for filtering on document source  
 SimpleField(  
 name="source",  
 type=SearchFieldDataType.String,  
 filterable=True,  
 ),  
]  
  
index\_name: str = "langchain-vector-demo-custom"  
  
vector\_store: AzureSearch = AzureSearch(  
 azure\_search\_endpoint=vector\_store\_address,  
 azure\_search\_key=vector\_store\_password,  
 index\_name=index\_name,  
 embedding\_function=embedding\_function,  
 fields=fields,  
)  

```

# Perform a query with a custom filter

```python
# Data in the metadata dictionary with a corresponding field in the index will be added to the index  
# In this example, the metadata dictionary contains a title, a source and a random field  
# The title and the source will be added to the index as separate fields, but the random won't. (as it is not defined in the fields list)  
# The random field will be only stored in the metadata field  
vector\_store.add\_texts(  
 ["Test 1", "Test 2", "Test 3"],  
 [  
 {"title": "Title 1", "source": "A", "random": "10290"},  
 {"title": "Title 2", "source": "A", "random": "48392"},  
 {"title": "Title 3", "source": "B", "random": "32893"},  
 ],  
)  

```

```python
res = vector\_store.similarity\_search(query="Test 3 source1", k=3, search\_type="hybrid")  
res  

```

```text
 [Document(page\_content='Test 3', metadata={'title': 'Title 3', 'source': 'B', 'random': '32893'}),  
 Document(page\_content='Test 1', metadata={'title': 'Title 1', 'source': 'A', 'random': '10290'}),  
 Document(page\_content='Test 2', metadata={'title': 'Title 2', 'source': 'A', 'random': '48392'})]  

```

```python
res = vector\_store.similarity\_search(query="Test 3 source1", k=3, search\_type="hybrid", filters="source eq 'A'")  
res  

```

```text
 [Document(page\_content='Test 1', metadata={'title': 'Title 1', 'source': 'A', 'random': '10290'}),  
 Document(page\_content='Test 2', metadata={'title': 'Title 2', 'source': 'A', 'random': '48392'})]  

```

# Create a new index with a Scoring Profile

```python
from azure.search.documents.indexes.models import (  
 SearchableField,  
 SearchField,  
 SearchFieldDataType,  
 SimpleField,  
 ScoringProfile,  
 TextWeights,  
 ScoringFunction,  
 FreshnessScoringFunction,  
 FreshnessScoringParameters  
)  
  
embeddings: OpenAIEmbeddings = OpenAIEmbeddings(deployment=model, chunk\_size=1)  
embedding\_function = embeddings.embed\_query  
  
fields = [  
 SimpleField(  
 name="id",  
 type=SearchFieldDataType.String,  
 key=True,  
 filterable=True,  
 ),  
 SearchableField(  
 name="content",  
 type=SearchFieldDataType.String,  
 searchable=True,  
 ),  
 SearchField(  
 name="content\_vector",  
 type=SearchFieldDataType.Collection(SearchFieldDataType.Single),  
 searchable=True,  
 vector\_search\_dimensions=len(embedding\_function("Text")),  
 vector\_search\_configuration="default",  
 ),  
 SearchableField(  
 name="metadata",  
 type=SearchFieldDataType.String,  
 searchable=True,  
 ),  
 # Additional field to store the title  
 SearchableField(  
 name="title",  
 type=SearchFieldDataType.String,  
 searchable=True,  
 ),  
 # Additional field for filtering on document source  
 SimpleField(  
 name="source",  
 type=SearchFieldDataType.String,  
 filterable=True,  
 ),  
 # Additional data field for last doc update  
 SimpleField(  
 name="last\_update",  
 type=SearchFieldDataType.DateTimeOffset,  
 searchable=True,  
 filterable=True  
 )  
]  
# Adding a custom scoring profile with a freshness function  
sc\_name = "scoring\_profile"  
sc = ScoringProfile(  
 name=sc\_name,  
 text\_weights=TextWeights(weights={"title": 5}),  
 function\_aggregation="sum",  
 functions=[  
 FreshnessScoringFunction(  
 field\_name="last\_update",  
 boost=100,  
 parameters=FreshnessScoringParameters(boosting\_duration="P2D"),  
 interpolation="linear"  
 )  
 ]  
)  
  
index\_name = "langchain-vector-demo-custom-scoring-profile"  
  
vector\_store: AzureSearch = AzureSearch(  
 azure\_search\_endpoint=vector\_store\_address,  
 azure\_search\_key=vector\_store\_password,  
 index\_name=index\_name,  
 embedding\_function=embeddings.embed\_query,  
 fields=fields,  
 scoring\_profiles = [sc],  
 default\_scoring\_profile = sc\_name  
)  

```

```python
# Adding same data with different last\_update to show Scoring Profile effect  
from datetime import datetime, timedelta  
  
today = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S-00:00')  
yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S-00:00')  
one\_month\_ago = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S-00:00')  
  
vector\_store.add\_texts(  
 ["Test 1", "Test 1", "Test 1"],  
 [  
 {"title": "Title 1", "source": "source1", "random": "10290", "last\_update": today},  
 {"title": "Title 1", "source": "source1", "random": "48392", "last\_update": yesterday},  
 {"title": "Title 1", "source": "source1", "random": "32893", "last\_update": one\_month\_ago},  
 ],  
)  

```

```text
 ['NjQyNTI5ZmMtNmVkYS00Njg5LTk2ZDgtMjM3OTY4NTJkYzFj',  
 'M2M0MGExZjAtMjhiZC00ZDkwLThmMTgtODNlN2Y2ZDVkMTMw',  
 'ZmFhMDE1NzMtMjZjNS00MTFiLTk0MTEtNGRkYjgwYWQwOTI0']  

```

```python
res = vector\_store.similarity\_search(query="Test 1", k=3, search\_type="similarity")  
res  

```

```text
 [Document(page\_content='Test 1', metadata={'title': 'Title 1', 'source': 'source1', 'random': '10290', 'last\_update': '2023-07-13T10:47:39-00:00'}),  
 Document(page\_content='Test 1', metadata={'title': 'Title 1', 'source': 'source1', 'random': '48392', 'last\_update': '2023-07-12T10:47:39-00:00'}),  
 Document(page\_content='Test 1', metadata={'title': 'Title 1', 'source': 'source1', 'random': '32893', 'last\_update': '2023-06-13T10:47:39-00:00'})]  

```

- [Import required libraries](#import-required-libraries)
- [Configure OpenAI settings](#configure-openai-settings)
- [Configure vector store settings](#configure-vector-store-settings)
- [Create embeddings and vector store instances](#create-embeddings-and-vector-store-instances)
- [Insert text and embeddings into vector store](#insert-text-and-embeddings-into-vector-store)
- [Perform a vector similarity search](#perform-a-vector-similarity-search)
- [Perform a vector similarity search with relevance scores](#perform-a-vector-similarity-search-with-relevance-scores)
- [Perform a Hybrid Search](#perform-a-hybrid-search)
