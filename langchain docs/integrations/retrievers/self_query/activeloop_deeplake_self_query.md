# Deep Lake

[Deep Lake](https://www.activeloop.ai) is a multimodal database for building AI applications
[Deep Lake](https://github.com/activeloopai/deeplake) is a database for AI.
Store Vectors, Images, Texts, Videos, etc. Use with LLMs/LangChain. Store, query, version,
& visualize any AI data. Stream data in real time to PyTorch/TensorFlow.

In the notebook, we'll demo the `SelfQueryRetriever` wrapped around a `Deep Lake` vector store.

## Creating a Deep Lake vector store[​](#creating-a-deep-lake-vector-store "Direct link to Creating a Deep Lake vector store")

First we'll want to create a Deep Lake vector store and seed it with some data. We've created a small demo set of documents that contain summaries of movies.

**Note:** The self-query retriever requires you to have `lark` installed (`pip install lark`). We also need the `deeplake` package.

```python
# !pip install lark  

```

```python
# in case if some queries fail consider installing libdeeplake manually  
# !pip install libdeeplake  

```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  
os.environ["ACTIVELOOP\_TOKEN"] = getpass.getpass("Activeloop token:")  

```

```python
from langchain.schema import Document  
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.vectorstores import DeepLake  
  
embeddings = OpenAIEmbeddings()  

```

```python
docs = [  
 Document(  
 page\_content="A bunch of scientists bring back dinosaurs and mayhem breaks loose",  
 metadata={"year": 1993, "rating": 7.7, "genre": "science fiction"},  
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
 "rating": 9.9,  
 "director": "Andrei Tarkovsky",  
 "genre": "science fiction",  
 "rating": 9.9,  
 },  
 ),  
]  
username\_or\_org = "<USERNAME\_OR\_ORG>"  
vectorstore = DeepLake.from\_documents(  
 docs, embeddings, dataset\_path=f"hub://{username\_or\_org}/self\_queery", overwrite=True,  
)  

```

```text
 Your Deep Lake dataset has been successfully created!  
  
  
 /  
  
 Dataset(path='hub://adilkhan/self\_queery', tensors=['embedding', 'id', 'metadata', 'text'])  
   
 tensor htype shape dtype compression  
 ------- ------- ------- ------- -------   
 embedding embedding (6, 1536) float32 None   
 id text (6, 1) str None   
 metadata json (6, 1) str None   
 text text (6, 1) str None   
  
  
   

```

## Creating our self-querying retriever[​](#creating-our-self-querying-retriever "Direct link to Creating our self-querying retriever")

Now we can instantiate our retriever. To do this we'll need to provide some information upfront about the metadata fields that our documents support and a short description of the document contents.

```python
from langchain.llms import OpenAI  
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
llm = OpenAI(temperature=0)  
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
 /home/ubuntu/langchain\_activeloop/langchain/libs/langchain/langchain/chains/llm.py:279: UserWarning: The predict\_and\_parse method is deprecated, instead pass an output parser directly to LLMChain.  
 warnings.warn(  
  
  
 query='dinosaur' filter=None limit=None  
  
  
  
  
  
 [Document(page\_content='A bunch of scientists bring back dinosaurs and mayhem breaks loose', metadata={'year': 1993, 'rating': 7.7, 'genre': 'science fiction'}),  
 Document(page\_content='Toys come alive and have a blast doing so', metadata={'year': 1995, 'genre': 'animated'}),  
 Document(page\_content='Three men walk into the Zone, three men walk out of the Zone', metadata={'year': 1979, 'rating': 9.9, 'director': 'Andrei Tarkovsky', 'genre': 'science fiction'}),  
 Document(page\_content='A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea', metadata={'year': 2006, 'director': 'Satoshi Kon', 'rating': 8.6})]  

```

```python
# This example only specifies a filter  
retriever.get\_relevant\_documents("I want to watch a movie rated higher than 8.5")  
  
# in case if this example errored out, consider installing libdeeplake manually: `pip install libdeeplake`, and then restart notebook.  

```

```text
 query=' ' filter=Comparison(comparator=<Comparator.GT: 'gt'>, attribute='rating', value=8.5) limit=None  
  
  
  
  
  
 [Document(page\_content='A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea', metadata={'year': 2006, 'director': 'Satoshi Kon', 'rating': 8.6}),  
 Document(page\_content='Three men walk into the Zone, three men walk out of the Zone', metadata={'year': 1979, 'rating': 9.9, 'director': 'Andrei Tarkovsky', 'genre': 'science fiction'})]  

```

```python
# This example specifies a query and a filter  
retriever.get\_relevant\_documents("Has Greta Gerwig directed any movies about women")  

```

```text
 query='women' filter=Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='director', value='Greta Gerwig') limit=None  
  
  
  
  
  
 [Document(page\_content='A bunch of normal-sized women are supremely wholesome and some men pine after them', metadata={'year': 2019, 'director': 'Greta Gerwig', 'rating': 8.3})]  

```

```python
# This example specifies a composite filter  
retriever.get\_relevant\_documents(  
 "What's a highly rated (above 8.5) science fiction film?"  
)  

```

```text
 query=' ' filter=Operation(operator=<Operator.AND: 'and'>, arguments=[Comparison(comparator=<Comparator.GTE: 'gte'>, attribute='rating', value=8.5), Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='genre', value='science fiction')]) limit=None  
  
  
  
  
  
 [Document(page\_content='Three men walk into the Zone, three men walk out of the Zone', metadata={'year': 1979, 'rating': 9.9, 'director': 'Andrei Tarkovsky', 'genre': 'science fiction'})]  

```

```python
# This example specifies a query and composite filter  
retriever.get\_relevant\_documents(  
 "What's a movie after 1990 but before 2005 that's all about toys, and preferably is animated"  
)  

```

```text
 query='toys' filter=Operation(operator=<Operator.AND: 'and'>, arguments=[Comparison(comparator=<Comparator.GT: 'gt'>, attribute='year', value=1990), Comparison(comparator=<Comparator.LT: 'lt'>, attribute='year', value=2005), Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='genre', value='animated')]) limit=None  
  
  
  
  
  
 [Document(page\_content='Toys come alive and have a blast doing so', metadata={'year': 1995, 'genre': 'animated'})]  

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
 query='dinosaur' filter=None limit=2  
  
  
  
  
  
 [Document(page\_content='A bunch of scientists bring back dinosaurs and mayhem breaks loose', metadata={'year': 1993, 'rating': 7.7, 'genre': 'science fiction'}),  
 Document(page\_content='Toys come alive and have a blast doing so', metadata={'year': 1995, 'genre': 'animated'})]  

```

- [Creating a Deep Lake vector store](#creating-a-deep-lake-vector-store)
- [Creating our self-querying retriever](#creating-our-self-querying-retriever)
- [Testing it out](#testing-it-out)
- [Filter k](#filter-k)
