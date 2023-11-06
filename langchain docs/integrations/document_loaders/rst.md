# RST

A [reStructured Text (RST)](https://en.wikipedia.org/wiki/ReStructuredText) file is a file format for textual data used primarily in the Python programming language community for technical documentation.

## `UnstructuredRSTLoader`[​](#unstructuredrstloader "Direct link to unstructuredrstloader")

You can load data from RST files with `UnstructuredRSTLoader` using the following workflow.

```python
from langchain.document\_loaders import UnstructuredRSTLoader  

```

```python
loader = UnstructuredRSTLoader(file\_path="example\_data/README.rst", mode="elements")  
docs = loader.load()  

```

```python
print(docs[0])  

```

```text
 page\_content='Example Docs' metadata={'source': 'example\_data/README.rst', 'filename': 'README.rst', 'file\_directory': 'example\_data', 'filetype': 'text/x-rst', 'page\_number': 1, 'category': 'Title'}  

```

- [`UnstructuredRSTLoader`](#unstructuredrstloader)
