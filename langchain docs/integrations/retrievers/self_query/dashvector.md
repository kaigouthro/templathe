# DashVector

[DashVector](https://help.aliyun.com/document_detail/2510225.html) is a fully managed vector DB service that supports high-dimension dense and sparse vectors, real-time insertion and filtered search. It is built to scale automatically and can adapt to different application requirements.
The vector retrieval service `DashVector` is based on the `Proxima` core of the efficient vector engine independently developed by `DAMO Academy`,
and provides a cloud-native, fully managed vector retrieval service with horizontal expansion capabilities.
`DashVector` exposes its powerful vector management, vector query and other diversified capabilities through a simple and
easy-to-use SDK/API interface, which can be quickly integrated by upper-layer AI applications, thereby providing services
including large model ecology, multi-modal AI search, molecular structure A variety of application scenarios, including analysis,
provide the required efficient vector retrieval capabilities.

In this notebook, we'll demo the `SelfQueryRetriever` with a `DashVector` vector store.

## Create DashVector vectorstore[​](#create-dashvector-vectorstore "Direct link to Create DashVector vectorstore")

First we'll want to create a `DashVector` VectorStore and seed it with some data. We've created a small demo set of documents that contain summaries of movies.

To use DashVector, you have to have `dashvector` package installed, and you must have an API key and an Environment. Here are the [installation instructions](https://help.aliyun.com/document_detail/2510223.html).

NOTE: The self-query retriever requires you to have `lark` package installed.

```python
# !pip install lark dashvector  

```

```python
import os  
import dashvector  
  
client = dashvector.Client(api\_key=os.environ["DASHVECTOR\_API\_KEY"])  

```

```python
from langchain.schema import Document  
from langchain.embeddings import DashScopeEmbeddings  
from langchain.vectorstores import DashVector  
  
embeddings = DashScopeEmbeddings()  
  
# create DashVector collection  
client.create("langchain-self-retriever-demo", dimension=1536)  

```

```python
docs = [  
 Document(  
 page\_content="A bunch of scientists bring back dinosaurs and mayhem breaks loose",  
 metadata={"year": 1993, "rating": 7.7, "genre": "action"},  
 ),  
 Document(  
 page\_content="Leo DiCaprio gets lost in a dream within a dream within a dream within a ...",  
 metadata={"year": 2010, "director": "Christopher Nolan", "rating": 8.2},  
 ),  
 Document(  
 page\_content="A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea",  
 metadata={"year": 2006, "director": "Satoshi Kon", "rating": 8.6},  
 ),  
 Document(  
 page\_content="A bunch of normal-sized women are supremely wholesome and some men pine after them",  
 metadata={"year": 2019, "director": "Greta Gerwig", "rating": 8.3},  
 ),  
 Document(  
 page\_content="Toys come alive and have a blast doing so",  
 metadata={"year": 1995, "genre": "animated"},  
 ),  
 Document(  
 page\_content="Three men walk into the Zone, three men walk out of the Zone",  
 metadata={  
 "year": 1979,  
 "director": "Andrei Tarkovsky",  
 "genre": "science fiction",  
 "rating": 9.9,  
 },  
 ),  
]  
vectorstore = DashVector.from\_documents(  
 docs, embeddings, collection\_name="langchain-self-retriever-demo"  
)  

```

## Create your self-querying retriever[​](#create-your-self-querying-retriever "Direct link to Create your self-querying retriever")

Now we can instantiate our retriever. To do this we'll need to provide some information upfront about the metadata fields that our documents support and a short description of the document contents.

```python
from langchain.llms import Tongyi  
from langchain.retrievers.self\_query.base import SelfQueryRetriever  
from langchain.chains.query\_constructor.base import AttributeInfo  
  
metadata\_field\_info = [  
 AttributeInfo(  
 name="genre",  
 description="The genre of the movie",  
 type="string or list[string]",  
 ),  
 AttributeInfo(  
 name="year",  
 description="The year the movie was released",  
 type="integer",  
 ),  
 AttributeInfo(  
 name="director",  
 description="The name of the movie director",  
 type="string",  
 ),  
 AttributeInfo(  
 name="rating", description="A 1-10 rating for the movie", type="float"  
 ),  
]  
document\_content\_description = "Brief summary of a movie"  
llm = Tongyi(temperature=0)  
retriever = SelfQueryRetriever.from\_llm(  
 llm, vectorstore, document\_content\_description, metadata\_field\_info, verbose=True  
)  

```

## Testing it out[​](#testing-it-out "Direct link to Testing it out")

And now we can try actually using our retriever!

```python
# This example only specifies a relevant query  
retriever.get\_relevant\_documents("What are some movies about dinosaurs")  

```

```text
 query='dinosaurs' filter=None limit=None  
  
  
  
  
  
 [Document(page\_content='A bunch of scientists bring back dinosaurs and mayhem breaks loose', metadata={'year': 1993, 'rating': 7.699999809265137, 'genre': 'action'}),  
 Document(page\_content='Toys come alive and have a blast doing so', metadata={'year': 1995, 'genre': 'animated'}),  
 Document(page\_content='Leo DiCaprio gets lost in a dream within a dream within a dream within a ...', metadata={'year': 2010, 'director': 'Christopher Nolan', 'rating': 8.199999809265137}),  
 Document(page\_content='A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea', metadata={'year': 2006, 'director': 'Satoshi Kon', 'rating': 8.600000381469727})]  

```

```python
# This example only specifies a filter  
retriever.get\_relevant\_documents("I want to watch a movie rated higher than 8.5")  

```

```text
 query=' ' filter=Comparison(comparator=<Comparator.GTE: 'gte'>, attribute='rating', value=8.5) limit=None  
  
  
  
  
  
 [Document(page\_content='Three men walk into the Zone, three men walk out of the Zone', metadata={'year': 1979, 'director': 'Andrei Tarkovsky', 'rating': 9.899999618530273, 'genre': 'science fiction'}),  
 Document(page\_content='A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea', metadata={'year': 2006, 'director': 'Satoshi Kon', 'rating': 8.600000381469727})]  

```

```python
# This example specifies a query and a filter  
retriever.get\_relevant\_documents("Has Greta Gerwig directed any movies about women")  

```

```text
 query='Greta Gerwig' filter=Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='director', value='Greta Gerwig') limit=None  
  
  
  
  
  
 [Document(page\_content='A bunch of normal-sized women are supremely wholesome and some men pine after them', metadata={'year': 2019, 'director': 'Greta Gerwig', 'rating': 8.300000190734863})]  

```

```python
# This example specifies a composite filter  
retriever.get\_relevant\_documents("What's a highly rated (above 8.5) science fiction film?")  

```

```text
 query='science fiction' filter=Operation(operator=<Operator.AND: 'and'>, arguments=[Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='genre', value='science fiction'), Comparison(comparator=<Comparator.GT: 'gt'>, attribute='rating', value=8.5)]) limit=None  
  
  
  
  
  
 [Document(page\_content='Three men walk into the Zone, three men walk out of the Zone', metadata={'year': 1979, 'director': 'Andrei Tarkovsky', 'rating': 9.899999618530273, 'genre': 'science fiction'})]  

```

## Filter k[​](#filter-k "Direct link to Filter k")

We can also use the self query retriever to specify `k`: the number of documents to fetch.

We can do this by passing `enable_limit=True` to the constructor.

```python
retriever = SelfQueryRetriever.from\_llm(  
 llm,  
 vectorstore,  
 document\_content\_description,  
 metadata\_field\_info,  
 enable\_limit=True,  
 verbose=True,  
)  

```

```python
# This example only specifies a relevant query  
retriever.get\_relevant\_documents("what are two movies about dinosaurs")  

```

```text
 query='dinosaurs' filter=None limit=2  
  
  
  
  
  
 [Document(page\_content='A bunch of scientists bring back dinosaurs and mayhem breaks loose', metadata={'year': 1993, 'rating': 7.699999809265137, 'genre': 'action'}),  
 Document(page\_content='Toys come alive and have a blast doing so', metadata={'year': 1995, 'genre': 'animated'})]  

```

- [Create DashVector vectorstore](#create-dashvector-vectorstore)
- [Create your self-querying retriever](#create-your-self-querying-retriever)
- [Testing it out](#testing-it-out)
- [Filter k](#filter-k)
