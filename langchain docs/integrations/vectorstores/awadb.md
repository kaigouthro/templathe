# AwaDB

[AwaDB](https://github.com/awa-ai/awadb) is an AI Native database for the search and storage of embedding vectors used by LLM Applications.

This notebook shows how to use functionality related to the `AwaDB`.

```bash
pip install awadb  

```

```python
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import AwaDB  
from langchain.document\_loaders import TextLoader  

```

```python
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=100, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  

```

```python
db = AwaDB.from\_documents(docs)  
query = "What did the president say about Ketanji Brown Jackson"  
docs = db.similarity\_search(query)  

```

```python
print(docs[0].page\_content)  

```

```text
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

## Similarity search with score[​](#similarity-search-with-score "Direct link to Similarity search with score")

The returned distance score is between 0-1. 0 is dissimilar, 1 is the most similar

```python
docs = db.similarity\_search\_with\_score(query)  

```

```python
print(docs[0])  

```

```text
 (Document(page\_content='And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../modules/state\_of\_the\_union.txt'}), 0.561813814013747)  

```

## Restore the table created and added data before[​](#restore-the-table-created-and-added-data-before "Direct link to Restore the table created and added data before")

```python
AwaDB automatically persists added document data  

```

If you can restore the table you created and added before, you can just do this as below:

```python
awadb\_client = awadb.Client()  
ret = awadb\_client.Load("langchain\_awadb")  
if ret:  
 print("awadb load table success")  
else:  
 print("awadb load table failed")  

```

awadb load table success

- [Similarity search with score](#similarity-search-with-score)
- [Restore the table created and added data before](#restore-the-table-created-and-added-data-before)
