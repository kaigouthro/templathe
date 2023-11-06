# BagelDB

[BagelDB](https://www.bageldb.ai/) (`Open Vector Database for AI`), is like GitHub for AI data.
It is a collaborative platform where users can create,
share, and manage vector datasets. It can support private projects for independent developers,
internal collaborations for enterprises, and public contributions for data DAOs.

### Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

```bash
pip install betabageldb  

```

## Create VectorStore from texts[​](#create-vectorstore-from-texts "Direct link to Create VectorStore from texts")

```python
from langchain.vectorstores import Bagel  
  
texts = ["hello bagel", "hello langchain", "I love salad", "my car", "a dog"]  
# create cluster and add texts  
cluster = Bagel.from\_texts(cluster\_name="testing", texts=texts)  

```

```python
# similarity search  
cluster.similarity\_search("bagel", k=3)  

```

```text
 [Document(page\_content='hello bagel', metadata={}),  
 Document(page\_content='my car', metadata={}),  
 Document(page\_content='I love salad', metadata={})]  

```

```python
# the score is a distance metric, so lower is better  
cluster.similarity\_search\_with\_score("bagel", k=3)  

```

```text
 [(Document(page\_content='hello bagel', metadata={}), 0.27392977476119995),  
 (Document(page\_content='my car', metadata={}), 1.4783176183700562),  
 (Document(page\_content='I love salad', metadata={}), 1.5342965126037598)]  

```

```python
# delete the cluster  
cluster.delete\_cluster()  

```

## Create VectorStore from docs[​](#create-vectorstore-from-docs "Direct link to Create VectorStore from docs")

```python
from langchain.document\_loaders import TextLoader  
from langchain.text\_splitter import CharacterTextSplitter  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)[:10]  

```

```python
# create cluster with docs  
cluster = Bagel.from\_documents(cluster\_name="testing\_with\_docs", documents=docs)  

```

```python
# similarity search  
query = "What did the president say about Ketanji Brown Jackson"  
docs = cluster.similarity\_search(query)  
print(docs[0].page\_content[:102])  

```

```text
 Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the   

```

## Get all text/doc from Cluster[​](#get-all-textdoc-from-cluster "Direct link to Get all text/doc from Cluster")

```python
texts = ["hello bagel", "this is langchain"]  
cluster = Bagel.from\_texts(cluster\_name="testing", texts=texts)  
cluster\_data = cluster.get()  

```

```python
# all keys  
cluster\_data.keys()  

```

```text
 dict\_keys(['ids', 'embeddings', 'metadatas', 'documents'])  

```

```python
# all values and keys  
cluster\_data  

```

```text
 {'ids': ['578c6d24-3763-11ee-a8ab-b7b7b34f99ba',  
 '578c6d25-3763-11ee-a8ab-b7b7b34f99ba',  
 'fb2fc7d8-3762-11ee-a8ab-b7b7b34f99ba',  
 'fb2fc7d9-3762-11ee-a8ab-b7b7b34f99ba',  
 '6b40881a-3762-11ee-a8ab-b7b7b34f99ba',  
 '6b40881b-3762-11ee-a8ab-b7b7b34f99ba',  
 '581e691e-3762-11ee-a8ab-b7b7b34f99ba',  
 '581e691f-3762-11ee-a8ab-b7b7b34f99ba'],  
 'embeddings': None,  
 'metadatas': [{}, {}, {}, {}, {}, {}, {}, {}],  
 'documents': ['hello bagel',  
 'this is langchain',  
 'hello bagel',  
 'this is langchain',  
 'hello bagel',  
 'this is langchain',  
 'hello bagel',  
 'this is langchain']}  

```

```python
cluster.delete\_cluster()  

```

## Create cluster with metadata & filter using metadata[​](#create-cluster-with-metadata--filter-using-metadata "Direct link to Create cluster with metadata & filter using metadata")

```python
texts = ["hello bagel", "this is langchain"]  
metadatas = [{"source": "notion"}, {"source": "google"}]  
  
cluster = Bagel.from\_texts(cluster\_name="testing", texts=texts, metadatas=metadatas)  
cluster.similarity\_search\_with\_score("hello bagel", where={"source": "notion"})  

```

```text
 [(Document(page\_content='hello bagel', metadata={'source': 'notion'}), 0.0)]  

```

```python
# delete the cluster  
cluster.delete\_cluster()  

```

- [Installation and Setup](#installation-and-setup)
- [Create VectorStore from texts](#create-vectorstore-from-texts)
- [Create VectorStore from docs](#create-vectorstore-from-docs)
- [Get all text/doc from Cluster](#get-all-textdoc-from-cluster)
- [Create cluster with metadata & filter using metadata](#create-cluster-with-metadata--filter-using-metadata)
