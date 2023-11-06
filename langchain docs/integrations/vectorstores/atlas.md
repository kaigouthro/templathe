# Atlas

[Atlas](https://docs.nomic.ai/index.html) is a platform by Nomic made for interacting with both small and internet scale unstructured datasets. It enables anyone to visualize, search, and share massive datasets in their browser.

This notebook shows you how to use functionality related to the `AtlasDB` vectorstore.

```bash
pip install spacy  

```

```bash
python3 -m spacy download en\_core\_web\_sm  

```

```bash
pip install nomic  

```

### Load Packages[​](#load-packages "Direct link to Load Packages")

```python
import time  
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import SpacyTextSplitter  
from langchain.vectorstores import AtlasDB  
from langchain.document\_loaders import TextLoader  

```

```python
ATLAS\_TEST\_API\_KEY = "7xDPkYXSYDc1\_ErdTPIcoAR9RNd8YDlkS3nVNXcVoIMZ6"  

```

### Prepare the Data[​](#prepare-the-data "Direct link to Prepare the Data")

```python
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = SpacyTextSplitter(separator="|")  
texts = []  
for doc in text\_splitter.split\_documents(documents):  
 texts.extend(doc.page\_content.split("|"))  
  
texts = [e.strip() for e in texts]  

```

### Map the Data using Nomic's Atlas[​](#map-the-data-using-nomics-atlas "Direct link to Map the Data using Nomic's Atlas")

```python
db = AtlasDB.from\_texts(  
 texts=texts,  
 name="test\_index\_" + str(time.time()), # unique name for your vector store  
 description="test\_index", # a description for your vector store  
 api\_key=ATLAS\_TEST\_API\_KEY,  
 index\_kwargs={"build\_topic\_model": True},  
)  

```

```python
db.project.wait\_for\_project\_lock()  

```

```python
db.project  

```

Here is a map with the result of this code. This map displays the texts of the State of the Union.
<https://atlas.nomic.ai/map/3e4de075-89ff-486a-845c-36c23f30bb67/d8ce2284-8edb-4050-8b9b-9bb543d7f647>

- [Load Packages](#load-packages)
- [Prepare the Data](#prepare-the-data)
- [Map the Data using Nomic's Atlas](#map-the-data-using-nomics-atlas)
