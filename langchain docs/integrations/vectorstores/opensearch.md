# OpenSearch

[OpenSearch](https://opensearch.org/) is a scalable, flexible, and extensible open-source software suite for search, analytics, and observability applications licensed under Apache 2.0. `OpenSearch` is a distributed search and analytics engine based on `Apache Lucene`.

This notebook shows how to use functionality related to the `OpenSearch` database.

To run, you should have an OpenSearch instance up and running: [see here for an easy Docker installation](https://hub.docker.com/r/opensearchproject/opensearch).

`similarity_search` by default performs the Approximate k-NN Search which uses one of the several algorithms like lucene, nmslib, faiss recommended for
large datasets. To perform brute force search we have other search methods known as Script Scoring and Painless Scripting.
Check [this](https://opensearch.org/docs/latest/search-plugins/knn/index/) for more details.

## Installation[​](#installation "Direct link to Installation")

Install the Python client.

```bash
pip install opensearch-py  

```

We want to use OpenAIEmbeddings so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import OpenSearchVectorSearch  
from langchain.document\_loaders import TextLoader  

```

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

## similarity_search using Approximate k-NN[​](#similarity_search-using-approximate-k-nn "Direct link to similarity_search using Approximate k-NN")

`similarity_search` using `Approximate k-NN` Search with Custom Parameters

```python
docsearch = OpenSearchVectorSearch.from\_documents(  
 docs, embeddings, opensearch\_url="http://localhost:9200"  
)  
  
# If using the default Docker installation, use this instantiation instead:  
# docsearch = OpenSearchVectorSearch.from\_documents(  
# docs,  
# embeddings,  
# opensearch\_url="https://localhost:9200",  
# http\_auth=("admin", "admin"),  
# use\_ssl = False,  
# verify\_certs = False,  
# ssl\_assert\_hostname = False,  
# ssl\_show\_warn = False,  
# )  

```

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs = docsearch.similarity\_search(query, k=10)  

```

```python
print(docs[0].page\_content)  

```

```python
docsearch = OpenSearchVectorSearch.from\_documents(  
 docs,  
 embeddings,  
 opensearch\_url="http://localhost:9200",  
 engine="faiss",  
 space\_type="innerproduct",  
 ef\_construction=256,  
 m=48,  
)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs = docsearch.similarity\_search(query)  

```

```python
print(docs[0].page\_content)  

```

## similarity_search using Script Scoring[​](#similarity_search-using-script-scoring "Direct link to similarity_search using Script Scoring")

`similarity_search` using `Script Scoring` with Custom Parameters

```python
docsearch = OpenSearchVectorSearch.from\_documents(  
 docs, embeddings, opensearch\_url="http://localhost:9200", is\_appx\_search=False  
)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs = docsearch.similarity\_search(  
 "What did the president say about Ketanji Brown Jackson",  
 k=1,  
 search\_type="script\_scoring",  
)  

```

```python
print(docs[0].page\_content)  

```

## similarity_search using Painless Scripting[​](#similarity_search-using-painless-scripting "Direct link to similarity_search using Painless Scripting")

`similarity_search` using `Painless Scripting` with Custom Parameters

```python
docsearch = OpenSearchVectorSearch.from\_documents(  
 docs, embeddings, opensearch\_url="http://localhost:9200", is\_appx\_search=False  
)  
filter = {"bool": {"filter": {"term": {"text": "smuggling"}}}}  
query = "What did the president say about Ketanji Brown Jackson"  
docs = docsearch.similarity\_search(  
 "What did the president say about Ketanji Brown Jackson",  
 search\_type="painless\_scripting",  
 space\_type="cosineSimilarity",  
 pre\_filter=filter,  
)  

```

```python
print(docs[0].page\_content)  

```

## Maximum marginal relevance search (MMR)[​](#maximum-marginal-relevance-search-mmr "Direct link to Maximum marginal relevance search (MMR)")

If you’d like to look up for some similar documents, but you’d also like to receive diverse results, MMR is method you should consider. Maximal marginal relevance optimizes for similarity to query AND diversity among selected documents.

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs = docsearch.max\_marginal\_relevance\_search(query, k=2, fetch\_k=10, lambda\_param=0.5)  

```

## Using a preexisting OpenSearch instance[​](#using-a-preexisting-opensearch-instance "Direct link to Using a preexisting OpenSearch instance")

It's also possible to use a preexisting OpenSearch instance with documents that already have vectors present.

```python
# this is just an example, you would need to change these values to point to another opensearch instance  
docsearch = OpenSearchVectorSearch(  
 index\_name="index-\*",  
 embedding\_function=embeddings,  
 opensearch\_url="http://localhost:9200",  
)  
  
# you can specify custom field names to match the fields you're using to store your embedding, document text value, and metadata  
docs = docsearch.similarity\_search(  
 "Who was asking about getting lunch today?",  
 search\_type="script\_scoring",  
 space\_type="cosinesimil",  
 vector\_field="message\_embedding",  
 text\_field="message",  
 metadata\_field="message\_metadata",  
)  

```

## Using AOSS (Amazon OpenSearch Service Serverless)[​](#using-aoss-amazon-opensearch-service-serverless "Direct link to Using AOSS (Amazon OpenSearch Service Serverless)")

```python
# This is just an example to show how to use AOSS with faiss engine and efficient\_filter, you need to set proper values.  
  
service = 'aoss' # must set the service as 'aoss'  
region = 'us-east-2'  
credentials = boto3.Session(aws\_access\_key\_id='xxxxxx',aws\_secret\_access\_key='xxxxx').get\_credentials()  
awsauth = AWS4Auth('xxxxx', 'xxxxxx', region,service, session\_token=credentials.token)  
  
docsearch = OpenSearchVectorSearch.from\_documents(  
 docs,  
 embeddings,  
 opensearch\_url="host url",  
 http\_auth=awsauth,  
 timeout = 300,  
 use\_ssl = True,  
 verify\_certs = True,  
 connection\_class = RequestsHttpConnection,  
 index\_name="test-index-using-aoss",  
 engine="faiss",  
)  
  
docs = docsearch.similarity\_search(  
 "What is feature selection",  
 efficient\_filter=filter,  
 k=200,  
)  

```

## Using AOS (Amazon OpenSearch Service)[​](#using-aos-amazon-opensearch-service "Direct link to Using AOS (Amazon OpenSearch Service)")

```python
# This is just an example to show how to use AOS , you need to set proper values.  
  
service = 'es' # must set the service as 'es'  
region = 'us-east-2'  
credentials = boto3.Session(aws\_access\_key\_id='xxxxxx',aws\_secret\_access\_key='xxxxx').get\_credentials()  
awsauth = AWS4Auth('xxxxx', 'xxxxxx', region,service, session\_token=credentials.token)  
  
docsearch = OpenSearchVectorSearch.from\_documents(  
 docs,  
 embeddings,  
 opensearch\_url="host url",  
 http\_auth=awsauth,  
 timeout = 300,  
 use\_ssl = True,  
 verify\_certs = True,  
 connection\_class = RequestsHttpConnection,  
 index\_name="test-index",  
)  
  
docs = docsearch.similarity\_search(  
 "What is feature selection",  
 k=200,  
)  

```

- [Installation](#installation)
- [similarity_search using Approximate k-NN](#similarity_search-using-approximate-k-nn)
- [similarity_search using Script Scoring](#similarity_search-using-script-scoring)
- [similarity_search using Painless Scripting](#similarity_search-using-painless-scripting)
- [Maximum marginal relevance search (MMR)](#maximum-marginal-relevance-search-mmr)
- [Using a preexisting OpenSearch instance](#using-a-preexisting-opensearch-instance)
- [Using AOSS (Amazon OpenSearch Service Serverless)](#using-aoss-amazon-opensearch-service-serverless)
- [Using AOS (Amazon OpenSearch Service)](#using-aos-amazon-opensearch-service)
