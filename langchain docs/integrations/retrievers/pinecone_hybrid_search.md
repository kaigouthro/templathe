# Pinecone Hybrid Search

[Pinecone](https://docs.pinecone.io/docs/overview) is a vector database with broad functionality.

This notebook goes over how to use a retriever that under the hood uses Pinecone and Hybrid Search.

The logic of this retriever is taken from [this documentation](https://docs.pinecone.io/docs/hybrid-search)

To use Pinecone, you must have an API key and an Environment.
Here are the [installation instructions](https://docs.pinecone.io/docs/quickstart).

```python
#!pip install pinecone-client pinecone-text  

```

```python
import os  
import getpass  
  
os.environ["PINECONE\_API\_KEY"] = getpass.getpass("Pinecone API Key:")  

```

```python
from langchain.retrievers import PineconeHybridSearchRetriever  

```

```python
os.environ["PINECONE\_ENVIRONMENT"] = getpass.getpass("Pinecone Environment:")  

```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.

```python
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

## Setup Pinecone[​](#setup-pinecone "Direct link to Setup Pinecone")

You should only have to do this part once.

Note: it's important to make sure that the "context" field that holds the document text in the metadata is not indexed. Currently you need to specify explicitly the fields you do want to index. For more information checkout Pinecone's [docs](https://docs.pinecone.io/docs/manage-indexes#selective-metadata-indexing).

```python
import os  
import pinecone  
  
api\_key = os.getenv("PINECONE\_API\_KEY") or "PINECONE\_API\_KEY"  
# find environment next to your API key in the Pinecone console  
env = os.getenv("PINECONE\_ENVIRONMENT") or "PINECONE\_ENVIRONMENT"  
  
index\_name = "langchain-pinecone-hybrid-search"  
  
pinecone.init(api\_key=api\_key, environment=env)  
pinecone.whoami()  

```

```text
 WhoAmIResponse(username='load', user\_label='label', projectname='load-test')  

```

```python
# create the index  
pinecone.create\_index(  
 name=index\_name,  
 dimension=1536, # dimensionality of dense model  
 metric="dotproduct", # sparse values supported only for dotproduct  
 pod\_type="s1",  
 metadata\_config={"indexed": []}, # see explanation above  
)  

```

Now that its created, we can use it

```python
index = pinecone.Index(index\_name)  

```

## Get embeddings and sparse encoders[​](#get-embeddings-and-sparse-encoders "Direct link to Get embeddings and sparse encoders")

Embeddings are used for the dense vectors, tokenizer is used for the sparse vector

```python
from langchain.embeddings import OpenAIEmbeddings  
  
embeddings = OpenAIEmbeddings()  

```

To encode the text to sparse values you can either choose SPLADE or BM25. For out of domain tasks we recommend using BM25.

For more information about the sparse encoders you can checkout pinecone-text library [docs](https://pinecone-io.github.io/pinecone-text/pinecone_text.html).

```python
from pinecone\_text.sparse import BM25Encoder  
  
# or from pinecone\_text.sparse import SpladeEncoder if you wish to work with SPLADE  
  
# use default tf-idf values  
bm25\_encoder = BM25Encoder().default()  

```

The above code is using default tfids values. It's highly recommended to fit the tf-idf values to your own corpus. You can do it as follow:

```python
corpus = ["foo", "bar", "world", "hello"]  
  
# fit tf-idf values on your corpus  
bm25\_encoder.fit(corpus)  
  
# store the values to a json file  
bm25\_encoder.dump("bm25\_values.json")  
  
# load to your BM25Encoder object  
bm25\_encoder = BM25Encoder().load("bm25\_values.json")  

```

## Load Retriever[​](#load-retriever "Direct link to Load Retriever")

We can now construct the retriever!

```python
retriever = PineconeHybridSearchRetriever(  
 embeddings=embeddings, sparse\_encoder=bm25\_encoder, index=index  
)  

```

## Add texts (if necessary)[​](#add-texts-if-necessary "Direct link to Add texts (if necessary)")

We can optionally add texts to the retriever (if they aren't already in there)

```python
retriever.add\_texts(["foo", "bar", "world", "hello"])  

```

```text
 100%|██████████| 1/1 [00:02<00:00, 2.27s/it]  

```

## Use Retriever[​](#use-retriever "Direct link to Use Retriever")

We can now use the retriever!

```python
result = retriever.get\_relevant\_documents("foo")  

```

```python
result[0]  

```

```text
 Document(page\_content='foo', metadata={})  

```

- [Setup Pinecone](#setup-pinecone)
- [Get embeddings and sparse encoders](#get-embeddings-and-sparse-encoders)
- [Load Retriever](#load-retriever)
- [Add texts (if necessary)](#add-texts-if-necessary)
- [Use Retriever](#use-retriever)
