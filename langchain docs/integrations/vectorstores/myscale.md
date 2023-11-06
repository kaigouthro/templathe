# MyScale

[MyScale](https://docs.myscale.com/en/overview/) is a cloud-based database optimized for AI applications and solutions, built on the open-source [ClickHouse](https://github.com/ClickHouse/ClickHouse).

This notebook shows how to use functionality related to the `MyScale` vector database.

## Setting up environments[​](#setting-up-environments "Direct link to Setting up environments")

```bash
pip install clickhouse-connect  

```

We want to use OpenAIEmbeddings so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  
os.environ["OPENAI\_API\_BASE"] = getpass.getpass("OpenAI Base:")  
os.environ["MYSCALE\_HOST"] = getpass.getpass("MyScale Host:")  
os.environ["MYSCALE\_PORT"] = getpass.getpass("MyScale Port:")  
os.environ["MYSCALE\_USERNAME"] = getpass.getpass("MyScale Username:")  
os.environ["MYSCALE\_PASSWORD"] = getpass.getpass("MyScale Password:")  

```

There are two ways to set up parameters for myscale index.

1. Environment Variables

Before you run the app, please set the environment variable with `export`:
`export MYSCALE_HOST='<your-endpoints-url>' MYSCALE_PORT=<your-endpoints-port> MYSCALE_USERNAME=<your-username> MYSCALE_PASSWORD=<your-password> ...`

You can easily find your account, password and other info on our SaaS. For details please refer to [this document](https://docs.myscale.com/en/cluster-management/)

Every attributes under `MyScaleSettings` can be set with prefix `MYSCALE_` and is case insensitive.
2\. Create `MyScaleSettings` object with parameters

Environment Variables

Before you run the app, please set the environment variable with `export`:
`export MYSCALE_HOST='<your-endpoints-url>' MYSCALE_PORT=<your-endpoints-port> MYSCALE_USERNAME=<your-username> MYSCALE_PASSWORD=<your-password> ...`

You can easily find your account, password and other info on our SaaS. For details please refer to [this document](https://docs.myscale.com/en/cluster-management/)

Every attributes under `MyScaleSettings` can be set with prefix `MYSCALE_` and is case insensitive.

Create `MyScaleSettings` object with parameters

````text
```python  
from langchain.vectorstores import MyScale, MyScaleSettings  
config = MyScaleSetting(host="<your-backend-url>", port=8443, ...)  
index = MyScale(embedding\_function, config)  
index.add\_documents(...)  
````

````



```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import MyScale  
from langchain.document\_loaders import TextLoader  

````

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

```python
for d in docs:  
 d.metadata = {"some": "metadata"}  
docsearch = MyScale.from\_documents(docs, embeddings)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs = docsearch.similarity\_search(query)  

```

```text
 Inserting data...: 100%|██████████| 42/42 [00:15<00:00, 2.66it/s]  

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

## Get connection info and data schema[​](#get-connection-info-and-data-schema "Direct link to Get connection info and data schema")

```python
print(str(docsearch))  

```

## Filtering[​](#filtering "Direct link to Filtering")

You can have direct access to myscale SQL where statement. You can write `WHERE` clause following standard SQL.

**NOTE**: Please be aware of SQL injection, this interface must not be directly called by end-user.

If you customized your `column_map` under your setting, you search with filter like this:

```python
from langchain.vectorstores import MyScale, MyScaleSettings  
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  
  
for i, d in enumerate(docs):  
 d.metadata = {"doc\_id": i}  
  
docsearch = MyScale.from\_documents(docs, embeddings)  

```

```text
 Inserting data...: 100%|██████████| 42/42 [00:15<00:00, 2.68it/s]  

```

### Similarity search with score[​](#similarity-search-with-score "Direct link to Similarity search with score")

The returned distance score is cosine distance. Therefore, a lower score is better.

```python
meta = docsearch.metadata\_column  
output = docsearch.similarity\_search\_with\_relevance\_scores(  
 "What did the president say about Ketanji Brown Jackson?",  
 k=4,  
 where\_str=f"{meta}.doc\_id<10",  
)  
for d, dist in output:  
 print(dist, d.metadata, d.page\_content[:20] + "...")  

```

```text
 0.229655921459198 {'doc\_id': 0} Madam Speaker, Madam...  
 0.24506962299346924 {'doc\_id': 8} And so many families...  
 0.24786919355392456 {'doc\_id': 1} Groups of citizens b...  
 0.24875116348266602 {'doc\_id': 6} And I’m taking robus...  

```

## Deleting your data[​](#deleting-your-data "Direct link to Deleting your data")

You can either drop the table with `.drop()` method or partially delete your data with `.delete()` method.

```python
# use directly a `where\_str` to delete  
docsearch.delete(where\_str=f"{docsearch.metadata\_column}.doc\_id < 5")  
meta = docsearch.metadata\_column  
output = docsearch.similarity\_search\_with\_relevance\_scores(  
 "What did the president say about Ketanji Brown Jackson?",  
 k=4,  
 where\_str=f"{meta}.doc\_id<10",  
)  
for d, dist in output:  
 print(dist, d.metadata, d.page\_content[:20] + "...")  

```

```text
 0.24506962299346924 {'doc\_id': 8} And so many families...  
 0.24875116348266602 {'doc\_id': 6} And I’m taking robus...  
 0.26027143001556396 {'doc\_id': 7} We see the unity amo...  
 0.26390212774276733 {'doc\_id': 9} And unlike the $2 Tr...  

```

```python
docsearch.drop()  

```

- [Setting up environments](#setting-up-environments)

- [Get connection info and data schema](#get-connection-info-and-data-schema)

- [Filtering](#filtering)

  - [Similarity search with score](#similarity-search-with-score)

- [Deleting your data](#deleting-your-data)

- [Similarity search with score](#similarity-search-with-score)
