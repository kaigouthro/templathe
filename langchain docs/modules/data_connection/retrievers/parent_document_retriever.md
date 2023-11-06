# Parent Document Retriever

When splitting documents for retrieval, there are often conflicting desires:

1. You may want to have small documents, so that their embeddings can most
   accurately reflect their meaning. If too long, then the embeddings can
   lose meaning.
1. You want to have long enough documents that the context of each chunk is
   retained.

The `ParentDocumentRetriever` strikes that balance by splitting and storing
small chunks of data. During retrieval, it first fetches the small chunks
but then looks up the parent ids for those chunks and returns those larger
documents.

Note that "parent document" refers to the document that a small chunk
originated from. This can either be the whole raw document OR a larger
chunk.

```python
from langchain.retrievers import ParentDocumentRetriever  

```

```python
from langchain.vectorstores import Chroma  
from langchain.embeddings import OpenAIEmbeddings  
from langchain.text\_splitter import RecursiveCharacterTextSplitter  
from langchain.storage import InMemoryStore  
from langchain.document\_loaders import TextLoader  

```

```python
loaders = [  
 TextLoader('../../paul\_graham\_essay.txt'),  
 TextLoader('../../state\_of\_the\_union.txt'),  
]  
docs = []  
for l in loaders:  
 docs.extend(l.load())  

```

## Retrieving full documents[​](#retrieving-full-documents "Direct link to Retrieving full documents")

In this mode, we want to retrieve the full documents. Therefore, we only specify a child splitter.

```python
# This text splitter is used to create the child documents  
child\_splitter = RecursiveCharacterTextSplitter(chunk\_size=400)  
# The vectorstore to use to index the child chunks  
vectorstore = Chroma(  
 collection\_name="full\_documents",  
 embedding\_function=OpenAIEmbeddings()  
)  
# The storage layer for the parent documents  
store = InMemoryStore()  
retriever = ParentDocumentRetriever(  
 vectorstore=vectorstore,   
 docstore=store,   
 child\_splitter=child\_splitter,  
)  

```

```python
retriever.add\_documents(docs, ids=None)  

```

This should yield two keys, because we added two documents.

```python
list(store.yield\_keys())  

```

```text
 ['05fe8d8a-bf60-4f87-b576-4351b23df266',  
 '571cc9e5-9ef7-4f6c-b800-835c83a1858b']  

```

Let's now call the vector store search functionality - we should see that it returns small chunks (since we're storing the small chunks).

```python
sub\_docs = vectorstore.similarity\_search("justice breyer")  

```

```python
print(sub\_docs[0].page\_content)  

```

```text
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.  

```

Let's now retrieve from the overall retriever. This should return large documents - since it returns the documents where the smaller chunks are located.

```python
retrieved\_docs = retriever.get\_relevant\_documents("justice breyer")  

```

```python
len(retrieved\_docs[0].page\_content)  

```

```text
 38539  

```

## Retrieving larger chunks[​](#retrieving-larger-chunks "Direct link to Retrieving larger chunks")

Sometimes, the full documents can be too big to want to retrieve them as is. In that case, what we really want to do is to first split the raw documents into larger chunks, and then split it into smaller chunks. We then index the smaller chunks, but on retrieval we retrieve the larger chunks (but still not the full documents).

```python
# This text splitter is used to create the parent documents  
parent\_splitter = RecursiveCharacterTextSplitter(chunk\_size=2000)  
# This text splitter is used to create the child documents  
# It should create documents smaller than the parent  
child\_splitter = RecursiveCharacterTextSplitter(chunk\_size=400)  
# The vectorstore to use to index the child chunks  
vectorstore = Chroma(collection\_name="split\_parents", embedding\_function=OpenAIEmbeddings())  
# The storage layer for the parent documents  
store = InMemoryStore()  

```

```python
retriever = ParentDocumentRetriever(  
 vectorstore=vectorstore,   
 docstore=store,   
 child\_splitter=child\_splitter,  
 parent\_splitter=parent\_splitter,  
)  

```

```python
retriever.add\_documents(docs)  

```

We can see that there are much more than two documents now - these are the larger chunks.

```python
len(list(store.yield\_keys()))  

```

```text
 66  

```

Let's make sure the underlying vector store still retrieves the small chunks.

```python
sub\_docs = vectorstore.similarity\_search("justice breyer")  

```

```python
print(sub\_docs[0].page\_content)  

```

```text
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.  

```

```python
retrieved\_docs = retriever.get\_relevant\_documents("justice breyer")  

```

```python
len(retrieved\_docs[0].page\_content)  

```

```text
 1849  

```

```python
print(retrieved\_docs[0].page\_content)  

```

```text
 In state after state, new laws have been passed, not only to suppress the vote, but to subvert entire elections.   
   
 We cannot let this happen.   
   
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.   
   
 A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans.   
   
 And if we are to advance liberty and justice, we need to secure the Border and fix the immigration system.   
   
 We can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.   
   
 We’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.   
   
 We’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster.   
   
 We’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.  

```

- [Retrieving full documents](#retrieving-full-documents)
- [Retrieving larger chunks](#retrieving-larger-chunks)
