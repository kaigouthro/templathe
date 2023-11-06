# Marqo

This notebook shows how to use functionality related to the Marqo vectorstore.

[Marqo](https://www.marqo.ai/) is an open-source vector search engine. Marqo allows you to store and query multi-modal data such as text and images. Marqo creates the vectors for you using a huge selection of open-source models, you can also provide your own fine-tuned models and Marqo will handle the loading and inference for you.

To run this notebook with our docker image please run the following commands first to get Marqo:

```text
docker pull marqoai/marqo:latest  
docker rm -f marqo  
docker run --name marqo -it --privileged -p 8882:8882 --add-host host.docker.internal:host-gateway marqoai/marqo:latest  

```

```bash
pip install marqo  

```

```python
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Marqo  
from langchain.document\_loaders import TextLoader  

```

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  

```

```python
import marqo  
  
# initialize marqo  
marqo\_url = "http://localhost:8882" # if using marqo cloud replace with your endpoint (console.marqo.ai)  
marqo\_api\_key = "" # if using marqo cloud replace with your api key (console.marqo.ai)  
  
client = marqo.Client(url=marqo\_url, api\_key=marqo\_api\_key)  
  
index\_name = "langchain-demo"  
  
docsearch = Marqo.from\_documents(docs, index\_name=index\_name)  
  
query = "What did the president say about Ketanji Brown Jackson"  
result\_docs = docsearch.similarity\_search(query)  

```

```text
 Index langchain-demo exists.  

```

```python
print(result\_docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

```python
result\_docs = docsearch.similarity\_search\_with\_score(query)  
print(result\_docs[0][0].page\_content, result\_docs[0][1], sep="\n")  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  
 0.68647254  

```

## Additional features[​](#additional-features "Direct link to Additional features")

One of the powerful features of Marqo as a vectorstore is that you can use indexes created externally. For example:

- If you had a database of image and text pairs from another application, you can simply just use it in langchain with the Marqo vectorstore. Note that bringing your own multimodal indexes will disable the `add_texts` method.
- If you had a database of text documents, you can bring it into the langchain framework and add more texts through `add_texts`.

If you had a database of image and text pairs from another application, you can simply just use it in langchain with the Marqo vectorstore. Note that bringing your own multimodal indexes will disable the `add_texts` method.

If you had a database of text documents, you can bring it into the langchain framework and add more texts through `add_texts`.

The documents that are returned are customised by passing your own function to the `page_content_builder` callback in the search methods.

#### Multimodal Example[​](#multimodal-example "Direct link to Multimodal Example")

```python
# use a new index  
index\_name = "langchain-multimodal-demo"  
  
# incase the demo is re-run  
try:  
 client.delete\_index(index\_name)  
except Exception:  
 print(f"Creating {index\_name}")  
  
# This index could have been created by another system  
settings = {"treat\_urls\_and\_pointers\_as\_images": True, "model": "ViT-L/14"}  
client.create\_index(index\_name, \*\*settings)  
client.index(index\_name).add\_documents(  
 [  
 # image of a bus  
 {  
 "caption": "Bus",  
 "image": "https://raw.githubusercontent.com/marqo-ai/marqo/mainline/examples/ImageSearchGuide/data/image4.jpg",  
 },  
 # image of a plane  
 {  
 "caption": "Plane",  
 "image": "https://raw.githubusercontent.com/marqo-ai/marqo/mainline/examples/ImageSearchGuide/data/image2.jpg",  
 },  
 ],  
)  

```

```text
 {'errors': False,  
 'processingTimeMs': 2090.2822139996715,  
 'index\_name': 'langchain-multimodal-demo',  
 'items': [{'\_id': 'aa92fc1c-1fb2-4d86-b027-feb507c419f7',  
 'result': 'created',  
 'status': 201},  
 {'\_id': '5142c258-ef9f-4bf2-a1a6-2307280173a0',  
 'result': 'created',  
 'status': 201}]}  

```

```python
def get\_content(res):  
 """Helper to format Marqo's documents into text to be used as page\_content"""  
 return f"{res['caption']}: {res['image']}"  
  
  
docsearch = Marqo(client, index\_name, page\_content\_builder=get\_content)  
  
  
query = "vehicles that fly"  
doc\_results = docsearch.similarity\_search(query)  

```

```python
for doc in doc\_results:  
 print(doc.page\_content)  

```

```text
 Plane: https://raw.githubusercontent.com/marqo-ai/marqo/mainline/examples/ImageSearchGuide/data/image2.jpg  
 Bus: https://raw.githubusercontent.com/marqo-ai/marqo/mainline/examples/ImageSearchGuide/data/image4.jpg  

```

#### Text only example[​](#text-only-example "Direct link to Text only example")

```python
# use a new index  
index\_name = "langchain-byo-index-demo"  
  
# incase the demo is re-run  
try:  
 client.delete\_index(index\_name)  
except Exception:  
 print(f"Creating {index\_name}")  
  
# This index could have been created by another system  
client.create\_index(index\_name)  
client.index(index\_name).add\_documents(  
 [  
 {  
 "Title": "Smartphone",  
 "Description": "A smartphone is a portable computer device that combines mobile telephone "  
 "functions and computing functions into one unit.",  
 },  
 {  
 "Title": "Telephone",  
 "Description": "A telephone is a telecommunications device that permits two or more users to"  
 "conduct a conversation when they are too far apart to be easily heard directly.",  
 },  
 ],  
)  

```

```text
 {'errors': False,  
 'processingTimeMs': 139.2144540004665,  
 'index\_name': 'langchain-byo-index-demo',  
 'items': [{'\_id': '27c05a1c-b8a9-49a5-ae73-fbf1eb51dc3f',  
 'result': 'created',  
 'status': 201},  
 {'\_id': '6889afe0-e600-43c1-aa3b-1d91bf6db274',  
 'result': 'created',  
 'status': 201}]}  

```

```python
# Note text indexes retain the ability to use add\_texts despite different field names in documents  
# this is because the page\_content\_builder callback lets you handle these document fields as required  
  
  
def get\_content(res):  
 """Helper to format Marqo's documents into text to be used as page\_content"""  
 if "text" in res:  
 return res["text"]  
 return res["Description"]  
  
  
docsearch = Marqo(client, index\_name, page\_content\_builder=get\_content)  
  
docsearch.add\_texts(["This is a document that is about elephants"])  

```

```text
 ['9986cc72-adcd-4080-9d74-265c173a9ec3']  

```

```python
query = "modern communications devices"  
doc\_results = docsearch.similarity\_search(query)  
  
print(doc\_results[0].page\_content)  

```

```text
 A smartphone is a portable computer device that combines mobile telephone functions and computing functions into one unit.  

```

```python
query = "elephants"  
doc\_results = docsearch.similarity\_search(query, page\_content\_builder=get\_content)  
  
print(doc\_results[0].page\_content)  

```

```text
 This is a document that is about elephants  

```

## Weighted Queries[​](#weighted-queries "Direct link to Weighted Queries")

We also expose marqos weighted queries which are a powerful way to compose complex semantic searches.

```python
query = {"communications devices": 1.0}  
doc\_results = docsearch.similarity\_search(query)  
print(doc\_results[0].page\_content)  

```

```text
 A smartphone is a portable computer device that combines mobile telephone functions and computing functions into one unit.  

```

```python
query = {"communications devices": 1.0, "technology post 2000": -1.0}  
doc\_results = docsearch.similarity\_search(query)  
print(doc\_results[0].page\_content)  

```

```text
 A telephone is a telecommunications device that permits two or more users toconduct a conversation when they are too far apart to be easily heard directly.  

```

# Question Answering with Sources

This section shows how to use Marqo as part of a `RetrievalQAWithSourcesChain`. Marqo will perform the searches for information in the sources.

```python
from langchain.chains import RetrievalQAWithSourcesChain  
from langchain.llms import OpenAI  
  
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```text
 OpenAI API Key:········  

```

```python
with open("../../modules/state\_of\_the\_union.txt") as f:  
 state\_of\_the\_union = f.read()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
texts = text\_splitter.split\_text(state\_of\_the\_union)  

```

```python
index\_name = "langchain-qa-with-retrieval"  
docsearch = Marqo.from\_documents(docs, index\_name=index\_name)  

```

```text
 Index langchain-qa-with-retrieval exists.  

```

```python
chain = RetrievalQAWithSourcesChain.from\_chain\_type(  
 OpenAI(temperature=0), chain\_type="stuff", retriever=docsearch.as\_retriever()  
)  

```

```python
chain(  
 {"question": "What did the president say about Justice Breyer"},  
 return\_only\_outputs=True,  
)  

```

```text
 {'answer': ' The president honored Justice Breyer, thanking him for his service and noting that he is a retiring Justice of the United States Supreme Court.\n',  
 'sources': '../../../state\_of\_the\_union.txt'}  

```

- [Additional features](#additional-features)
- [Weighted Queries](#weighted-queries)
