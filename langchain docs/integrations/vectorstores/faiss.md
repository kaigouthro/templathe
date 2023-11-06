# Faiss

[Facebook AI Similarity Search (Faiss)](https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/) is a library for efficient similarity search and clustering of dense vectors. It contains algorithms that search in sets of vectors of any size, up to ones that possibly do not fit in RAM. It also contains supporting code for evaluation and parameter tuning.

[Faiss documentation](https://faiss.ai/).

This notebook shows how to use functionality related to the `FAISS` vector database.

```bash
pip install faiss-gpu # For CUDA 7.5+ Supported GPU's.  
# OR  
pip install faiss-cpu # For CPU Installation  

```

We want to use OpenAIEmbeddings so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  
  
# Uncomment the following line if you need to initialize FAISS with no AVX2 optimization  
# os.environ['FAISS\_NO\_AVX2'] = '1'  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import FAISS  
from langchain.document\_loaders import TextLoader  

```

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../../extras/modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

```python
db = FAISS.from\_documents(docs, embeddings)  
  
query = "What did the president say about Ketanji Brown Jackson"  
docs = db.similarity\_search(query)  

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

## Similarity Search with score[​](#similarity-search-with-score "Direct link to Similarity Search with score")

There are some FAISS specific methods. One of them is `similarity_search_with_score`, which allows you to return not only the documents but also the distance score of the query to them. The returned distance score is L2 distance. Therefore, a lower score is better.

```python
docs\_and\_scores = db.similarity\_search\_with\_score(query)  

```

```python
docs\_and\_scores[0]  

```

```text
 (Document(page\_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../modules/state\_of\_the\_union.txt'}),  
 0.36913747)  

```

It is also possible to do a search for documents similar to a given embedding vector using `similarity_search_by_vector` which accepts an embedding vector as a parameter instead of a string.

```python
embedding\_vector = embeddings.embed\_query(query)  
docs\_and\_scores = db.similarity\_search\_by\_vector(embedding\_vector)  

```

## Saving and loading[​](#saving-and-loading "Direct link to Saving and loading")

You can also save and load a FAISS index. This is useful so you don't have to recreate it everytime you use it.

```python
db.save\_local("faiss\_index")  

```

```python
new\_db = FAISS.load\_local("faiss\_index", embeddings)  

```

```python
docs = new\_db.similarity\_search(query)  

```

```python
docs[0]  

```

```text
 Document(page\_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../../state\_of\_the\_union.txt'})  

```

# Serializing and De-Serializing to bytes

you can pickle the FAISS Index by these functions. If you use embeddings model which is of 90 mb (sentence-transformers/all-MiniLM-L6-v2 or any other model), the resultant pickle size would be more than 90 mb. the size of the model is also included in the overall size. To overcome this, use the below functions. These functions only serializes FAISS index and size would be much lesser. this can be helpful if you wish to store the index in database like sql.

```python
pkl = db.serialize\_to\_bytes() # serializes the faiss index  

```

```python
embeddings = HuggingFaceEmbeddings(model\_name="all-MiniLM-L6-v2")  

```

```python
db = FAISS.deserialize\_from\_bytes(embeddings = embeddings, serialized = pkl) # Load the index  

```

## Merging[​](#merging "Direct link to Merging")

You can also merge two FAISS vectorstores

```python
db1 = FAISS.from\_texts(["foo"], embeddings)  
db2 = FAISS.from\_texts(["bar"], embeddings)  

```

```python
db1.docstore.\_dict  

```

```text
 {'068c473b-d420-487a-806b-fb0ccea7f711': Document(page\_content='foo', metadata={})}  

```

```python
db2.docstore.\_dict  

```

```text
 {'807e0c63-13f6-4070-9774-5c6f0fbb9866': Document(page\_content='bar', metadata={})}  

```

```python
db1.merge\_from(db2)  

```

```python
db1.docstore.\_dict  

```

```text
 {'068c473b-d420-487a-806b-fb0ccea7f711': Document(page\_content='foo', metadata={}),  
 '807e0c63-13f6-4070-9774-5c6f0fbb9866': Document(page\_content='bar', metadata={})}  

```

## Similarity Search with filtering[​](#similarity-search-with-filtering "Direct link to Similarity Search with filtering")

FAISS vectorstore can also support filtering, since the FAISS does not natively support filtering we have to do it manually. This is done by first fetching more results than `k` and then filtering them. You can filter the documents based on metadata. You can also set the `fetch_k` parameter when calling any search method to set how many documents you want to fetch before filtering. Here is a small example:

```python
from langchain.schema import Document  
  
list\_of\_documents = [  
 Document(page\_content="foo", metadata=dict(page=1)),  
 Document(page\_content="bar", metadata=dict(page=1)),  
 Document(page\_content="foo", metadata=dict(page=2)),  
 Document(page\_content="barbar", metadata=dict(page=2)),  
 Document(page\_content="foo", metadata=dict(page=3)),  
 Document(page\_content="bar burr", metadata=dict(page=3)),  
 Document(page\_content="foo", metadata=dict(page=4)),  
 Document(page\_content="bar bruh", metadata=dict(page=4)),  
]  
db = FAISS.from\_documents(list\_of\_documents, embeddings)  
results\_with\_scores = db.similarity\_search\_with\_score("foo")  
for doc, score in results\_with\_scores:  
 print(f"Content: {doc.page\_content}, Metadata: {doc.metadata}, Score: {score}")  

```

```text
 Content: foo, Metadata: {'page': 1}, Score: 5.159960813797904e-15  
 Content: foo, Metadata: {'page': 2}, Score: 5.159960813797904e-15  
 Content: foo, Metadata: {'page': 3}, Score: 5.159960813797904e-15  
 Content: foo, Metadata: {'page': 4}, Score: 5.159960813797904e-15  

```

Now we make the same query call but we filter for only `page = 1`

```python
results\_with\_scores = db.similarity\_search\_with\_score("foo", filter=dict(page=1))  
for doc, score in results\_with\_scores:  
 print(f"Content: {doc.page\_content}, Metadata: {doc.metadata}, Score: {score}")  

```

```text
 Content: foo, Metadata: {'page': 1}, Score: 5.159960813797904e-15  
 Content: bar, Metadata: {'page': 1}, Score: 0.3131446838378906  

```

Same thing can be done with the `max_marginal_relevance_search` as well.

```python
results = db.max\_marginal\_relevance\_search("foo", filter=dict(page=1))  
for doc in results:  
 print(f"Content: {doc.page\_content}, Metadata: {doc.metadata}")  

```

```text
 Content: foo, Metadata: {'page': 1}  
 Content: bar, Metadata: {'page': 1}  

```

Here is an example of how to set `fetch_k` parameter when calling `similarity_search`. Usually you would want the `fetch_k` parameter >> `k` parameter. This is because the `fetch_k` parameter is the number of documents that will be fetched before filtering. If you set `fetch_k` to a low number, you might not get enough documents to filter from.

```python
results = db.similarity\_search("foo", filter=dict(page=1), k=1, fetch\_k=4)  
for doc in results:  
 print(f"Content: {doc.page\_content}, Metadata: {doc.metadata}")  

```

```text
 Content: foo, Metadata: {'page': 1}  

```

## Delete[​](#delete "Direct link to Delete")

You can also delete ids. Note that the ids to delete should be the ids in the docstore.

```python
db.delete([db.index\_to\_docstore\_id[0]])  

```

```text
 True  

```

```python
# Is now missing  
0 in db.index\_to\_docstore\_id  

```

```text
 False  

```

- [Similarity Search with score](#similarity-search-with-score)
- [Saving and loading](#saving-and-loading)
- [Merging](#merging)
- [Similarity Search with filtering](#similarity-search-with-filtering)
- [Delete](#delete)
