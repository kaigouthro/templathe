# rspace

This notebook shows how to use the RSpace document loader to import research notes and documents from RSpace Electronic
Lab Notebook into Langchain pipelines.

To start you'll need an RSpace account and an API key.

You can set up a free account at <https://community.researchspace.com> or use your institutional RSpace.

You can get an RSpace API token from your account's profile page.

```bash
pip install rspace\_client  

```

It's best to store your RSpace API key as an environment variable.

```text
RSPACE\_API\_KEY=<YOUR\_KEY>  

```

You'll also need to set the URL of your RSpace installation e.g.

```text
RSPACE\_URL=https://community.researchspace.com  

```

If you use these exact environment variable names, they will be detected automatically.

```python
from langchain.document\_loaders.rspace import RSpaceLoader  

```

You can import various items from RSpace:

- A single RSpace structured or basic document. This will map 1-1 to a Langchain document.
- A folder or noteook. All documents inside the notebook or folder are imported as Langchain documents.
- If you have PDF files in the RSpace Gallery, these can be imported individually as well. Under the hood, Langchain's PDF loader will be used and this creates one Langchain document per PDF page.

```python
## replace these ids with some from your own research notes.  
## Make sure to use global ids (with the 2 character prefix). This helps the loader know which API calls to make   
## to RSpace API.  
  
rspace\_ids = ["NB1932027", "FL1921314", "SD1932029", "GL1932384"]  
for rs\_id in rspace\_ids:  
 loader = RSpaceLoader(global\_id=rs\_id)  
 docs = loader.load()  
 for doc in docs:  
 ## the name and ID are added to the 'source' metadata property.  
 print (doc.metadata)  
 print(doc.page\_content[:500])  

```

If you don't want to use the environment variables as above, you can pass these into the RSpaceLoader

```python
loader = RSpaceLoader(global\_id=rs\_id, api\_key="MY\_API\_KEY", url="https://my.researchspace.com")  

```
