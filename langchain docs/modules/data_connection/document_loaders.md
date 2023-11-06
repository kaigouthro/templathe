# Document loaders

Head to [Integrations](/docs/integrations/document_loaders/) for documentation on built-in document loader integrations with 3rd-party tools.

Use document loaders to load data from a source as `Document`'s. A `Document` is a piece of text
and associated metadata. For example, there are document loaders for loading a simple `.txt` file, for loading the text
contents of any web page, or even for loading a transcript of a YouTube video.

Document loaders provide a "load" method for loading data as documents from a configured source. They optionally
implement a "lazy load" as well for lazily loading data into memory.

## Get started[​](#get-started "Direct link to Get started")

The simplest loader reads in a file as text and places it all into one document.

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("./index.md")  
loader.load()  

```

```text
[  
 Document(page\_content='---\nsidebar\_position: 0\n---\n# Document loaders\n\nUse document loaders to load data from a source as `Document`\'s. A `Document` is a piece of text\nand associated metadata. For example, there are document loaders for loading a simple `.txt` file, for loading the text\ncontents of any web page, or even for loading a transcript of a YouTube video.\n\nEvery document loader exposes two methods:\n1. "Load": load documents from the configured source\n2. "Load and split": load documents from the configured source and split them using the passed in text splitter\n\nThey optionally implement:\n\n3. "Lazy load": load documents into memory lazily\n', metadata={'source': '../docs/docs/modules/data\_connection/document\_loaders/index.md'})  
]  

```

- [Get started](#get-started)
