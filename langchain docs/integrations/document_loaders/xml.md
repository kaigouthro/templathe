# XML

The `UnstructuredXMLLoader` is used to load `XML` files. The loader works with `.xml` files. The page content will be the text extracted from the XML tags.

```python
from langchain.document\_loaders import UnstructuredXMLLoader  

```

```python
loader = UnstructuredXMLLoader(  
 "example\_data/factbook.xml",  
)  
docs = loader.load()  
docs[0]  

```

```text
 Document(page\_content='United States\n\nWashington, DC\n\nJoe Biden\n\nBaseball\n\nCanada\n\nOttawa\n\nJustin Trudeau\n\nHockey\n\nFrance\n\nParis\n\nEmmanuel Macron\n\nSoccer\n\nTrinidad & Tobado\n\nPort of Spain\n\nKeith Rowley\n\nTrack & Field', metadata={'source': 'example\_data/factbook.xml'})  

```
