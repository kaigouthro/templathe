# Nuclia

[Nuclia](https://nuclia.com) automatically indexes your unstructured data from any internal and external source, providing optimized search results and generative answers. It can handle video and audio transcription, image content extraction, and document parsing.

`Nuclia Understanding API` document transformer splits text into paragraphs and sentences, identifies entities, provides a summary of the text and generates embeddings for all the sentences.

To use the Nuclia Understanding API, you need to have a Nuclia account. You can create one for free at <https://nuclia.cloud>, and then [create a NUA key](https://docs.nuclia.dev/docs/docs/using/understanding/intro).

from langchain.document_transformers.nuclia_text_transform import NucliaTextTransformer

```python
#!pip install --upgrade protobuf  
#!pip install nucliadb-protos  

```

```python
import os  
  
os.environ["NUCLIA\_ZONE"] = "<YOUR\_ZONE>" # e.g. europe-1  
os.environ["NUCLIA\_NUA\_KEY"] = "<YOUR\_API\_KEY>"  

```

To use the Nuclia document transformer, you need to instantiate a `NucliaUnderstandingAPI` tool with `enable_ml` set to `True`:

```python
from langchain.tools.nuclia import NucliaUnderstandingAPI  
  
nua = NucliaUnderstandingAPI(enable\_ml=True)  

```

The Nuclia document transformer must be called in async mode, so you need to use the `atransform_documents` method:

```python
import asyncio  
  
from langchain.document\_transformers.nuclia\_text\_transform import NucliaTextTransformer  
from langchain.schema.document import Document  
  
  
async def process():  
 documents = [  
 Document(page\_content="<TEXT 1>", metadata={}),  
 Document(page\_content="<TEXT 2>", metadata={}),  
 Document(page\_content="<TEXT 3>", metadata={}),  
 ]  
 nuclia\_transformer = NucliaTextTransformer(nua)  
 transformed\_documents = await nuclia\_transformer.atransform\_documents(documents)  
 print(transformed\_documents)  
  
  
asyncio.run(process())  

```
