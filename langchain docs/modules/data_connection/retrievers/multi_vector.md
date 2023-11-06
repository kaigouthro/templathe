# MultiVector Retriever

It can often be beneficial to store multiple vectors per document. There are multiple use cases where this is beneficial. LangChain has a base `MultiVectorRetriever` which makes querying this type of setup easy. A lot of the complexity lies in how to create the multiple vectors per document. This notebook covers some of the common ways to create those vectors and use the `MultiVectorRetriever`.

The methods to create multiple vectors per document include:

- Smaller chunks: split a document into smaller chunks, and embed those (this is ParentDocumentRetriever).
- Summary: create a summary for each document, embed that along with (or instead of) the document.
- Hypothetical questions: create hypothetical questions that each document would be appropriate to answer, embed those along with (or instead of) the document.

Note that this also enables another method of adding embeddings - manually. This is great because you can explicitly add questions or queries that should lead to a document being recovered, giving you more control.

```python
from langchain.retrievers.multi\_vector import MultiVectorRetriever  

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
text\_splitter = RecursiveCharacterTextSplitter(chunk\_size=10000)  
docs = text\_splitter.split\_documents(docs)  

```

## Smaller chunks[​](#smaller-chunks "Direct link to Smaller chunks")

Often times it can be useful to retrieve larger chunks of information, but embed smaller chunks. This allows for embeddings to capture the semantic meaning as closely as possible, but for as much context as possible to be passed downstream. Note that this is what the `ParentDocumentRetriever` does. Here we show what is going on under the hood.

```python
# The vectorstore to use to index the child chunks  
vectorstore = Chroma(  
 collection\_name="full\_documents",  
 embedding\_function=OpenAIEmbeddings()  
)  
# The storage layer for the parent documents  
store = InMemoryStore()  
id\_key = "doc\_id"  
# The retriever (empty to start)  
retriever = MultiVectorRetriever(  
 vectorstore=vectorstore,   
 docstore=store,   
 id\_key=id\_key,  
)  
import uuid  
doc\_ids = [str(uuid.uuid4()) for \_ in docs]  

```

```python
# The splitter to use to create smaller chunks  
child\_text\_splitter = RecursiveCharacterTextSplitter(chunk\_size=400)  

```

```python
sub\_docs = []  
for i, doc in enumerate(docs):  
 \_id = doc\_ids[i]  
 \_sub\_docs = child\_text\_splitter.split\_documents([doc])  
 for \_doc in \_sub\_docs:  
 \_doc.metadata[id\_key] = \_id  
 sub\_docs.extend(\_sub\_docs)  

```

```python
retriever.vectorstore.add\_documents(sub\_docs)  
retriever.docstore.mset(list(zip(doc\_ids, docs)))  

```

```python
# Vectorstore alone retrieves the small chunks  
retriever.vectorstore.similarity\_search("justice breyer")[0]  

```

```text
 Document(page\_content='Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.', metadata={'doc\_id': '10e9cbc0-4ba5-4d79-a09b-c033d1ba7b01', 'source': '../../state\_of\_the\_union.txt'})  

```

```python
# Retriever returns larger chunks  
len(retriever.get\_relevant\_documents("justice breyer")[0].page\_content)  

```

```text
 9874  

```

## Summary[​](#summary "Direct link to Summary")

Oftentimes a summary may be able to distill more accurately what a chunk is about, leading to better retrieval. Here we show how to create summaries, and then embed those.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.prompts import ChatPromptTemplate  
from langchain.schema.output\_parser import StrOutputParser  
import uuid  
from langchain.schema.document import Document  

```

```python
chain = (  
 {"doc": lambda x: x.page\_content}  
 | ChatPromptTemplate.from\_template("Summarize the following document:\n\n{doc}")  
 | ChatOpenAI(max\_retries=0)  
 | StrOutputParser()  
)  

```

```python
summaries = chain.batch(docs, {"max\_concurrency": 5})  

```

```python
# The vectorstore to use to index the child chunks  
vectorstore = Chroma(  
 collection\_name="summaries",  
 embedding\_function=OpenAIEmbeddings()  
)  
# The storage layer for the parent documents  
store = InMemoryStore()  
id\_key = "doc\_id"  
# The retriever (empty to start)  
retriever = MultiVectorRetriever(  
 vectorstore=vectorstore,   
 docstore=store,   
 id\_key=id\_key,  
)  
doc\_ids = [str(uuid.uuid4()) for \_ in docs]  

```

```python
summary\_docs = [Document(page\_content=s,metadata={id\_key: doc\_ids[i]}) for i, s in enumerate(summaries)]  

```

```python
retriever.vectorstore.add\_documents(summary\_docs)  
retriever.docstore.mset(list(zip(doc\_ids, docs)))  

