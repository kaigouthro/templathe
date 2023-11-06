# Timescale Vector (Postgres) self-querying

[Timescale Vector](https://www.timescale.com/ai) is PostgreSQL++ for AI applications. It enables you to efficiently store and query billions of vector embeddings in `PostgreSQL`.

This notebook shows how to use the Postgres vector database (`TimescaleVector`) to perform self-querying. In the notebook we'll demo the `SelfQueryRetriever` wrapped around a TimescaleVector vector store.

## What is Timescale Vector?[​](#what-is-timescale-vector "Direct link to What is Timescale Vector?")

**[Timescale Vector](https://www.timescale.com/ai) is PostgreSQL++ for AI applications.**

Timescale Vector enables you to efficiently store and query millions of vector embeddings in `PostgreSQL`.

- Enhances `pgvector` with faster and more accurate similarity search on 1B+ vectors via DiskANN inspired indexing algorithm.
- Enables fast time-based vector search via automatic time-based partitioning and indexing.
- Provides a familiar SQL interface for querying vector embeddings and relational data.

Timescale Vector is cloud PostgreSQL for AI that scales with you from POC to production:

- Simplifies operations by enabling you to store relational metadata, vector embeddings, and time-series data in a single database.
- Benefits from rock-solid PostgreSQL foundation with enterprise-grade feature liked streaming backups and replication, high-availability and row-level security.
- Enables a worry-free experience with enterprise-grade security and compliance.

## How to access Timescale Vector[​](#how-to-access-timescale-vector "Direct link to How to access Timescale Vector")

Timescale Vector is available on [Timescale](https://www.timescale.com/ai), the cloud PostgreSQL platform. (There is no self-hosted version at this time.)

LangChain users get a 90-day free trial for Timescale Vector.

- To get started, [signup](https://console.cloud.timescale.com/signup?utm_campaign=vectorlaunch&utm_source=langchain&utm_medium=referral) to Timescale, create a new database and follow this notebook!
- See the [Timescale Vector explainer blog](https://www.timescale.com/blog/how-we-made-postgresql-the-best-vector-database/?utm_campaign=vectorlaunch&utm_source=langchain&utm_medium=referral) for more details and performance benchmarks.
- See the [installation instructions](https://github.com/timescale/python-vector) for more details on using Timescale Vector in python.

## Creating a TimescaleVector vectorstore[​](#creating-a-timescalevector-vectorstore "Direct link to Creating a TimescaleVector vectorstore")

First we'll want to create a Timescale Vector vectorstore and seed it with some data. We've created a small demo set of documents that contain summaries of movies.

NOTE: The self-query retriever requires you to have `lark` installed (`pip install lark`). We also need the `timescale-vector` package.

```text
#!pip install lark  

```

```text
#!pip install timescale-vector  

```

In this example, we'll use `OpenAIEmbeddings`, so let's load your OpenAI API key.

```text
# Get openAI api key by reading local .env file  
# The .env file should contain a line starting with `OPENAI\_API\_KEY=sk-`  
import os  
from dotenv import load\_dotenv, find\_dotenv  
\_ = load\_dotenv(find\_dotenv())  
  
OPENAI\_API\_KEY = os.environ['OPENAI\_API\_KEY']  
# Alternatively, use getpass to enter the key in a prompt  
#import os  
#import getpass  
#os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

To connect to your PostgreSQL database, you'll need your service URI, which can be found in the cheatsheet or `.env` file you downloaded after creating a new database.

If you haven't already, [signup for Timescale](https://console.cloud.timescale.com/signup?utm_campaign=vectorlaunch&utm_source=langchain&utm_medium=referral), and create a new database.

The URI will look something like this: `postgres://tsdbadmin:<password>@<id>.tsdb.cloud.timescale.com:<port>/tsdb?sslmode=require`

```text
# Get the service url by reading local .env file  
# The .env file should contain a line starting with `TIMESCALE\_SERVICE\_URL=postgresql://`  
\_ = load\_dotenv(find\_dotenv())  
TIMESCALE\_SERVICE\_URL = os.environ["TIMESCALE\_SERVICE\_URL"]  
  
# Alternatively, use getpass to enter the key in a prompt  
#import os  
#import getpass  
#TIMESCALE\_SERVICE\_URL = getpass.getpass("Timescale Service URL:")  

```

```text
from langchain.schema import Document  
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.vectorstores.timescalevector import TimescaleVector  
  
embeddings = OpenAIEmbeddings()  

```

Here's the sample documents we'll use for this demo. The data is about movies, and has both content and metadata fields with information about particular movie.

```text
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

```

Finally, we'll create our Timescale Vector vectorstore. Note that the collection name will be the name of the PostgreSQL table in which the documents are stored in.

```text
COLLECTION\_NAME = "langchain\_self\_query\_demo"  
vectorstore = TimescaleVector.from\_documents(  
 embedding=embeddings,  
 documents=docs,  
 collection\_name=COLLECTION\_NAME,  
 service\_url=TIMESCALE\_SERVICE\_URL,  
)  

```

## Creating our self-querying retriever[​](#creating-our-self-querying-retriever "Direct link to Creating our self-querying retriever")

Now we can instantiate our retriever. To do this we'll need to provide some information upfront about the metadata fields that our documents support and a short description of the document contents.

```text
from langchain.llms import OpenAI  
from langchain.retrievers.self\_query.base import SelfQueryRetriever  
from langchain.chains.query\_constructor.base import AttributeInfo  
  
# Give LLM info about the metadata fields  
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
  
# Instantiate the self-query retriever from an LLM  
llm = OpenAI(temperature=0)  
retriever = SelfQueryRetriever.from\_llm(  
 llm, vectorstore, document\_content\_description, metadata\_field\_info, verbose=True  
)  

```

## Self Querying Retrieval with Timescale Vector[​](#self-querying-retrieval-with-timescale-vector "Direct link to Self Querying Retrieval with Timescale Vector")

And now we can try actually using our retriever!

Run the queries below and note how you can specify a query, filter, composite filter (filters with AND, OR) in natural language and the self-query retriever will translate that query into SQL and perform the search on the Timescale Vector (Postgres) vectorstore.

This illustrates the power of the self-query retriever. You can use it to perform complex searches over your vectorstore without you or your users having to write any SQL directly!

```text
# This example only specifies a relevant query  
retriever.get\_relevant\_documents("What are some movies about dinosaurs")  

```

```text
 /Users/avtharsewrathan/sideprojects2023/timescaleai/tsv-langchain/langchain/libs/langchain/langchain/chains/llm.py:275: UserWarning: The predict\_and\_parse method is deprecated, instead pass an output parser directly to LLMChain.  
 warnings.warn(  
  
  
 query='dinosaur' filter=None limit=None  
  
  
  
  
  
 [Document(page\_content='A bunch of scientists bring back dinosaurs and mayhem breaks loose', metadata={'year': 1993, 'genre': 'science fiction', 'rating': 7.7}),  
 Document(page\_content='A bunch of scientists bring back dinosaurs and mayhem breaks loose', metadata={'year': 1993, 'genre': 'science fiction', 'rating': 7.7}),  
 Document(page\_content='Toys come alive and have a blast doing so', metadata={'year': 1995, 'genre': 'animated'}),  
 Document(page\_content='Toys come alive and have a blast doing so', metadata={'year': 1995, 'genre': 'animated'})]  

```

```text
# This example only specifies a filter  
retriever.get\_relevant\_documents("I want to watch a movie rated higher than 8.5")  

```

```text
 query=' ' filter=Comparison(comparator=<Comparator.GT: 'gt'>, attribute='rating', value=8.5) limit=None  
  
  
  
  
  
 [Document(page\_content='Three men walk into the Zone, three men walk out of the Zone', metadata={'year': 1979, 'genre': 'science fiction', 'rating': 9.9, 'director': 'Andrei Tarkovsky'}),  
 Document(page\_content='Three men walk into the Zone, three men walk out of the Zone', metadata={'year': 1979, 'genre': 'science fiction', 'rating': 9.9, 'director': 'Andrei Tarkovsky'}),  
 Document(page\_content='A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea', metadata={'year': 2006, 'rating': 8.6, 'director': 'Satoshi Kon'}),  
 Document(page\_content='A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea', metadata={'year': 2006, 'rating': 8.6, 'director': 'Satoshi Kon'})]  

```

```text
# This example specifies a query and a filter  
retriever.get\_relevant\_documents("Has Greta Gerwig directed any movies about women")  

```

```text
 query='women' filter=Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='director', value='Greta Gerwig') limit=None  
  
  
  
  
  
 [Document(page\_content='A bunch of normal-sized women are supremely wholesome and some men pine after them', metadata={'year': 2019, 'rating': 8.3, 'director': 'Greta Gerwig'}),  
 Document(page\_content='A bunch of normal-sized women are supremely wholesome and some men pine after them', metadata={'year': 2019, 'rating': 8.3, 'director': 'Greta Gerwig'})]  

```

```text
# This example specifies a composite filter  
retriever.get\_relevant\_documents(  
 "What's a highly rated (above 8.5) science fiction film?"  
)  

```

```text
 query=' ' filter=Operation(operator=<Operator.AND: 'and'>, arguments=[Comparison(comparator=<Comparator.GTE: 'gte'>, attribute='rating', value=8.5), Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='genre', value='science fiction')]) limit=None  
  
  
  
  
  
 [Document(page\_content='Three men walk into the Zone, three men walk out of the Zone', metadata={'year': 1979, 'genre': 'science fiction', 'rating': 9.9, 'director': 'Andrei Tarkovsky'}),  
 Document(page\_content='Three men walk into the Zone, three men walk out of the Zone', metadata={'year': 1979, 'genre': 'science fiction', 'rating': 9.9, 'director': 'Andrei Tarkovsky'})]  

```

```text
# This example specifies a query and composite filter  
retriever.get\_relevant\_documents(  
 "What's a movie after 1990 but before 2005 that's all about toys, and preferably is animated"  
)  

```

```text
 query='toys' filter=Operation(operator=<Operator.AND: 'and'>, arguments=[Comparison(comparator=<Comparator.GT: 'gt'>, attribute='year', value=1990), Comparison(comparator=<Comparator.LT: 'lt'>, attribute='year', value=2005), Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='genre', value='animated')]) limit=None  
  
  
  
  
  
 [Document(page\_content='Toys come alive and have a blast doing so', metadata={'year': 1995, 'genre': 'animated'})]  

```

### Filter k[​](#filter-k "Direct link to Filter k")

We can also use the self query retriever to specify `k`: the number of documents to fetch.

We can do this by passing `enable_limit=True` to the constructor.

```text
retriever = SelfQueryRetriever.from\_llm(  
 llm,  
 vectorstore,  
 document\_content\_description,  
 metadata\_field\_info,  
 enable\_limit=True,  
 verbose=True,  
)  

```

```text
# This example specifies a query with a LIMIT value  
retriever.get\_relevant\_documents("what are two movies about dinosaurs")  

```

```text
 query='dinosaur' filter=None limit=2  
  
  
  
  
  
 [Document(page\_content='A bunch of scientists bring back dinosaurs and mayhem breaks loose', metadata={'year': 1993, 'genre': 'science fiction', 'rating': 7.7}),  
 Document(page\_content='A bunch of scientists bring back dinosaurs and mayhem breaks loose', metadata={'year': 1993, 'genre': 'science fiction', 'rating': 7.7})]  

```

- [What is Timescale Vector?](#what-is-timescale-vector)

- [How to access Timescale Vector](#how-to-access-timescale-vector)

- [Creating a TimescaleVector vectorstore](#creating-a-timescalevector-vectorstore)

- [Creating our self-querying retriever](#creating-our-self-querying-retriever)

- [Self Querying Retrieval with Timescale Vector](#self-querying-retrieval-with-timescale-vector)

  - [Filter k](#filter-k)

- [Filter k](#filter-k)
