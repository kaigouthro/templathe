# Vectara

[Vectara](https://docs.vectara.com/docs/) is a GenAI platform for developers. It provides a simple API to build Grounded Generation
(aka Retrieval-augmented-generation or RAG) applications.

In the notebook, we'll demo the `SelfQueryRetriever` wrapped around a Vectara vector store.

# Setup

You will need a Vectara account to use Vectara with LangChain. To get started, use the following steps (see our [quickstart](https://docs.vectara.com/docs/quickstart) guide):

1. [Sign up](https://console.vectara.com/signup) for a Vectara account if you don't already have one. Once you have completed your sign up you will have a Vectara customer ID. You can find your customer ID by clicking on your name, on the top-right of the Vectara console window.
1. Within your account you can create one or more corpora. Each corpus represents an area that stores text data upon ingest from input documents. To create a corpus, use the **"Create Corpus"** button. You then provide a name to your corpus as well as a description. Optionally you can define filtering attributes and apply some advanced options. If you click on your created corpus, you can see its name and corpus ID right on the top.
1. Next you'll need to create API keys to access the corpus. Click on the **"Authorization"** tab in the corpus view and then the **"Create API Key"** button. Give your key a name, and choose whether you want query only or query+index for your key. Click "Create" and you now have an active API key. Keep this key confidential.

To use LangChain with Vectara, you'll need to have these three values: customer ID, corpus ID and api_key.
You can provide those to LangChain in two ways:

1. Include in your environment these three variables: `VECTARA_CUSTOMER_ID`, `VECTARA_CORPUS_ID` and `VECTARA_API_KEY`.

For example, you can set these variables using os.environ and getpass as follows:

```python
import os  
import getpass  
  
os.environ["VECTARA\_CUSTOMER\_ID"] = getpass.getpass("Vectara Customer ID:")  
os.environ["VECTARA\_CORPUS\_ID"] = getpass.getpass("Vectara Corpus ID:")  
os.environ["VECTARA\_API\_KEY"] = getpass.getpass("Vectara API Key:")  

```

1. Provide them as arguments when creating the Vectara vectorstore object:

```python
vectorstore = Vectara(  
 vectara\_customer\_id=vectara\_customer\_id,  
 vectara\_corpus\_id=vectara\_corpus\_id,  
 vectara\_api\_key=vectara\_api\_key  
 )  

```

**Note:** The self-query retriever requires you to have `lark` installed (`pip install lark`).

## Connecting to Vectara from LangChain[​](#connecting-to-vectara-from-langchain "Direct link to Connecting to Vectara from LangChain")

In this example, we assume that you've created an account and a corpus, and added your VECTARA_CUSTOMER_ID, VECTARA_CORPUS_ID and VECTARA_API_KEY (created with permissions for both indexing and query) as environment variables.

The corpus has 4 fields defined as metadata for filtering: year, director, rating, and genre

```python
from langchain.embeddings import FakeEmbeddings  
from langchain.schema import Document  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Vectara  
from langchain.document\_loaders import TextLoader  
  
from langchain.llms import OpenAI  
from langchain.chains import ConversationalRetrievalChain  
from langchain.retrievers.self\_query.base import SelfQueryRetriever  
from langchain.chains.query\_constructor.base import AttributeInfo  

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
 },  
 ),  
]  
  
vectara = Vectara()  
for doc in docs:  
 vectara.add\_texts([doc.page\_content], embedding=FakeEmbeddings(size=768), doc\_metadata=doc.metadata)  

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
 llm, vectara, document\_content\_description, metadata\_field\_info, verbose=True  
)  

```

## Testing it out[​](#testing-it-out "Direct link to Testing it out")

And now we can try actually using our retriever!

```python
# This example only specifies a relevant query  
retriever.get\_relevant\_documents("What are some movies about dinosaurs")  

```

```text
 /Users/ofer/dev/langchain/libs/langchain/langchain/chains/llm.py:278: UserWarning: The predict\_and\_parse method is deprecated, instead pass an output parser directly to LLMChain.  
 warnings.warn(  
  
  
 query='dinosaur' filter=None limit=None  
  
  
  
  
  
 [Document(page\_content='A bunch of scientists bring back dinosaurs and mayhem breaks loose', metadata={'lang': 'eng', 'offset': '0', 'len': '66', 'year': '1993', 'rating': '7.7', 'genre': 'science fiction', 'source': 'langchain'}),  
 Document(page\_content='Toys come alive and have a blast doing so', metadata={'lang': 'eng', 'offset': '0', 'len': '41', 'year': '1995', 'genre': 'animated', 'source': 'langchain'}),  
 Document(page\_content='Three men walk into the Zone, three men walk out of the Zone', metadata={'lang': 'eng', 'offset': '0', 'len': '60', 'year': '1979', 'rating': '9.9', 'director': 'Andrei Tarkovsky', 'genre': 'science fiction', 'source': 'langchain'}),  
 Document(page\_content='Leo DiCaprio gets lost in a dream within a dream within a dream within a ...', metadata={'lang': 'eng', 'offset': '0', 'len': '76', 'year': '2010', 'director': 'Christopher Nolan', 'rating': '8.2', 'source': 'langchain'}),  
 Document(page\_content='A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea', metadata={'lang': 'eng', 'offset': '0', 'len': '116', 'year': '2006', 'director': 'Satoshi Kon', 'rating': '8.6', 'source': 'langchain'})]  

```

```python
# This example only specifies a filter  
retriever.get\_relevant\_documents("I want to watch a movie rated higher than 8.5")  

```

```text
 query=' ' filter=Comparison(comparator=<Comparator.GT: 'gt'>, attribute='rating', value=8.5) limit=None  
  
  
  
  
  
 [Document(page\_content='Three men walk into the Zone, three men walk out of the Zone', metadata={'lang': 'eng', 'offset': '0', 'len': '60', 'year': '1979', 'rating': '9.9', 'director': 'Andrei Tarkovsky', 'genre': 'science fiction', 'source': 'langchain'}),  
 Document(page\_content='A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea', metadata={'lang': 'eng', 'offset': '0', 'len': '116', 'year': '2006', 'director': 'Satoshi Kon', 'rating': '8.6', 'source': 'langchain'})]  

```

```python
# This example specifies a query and a filter  
retriever.get\_relevant\_documents("Has Greta Gerwig directed any movies about women")  

```

```text
 query='women' filter=Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='director', value='Greta Gerwig') limit=None  
  
  
  
  
  
 [Document(page\_content='A bunch of normal-sized women are supremely wholesome and some men pine after them', metadata={'lang': 'eng', 'offset': '0', 'len': '82', 'year': '2019', 'director': 'Greta Gerwig', 'rating': '8.3', 'source': 'langchain'})]  

```

```python
# This example specifies a composite filter  
retriever.get\_relevant\_documents(  
 "What's a highly rated (above 8.5) science fiction film?"  
)  

```

```text
 query=' ' filter=Operation(operator=<Operator.AND: 'and'>, arguments=[Comparison(comparator=<Comparator.GTE: 'gte'>, attribute='rating', value=8.5), Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='genre', value='science fiction')]) limit=None  
  
  
  
  
  
 [Document(page\_content='Three men walk into the Zone, three men walk out of the Zone', metadata={'lang': 'eng', 'offset': '0', 'len': '60', 'year': '1979', 'rating': '9.9', 'director': 'Andrei Tarkovsky', 'genre': 'science fiction', 'source': 'langchain'})]  

```

```python
# This example specifies a query and composite filter  
retriever.get\_relevant\_documents(  
 "What's a movie after 1990 but before 2005 that's all about toys, and preferably is animated"  
)  

```

```text
 query='toys' filter=Operation(operator=<Operator.AND: 'and'>, arguments=[Comparison(comparator=<Comparator.GT: 'gt'>, attribute='year', value=1990), Comparison(comparator=<Comparator.LT: 'lt'>, attribute='year', value=2005), Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='genre', value='animated')]) limit=None  
  
  
  
  
  
 [Document(page\_content='Toys come alive and have a blast doing so', metadata={'lang': 'eng', 'offset': '0', 'len': '41', 'year': '1995', 'genre': 'animated', 'source': 'langchain'})]  

```

## Filter k[​](#filter-k "Direct link to Filter k")

We can also use the self query retriever to specify `k`: the number of documents to fetch.

We can do this by passing `enable_limit=True` to the constructor.

```python
retriever = SelfQueryRetriever.from\_llm(  
 llm,  
 vectara,  
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
  
  
  
  
  
 [Document(page\_content='A bunch of scientists bring back dinosaurs and mayhem breaks loose', metadata={'lang': 'eng', 'offset': '0', 'len': '66', 'year': '1993', 'rating': '7.7', 'genre': 'science fiction', 'source': 'langchain'}),  
 Document(page\_content='Toys come alive and have a blast doing so', metadata={'lang': 'eng', 'offset': '0', 'len': '41', 'year': '1995', 'genre': 'animated', 'source': 'langchain'})]  

```

- [Connecting to Vectara from LangChain](#connecting-to-vectara-from-langchain)
- [Creating our self-querying retriever](#creating-our-self-querying-retriever)
- [Testing it out](#testing-it-out)
- [Filter k](#filter-k)