```

```python
# # We can also add the original chunks to the vectorstore if we so want  
# for i, doc in enumerate(docs):  
# doc.metadata[id\_key] = doc\_ids[i]  
# retriever.vectorstore.add\_documents(docs)  

```

```python
sub\_docs = vectorstore.similarity\_search("justice breyer")  

```

```python
sub\_docs[0]  

```

```text
 Document(page\_content="The document is a transcript of a speech given by the President of the United States. The President discusses several important issues and initiatives, including the nomination of a Supreme Court Justice, border security and immigration reform, protecting women's rights, advancing LGBTQ+ equality, bipartisan legislation, addressing the opioid epidemic and mental health, supporting veterans, investigating the health effects of burn pits on military personnel, ending cancer, and the strength and resilience of the American people.", metadata={'doc\_id': '79fa2e9f-28d9-4372-8af3-2caf4f1de312'})  

```

```python
retrieved\_docs = retriever.get\_relevant\_documents("justice breyer")  

```

```python
len(retrieved\_docs[0].page\_content)  

```

```text
 9194  

```

## Hypothetical Queries[​](#hypothetical-queries "Direct link to Hypothetical Queries")

An LLM can also be used to generate a list of hypothetical questions that could be asked of a particular document. These questions can then be embedded

```python
functions = [  
 {  
 "name": "hypothetical\_questions",  
 "description": "Generate hypothetical questions",  
 "parameters": {  
 "type": "object",  
 "properties": {  
 "questions": {  
 "type": "array",  
 "items": {  
 "type": "string"  
 },  
 },  
 },  
 "required": ["questions"]  
 }  
 }  
 ]  

```

```python
from langchain.output\_parsers.openai\_functions import JsonKeyOutputFunctionsParser  
chain = (  
 {"doc": lambda x: x.page\_content}  
 # Only asking for 3 hypothetical questions, but this could be adjusted  
 | ChatPromptTemplate.from\_template("Generate a list of 3 hypothetical questions that the below document could be used to answer:\n\n{doc}")  
 | ChatOpenAI(max\_retries=0, model="gpt-4").bind(functions=functions, function\_call={"name": "hypothetical\_questions"})  
 | JsonKeyOutputFunctionsParser(key\_name="questions")  
)  

```

```python
chain.invoke(docs[0])  

```

```text
 ["What was the author's initial impression of philosophy as a field of study, and how did it change when they got to college?",  
 'Why did the author decide to switch their focus to Artificial Intelligence (AI)?',  
 "What led to the author's disillusionment with the field of AI as it was practiced at the time?"]  

```

```python
hypothetical\_questions = chain.batch(docs, {"max\_concurrency": 5})  

```

```python
# The vectorstore to use to index the child chunks  
vectorstore = Chroma(  
 collection\_name="hypo-questions",  
 embedding\_function=OpenAIEmbeddings()  
)  
# The storage layer for the parent documents  
store = InMemoryStore()  
id\_key = "doc\_id"  
# The retriever (empty to start)  
retriever = MultiVectorRetriever(  
 vectorstore=vectorstore,   
 docstore=store,   
 id\_key=id\_key,  
)  
doc\_ids = [str(uuid.uuid4()) for \_ in docs]  

```

```python
question\_docs = []  
for i, question\_list in enumerate(hypothetical\_questions):  
 question\_docs.extend([Document(page\_content=s,metadata={id\_key: doc\_ids[i]}) for s in question\_list])  

```

```python
retriever.vectorstore.add\_documents(question\_docs)  
retriever.docstore.mset(list(zip(doc\_ids, docs)))  

```

```python
sub\_docs = vectorstore.similarity\_search("justice breyer")  

```

```python
sub\_docs  

```

```text
 [Document(page\_content="What is the President's stance on immigration reform?", metadata={'doc\_id': '505d73e3-8350-46ec-a58e-3af032f04ab3'}),  
 Document(page\_content="What is the President's stance on immigration reform?", metadata={'doc\_id': '1c9618f0-7660-4b4f-a37c-509cbbbf6dba'}),  
 Document(page\_content="What is the President's stance on immigration reform?", metadata={'doc\_id': '82c08209-b904-46a8-9532-edd2380950b7'}),  
 Document(page\_content='What measures is the President proposing to protect the rights of LGBTQ+ Americans?', metadata={'doc\_id': '82c08209-b904-46a8-9532-edd2380950b7'})]  

```

```python
retrieved\_docs = retriever.get\_relevant\_documents("justice breyer")  

```

```python
len(retrieved\_docs[0].page\_content)  

```

```text
 9194  

```

- [Smaller chunks](#smaller-chunks)
- [Summary](#summary)
- [Hypothetical Queries](#hypothetical-queries)
