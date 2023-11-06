# Time-weighted vector store retriever

This retriever uses a combination of semantic similarity and a time decay.

The algorithm for scoring them is:

```text
semantic\_similarity + (1.0 - decay\_rate) ^ hours\_passed  

```

Notably, `hours_passed` refers to the hours passed since the object in the retriever **was last accessed**, not since it was created. This means that frequently accessed objects remain "fresh".

```python
import faiss  
  
from datetime import datetime, timedelta  
from langchain.docstore import InMemoryDocstore  
from langchain.embeddings import OpenAIEmbeddings  
from langchain.retrievers import TimeWeightedVectorStoreRetriever  
from langchain.schema import Document  
from langchain.vectorstores import FAISS  

```

## Low decay rate[​](#low-decay-rate "Direct link to Low decay rate")

A low `decay rate` (in this, to be extreme, we will set it close to 0) means memories will be "remembered" for longer. A `decay rate` of 0 means memories never be forgotten, making this retriever equivalent to the vector lookup.

```python
# Define your embedding model  
embeddings\_model = OpenAIEmbeddings()  
# Initialize the vectorstore as empty  
embedding\_size = 1536  
index = faiss.IndexFlatL2(embedding\_size)  
vectorstore = FAISS(embeddings\_model.embed\_query, index, InMemoryDocstore({}), {})  
retriever = TimeWeightedVectorStoreRetriever(vectorstore=vectorstore, decay\_rate=.0000000000000000000000001, k=1)  

```

```python
yesterday = datetime.now() - timedelta(days=1)  
retriever.add\_documents([Document(page\_content="hello world", metadata={"last\_accessed\_at": yesterday})])  
retriever.add\_documents([Document(page\_content="hello foo")])  

```

```text
 ['d7f85756-2371-4bdf-9140-052780a0f9b3']  

```

```python
# "Hello World" is returned first because it is most salient, and the decay rate is close to 0., meaning it's still recent enough  
retriever.get\_relevant\_documents("hello world")  

```

```text
 [Document(page\_content='hello world', metadata={'last\_accessed\_at': datetime.datetime(2023, 5, 13, 21, 0, 27, 678341), 'created\_at': datetime.datetime(2023, 5, 13, 21, 0, 27, 279596), 'buffer\_idx': 0})]  

```

## High decay rate[​](#high-decay-rate "Direct link to High decay rate")

With a high `decay rate` (e.g., several 9's), the `recency score` quickly goes to 0! If you set this all the way to 1, `recency` is 0 for all objects, once again making this equivalent to a vector lookup.

```python
# Define your embedding model  
embeddings\_model = OpenAIEmbeddings()  
# Initialize the vectorstore as empty  
embedding\_size = 1536  
index = faiss.IndexFlatL2(embedding\_size)  
vectorstore = FAISS(embeddings\_model.embed\_query, index, InMemoryDocstore({}), {})  
retriever = TimeWeightedVectorStoreRetriever(vectorstore=vectorstore, decay\_rate=.999, k=1)  

```

```python
yesterday = datetime.now() - timedelta(days=1)  
retriever.add\_documents([Document(page\_content="hello world", metadata={"last\_accessed\_at": yesterday})])  
retriever.add\_documents([Document(page\_content="hello foo")])  

```

```text
 ['40011466-5bbe-4101-bfd1-e22e7f505de2']  

```

```python
# "Hello Foo" is returned first because "hello world" is mostly forgotten  
retriever.get\_relevant\_documents("hello world")  

```

```text
 [Document(page\_content='hello foo', metadata={'last\_accessed\_at': datetime.datetime(2023, 4, 16, 22, 9, 2, 494798), 'created\_at': datetime.datetime(2023, 4, 16, 22, 9, 2, 178722), 'buffer\_idx': 1})]  

```

## Virtual time[​](#virtual-time "Direct link to Virtual time")

Using some utils in LangChain, you can mock out the time component.

```python
from langchain.utils import mock\_now  
import datetime  

```

```python
# Notice the last access time is that date time  
with mock\_now(datetime.datetime(2011, 2, 3, 10, 11)):  
 print(retriever.get\_relevant\_documents("hello world"))  

```

```text
 [Document(page\_content='hello world', metadata={'last\_accessed\_at': MockDateTime(2011, 2, 3, 10, 11), 'created\_at': datetime.datetime(2023, 5, 13, 21, 0, 27, 279596), 'buffer\_idx': 0})]  

```

- [Low decay rate](#low-decay-rate)
- [High decay rate](#high-decay-rate)
- [Virtual time](#virtual-time)
