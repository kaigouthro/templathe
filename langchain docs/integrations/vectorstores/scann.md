# ScaNN

ScaNN (Scalable Nearest Neighbors) is a method for efficient vector similarity search at scale.

ScaNN includes search space pruning and quantization for Maximum Inner Product Search and also supports other distance functions such as Euclidean distance. The implementation is optimized for x86 processors with AVX2 support. See its [Google Research github](https://github.com/google-research/google-research/tree/master/scann) for more details.

## Installation[​](#installation "Direct link to Installation")

Install ScaNN through pip. Alternatively, you can follow instructions on the [ScaNN Website](https://github.com/google-research/google-research/tree/master/scann#building-from-source) to install from source.

```bash
pip install scann  

```

## Retrieval Demo[​](#retrieval-demo "Direct link to Retrieval Demo")

Below we show how to use ScaNN in conjunction with Huggingface Embeddings.

```python
from langchain.embeddings import HuggingFaceEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import ScaNN  
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
from langchain.embeddings import TensorflowHubEmbeddings  
embeddings = HuggingFaceEmbeddings()  
  
db = ScaNN.from\_documents(docs, embeddings)  
query = "What did the president say about Ketanji Brown Jackson"  
docs = db.similarity\_search(query)  
  
docs[0]  

```

```text
 Document(page\_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': 'state\_of\_the\_union.txt'})  

```

## RetrievalQA Demo[​](#retrievalqa-demo "Direct link to RetrievalQA Demo")

Next, we demonstrate using ScaNN in conjunction with Google PaLM API.

You can obtain an API key from <https://developers.generativeai.google/tutorials/setup>

```python
from langchain.chains import RetrievalQA  
from langchain.chat\_models import google\_palm  
  
palm\_client = google\_palm.ChatGooglePalm(google\_api\_key='YOUR\_GOOGLE\_PALM\_API\_KEY')  
  
qa = RetrievalQA.from\_chain\_type(  
 llm=palm\_client,  
 chain\_type="stuff",  
 retriever=db.as\_retriever(search\_kwargs={'k': 10})  
)  

```

```python
print(qa.run('What did the president say about Ketanji Brown Jackson?'))  

```

```text
 The president said that Ketanji Brown Jackson is one of our nation's top legal minds, who will continue Justice Breyer's legacy of excellence.  

```

```python
print(qa.run('What did the president say about Michael Phelps?'))  

```

```text
 The president did not mention Michael Phelps in his speech.  

```

## Save and loading local retrieval index[​](#save-and-loading-local-retrieval-index "Direct link to Save and loading local retrieval index")

```python
db.save\_local('/tmp/db', 'state\_of\_union')  
restored\_db = ScaNN.load\_local('/tmp/db', embeddings, index\_name='state\_of\_union')  

```

- [Installation](#installation)
- [Retrieval Demo](#retrieval-demo)
- [RetrievalQA Demo](#retrievalqa-demo)
- [Save and loading local retrieval index](#save-and-loading-local-retrieval-index)
